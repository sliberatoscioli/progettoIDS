import os
import pickle

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QDateTime, Qt
import sys

from Attivita.dipendente import Dipendente
from Controls.gestore_dipendenti import GestoreDipendenti
from Viste.vista_home import VistaHome
from PyQt5.QtWidgets import QDateEdit


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


class InserisciDipendente(QMainWindow):
    def __init__(self):
        super().__init__()

        self.msg_box = QMessageBox()  # Inizializzazione della QMessageBox
        # Impostazioni della finestra
        self.setWindowTitle("INSERISCI DIPENDENTE")
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
        title_label = QLabel("INSERISCI NUOVO DIPENDENTE", self)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)  # Qt.AlignCenter

        # Icona utente simulata
        user_icon = QLabel("👷", self)
        user_icon.setFont(QFont("Arial", 60))
        user_icon.setStyleSheet("color: white;")
        main_layout.addWidget(user_icon, alignment=Qt.AlignCenter)  # Qt.AlignCenter

        # Campo Nome
        self.nome_entry = QLineEdit(self)
        self.nome_entry.setFont(label_font)
        self.nome_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.nome_entry.setPlaceholderText("NOME")
        self.nome_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.nome_entry)

        # Campo Cognome
        self.cognome_entry = QLineEdit(self)
        self.cognome_entry.setFont(label_font)
        self.cognome_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.cognome_entry.setPlaceholderText("COGNOME")
        self.cognome_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.cognome_entry)

        # Campo Residenza
        self.residenza_entry = QLineEdit(self)
        self.residenza_entry.setFont(label_font)
        self.residenza_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.residenza_entry.setPlaceholderText("RESIDENZA")
        self.residenza_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.residenza_entry)

        #Campo Email
        self.email_entry = QLineEdit(self)
        self.email_entry.setFont(label_font)
        self.email_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.email_entry.setPlaceholderText("EMAIL")
        self.email_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.email_entry)

        #Campo telefono
        self.telefono_entry = QLineEdit(self)
        self.telefono_entry.setFont(label_font)
        self.telefono_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.telefono_entry.setPlaceholderText("TELEFONO")
        self.telefono_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.telefono_entry)

        # Campo magazzino
        # self.magazzino_entry = QLineEdit(self)
        # self.magazzino_entry.setFont(label_font)
        #self.magazzino_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        #self.magazzino_entry.setPlaceholderText("MAGAZZINO (1/2)")
        #self.magazzino_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        #main_layout.addWidget(self.magazzino_entry)

        # Campo Data di Nascita
        self.data_entry = QDateEdit(self)
        self.data_entry.setFont(label_font)
        self.data_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.data_entry.setDisplayFormat("dd/MM/yyyy")  # Formato della data
        self.data_entry.setCalendarPopup(True)  # Abilita la selezione della data tramite un calendario
        self.data_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.data_entry)

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

    def _ottieni_ultimo_id(self):
        lista_dipendenti_salvata = []

        # Verifica se il file Dipendenti.pkl esiste
        if os.path.isfile('Dati/Dipendenti.pkl'):
            with open('Dati/Dipendenti.pkl', 'rb') as f:
                lista_dipendenti_salvata = pickle.load(f)

        # Se la lista non è vuota, trova il massimo ID
        if len(lista_dipendenti_salvata) > 0:
            return max([dipendente.get_id() for dipendente in lista_dipendenti_salvata])
        else:
            # Se non ci sono dipendenti, restituisce 0
            return 0

    def enter_clicked(self):
        #Inserisci nel file
        id = self._ottieni_ultimo_id()+1
        nome = self.nome_entry.text()
        cognome = self.cognome_entry.text()
        residenza = self.residenza_entry.text()
        email = self.email_entry.text()
        telefono = self.telefono_entry.text()
        data_di_nascita = self.data_entry.date().toString("yyyy-MM-dd")  # Formatta la data come '2003-01-01'
        dipendente = Dipendente(id,nome,cognome,data_di_nascita,telefono,email,residenza)

        if not all([nome, cognome, residenza, email, telefono, data_di_nascita]):
            self.msg_box.setText("Errore: tutti i campi devono essere compilati.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

        if not telefono.isdigit():
            self.msg_box.setText("Errore: il numero di telefono deve essere composto solo da cifre.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

        gestore_dipendente = GestoreDipendenti()
        gestore_dipendente.aggiungi_dipendenti(dipendente)


    def reset_clicked(self):
        self.nome_entry.clear()
        self.cognome_entry.clear()
        self.residenza_entry.clear()
        self.email_entry.clear()
        self.telefono_entry.clear()
        self.cognome_entry.clear() # inserire eliminazione data nascita



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
    dipendente = InserisciDipendente()
    dipendente.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()