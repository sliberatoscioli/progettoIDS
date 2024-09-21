import os
import pickle

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

        back_button = QPushButton("🏠")
        back_button.setFixedSize(30, 30)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

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

    def go_back(self):
        from Viste.vista_home import VistaHome
        self.home_view = VistaHome()
        self.home_view.showFullScreen()
        self.close_window()



class VistaCredenziali(QMainWindow):
    def __init__(self):
        super().__init__()

        self.msg_box = QMessageBox()  # Inizializzazione della QMessageBox
        # Impostazioni della finestra
        self.setWindowTitle("REIMPOSTA CREDENZIALI")
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
        title_label = QLabel("REIMPOSTA CREDENZIALI", self)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)  # Qt.AlignCenter

        # Icona utente simulata
        user_icon = QLabel("🔑", self)
        user_icon.setFont(QFont("Arial", 60))
        user_icon.setStyleSheet("color: white;")
        main_layout.addWidget(user_icon, alignment=Qt.AlignCenter)  # Qt.AlignCenter

        #Campo username precedente
        self.oldusername_entry = QLineEdit(self)
        self.oldusername_entry.setFont(label_font)
        self.oldusername_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.oldusername_entry.setPlaceholderText("USERNAME PRECEDENTE")
        self.oldusername_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.oldusername_entry)

        # Campo unsername nuovo
        self.newusername_entry = QLineEdit(self)
        self.newusername_entry.setFont(label_font)
        self.newusername_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.newusername_entry.setPlaceholderText("USERNAME AGGIORNATO")
        self.newusername_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.newusername_entry)

        #Campo password precedente
        self.oldpassword_entry = QLineEdit(self)
        self.oldpassword_entry.setFont(label_font)
        self.oldpassword_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.oldpassword_entry.setPlaceholderText("PASSWORD PRECEDENTE")
        self.oldpassword_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.oldpassword_entry)

        # Campo password aggiornata
        self.newpassword_entry = QLineEdit(self)
        self.newpassword_entry.setFont(label_font)
        self.newpassword_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.newpassword_entry.setPlaceholderText("PASSWORD AGGIORNATA")
        self.newpassword_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.newpassword_entry)

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

        # Recupera i dati dalle entry e assicurati che non siano vuoti
        old_username = self.oldusername_entry.text()
        new_username = self.newusername_entry.text()
        old_password = self.oldpassword_entry.text()
        new_password = self.newpassword_entry.text()

        # Controlla se tutti i campi sono stati compilati
        if not all([old_username, new_username, old_password, new_password]):
            self.msg_box.setText("Errore: tutti i campi devono essere compilati.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

    def reset_clicked(self):
        self.oldusername_entry.clear()
        self.newusername_entry.clear()
        self.oldpassword_entry.clear()
        self.newpassword_entry.clear()


    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    # All'interno della classe LoginForm

    def open_home_view(self):
        self.home_view = VistaHome()
        self.home_view.showFullScreen()
        self.close()



# Funzione principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    cliente = VistaCredenziali()
    cliente.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
