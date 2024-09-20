from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QDateTime, Qt
import sys
from Viste.vista_home import VistaHome


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Pulsanti della barra del titolo con stile raffinato
        close_button = QPushButton("✕")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5f57;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e04b3d;
            }
        """)
        close_button.clicked.connect(self.close_window)
        layout.addWidget(close_button)

        minimize_button = QPushButton("−")
        minimize_button.setFixedSize(30, 30)
        minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #fdbc40;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e69d24;
            }
        """)
        minimize_button.clicked.connect(self.minimize_window)
        layout.addWidget(minimize_button)

        maximize_button = QPushButton("□")
        maximize_button.setFixedSize(30, 30)
        maximize_button.setStyleSheet("""
            QPushButton {
                background-color: #28c840;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #20a034;
            }
        """)
        maximize_button.clicked.connect(self.toggle_maximize_restore)
        layout.addWidget(maximize_button)



        self.is_maximized = False

    def close_window(self):
        self.window().close()

    def minimize_window(self):
        self.window().showMinimized()

    def toggle_maximize_restore(self):
        if self.is_maximized:
            self.window().showNormal()
        else:
            self.window().showMaximized()
        self.is_maximized = not self.is_maximized

class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()

        # Impostazioni della finestra
        self.setWindowTitle("New Shops Login")
        self.setStyleSheet("background-color: black;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimuove il bordo della finestra

        # Font personalizzati
        title_font = QFont("Arial", 20, QFont.Bold)
        label_font = QFont("Arial", 14)
        button_font = QFont("Arial", 14)

        # Layout principale
        main_layout = QVBoxLayout()

        # Barra del titolo personalizzata
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Spazio sopra i widget principali
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_top)

        # Label per data e ora
        self.datetime_label = QLabel(self)
        self.datetime_label.setFont(label_font)
        self.datetime_label.setStyleSheet("color: white;")
        main_layout.addWidget(self.datetime_label, alignment=Qt.AlignCenter)  # Qt.AlignCenter
        self.update_time()

        # Label per il titolo "LOGIN NEW SHOPS"
        title_label = QLabel("LOGIN NEW SHOPS", self)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)  # Qt.AlignCenter

        # Icona utente simulata
        user_icon = QLabel("👤", self)
        user_icon.setFont(QFont("Arial", 60))
        user_icon.setStyleSheet("color: white;")
        main_layout.addWidget(user_icon, alignment=Qt.AlignCenter)  # Qt.AlignCenter

        # Campo Username
        self.username_entry = QLineEdit(self)
        self.username_entry.setFont(label_font)
        self.username_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.username_entry.setPlaceholderText("USERNAME")
        self.username_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.username_entry)

        # Campo Password
        self.password_entry = QLineEdit(self)
        self.password_entry.setFont(label_font)
        self.password_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.password_entry.setPlaceholderText("PASSWORD")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.password_entry)

        # Layout per i pulsanti
        button_layout = QHBoxLayout()

        # Pulsante Enter
        enter_button = QPushButton("ENTER", self)
        enter_button.setFont(button_font)
        enter_button.setStyleSheet("color: white; background-color: purple;")
        enter_button.setMinimumHeight(50)  # Altezza minima del pulsante
        enter_button.clicked.connect(self.enter_clicked)
        button_layout.addWidget(enter_button)

        # Pulsante Reset
        reset_button = QPushButton("RESET", self)
        reset_button.setFont(button_font)
        reset_button.setStyleSheet("color: white; background-color: purple;")
        reset_button.setMinimumHeight(50)  # Altezza minima del pulsante
        reset_button.clicked.connect(self.reset_clicked)
        button_layout.addWidget(reset_button)

        # Aggiunta del layout dei pulsanti al layout principale
        main_layout.addLayout(button_layout)

        # Pulsante "Reimposta Credenziali" sotto i pulsanti Enter e Reset
        nuovo_cliente_button = QPushButton("REIMPOSTA CREDENZIALI", self)
        nuovo_cliente_button.setFont(button_font)
        nuovo_cliente_button.setStyleSheet("color: white; background-color: green;")
        nuovo_cliente_button.setMinimumHeight(50)
        #nuovo_cliente_button.clicked.connect(self.open_nuovo_cliente)  # Collega il pulsante al metodo
        main_layout.addWidget(nuovo_cliente_button)

        # Spazio sotto i widget principali
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        # Imposta il layout principale nel widget centrale
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("dd/MM/yy  HH:mm:ss")
        self.datetime_label.setText(current_time)
        QTimer.singleShot(1000, self.update_time)

    def enter_clicked(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        # Verifica delle credenziali
        if username == "admin" and password == "admin":
            self.open_home_view()
        else:
            self.show_message("Username o password errati!", "Username e password errati!")

    def reset_clicked(self):
        self.username_entry.clear()
        self.password_entry.clear()

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        # Apply custom style to QMessageBox (text color set to white)
        msg_box.setStyleSheet("QLabel { color: white; }")
        # Display the message box
        msg_box.exec_()
    # All'interno della classe LoginForm

    def open_home_view(self):
        self.home_view = VistaHome()
        self.home_view.showFullScreen()
        self.close()


# Funzione principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    login = LoginForm()
    login.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
#COMMIT FINALE