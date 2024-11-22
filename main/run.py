import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtGui import QFont

class Main(QMainWindow):
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
            ('1. Connection', self.connect_database),
            ('2. Select DataBase', self.select_database), # 데이터 베이스 실행
            ('3. Execute Query', self.execute_query), # 쿼리 실행
            ('4. Show Tables', self.show_tables), # 데이터 베이스 내 table 보여주기
            ('5. Describe Table', self.describe_table), # 어떤 테이블 설명
            ('6. Clear Results', self.clear_results),
        ]

        for text, func in buttons:
            button = QPushButton(text, self)
            button.clicked.connect(func)
            layout.addWidget(button)


        # 텍스트 에디터 설정
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont('Courier', 10))
        layout.addWidget(self.text_edit)
        
        # 사용자 입력을 받을 수 있는 QLineEdit 추가
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Enter SQL commands or database name here...")
        layout.addWidget(self.input_line)
        self.input_line.returnPressed.connect(self.processInput)

        # 창 설정
        self.setGeometry(300, 300, 350, 400)
        self.setWindowTitle('DataBaseSystem Term Project')
        
    def processInput(self):
        """ 사용자 Input"""
        print('input')
        command = self.input_line.text()
        self.text_edit.append(f"Command Entered: {command}")
        self.input_line.clear() # 모두 clear
        
    def connect_database(self):
        """DB 연결"""
        ################## mySQL과 GUI 연결 구현 필요 ##################
        # 연결 성공 시
        self.text_edit.append("Success Connection!") 
        # 연결 실패 시
        
    def select_database(self):
        """USE DB"""
        self.text_edit.append("Which database would you like to select?")
        
        self.input_line.setFocus() # input line에 포커스
        # 이전에 연결된 모든 핸들러를 제거
        self.input_line.returnPressed.disconnect()
        self.input_line.returnPressed.connect(self.get_database_name)

    def get_database_name(self):
        """유저가 입력한 사용할 db이름 가져오기"""
        db_name = self.input_line.text()
        print(db_name)
        self.text_edit.append(f"Selected Database: {db_name}")
        self.input_line.clear()  # input_line을 clear
        ################## DB 이름을 mySQL에서 Search(use databases;) 구현 필요 ##################
        
        # 다시 제거 후  processInput에 연결
        self.input_line.returnPressed.disconnect()
        self.input_line.returnPressed.connect(self.processInput)

    def execute_query(self):
        """Query 실행"""
        self.text_edit.append("Which query would you like to find?") # 말 고칠 필요가 있음
        
        self.input_line.setFocus() # input line에 포커스
        self.input_line.returnPressed.disconnect()
        self.input_line.returnPressed.connect(self.get_query)
        
    def get_query(self):
        """유저가 입력한 query 가져오기"""
        query = self.input_line.text()
        self.text_edit.append(f"Query: {query}")
        self.input_line.clear()  # input_line을 clear
        ################## DB 이름을 mySQL에서 Query 그대로 실행하는 함수 구현 필요 ##################
        
        # 다시 processInput에 제거 후 연결
        self.input_line.returnPressed.disconnect()
        self.input_line.returnPressed.connect(self.processInput)

    def show_tables(self):
        "보고 싶은 table select 하기 LIMIT5"
        self.text_edit.append("Which table would you like to see?") # 말 고칠 필요가 있음
        
        self.input_line.setFocus() # input line에 포커스
        self.input_line.returnPressed.disconnect()
        self.input_line.returnPressed.connect(self.get_select_table)
        
    def get_select_table(self):
        """유저가 입력한 query 가져오기"""
        table_name = self.input_line.text()
        self.text_edit.append(f"Select Table: {table_name}")
        self.input_line.clear()  # input_line을 clear
        ################## DB에서 해당 Table을 *로(limit 5) 가져오기 ##################
        
        # 다시 processInput에 제거 후 연결
        self.input_line.returnPressed.disconnect()
        self.input_line.returnPressed.connect(self.processInput)
        
    def describe_table(self):
        """테이블 DESC"""
        self.text_edit.append("Which table would you like to describe?") # 말 고칠 필요가 있음

        self.input_line.setFocus() # input line에 포커스
        self.input_line.returnPressed.disconnect()
        self.input_line.returnPressed.connect(self.get_desc_table)
        
    def get_desc_table(self):
        """유저가 입력한 table의 Desc 가져오기"""
        table_name = self.input_line.text()
        self.text_edit.append(f"DESC Table: {table_name}")
        self.input_line.clear()  # input_line을 clear
        ################## DB에서 해당 Table을 DESC 결과 가져오기 ##################
        
        # 다시 processInput에 제거 후 연결
        self.input_line.returnPressed.disconnect()
        self.input_line.returnPressed.connect(self.processInput)
        
    def clear_results(self):
        """Text 창 clear"""
        self.text_edit.clear()

def main():
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
