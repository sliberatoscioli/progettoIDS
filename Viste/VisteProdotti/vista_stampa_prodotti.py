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
        self.window().close()


class VistaStampaProdotti(QMainWindow):
    def __init__(self):
        super().__init__()

        # Impostazioni della finestra
        self.setWindowTitle("Tabella Prodotti")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2c3e50;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimozione del bordo della finestra

        # Layout principale
        main_layout = QVBoxLayout()

        # Barra del titolo personalizzata con pulsanti
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Titolo della finestra
        self.title_label = QLabel("LISTA PRODOTTI IN MAGAZZINO 📄", self)
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

        # Tabella aggiunta al layout principale
        main_layout.addWidget(self.table_widget)

        # Layout per il pulsante
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 50, 0, 0)  # Margini sopra il pulsante
        button_layout.setSpacing(10)

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

    # Metodo per caricare i dati da stampare
    def load_data(self):
        # Richiesta della lista prodotti
        from Controls.gestore_prodotti import GestoreProdotti
        prodotti = GestoreProdotti().ritorna_lista_prodotti()

        # Si verifica che i dati siano stati recuperati
        if not prodotti:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(11)
            self.table_widget.setHorizontalHeaderLabels(
                ["ID PRODOTTO", "MARCA", "COLORE", "PREZZO", "TAGLIA", "DESCRIZIONE\nPRODOTTO", "TIPO\nPRODOTTO",
                 "GIACENZA", "ID SCATOLA", "DESCRIZIONE\nSCATOLA", "ID MAGAZZINO"])
            return

        # Numero di righe e colonne
        self.table_widget.setRowCount(len(prodotti))
        self.table_widget.setColumnCount(11)

        # Intestazioni delle colonne
        self.table_widget.setHorizontalHeaderLabels(
            ["ID PRODOTTO", "MARCA", "COLORE", "PREZZO", "TAGLIA", "DESCRIZIONE\nPRODOTTO", "TIPO\nPRODOTTO",
             "GIACENZA", "ID SCATOLA", "DESCRIZIONE\nSCATOLA", "ID MAGAZZINO"])

        # Intestazioni centrate
        self.table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Popolamento della tabella con i dati
        for row_idx, prodotto in enumerate(prodotti):
            scatola = prodotto.get_scatola()  # Scatola associata al prodotto

            self.table_widget.setItem(row_idx, 0, QTableWidgetItem(str(prodotto.get_id_prodotto())))
            self.table_widget.setItem(row_idx, 1, QTableWidgetItem(prodotto.get_marca()))
            self.table_widget.setItem(row_idx, 2, QTableWidgetItem(prodotto.get_colore()))
            self.table_widget.setItem(row_idx, 3, QTableWidgetItem(str(prodotto.get_prezzo())))
            self.table_widget.setItem(row_idx, 4, QTableWidgetItem(prodotto.get_taglia()))
            self.table_widget.setItem(row_idx, 5, QTableWidgetItem(prodotto.get_descrizione()))
            self.table_widget.setItem(row_idx, 6, QTableWidgetItem(prodotto.get_tipo_prodotto()))
            self.table_widget.setItem(row_idx, 7, QTableWidgetItem(str(prodotto.get_giacenza())))

            # Popolamento dati scatola associata
            self.table_widget.setItem(row_idx, 8, QTableWidgetItem(str(scatola.get_IDscatola())))
            self.table_widget.setItem(row_idx, 9, QTableWidgetItem(scatola.get_descrizione_scatola()))
            self.table_widget.setItem(row_idx, 10, QTableWidgetItem(str(scatola.get_magazzino_scatola())))

        # Visualizzazione della tabella
        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(f"Data e Ora: {current_time}")

# Metodo principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    window = VistaStampaProdotti()
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
#COMMIT FINALE