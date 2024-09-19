import sys
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QGroupBox, QRadioButton
from Attivita.acquisto import Acquisto

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Pulsanti della barra del titolo con stile raffinato
        close_button = QPushButton("x")
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

        minimize_button = QPushButton("-")
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

class VistaCaricaWallet(QMainWindow):
    def __init__(self):
        super().__init__()

        self.msg_box = QMessageBox()  # Inizializzazione della QMessageBox
        # Impostazioni della finestra
        self.setWindowTitle("CARICA WALLET")
        self.setStyleSheet("background-color: black;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimuove il bordo della finestra

        # Font personalizzati
        title_font = QFont("Arial", 30, QFont.Bold)
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
        main_layout.addWidget(self.datetime_label, alignment=Qt.AlignCenter)
        self.update_time()

        # Label per il titolo "CARICA WALLET"
        title_label = QLabel("CARICA WALLET", self)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Icona utente simulata
        user_icon = QLabel("📁", self)
        user_icon.setFont(QFont("Arial", 60))
        user_icon.setStyleSheet("color: white;")
        main_layout.addWidget(user_icon, alignment=Qt.AlignCenter)

        # Campo NUMERO TELEFONICO
        self.telefono_entry = QLineEdit(self)
        self.telefono_entry.setFont(label_font)
        self.telefono_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.telefono_entry.setPlaceholderText("NUMERO DI TELEFONO DEL CLIENTE")
        self.telefono_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.telefono_entry)

        # Campo IMPORTO
        self.importo_entry = QLineEdit(self)
        self.importo_entry.setFont(label_font)
        self.importo_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.importo_entry.setPlaceholderText("IMPORTO")
        self.importo_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.importo_entry)

        # Campo TIPO PAGAMENTO
        payment_group_box = QGroupBox("TIPO PAGAMENTO")
        payment_group_box.setFont(label_font)
        payment_group_box.setStyleSheet("color: white;")
        payment_layout = QVBoxLayout()
        self.cash_radio = QRadioButton("CONTANTI")
        self.cash_radio.setFont(label_font)
        self.cash_radio.setStyleSheet("color: white;")
        self.cash_radio.setChecked(True)
        payment_layout.addWidget(self.cash_radio)

        self.credit_card_radio = QRadioButton("CARTA DI CREDITO")
        self.credit_card_radio.setFont(label_font)
        self.credit_card_radio.setStyleSheet("color: white;")
        payment_layout.addWidget(self.credit_card_radio)

        payment_group_box.setLayout(payment_layout)
        main_layout.addWidget(payment_group_box)

        # Layout per i pulsanti Enter e Reset (stessa riga)
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

        # Aggiunta del layout dei pulsanti Enter e Reset al layout principale
        main_layout.addLayout(button_layout)

        # Pulsante "Inserisci Nuovo Cliente" sotto i pulsanti Enter e Reset
        nuovo_cliente_button = QPushButton("INSERISCI NUOVO CLIENTE", self)
        nuovo_cliente_button.setFont(button_font)
        nuovo_cliente_button.setStyleSheet("color: white; background-color: green;")
        nuovo_cliente_button.setMinimumHeight(50)
        nuovo_cliente_button.clicked.connect(self.open_nuovo_cliente)  # Collega il pulsante al metodo
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
        # Verifica se i campi sono riempiti correttamente
        numero_telefono = self.telefono_entry.text().strip()
        importo = self.importo_entry.text().strip()
        metodo_pagamento = "CONTANTI" if self.cash_radio.isChecked() else "CARTA DI CREDITO" if self.credit_card_radio.isChecked() else None

        if not numero_telefono.isdigit():
            self.msg_box.setText("ERRORE, digitare un numero corretto")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
            return

        if not importo.replace('.', '', 1).isdigit():  # Permette anche importi con decimali
            self.msg_box.setText("ERRORE, digitare un importo corretto")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
            return

        if metodo_pagamento is None:
            self.msg_box.setText("ERRORE, selezionare un metodo di pagamento")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
            return

        try:
            importo_val = float(importo)
            self.load_data(numero_telefono, importo_val, metodo_pagamento)
        except ValueError:
            self.show_message("Errore", "Errore nel caricamento dei dati.")

    def reset_clicked(self):
        self.telefono_entry.clear()
        self.importo_entry.clear()
        self.cash_radio.setChecked(False)
        self.credit_card_radio.setChecked(False)

    def open_nuovo_cliente(self):
        from Viste.VisteClienti.vista_inserisci_cliente import InserisciCliente
        self.inserisci_cliente_view = InserisciCliente()
        self.inserisci_cliente_view.resize(500, 600)  # Imposta la dimensione della finestra ridotta
        self.inserisci_cliente_view.show()


    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def load_data(self, telefonoCliente_cercato, importo, metodo_pagamento):
        carica_wallet = acquistare().carica_wallet(telefonoCliente_cercato, importo, metodo_pagamento)

# Funzione principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    caricaWallet = VistaCaricaWallet()
    caricaWallet.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


