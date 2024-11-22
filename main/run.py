import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtGui import QFont

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 중앙 위젯 및 레이아웃 설정
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 메뉴 옵션 버튼 생성
        buttons = [
            ('1. Connection', 'Connection established.'),
            ('2. Find', 'Finding records...'),
            ('3. Insert', 'Inserting a new record.'),
            ('4. Update', 'Updating a record...'),
            ('5. View / List', 'Listing records...'),
            ('99. Quit', 'Exiting application.')
        ]

        for text, response in buttons:
            button = QPushButton(text, self)
            button.clicked.connect(lambda _, b=button, r=response: self.buttonClicked(b, r))
            layout.addWidget(button)

        # 텍스트 에디터 설정
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont('Courier', 10))
        layout.addWidget(self.text_edit)
        
        # 사용자 입력을 받을 수 있는 QLineEdit 추가
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Enter commands here...")
        layout.addWidget(self.input_line)
        self.input_line.returnPressed.connect(self.processInput)
        
        # 창 설정
        self.setGeometry(300, 300, 350, 400)
        self.setWindowTitle('DataBaseSystem Term Project')

    def buttonClicked(self, button, response):
        if button.text() == '99. Quit':
            QApplication.quit()
        else:
            self.text_edit.append(response)

    def processInput(self):
        command = self.input_line.text()
        self.text_edit.append(f"Command entered: {command}")
        self.input_line.clear()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
