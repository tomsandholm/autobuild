#!/usr/bin/env python3
import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QPlainTextEdit, QMessageBox, QDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QProcess, Qt

AUTH_FILE = '.auth.json'

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.authenticated = False

    def initUI(self):
        self.setWindowTitle('Login - Autobuild Manager')
        self.setFixedSize(300, 150)
        layout = QVBoxLayout(self)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not os.path.exists(AUTH_FILE):
            # Create default if not exists
            default_auth = {"username": "admin", "password": "password"}
            with open(AUTH_FILE, 'w') as f:
                json.dump(default_auth, f)
            QMessageBox.information(self, 'Auth Initialized', 
                                    f'Authentication file created.\nDefault: admin / password')

        try:
            with open(AUTH_FILE, 'r') as f:
                auth_data = json.load(f)
            
            if username == auth_data.get('username') and password == auth_data.get('password'):
                self.authenticated = True
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Invalid username or password')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Could not read auth file: {str(e)}')

class AutobuildGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.process = None

    def initUI(self):
        self.setWindowTitle('Autobuild Manager')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # FQDN Input
        fqdn_layout = QHBoxLayout()
        fqdn_label = QLabel('FQDN:')
        self.fqdn_input = QLineEdit()
        self.fqdn_input.setPlaceholderText('e.g. node1.example.com')
        fqdn_layout.addWidget(fqdn_label)
        fqdn_layout.addWidget(self.fqdn_input)
        layout.addLayout(fqdn_layout)

        # ROLE Selection
        role_layout = QHBoxLayout()
        role_label = QLabel('ROLE:')
        self.role_combo = QComboBox()
        roles = ['general', 'ansible', 'apache', 'docker', 'dockldap', 
                 'gitlab', 'gitolite', 'gitserver', 'gluster', 'jenkins', 'qemu']
        self.role_combo.addItems(roles)
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.create_btn = QPushButton('Create Node')
        self.create_btn.clicked.connect(self.create_node)
        self.create_btn.setStyleSheet("background-color: #007bff; color: white;")
        
        self.delete_btn = QPushButton('Delete Node')
        self.delete_btn.clicked.connect(self.delete_node)
        self.delete_btn.setStyleSheet("background-color: #dc3545; color: white;")
        
        btn_layout.addWidget(self.create_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

        # Output Area
        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Monospace"))
        layout.addWidget(QLabel('Output:'))
        layout.addWidget(self.output_area)

    def create_node(self):
        fqdn = self.fqdn_input.text().strip()
        role = self.role_combo.currentText()
        if not fqdn:
            QMessageBox.warning(self, 'Input Error', 'Please enter an FQDN')
            return
        
        command = ['make', 'node', f'NAME={fqdn}', f'ROLE={role}']
        self.run_command(command)

    def delete_node(self):
        fqdn = self.fqdn_input.text().strip()
        if not fqdn:
            QMessageBox.warning(self, 'Input Error', 'Please enter an FQDN')
            return
        
        reply = QMessageBox.question(self, 'Confirm Deletion', 
                                     f'Are you sure you want to delete {fqdn}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            command = ['make', 'Delete', f'NAME={fqdn}']
            self.run_command(command)

    def run_command(self, command):
        if self.process and self.process.state() == QProcess.Running:
            QMessageBox.warning(self, 'Process Running', 'A command is already running.')
            return

        self.output_area.clear()
        
        # Setup logging
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        self.log_file_path = os.path.join(log_dir, f"autobuild_{timestamp}.log")
        
        self.output_area.appendPlainText(f"Executing: {' '.join(command)}")
        self.output_area.appendPlainText(f"Logging to: {self.log_file_path}\n")
        
        try:
            self.log_file = open(self.log_file_path, 'w')
            self.log_file.write(f"Command: {' '.join(command)}\n")
            self.log_file.write(f"Started at: {datetime.datetime.now()}\n")
            self.log_file.write("-" * 40 + "\n")
        except Exception as e:
            QMessageBox.critical(self, 'Logging Error', f'Could not create log file: {str(e)}')
            return

        self.create_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.finished.connect(self.process_finished)
        
        # Set working directory to project root
        project_root = os.path.dirname(os.path.abspath(__file__))
        self.process.setWorkingDirectory(project_root)
        
        self.process.start(command[0], command[1:])

    def handle_output(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output_area.appendPlainText(data)
        if hasattr(self, 'log_file') and self.log_file:
            self.log_file.write(data)
            self.log_file.flush()
        
        # Scroll to bottom
        self.output_area.verticalScrollBar().setValue(
            self.output_area.verticalScrollBar().maximum()
        )

    def process_finished(self):
        self.create_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        self.output_area.appendPlainText("\nProcess finished.")
        
        if hasattr(self, 'log_file') and self.log_file:
            import datetime
            self.log_file.write(f"\n" + "-" * 40 + "\n")
            self.log_file.write(f"Finished at: {datetime.datetime.now()}\n")
            self.log_file.close()
            self.log_file = None
            
        self.process = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        ex = AutobuildGUI()
        ex.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
