from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from user import *
import bcrypt

class LoginApp(QDialog):
    authentication = pyqtSignal(object)
    register = pyqtSignal(bool)

    def __init__(self, conn):
        super(LoginApp, self).__init__()
        loadUi("login_form.ui", self)
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.show_reg)
        self.tb2.returnPressed.connect(self.login)
        self.conn = conn

    def login(self):
        email = self.tb1.text()
        password = self.tb2.text()

        cur = self.conn.cursor()

        command = f'''
SELECT * FROM users 
WHERE email = '{email}'
'''
        cur.execute(command)

        row = cur.fetchone()
        if row:
            if self.verify_password(password, row[2]):
                user = User(*row)
                self.authentication.emit(user)

            else:
                QMessageBox.warning(self, "Login Error", "Incorrect Password")    
        
        else:
            QMessageBox.warning(self, "Login Error", "There is no user matched")



        cur.close()

        self.conn.commit()

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, entered_password, hashed_password):
        entered_password = self.hash_password(entered_password)
        print(hashed_password)
        print(entered_password)
        return entered_password == hashed_password

    def show_reg(self):
        self.register.emit(True)