import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtGui import QFont
import pymysql


######DBMS 함수들######

def connect_to_database():
    """ MySQL 서버 연결 """
    try:
        connection = pymysql.connect(
            host="192.168.56.4",  # 사용하는 Ip
            user="geonyoung", # 계정 명
            password="1234",   
            database="madang", # 사용할 디비         
            port=4567 # mysql port
        )
        print("MySQL 서버에 성공적으로 연결되었습니다.")
        return connection
    except:
        print(f"MySQL 연결 실패!! 다시 시도해주세요!")
        return None
    
def insert_data(connection, table_name, data):
    """ 데이터 삽입 (insert) """
    try:
        cursor = connection.cursor()
        # col, value를 무조건 지정해주어야 함. 추후에 고칠 필요가 있음
        value = ', '.join(['%s'] * len(data)) # 데이터가 여러개 넣기 위하여
        columns = ', '.join(data.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({value})"
        cursor.execute(query, tuple(data.values())) 
        connection.commit() # 쿼리 커밋
        print("데이터 삽입 성공")
    except:
        print(f"데이터 삽입 실패!!")

def execute_query(connection, query):
    """ SQL 쿼리 실행 및 커밋 """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("쿼리 실행 및 커밋 성공")
    except Exception as e:
        print(f"쿼리 실행 실패: {e}")
        
def update_data(connection, table_name, data, condition):
    """ 데이터 업데이트 (update) """
    try:
        cursor = connection.cursor()
        # 데이터를 업데이트 쿼리 문자열로 변환
        update_statement = ', '.join([f"{key} = %s" for key in data.keys()])
        # 전체 쿼리
        query = f"UPDATE {table_name} SET {update_statement} WHERE {condition}"
        # 쿼리 실행
        cursor.execute(query, tuple(data.values()))
        connection.commit()  # 쿼리 커밋
        print("데이터 업데이트 성공")
    except Exception as e:
        print(f"데이터 업데이트 실패: {e}")

        
def delete_data(connection, table_name, condition):
    """ 데이터 삭제 (delete) """
    try:
        cursor = connection.cursor()
        if condition: # condition 있다면
            query = f"DELETE FROM {table_name} WHERE {condition}"
        else:
            query = f"DELETE FROM {table_name}" 
        cursor.execute(query)
        connection.commit() # 쿼리 커밋
        print("데이터 삭제 성공")
    except:
        print(f"데이터 삭제 실패!!!")

def search_data(connection, table_name, columns="*", condition="1=1"):
    """ 데이터 검색 (select)"""
    try:
        cursor = connection.cursor()
        if condition: # condition 있다면
            query = f"SELECT {columns} FROM {table_name} WHERE {condition}"
        else:
            query = f"SELECT {columns} FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall() # 모든 결과 가져오기
        print("검색된 데이터:")
        for row in results:
            print(row)
        return results
    except:
        print(f"데이터 검색 실패 !!!")
        
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connection = connect_to_database()
        
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
        """기본 DB 연결"""
        ################## mySQL과 GUI 연결 구현 필요 ##################
        """ MySQL 서버 연결 """
        try:
            self.connection = pymysql.connect(
                host="192.168.56.4",  # 사용하는 Ip
                user="geonyoung", # 계정 명
                password="1234",   
                database="madang", # 사용할 디비         
                port=4567 # mysql port
            )
            print("MySQL 서버에 성공적으로 연결되었습니다.")
            self.text_edit.append("Success Connection!") 
        except:
            print(f"MySQL 연결 실패!! 다시 시도해주세요!")
            return None
        
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
        
        self.connection = pymysql.connect(
            host="192.168.56.4",  # 사용하는 Ip
            user="geonyoung", # 계정 명
            password="1234",   
            database=db_name, # 사용할 디비         
            port=4567 # mysql port
        )
        
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

        cursor = self.connection.cursor()
        cursor.execute(query) # 쿼리 실행
        
        results = cursor.fetchall() # 모든 결과 가져오기
        # prompt 창에 다시 뿌림
        self.text_edit.append("유저 쿼리 결과:")
        for row in results:
            self.text_edit.append(row)
            
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
        """유저가 table 정보 가져오기"""
        table_name = self.input_line.text()
        self.text_edit.append(f"Select Table: {table_name}")
        self.input_line.clear()  # input_line을 clear
        ################## DB에서 해당 Table을 *로(limit 5) 가져오기 ##################
        
        query = f"SELECT * FROM {table_name}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        results = cursor.fetchall() # 모든 결과 가져오기
        # prompt 창에 다시 뿌림
        self.text_edit.append("검색된 데이터:")
        for row in results:
            self.text_edit.append(row)
            
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
        query = f"DESC {table_name}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        results = cursor.fetchall() # 모든 결과 가져오기
        # prompt 창에 다시 뿌림
        self.text_edit.append("검색된 데이터:")
        for row in results:
            self.text_edit.append(row)
            
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
