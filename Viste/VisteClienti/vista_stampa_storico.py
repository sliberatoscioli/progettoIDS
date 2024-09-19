
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel
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

class VistaStampaStoricoCliente(QMainWindow):

    def __init__(self,IdCliente):
        super().__init__()
        self.IdCliente = IdCliente

        # Impostazioni della finestra
        self.setWindowTitle(f"Stampa Storico Acquisti cliente ID {IdCliente}")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #34495e;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimuove il bordo della finestra

        # Layout principale
        main_layout = QVBoxLayout()

        # Barra del titolo personalizzata con pulsanti
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Titolo della finestra
        self.title_label = QLabel(f"Storico acquisti cliente ID : {IdCliente} ", self)
        self.title_label.setFont(QFont("Times New Roman", 20, QFont.Bold))
        self.title_label.setStyleSheet("color: White;")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Label per data e ora
        self.datetime_label = QLabel(self)
        self.datetime_label.setFont(QFont("Times New Roman", 14))
        self.datetime_label.setStyleSheet("color: white;")
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

        # Modifica delle intestazioni delle colonne
        self.table_widget.horizontalHeader().setStyleSheet(
            "background-color: black; color: black; font-weight: bold;"
        )

        # Aggiungi la tabella al layout principale
        main_layout.addWidget(self.table_widget)

        # Layout per il pulsante
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 50, 0, 0)  # Margini sopra il pulsante
        button_layout.setSpacing(10)

        button_layout = QHBoxLayout()
        button_font = QFont("Times New Roman", 14)


        # Aggiungi il layout del pulsante al layout principale
        main_layout.addLayout(button_layout)

        # Widget centrale
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Carica i dati dal database e popola la tabella
        self.load_data()

        # Timer per aggiornare la data e l'ora ogni secondo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Aggiorna ogni 1000 millisecondi (1 secondo)
        self.update_time()



    def load_data(self):
       # DA MODIFICARE PERCHE BISGONA PRENDERE GLI ACQUISTI ECC...
        from Attivita.cliente import Cliente
        clientiDB = Cliente()
        clienti = clientiDB.stampa_storico_cliente(self.IdCliente)

        # Assicurati che i dati siano stati recuperati
        if clienti is None:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(10)  # Imposta il numero corretto di colonne
            self.table_widget.setHorizontalHeaderLabels(
                ["ID PRODOTTO", "MARCA", "PREZZO", "DESCRIZIONE", "TIPO PRODOTTO", "DATA ACQUISTO", "QUANTITA", "METODO PAGAMENTO"])
            return

        # Imposta il numero di righe e colonne
        self.table_widget.setRowCount(len(clienti))
        self.table_widget.setColumnCount(8)  # Imposta il numero corretto di colonne

        # Imposta le intestazioni delle colonne
        self.table_widget.setHorizontalHeaderLabels(
            ["ID PRODOTTO", "MARCA", "PREZZO", "DESCRIZIONE", "TIPO PRODOTTO", "DATA ACQUISTO", "QUANTITA", "METODO PAGAMENTO"])


        # Popola la tabella con i dati
        for row_idx, row_data in enumerate(clienti):
            for col_idx, col_data in enumerate(row_data):
                if col_idx < 8:  # Assicurati di non superare il numero di colonne
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
                    item = QTableWidgetItem(str(col_data))
                    item.setBackground(Qt.darkCyan)
                    self.table_widget.setItem(row_idx, col_idx, item)


        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(f"Data e Ora: {current_time}")

def main():
    app = QApplication(sys.argv)
    window = VistaStampaStoricoCliente()
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()