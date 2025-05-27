from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
import re
import sys
import requests

class AuthForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Registro")
        self.is_register = False
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Entrar")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input)
        self.username_input.hide()  # começa escondido

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.submit_button = QPushButton("Entrar")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.toggle_button = QPushButton("Não tem conta? Registrar")
        self.toggle_button.setFlat(True)
        self.toggle_button.setStyleSheet("color: blue;")
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.layout.addWidget(self.toggle_button)

        self.setLayout(self.layout)

    def toggle_mode(self):
        self.is_register = not self.is_register
        if self.is_register:
            self.title_label.setText("Registrar")
            self.username_input.show()
            self.submit_button.setText("Registrar")
            self.toggle_button.setText("Já tem conta? Entrar")
        else:
            self.title_label.setText("Entrar")
            self.username_input.hide()
            self.submit_button.setText("Entrar")
            self.toggle_button.setText("Não tem conta? Registrar")

    def is_valid_email(self, email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email)

    def is_valid_password(self, password):
        return re.match(r"^(?=.*[A-Z])(?=.*[\W_]).{8,}$", password)

    def is_valid_username(self, username):
        return re.match(r"^[a-zA-Z0-9_]{2,12}$", username)

    def submit(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        username = self.username_input.text().strip()

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Erro", "Email inválido.")
            return

        if not self.is_valid_password(password):
            QMessageBox.warning(self, "Erro", "Senha inválida. Deve ter ao menos 8 caracteres, 1 maiúscula e 1 símbolo.")
            return

        if self.is_register:
            if not self.is_valid_username(username):
                QMessageBox.warning(self, "Erro", "Username inválido.")
                return
            self.register_user(username, email, password)
        else:
            self.login_user(email, password)

    def register_user(self, username, email, password):
        try:
            payload = {
                "username": username,
                "email": email,
                "password": password,
                "last_name": "",
                "pic_square": ""
            }
            # Substitua a URL pela sua API real:
            response = requests.post("https://sua-api.com/player/register", json=payload)

            if response.status_code == 200:
                QMessageBox.information(self, "Sucesso", "Conta registrada com sucesso!")
                self.toggle_mode()
            else:
                QMessageBox.warning(self, "Erro", "Conta já existente ou erro na API.")
        except Exception as e:
            QMessageBox.critical(self, "Erro de Rede", str(e))

    def login_user(self, email, password):
        try:
            payload = {
                "email": email,
                "password": password
            }
            # Substitua pela URL da sua API:
            response = requests.post("https://sua-api.com/login", json=payload)

            if response.status_code == 200:
                QMessageBox.information(self, "Sucesso", "Login realizado!")
            else:
                QMessageBox.warning(self, "Erro", "Credenciais inválidas.")
        except Exception as e:
            QMessageBox.critical(self, "Erro de Rede", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthForm()
    window.resize(300, 250)
    window.show()
    sys.exit(app.exec_())