from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QDateTime, Qt
import sys
from Attivita.prodotto import Prodotto
import Viste.vista_home

from Attivita.scatola import Scatola


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
        self.window().close()


class VistaInserisciProdotto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.msg_box = QMessageBox()  # Inizializzazione della QMessageBox
        # Impostazioni della finestra
        self.setWindowTitle("INSERISCI PRODOTTO")
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

        # Label per il titolo "INSERISCI NUOVO PRODOTTO"
        title_label = QLabel("INSERISCI NUOVO PRODOTTO", self)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)  # Qt.AlignCenter

        # Icona utente simulata
        user_icon = QLabel("👚👖👟", self)
        user_icon.setFont(QFont("Arial", 60))
        user_icon.setStyleSheet("color: white;")
        main_layout.addWidget(user_icon, alignment=Qt.AlignCenter)  # Qt.AlignCenter

        # Campo TAGLIA
        self.taglia_entry = QLineEdit(self)
        self.taglia_entry.setFont(label_font)
        self.taglia_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.taglia_entry.setPlaceholderText("TAGLIA")
        self.taglia_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.taglia_entry)

        # Campo MARCA
        self.marca_entry = QLineEdit(self)
        self.marca_entry.setFont(label_font)
        self.marca_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.marca_entry.setPlaceholderText("MARCA")
        self.marca_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.marca_entry)

        # Campo COLORE
        self.colore_entry = QLineEdit(self)
        self.colore_entry.setFont(label_font)
        self.colore_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.colore_entry.setPlaceholderText("COLORE")
        self.colore_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.colore_entry)

        # Campo PREZZO
        self.prezzo_entry = QLineEdit(self)
        self.prezzo_entry.setFont(label_font)
        self.prezzo_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.prezzo_entry.setPlaceholderText("PREZZO")
        self.prezzo_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.prezzo_entry)

        # Campo DESCRIZIONE
        self.descrizione_entry = QLineEdit(self)
        self.descrizione_entry.setFont(label_font)
        self.descrizione_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.descrizione_entry.setPlaceholderText("DESCRIZIONE")
        self.descrizione_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.descrizione_entry)

        # Campo TIPO PRODOTTO
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems([
            "T-SHIRT",
            "MAGLIONE",
            "CAMICIA",
            "POLO",
            "CANOTTA",
            "SHORT",
            "PANTALONE",
            "TUTA",
            "ABITO",
            "GIACCA",
            "SCARPA",
            "ACCESSORIO"
        ])
        self.search_type_combo.setFont(label_font)
        self.search_type_combo.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.search_type_combo.setMinimumHeight(40)
        main_layout.addWidget(self.search_type_combo)

        # Campo GIACENZA
        self.giacenza_entry = QLineEdit(self)
        self.giacenza_entry.setFont(label_font)
        self.giacenza_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.giacenza_entry.setPlaceholderText("GIACENZA")
        self.giacenza_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.giacenza_entry)

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

        from Controls.gestore_prodotti import GestoreProdotti

        IDScatola_prodotto = GestoreProdotti().ritorna_ultimo_IDprodotto() + 1
        taglia = self.taglia_entry.text().upper()
        marca = self.marca_entry.text()
        colore = self.colore_entry.text().upper()
        prezzo = self.prezzo_entry.text()
        descrizione = self.descrizione_entry.text()
        tipoProdotto = self.search_type_combo.currentText()
        giacenza = self.giacenza_entry.text()

        scatola = Scatola(IDScatola_prodotto,descrizione)
        prodotto = Prodotto(IDScatola_prodotto,scatola,marca,taglia,colore,descrizione,tipoProdotto,giacenza,prezzo)


        # Stampa i valori dei campi per verificarli
        print(f"IDScatola_prodotto: {IDScatola_prodotto}")
        print(f"Taglia: {taglia}")
        print(f"Marca: {marca}")
        print(f"Colore: {colore}")
        print(f"Prezzo: {prezzo}")
        print(f"Descrizione: {descrizione}")
        print(f"Tipo Prodotto: {tipoProdotto}")
        print(f"Giacenza: {giacenza}")

        if not (taglia and marca and colore and prezzo and descrizione and tipoProdotto and giacenza):
            self.msg_box.setText("Tutti i campi devono essere compilati!")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
            return

        if not giacenza.isdigit():
            self.msg_box.setText("La giacenza deve essere un numero")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
            return

        try:
            prezzo_float = float(prezzo)
        except ValueError:
            self.msg_box.setText("Il prezzo deve essere un numero decimale")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
            return

        gestoreProdotti = GestoreProdotti().aggiungi_prodotto(prodotto)

    def reset_clicked(self):
        self.taglia_entry.clear()
        self.marca_entry.clear()
        self.colore_entry.clear()
        self.prezzo_entry.clear()
        self.descrizione_entry.clear()
        self.giacenza_entry.clear()

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def open_home_view(self):
        self.home_view = Viste.VistaHome.VistaHome()
        self.home_view.showFullScreen()
        self.close()


# Funzione principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    prodotto = VistaInserisciProdotto()
    prodotto.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()