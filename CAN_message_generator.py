import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLineEdit, QMessageBox,
                            QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout,
                            QGroupBox, QFormLayout, QLabel, QRadioButton, QPushButton, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initData()
        self.initUI()
        
    def initData(self):
        """初始化数据"""
        self.status = False
        self.start_bit = 0
        self.bit_length = 0
        self.resolution = 0
        self.offset = 1
        self.signalphys = 0
        self.lsb_checked = 0
        self.msb_checked = 0
        self.byte_count = 8  # 默认8字节
        self.CAN = [0] * (self.byte_count * 8)  # 动态设置CAN数组大小
        
        # 初始化UI控件为None
        self.startbit_le = None
        self.bitlength_le = None
        self.resolution_le = None
        self.offset_le = None
        self.signalphys_le = None
        self.signalraw_le = None
        self.lsb_rb = None
        self.msb_rb = None
        self.byte_select = None
        self.can_table = None
        self.message_le = None
        self.generate_pb = None

    def initUI(self):
        """初始化UI"""
        self.setWindowTitle("CAN报文生成工具 v1.0 @ChangXiaoqiang")
        
        # 设置窗口大小
        window_width = 825
        window_height = 600
        
        # 获取屏幕信息
        screen = QApplication.primaryScreen().geometry()
        # 计算窗口位置使其居中
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        
        # 设置窗口大小和位置
        self.setGeometry(x, y, window_width, window_height)
        
        # 创建中心部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 创建上部水平布局
        top_layout = QHBoxLayout()
        
        # 创建左侧信号配置组
        config_group = QGroupBox("信号属性")
        form_layout = QFormLayout()
        
        # 创建输入框并设置最小宽度
        self.startbit_le = QLineEdit()
        self.startbit_le.setMinimumWidth(100)
        self.bitlength_le = QLineEdit()
        self.bitlength_le.setMinimumWidth(100)
        self.resolution_le = QLineEdit()
        self.resolution_le.setMinimumWidth(100)
        self.offset_le = QLineEdit()
        self.offset_le.setMinimumWidth(100)
        
        # 添加标签和输入框
        form_layout.addRow("起始位：", self.startbit_le)
        form_layout.addRow("位长度：", self.bitlength_le)
        form_layout.addRow("精度：", self.resolution_le)
        form_layout.addRow("偏移量：", self.offset_le)
        
        # 添加物理值和原始值输入框
        self.signalphys_le = QLineEdit()
        self.signalphys_le.setMinimumWidth(100)
        self.signalphys_le.textChanged.connect(self.on_physical_value_changed)
        
        self.signalraw_le = QLineEdit()
        self.signalraw_le.setMinimumWidth(100)
        self.signalraw_le.textChanged.connect(self.on_raw_value_changed)
        self.signalraw_le.setPlaceholderText("0x")  # 添加提示文本
        
        form_layout.addRow("物理值：", self.signalphys_le)
        form_layout.addRow("原始值：", self.signalraw_le)
        
        # 创建单选按钮
        radio_layout = QHBoxLayout()
        self.lsb_rb = QRadioButton("Motorola LSB")
        self.msb_rb = QRadioButton("Motorola MSB")
        radio_layout.addWidget(self.lsb_rb)
        radio_layout.addWidget(self.msb_rb)
        form_layout.addRow("字节格式：", radio_layout)
        
        # 在form_layout中添加字节数选择
        self.byte_select = QComboBox()
        self.byte_select.addItems(['8字节', '16字节', '64字节'])
        self.byte_select.currentIndexChanged.connect(self.onByteCountChanged)
        form_layout.addRow("报文长度：", self.byte_select)
        
        # 添加空白标签来增加间距
        form_layout.addRow(QLabel(""))  # 添加空行
        
        # 添加测试数据按钮组
        test_group = QGroupBox("测试数据")
        test_layout = QVBoxLayout()
        
        # 创建测试数据按钮
        test_case1 = QPushButton("测试用例1 (LSB)")
        test_case1.clicked.connect(lambda: self.loadTestCase(1))
        
        test_case2 = QPushButton("测试用例2 (MSB)")
        test_case2.clicked.connect(lambda: self.loadTestCase(2))
        
        test_case3 = QPushButton("测试用例3 (跨字节LSB)")
        test_case3.clicked.connect(lambda: self.loadTestCase(3))
        
        test_case4 = QPushButton("测试用例4 (跨字节MSB)")
        test_case4.clicked.connect(lambda: self.loadTestCase(4))
        
        # 添加按钮到布局
        test_layout.addWidget(test_case1)
        test_layout.addWidget(test_case2)
        test_layout.addWidget(test_case3)
        test_layout.addWidget(test_case4)
        test_group.setLayout(test_layout)
        
        # 将测试组添加到form_layout
        form_layout.addRow(test_group)
        
        config_group.setLayout(form_layout)
        
        # 创建表格
        from PyQt6.QtWidgets import QTableWidget, QSizePolicy
        self.can_table = QTableWidget()
        
        # 设置表格的大小策略
        self.can_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.can_table.setMinimumWidth(400)  # 设置最小宽度
        
        self.initTable()
        
        # 设置左侧配置组的大小策略
        config_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
        # 将配置组和表格添加到上部布局
        top_layout.addWidget(config_group)
        top_layout.addWidget(self.can_table)
        
        # 设置上部布局的拉伸因子
        top_layout.setStretch(0, 0)  # 左侧配置组不拉伸
        top_layout.setStretch(1, 1)  # 右侧表格可以拉伸
        
        # 创建下部水平布局
        bottom_layout = QHBoxLayout()
        
        # 创建按钮和消息显示框
        self.generate_pb = QPushButton("生成报文")
        self.generate_pb.clicked.connect(self.convertCANMessage)
        
        self.copy_pb = QPushButton("复制报文")
        self.copy_pb.clicked.connect(self.copyMessage)
        
        self.clear_pb = QPushButton("清空报文")
        self.clear_pb.clicked.connect(self.clearMessage)
        
        self.message_le = QLineEdit()
        self.message_le.setReadOnly(True)
        
        # 添加到下部布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_pb)
        button_layout.addWidget(self.copy_pb)
        button_layout.addWidget(self.clear_pb)
        
        bottom_layout.addLayout(button_layout)
        bottom_layout.addWidget(self.message_le)
        
        # 设置布局的拉伸因子
        bottom_layout.setStretch(0, 0)  # 按钮布局不拉伸
        bottom_layout.setStretch(1, 1)  # 消息框可以拉伸
        
        # 将上部和下部布局添加到主布局
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        
        self.show()

    def onByteCountChanged(self, index):
        """字节数改变时的处理"""
        byte_counts = {0: 8, 1: 16, 2: 64}
        self.byte_count = byte_counts[index]
        self.CAN = [0] * (self.byte_count * 8)
        self.initTable()  # 重新初始化表格
        self.message_le.clear()  # 清空消息显示

    def initTable(self):
        """初始化CAN报文表格"""
        self.can_table.setRowCount(self.byte_count)  # 动态设置行数
        self.can_table.setColumnCount(8)  # 列数固定为8
        
        # 设置表格大小
        self.can_table.horizontalHeader().setDefaultSectionSize(50)
        self.can_table.verticalHeader().setDefaultSectionSize(50)
        
        # 初始化表格内容
        for row in range(self.byte_count):
            for col in range(8):
                item = QTableWidgetItem('0')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(QColor(255, 255, 255))  # 设置白色背景
                item.setForeground(QColor(0, 0, 0))  # 设置黑色文字
                self.can_table.setItem(row, col, item)
                
        # 设置表头
        # 水平表头显示bit位
        bit_labels = [f'Bit{i}' for i in range(7, -1, -1)]
        self.can_table.setHorizontalHeaderLabels(bit_labels)
        
        # 垂直表头显示字节，从上到下 Byte0~ByteN
        byte_labels = [f'Byte{i}' for i in range(self.byte_count)]
        self.can_table.setVerticalHeaderLabels(byte_labels)

    def updateTable(self):
        """重置表格显示"""
        for i in range(self.byte_count * 8):
            row = i // 8
            col = 7 - (i % 8)
            item = self.can_table.item(row, col)
            item.setText('0')  # 重置为0
            item.setBackground(QColor(255, 255, 255))  # 白色背景
            item.setForeground(QColor(0, 0, 0))  # 黑色文字

    def setTableCell(self, bit_position, value, is_start=False):
        """设置表格单元格的值和颜色"""
        row = bit_position // 8
        col = 7 - (bit_position % 8)
        item = self.can_table.item(row, col)
        item.setText(str(value))
        if is_start:
            item.setBackground(QColor(255, 182, 193))  # 起始位设置为淡红色
        else:
            item.setBackground(QColor(144, 238, 144))  # 其他占用位设置为淡绿色

    def checked_value(self, start_bit, bit_length, resolution, offset, signalphys, lsb_checked, msb_checked):
        """检查输入值的有效性"""
        if lsb_checked == 0 and msb_checked == 0:
            QMessageBox.critical(self, "错误", "请至少选择一种编码格式")
            return False
        if start_bit == '' or not start_bit.isdigit():
            QMessageBox.critical(self, "错误", "请输入起始位，且为正整数")
            return False
        if bit_length == '' or not bit_length.isdigit():
            QMessageBox.critical(self, "错误", "请输入信号长度，且为正整数")
            return False
        if resolution == '':
            QMessageBox.critical(self, "错误", "请输入精度")
            return False
        if offset == '':
            QMessageBox.critical(self, "错误", "请输入偏移量")
            return False
        if signalphys == '':
            QMessageBox.critical(self, "错误", "请输入信号值，物理值-十进制数")
            return False
            
        # 检查起始位是否超出范围
        if int(start_bit) >= self.byte_count * 8:
            QMessageBox.critical(self, "错误", f"起始位超出范围，最大值应小于{self.byte_count * 8}")
            return False
            
        return True

    def octToBin(self, octNum, bit):
        """十进制转换成倒序二进制list"""
        while (octNum != 0):
            # 求模运算，2的模值要么0，要么1
            bit.append(octNum % 2)
            # 除运算，15/2=7,int取整数
            octNum = int(octNum / 2)
        # 当输入的信号值二进制长度是小于总的信号长度，就在后面补0，倒序
        while len(bit) < self.bit_length:
            bit.append(0)

    def message_fill(self):
        """对CAN信号进行处理并输出显示到界面上"""
        message = []
        for i in range(0, self.byte_count * 8, 8):
            byte_bits = self.CAN[i:i+8]  # 获取一个字节的8位
            byte_bits.reverse()  # 反转位顺序
            byte_str = ''.join(map(str, byte_bits))  # 转换为字符串
            byte = hex(int(byte_str, 2)).upper().lstrip("0X").zfill(2)  # 转换为16进制
            message.append(byte)
        
        # 输出报��
        self.message_le.setText(" ".join(message))

    def CANMessage_msb(self):
        """MSB格式CAN报文生成"""
        output_message = True
        
        # 长度未超过1Byte的情况且未跨字节的信号
        if (self.bit_length <= 8) and (int(self.start_bit/8) == int((self.start_bit - self.bit_length + 1)/8)):
            bit = []
            self.octToBin(self.signalphys, bit)
            # 填充位并设置显示
            for i in range(self.bit_length):
                current_bit = self.start_bit - i
                self.CAN[current_bit] = bit[len(bit) - 1 - i]
                self.setTableCell(current_bit, self.CAN[current_bit], i == 0)
            
        # 跨字节的信号处理
        elif (self.bit_length - (int(self.start_bit % 8) + 1) <= 8):  # 共2个字节 跨了1个字节
            low_len = self.start_bit % 8 + 1
            high_len = self.bit_length - low_len
            bit = []
            self.octToBin(self.signalphys, bit)
            
            # 填充第一个字节的位
            for j1 in range(low_len):
                current_bit = self.start_bit - j1
                self.CAN[current_bit] = bit[len(bit) - 1 - j1]
                self.setTableCell(current_bit, self.CAN[current_bit], j1 == 0)
            
            # 填充第二个字节的位
            for j2 in range(high_len):
                current_bit = (int(self.start_bit / 8) + 1) * 8 + (8 - high_len) + j2
                self.CAN[current_bit] = bit[j2]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
            
        elif (self.bit_length - (int(self.start_bit % 8) + 1) <= 16) and \
                self.bit_length - (int(self.start_bit % 8) + 1) > 8:  # 共3个字节 跨了2个字节
            low_len = self.start_bit % 8 + 1
            high_len = self.bit_length - low_len - 8
            bit = []
            self.octToBin(self.signalphys, bit)
            
            # 填充第一个字节的位
            for j1 in range(low_len):
                current_bit = self.start_bit - j1
                self.CAN[current_bit] = bit[len(bit) - 1 - j1]
                self.setTableCell(current_bit, self.CAN[current_bit], j1 == 0)
            
            # 填充第三个字节的位
            for j2 in range(high_len):
                current_bit = self.start_bit+(8-low_len)+8+(8-high_len)+1+j2
                self.CAN[current_bit] = bit[j2]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
            
            # 填充中间字节的位
            for j3 in range(8):
                current_bit = (int(self.start_bit/8) +1)*8 +j3
                self.CAN[current_bit] = bit[high_len + j3]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
            
        elif (self.bit_length - (int(self.start_bit % 8) + 1) <= 24) and \
                self.bit_length - (int(self.start_bit % 8) + 1) > 16:  # 共4个字节 跨了3个字节
            low_len = self.start_bit % 8 + 1
            high_len = self.bit_length - low_len - 8*2
            bit = []
            self.octToBin(self.signalphys, bit)
            
            # 填充第一个字节的位
            for j1 in range(low_len):
                current_bit = self.start_bit - j1
                self.CAN[current_bit] = bit[len(bit) - 1 - j1]
                self.setTableCell(current_bit, self.CAN[current_bit], j1 == 0)
            
            # 填充最后一个字节的位
            for j2 in range(high_len):
                current_bit = self.start_bit+(8-low_len)+8*2+(8-high_len)+1+j2
                self.CAN[current_bit] = bit[j2]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
            
            # 填充间两个字节的位
            for j3 in range(8):
                current_bit = (int(self.start_bit / 8))*8 + 8*2 +j3
                self.CAN[current_bit] = bit[high_len + j3]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
            
            for j4 in range(8):
                current_bit = (int(self.start_bit / 8))*8 + 8 +j4
                self.CAN[current_bit] = bit[high_len + 8 + j4]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
        else:
            output_message = False
            
        if output_message:
            self.message_fill()
        else:
            QMessageBox.critical(self, "错误", "暂不支持！！！")

    def CANMessage_lsb(self):
        """LSB格式CAN报文生成"""
        output_message = True
        
        if (self.bit_length > ((8 - int(self.start_bit % 8)) + int(self.start_bit/8) * 8)):
            output_message = False
            QMessageBox.critical(self, "错误", "输入的信号长度超过范围，请重新输入")
            
        # 长度未超过1Byte的情况且未跨字节的信号
        elif ((self.start_bit % 8 + self.bit_length) <= 8):
            bit = []
            self.octToBin(self.signalphys, bit)
            # 填充位并设置显示
            for i in range(self.bit_length):
                current_bit = self.start_bit + i
                self.CAN[current_bit] = bit[i]
                self.setTableCell(current_bit, self.CAN[current_bit], i == 0)
                
        # 跨字节的信号处理
        elif (int(self.start_bit % 8) + self.bit_length) - 1 <= 15 and \
                (int(self.start_bit % 8) + self.bit_length) - 1 >= 8:  # 共两个字节 跨一个字节
            high_len = 8 - self.start_bit % 8
            low_len = self.bit_length - high_len
            bit = []
            self.octToBin(self.signalphys, bit)
            
            # 填充第一个字节的位
            for j1 in range(high_len):
                current_bit = self.start_bit + j1
                self.CAN[current_bit] = bit[j1]
                self.setTableCell(current_bit, self.CAN[current_bit], j1 == 0)
            
            # 填充第二个字节的位
            for j2 in range(low_len):
                current_bit = (int(self.start_bit / 8) - 1) * 8 + j2
                self.CAN[current_bit] = bit[high_len + j2]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
                
        elif (int(self.start_bit % 8) + self.bit_length) - 1 <= 23 and \
                (int(self.start_bit % 8) + self.bit_length) - 1 >= 16:  # 共3个字节 跨2个字节
            high_len = 8 - self.start_bit % 8
            low_len = self.bit_length - high_len - 8
            bit = []
            self.octToBin(self.signalphys, bit)
            
            # 填充第一个字节的位
            for j1 in range(high_len):
                current_bit = self.start_bit + j1
                self.CAN[current_bit] = bit[j1]
                self.setTableCell(current_bit, self.CAN[current_bit], j1 == 0)
            
            # 填充最后一个字节的位
            for j2 in range(low_len):
                current_bit = (low_len - 1) + (int(self.start_bit / 8) - 2) * 8 - j2
                self.CAN[current_bit] = bit[len(bit) - 1 - j2]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
            
            # 填充中间字节的位
            for j3 in range(8):
                current_bit = (int(self.start_bit / 8) - 1) * 8 + j3
                self.CAN[current_bit] = bit[high_len + j3]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
                
        elif (int(self.start_bit % 8) + self.bit_length) - 1 <= 31 and \
                (int(self.start_bit % 8) + self.bit_length) - 1 >= 24:  # 共4个字节 跨3个字节
            high_len = 8 - self.start_bit % 8
            low_len = self.bit_length - high_len - 8 * 2
            bit = []
            self.octToBin(self.signalphys, bit)
            
            # 填充第一个字节的位
            for j1 in range(high_len):
                current_bit = self.start_bit + j1
                self.CAN[current_bit] = bit[j1]
                self.setTableCell(current_bit, self.CAN[current_bit], j1 == 0)
            
            # 填充最后一个字节的位
            for j2 in range(low_len):
                current_bit = (low_len - 1) + (int(self.start_bit / 8) - 3) * 8 - j2
                self.CAN[current_bit] = bit[len(bit) - 1 - j2]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
            
            # 填充中间两个字节的位
            for j3 in range(8):
                current_bit = (int(self.start_bit / 8) - 1) * 8 + j3
                self.CAN[current_bit] = bit[high_len + j3]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
            
            for j4 in range(8):
                current_bit = (int(self.start_bit / 8) - 2) * 8 + j4
                self.CAN[current_bit] = bit[high_len + 8 + j4]
                self.setTableCell(current_bit, self.CAN[current_bit], False)
        else:
            output_message = False
            
        if output_message:
            self.message_fill()
        else:
            QMessageBox.critical(self, "错误", "暂不支持！！！")

    def message_generate(self):
        """生成CAN报文"""
        try:
            # 检查必要的输入
            if not all([self.resolution_le.text(), self.offset_le.text(), 
                       (self.signalphys_le.text() or self.signalraw_le.text())]):
                QMessageBox.critical(self, "错误", "请填写完整的信号信息")
                return
            
            # 获取原始值
            if self.signalraw_le.text():
                raw_text = self.signalraw_le.text()
                if raw_text.startswith('0x'):
                    raw_text = raw_text[2:]
                self.signalphys = int(raw_text, 16)
            else:
                phys_value = float(self.signalphys_le.text())
                resolution = float(self.resolution_le.text())
                offset = float(self.offset_le.text())
                self.signalphys = int((phys_value - offset) / resolution)
            
            self.start_bit = int(self.start_bit)
            self.bit_length = int(self.bit_length)
            
            # 检查范围
            max_value = 2 ** self.bit_length
            if self.signalphys >= max_value or self.signalphys < 0:
                QMessageBox.critical(self, "错误", "信号值超出范围！")
                return

            # 不再重置CAN数组，保留原有的值
            # self.CAN = [0] * (self.byte_count * 8)
            # self.updateTable()
            
            if self.lsb_checked == 1:
                self.CANMessage_lsb()
            if self.msb_checked == 1:
                self.CANMessage_msb()
            
        except ValueError:
            QMessageBox.critical(self, "错误", "请检查输入值的格式是否正确")

    def convertCANMessage(self):
        """转换CAN报文"""
        self.start_bit = self.startbit_le.text()
        self.bit_length = self.bitlength_le.text()
        self.resolution = self.resolution_le.text()
        self.offset = self.offset_le.text()
        self.signalphys = self.signalphys_le.text()
        
        # 不再清空message_le
        # self.message_le.setText('')
        
        self.lsb_checked = 1 if self.lsb_rb.isChecked() else 0
        self.msb_checked = 1 if self.msb_rb.isChecked() else 0

        if self.checked_value(self.start_bit, self.bit_length, self.resolution,
                            self.offset, self.signalphys, self.lsb_checked, self.msb_checked):
            self.message_generate()

    def on_physical_value_changed(self):
        """物理值改变时，计算并更新原始值"""
        try:
            if (self.signalphys_le and self.signalphys_le.text() and 
                self.resolution_le and self.resolution_le.text() and 
                self.offset_le and self.offset_le.text()):
                
                phys_value = float(self.signalphys_le.text())
                resolution = float(self.resolution_le.text())
                offset = float(self.offset_le.text())
                
                # 计算原始值
                raw_value = int((phys_value - offset) / resolution)
                
                # 检查是否超出范围
                if self.bitlength_le and self.bitlength_le.text():
                    max_value = 2 ** (int(self.bitlength_le.text()))
                    if raw_value >= max_value or raw_value < 0:
                        QMessageBox.critical(self, "错误", "计算的原始值超出范围！")
                        if self.signalraw_le:
                            self.signalraw_le.blockSignals(True)
                            self.signalraw_le.clear()
                            self.signalraw_le.blockSignals(False)
                        return
                
                # 更新原始值显示
                if self.signalraw_le:
                    self.signalraw_le.blockSignals(True)
                    self.signalraw_le.setText(hex(raw_value).upper().replace('X', 'x'))
                    self.signalraw_le.blockSignals(False)
        except ValueError:
            # 清空原始值
            if self.signalraw_le:
                self.signalraw_le.blockSignals(True)
                self.signalraw_le.clear()
                self.signalraw_le.blockSignals(False)

    def on_raw_value_changed(self):
        """原始值改变时，计算并更新物理值"""
        try:
            if (self.signalraw_le and self.signalraw_le.text() and 
                self.resolution_le and self.resolution_le.text() and 
                self.offset_le and self.offset_le.text()):
                
                # 处理十六进制输入
                raw_text = self.signalraw_le.text()
                if raw_text.startswith('0x'):
                    raw_text = raw_text[2:]
                raw_value = int(raw_text, 16)
                
                # 检查是否超出范围
                if self.bitlength_le and self.bitlength_le.text():
                    max_value = 2 ** (int(self.bitlength_le.text()))
                    if raw_value >= max_value or raw_value < 0:
                        QMessageBox.critical(self, "错误", "原始值超出范围！")
                        self.signalphys_le.blockSignals(True)
                        self.signalphys_le.clear()
                        self.signalphys_le.blockSignals(False)
                        return
                
                resolution = float(self.resolution_le.text())
                offset = float(self.offset_le.text())
                
                # 计算物理值
                phys_value = raw_value * resolution + offset
                
                # 更新物理值显示
                self.signalphys_le.blockSignals(True)
                self.signalphys_le.setText(str(phys_value))
                self.signalphys_le.blockSignals(False)
        except ValueError:
            # 清空物理值
            self.signalphys_le.blockSignals(True)
            self.signalphys_le.clear()
            self.signalphys_le.blockSignals(False)

    def copyMessage(self):
        """复制报文到剪贴板"""
        if self.message_le.text():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.message_le.text())
            QMessageBox.information(self, "提示", "报文已复制到剪贴板")
        else:
            QMessageBox.warning(self, "警告", "没有可复制的报文")

    def clearMessage(self):
        """清空报文显示和信号属性"""
        # 清空报文显示
        self.message_le.clear()
        
        # 清空CAN数组和表格
        self.CAN = [0] * (self.byte_count * 8)
        self.updateTable()
        
        # 清空所有输���框
        self.startbit_le.clear()
        self.bitlength_le.clear()
        self.resolution_le.clear()
        self.offset_le.clear()
        self.signalphys_le.clear()
        self.signalraw_le.clear()
        
        # 清空单选按钮选择
        self.lsb_rb.setChecked(False)
        self.msb_rb.setChecked(False)
        
        # 重置字节数为默认值（8字节）
        self.byte_select.setCurrentIndex(0)

    def loadTestCase(self, case_num):
        """加载预置的测试用例"""
        # 预置的测试数据
        test_cases = {
            1: {  # LSB 单字节测试
                'start_bit': '42',
                'bit_length': '2',
                'resolution': '1',
                'offset': '0',
                'physical_value': '2',
                'format': 'LSB',
                'byte_count': 0  # 0 表示 8字节
            },
            2: {  # MSB 单字节测试
                'start_bit': '42',
                'bit_length': '2',
                'resolution': '1',
                'offset': '0',
                'physical_value': '2',
                'format': 'MSB',
                'byte_count': 0
            },
            3: {  # LSB 跨字节测试
                'start_bit': '30',
                'bit_length': '12',
                'resolution': '1',
                'offset': '0',
                'physical_value': '1930',
                'format': 'LSB',
                'byte_count': 0
            },
            4: {  # MSB 跨字节测试
                'start_bit': '30',
                'bit_length': '12',
                'resolution': '1',
                'offset': '0',
                'physical_value': '1930',
                'format': 'MSB',
                'byte_count': 0
            }
        }
        
        if case_num in test_cases:
            case = test_cases[case_num]
            
            # 设置字节数
            self.byte_select.setCurrentIndex(case['byte_count'])
            
            # 设置各个输入框的值
            self.startbit_le.setText(case['start_bit'])
            self.bitlength_le.setText(case['bit_length'])
            self.resolution_le.setText(case['resolution'])
            self.offset_le.setText(case['offset'])
            self.signalphys_le.setText(case['physical_value'])
            
            # 设置编码格式
            if case['format'] == 'LSB':
                self.lsb_rb.setChecked(True)
                self.msb_rb.setChecked(False)
            else:
                self.lsb_rb.setChecked(False)
                self.msb_rb.setChecked(True)
            
            # 自动生成报文
            self.convertCANMessage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())