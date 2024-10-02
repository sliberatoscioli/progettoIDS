import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Pulsanti della barra del titolo
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


class VistaStampaClienti(QMainWindow):

    def __init__(self):
        super().__init__()

        # Impostazioni della finestra
        self.setWindowTitle("Tabella Clienti")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2c3e50;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimozione del bordo della finestra

        # Layout principale
        main_layout = QVBoxLayout()

        # Barra del titolo personalizzata con pulsanti
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Titolo della finestra
        self.title_label = QLabel("LISTA CLIENTI DEL NEGOZIO", self)
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setStyleSheet("color: #ecf0f1;")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Label per data e ora
        self.datetime_label = QLabel(self)
        self.datetime_label.setFont(QFont("Arial", 14))
        self.datetime_label.setStyleSheet("color: #ecf0f1;")
        self.datetime_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.datetime_label)

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

        #  Tabella aggiunta al layout principale
        main_layout.addWidget(self.table_widget)

        # Layout per il pulsante
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 50, 0, 0)
        button_layout.setSpacing(10)

        button_layout = QHBoxLayout()
        button_font = QFont("Arial", 14)

        # Pulsante Enter
        enter_button = QPushButton("STAMPA PDF CLIENTI", self)
        enter_button.setFont(button_font)
        enter_button.setStyleSheet("color: #ecf0f1; background-color: #8f00ff;")
        enter_button.setMinimumHeight(23)  # Altezza minima del pulsante
        enter_button.clicked.connect(self.stampa_pdf_clienti)
        button_layout.addWidget(enter_button)


        # Layout del pulsante aggiunto al layout principale
        main_layout.addLayout(button_layout)

        # Widget centrale
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Caricamento dei dati e popolamento della tabella
        self.load_data()

        # Timer per aggiornare la data e l'ora ogni secondo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Aggiorna ogni 1000 millisecondi
        self.update_time()

    # Metodo che rimanda alla stampa del pdf dei clienti
    def stampa_pdf_clienti(self):
        from Controls.gestore_clienti import GestoreClienti
        gestore = GestoreClienti().stampa_pdf_clienti()
        self.msg_box = QMessageBox()
        if (gestore == False):
            self.msg_box.setText(f"Errore durante la creazione del PDF")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
        else:
            self.msg_box.setText(f"PDF generato con successo: {gestore}")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

    # Metodo per il caricamento dei dati
    def load_data(self):
        # Carica Lista clienti
        from Controls.gestore_clienti import GestoreClienti
        clienti = GestoreClienti().ritorna_lista_clienti()

        if not clienti:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(10)
            self.table_widget.setHorizontalHeaderLabels(
                ["ID Cliente", "Nome", "Cognome", "Data di Nascita", "Residenza", "Codice Fiscale", "Email", "Telefono",
                 "IDDIPENDENTE", "Saldo_wallet"]
            )
            return

        # Numero di righe e colonne
        self.table_widget.setRowCount(len(clienti))
        self.table_widget.setColumnCount(10)

        # Intestazioni delle colonne
        self.table_widget.setHorizontalHeaderLabels(
            ["ID Cliente", "Nome", "Cognome", "Data di Nascita", "Residenza", "Codice Fiscale", "Email", "Telefono",
             "IDDIPENDENTE (Inserimento)", "Saldo_wallet €"]
        )

        # Popolamento della tabella con i dati degli oggetti Cliente
        for row_idx, cliente in enumerate(clienti):
            self.table_widget.setItem(row_idx, 0, QTableWidgetItem(str(cliente.get_id_cliente())))
            self.table_widget.setItem(row_idx, 1, QTableWidgetItem(cliente.get_nome_cliente()))
            self.table_widget.setItem(row_idx, 2, QTableWidgetItem(cliente.get_cognome_cliente()))
            self.table_widget.setItem(row_idx, 3, QTableWidgetItem(cliente.get_data_nascita_cliente()))
            self.table_widget.setItem(row_idx, 4, QTableWidgetItem(cliente.get_residenza_cliente()))
            self.table_widget.setItem(row_idx, 5, QTableWidgetItem(cliente.get_codice_fiscale_cliente()))
            self.table_widget.setItem(row_idx, 6, QTableWidgetItem(cliente.get_email_cliente()))
            self.table_widget.setItem(row_idx, 7, QTableWidgetItem(cliente.get_telefono_cliente()))

            # Ottieni l'ID del dipendente
            dipendente = cliente.get_dipendente_inserimento()
            dipendente_id = dipendente.get_id() if dipendente else "N/A"  # Gestione del caso in cui il dipendente sia None
            self.table_widget.setItem(row_idx, 8, QTableWidgetItem(str(dipendente_id)))

            self.table_widget.setItem(row_idx, 9, QTableWidgetItem(f"{cliente.get_saldo_wallet():.2f}"))

            # Colore di sfondo di ogni cella
            for col_idx in range(10):
                item = self.table_widget.item(row_idx, col_idx)
                item.setBackground(Qt.darkCyan)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(f"Data e Ora: {current_time}")

# Metodo principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    window = VistaStampaClienti()
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()