import sys
from functools import partial

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy,
    QMessageBox, QComboBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime


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


class RimuoviCliente(QMainWindow):
    def __init__(self):
        super().__init__()

        self.msg_box = QMessageBox()  # Inizializzazione della QMessageBox
        # Impostazioni della finestra
        self.setWindowTitle("RICERCA CLIENTE")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #34495e; color: white;")  # Sfondo nero e testo bianco
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimuove il bordo della finestra

        # Font personalizzati
        title_font = QFont("Arial", 20, QFont.Bold)
        label_font = QFont("Arial", 14)
        button_font = QFont("Arial", 14)

        # Layout principale
        main_layout = QVBoxLayout()

        # Barra del titolo personalizzata con pulsanti
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Titolo della finestra
        self.title_label = QLabel("Ricerca clienti 🔎", self)
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Label per data e ora
        self.datetime_label = QLabel(self)
        self.datetime_label.setFont(QFont("Arial", 14))
        self.datetime_label.setStyleSheet("color: white;")
        self.datetime_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.datetime_label)

        # Layout superiore per la ricerca e l'ordinamento
        search_layout = QHBoxLayout()

        # Campo di ricerca
        self.search_label = QLabel("INSERISCI INFORMAZIONI CLIENTE:")
        self.search_label.setStyleSheet("color: white;")  # Testo bianco per la label
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)

        # Dropdown per la selezione del tipo di ricerca
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems([
            "Ricerca per Nome",
            "Ricerca per ID",
            "Ricerca per Numero Telefonico",
            "Ricerca per Codice Fiscale"
        ])
        search_layout.addWidget(self.search_type_combo)

        # Pulsante di ricerca
        self.search_button = QPushButton("Cerca")
        self.search_button.setStyleSheet("background-color: purple; color: white; font-weight: bold;")  # Bottone viola
        self.search_button.clicked.connect(self.search)
        self.search_button.setMinimumHeight(25)  # Altezza minima del pulsant
        search_layout.addWidget(self.search_button)

        # Layout per l'ordinamento
        sort_layout = QHBoxLayout()

        # Aggiunta del layout di ricerca e ordinamento al layout principale
        main_layout.addLayout(search_layout)
        main_layout.addLayout(sort_layout)

        # Creazione della tabella
        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("""
                   QTableWidget {
                       background-color: #34495e;
                       color: #ecf0f1;
                       border: none;
                   }
                   QHeaderView::section {
                       background-color: #2c3e50;
                       color: #ecf0f1;
                       font-weight: bold;
                       border: none;
                   }
                   QTableWidget::item {
                       border-bottom: 1px solid #7f8c8d;
                   }
               """)

        # Modifica delle intestazioni delle colonne
        self.table_widget.horizontalHeader().setStyleSheet(
            "background-color: black; color: purple; font-weight: bold;"
        )

        # Aggiungi la tabella al layout principale
        main_layout.addWidget(self.table_widget)

        # Spazio sotto i widget principali
        spacer_bottom = QSpacerItem(80, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        # Widget centrale
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Timer per aggiornare la data e l'ora ogni secondo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Aggiorna ogni 1000 millisecondi (1 secondo)
        self.update_time()

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(f"Data e Ora: {current_time}")

    def search(self):
        search_text = self.search_input.text()
        search_type = self.search_type_combo.currentText()

        # Oggetto cliente
        from Controls.gestore_clienti import GestoreClienti
        clientiPK = GestoreClienti()

        # Determina il tipo di ricerca e costruisci la query SQL appropriata
        if search_type == "Ricerca per Nome":
            clienti = clientiPK.cerca_per_nome(search_text.upper())
        elif search_type == "Ricerca per ID":
            clienti = clientiPK.cerca_per_ID(search_text)
        elif search_type == "Ricerca per Numero Telefonico":
            clienti = clientiPK.cerca_per_telefono(search_text)
        elif search_type == "Ricerca per Codice Fiscale":
            clienti = clientiPK.cerca_per_codicefiscale(search_text.upper())
        else:
            clienti = []

        # Imposta le intestazioni delle colonne
        headers = ["ID Cliente", "Nome", "Cognome", "Data di Nascita", "Residenza", "Codice Fiscale", "Email",
                   "Telefono", "IDDIPENDENTE(Inserimento)", "Saldo_wallet €"]

        # Aggiungi la colonna "Azioni" solo se necessario
        if search_type in ["Ricerca per ID", "Ricerca per Numero Telefonico"]:
            headers.append("Azioni")

        # Assicurati che i dati siano stati recuperati
        if not clienti:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(len(headers))  # Imposta il numero corretto di colonne
            self.table_widget.setHorizontalHeaderLabels(headers)
            return

        # Imposta il numero di righe e colonne
        self.table_widget.setRowCount(len(clienti))
        self.table_widget.setColumnCount(len(headers))  # Imposta il numero corretto di colonne

        # Imposta le intestazioni delle colonne
        self.table_widget.setHorizontalHeaderLabels(headers)

        # Popola la tabella con i dati
        for row_idx, cliente in enumerate(clienti):
            dipendente = cliente.get_dipendente_inserimento()
            dipendente_id = dipendente.get_id() if dipendente else "N/A"  # Gestisce il caso in cui il dipendente sia None
            row_data = [
                cliente.get_id_cliente(),
                cliente.get_nome_cliente(),
                cliente.get_cognome_cliente(),
                cliente.get_data_nascita_cliente(),
                cliente.get_residenza_cliente(),
                cliente.get_codice_fiscale_cliente(),
                cliente.get_email_cliente(),
                cliente.get_telefono_cliente(),
                dipendente_id,
                cliente.get_saldo_wallet()
            ]

            for col_idx, col_data in enumerate(row_data):
                if col_idx < len(headers):
                    item = QTableWidgetItem(str(col_data))
                    item.setBackground(Qt.darkMagenta)
                    self.table_widget.setItem(row_idx, col_idx, item)

            # Aggiungi pulsante in base al tipo di ricerca
            if search_type == "Ricerca per ID":
                action_button = QPushButton("Stampa Storico Cliente 📄")
                action_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
                action_button.clicked.connect(partial(self.perform_action1, cliente.get_id_cliente()))
                self.table_widget.setCellWidget(row_idx, len(headers) - 1, action_button)


            elif search_type == "Ricerca per Numero Telefonico":
                action_button = QPushButton("Rimuovi Cliente")
                action_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
                action_button.clicked.connect(partial(self.perform_action2, cliente.get_telefono_cliente()))
                self.table_widget.setCellWidget(row_idx, len(headers) - 1, action_button)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def perform_action1(self, cliente_id):
        from Viste.VisteClienti.vista_stampa_storico import VistaStampaStoricoCliente
        self.Vista_Storico = VistaStampaStoricoCliente(cliente_id)
        self.Vista_Storico.showFullScreen()
        self.close()

    def perform_action2(self, telefono):
        from Controls.gestore_clienti import GestoreClienti
        GestoreClienti().elimina_cliente(telefono)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)


# Funzione principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    ricerca_cliente = RimuoviCliente()
    ricerca_cliente.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()