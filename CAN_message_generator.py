import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLineEdit, QMessageBox,
                            QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout,
                            QGroupBox, QFormLayout, QLabel, QRadioButton, QPushButton, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPixmap, QImage
import base64
from io import BytesIO

class MyApp(QMainWindow):
    ICON_BASE64 = """
    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
    """  # 这里替换为实际的 base64 字符串
    
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
        
        # 设置应用图标
        icon_data = base64.b64decode(self.ICON_BASE64)
        icon_pixmap = QIcon()
        icon_pixmap.addPixmap(QPixmap.fromImage(QImage.fromData(icon_data)))
        self.setWindowIcon(icon_pixmap)
        
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
        
        # 输出报
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
        
        # 清空所有输框
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