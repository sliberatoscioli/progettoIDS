import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QLineEdit, QMessageBox
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


class VistaResoProdotto(QMainWindow):

    def __init__(self):
        super().__init__()

        # Impostazioni della finestra
        self.setWindowTitle("Reso Prodotto")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2c3e50;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimozione del bordo della finestra

        # Layout principale
        main_layout = QVBoxLayout()

        # Barra del titolo personalizzata con pulsanti
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Titolo della finestra
        self.title_label = QLabel("RESO PRODOTTO 📦🔄", self)
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setStyleSheet("color: #ecf0f2;")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Label per data e ora
        self.datetime_label = QLabel(self)
        self.datetime_label.setFont(QFont("Arial", 14))
        self.datetime_label.setStyleSheet("color: #ecf0f2;")
        self.datetime_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.datetime_label)

        # Form ingresso
        self.codiceVendita_entry = QLineEdit(self)
        label_font = QFont("Arial", 14)
        self.codiceVendita_entry.setFont(label_font)
        self.codiceVendita_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.codiceVendita_entry.setPlaceholderText("Inserisci Codice Vendita")
        self.codiceVendita_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.codiceVendita_entry)

        # Bottone invio
        button_font = QFont("Arial", 14)
        enter_button = QPushButton("Cerca movimento di vendita", self)
        enter_button.setFont(button_font)
        enter_button.setStyleSheet("color: white; background-color: purple;")
        enter_button.setMinimumHeight(50)  # Altezza minima del pulsante
        enter_button.clicked.connect(self.enter_clicked)
        button_layout = QHBoxLayout()
        button_layout.addWidget(enter_button)
        main_layout.addLayout(button_layout)

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

        # Aggiunta della tabella al layout principale
        main_layout.addWidget(self.table_widget)

        # Widget centrale
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Timer per aggiornare la data e l'ora ogni secondo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Aggiorna ogni 1000 millisecondi (1 secondo)
        self.update_time()

    # Metodo che ricerca il codice della vendita
    def enter_clicked(self):
        try:
            codice_vendita = self.codiceVendita_entry.text().upper()
            print(codice_vendita)
            self.load_data(codice_vendita)

        except ValueError:
            self.codiceVendita_entry.setStyleSheet("color: red; background-color: #1a1a1a;")
            self.codiceVendita_entry.setPlaceholderText("Inserisci un Codice Vendita valido")

    # Metodo che recupera le informazioni di vendita
    def load_data(self, codice_vendita):  # recupera info e stampa in una tabella
        #Si restituiscono le informazioni relative a quella vendita
        from Controls.gestore_vendite import GestoreVendite
        info_acquisto = GestoreVendite()
        prodotti = info_acquisto.ricerca_acquisti(codice_vendita)

        # Si verifica se i prodotti sono caricati correttamente
        if not prodotti:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(12)
            self.table_widget.setHorizontalHeaderLabels(
                ["ID ACQUISTO", "ID CLIENTE", "DATA ACQUISTO", "ID PRODOTTO", "QUANTITA", "METODO PAGAMENTO",
                 "CODICE VENDITA", "MARCA", "COLORE", "PREZZO", "DESCRIZIONE PRODOTTO", "AZIONE\nRESO PRODOTTO"])
            return

        # Numero di righe e colonne
        self.table_widget.setRowCount(len(prodotti))
        self.table_widget.setColumnCount(12)  # Imposta il numero corretto di colonne

        # Intestazioni delle colonne
        self.table_widget.setHorizontalHeaderLabels(
            ["ID ACQUISTO", "ID CLIENTE", "DATA ACQUISTO", "ID PRODOTTO", "QUANTITA", "METODO PAGAMENTO",
             "CODICE VENDITA", "MARCA", "COLORE", "PREZZO", "DESCRIZIONE PRODOTTO", "AZIONE\nRESO PRODOTTO"])

        # Popola la tabella con i dati
        for row_idx, row_data in enumerate(prodotti):
            for col_idx, col_data in enumerate(row_data):
                if col_idx < 11:  # Assicurati di non superare il numero di colonne
                    item = QTableWidgetItem(str(col_data))
                    item.setBackground(Qt.darkCyan)
                    self.table_widget.setItem(row_idx, col_idx, item)
            action_button = QPushButton("RESO PRODOTTO")
            action_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
            action_button.clicked.connect(partial(self.reso_prodotto, row_data))
            self.table_widget.setCellWidget(row_idx, 11, action_button)  # Imposta il pulsante nell'ultima colonna

        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    # Metodo per effetuare il reso del prodotto (aumenta giacenza e carica wallet cliente)
    def reso_prodotto(self, row_data):
        from Controls.gestore_vendite import GestoreVendite
        self.msg_box = QMessageBox()
        # Estrazione dei dati dalla riga
        id_cliente = row_data[1]
        codice_vendita = row_data[6]
        id_prodotto = row_data[3]
        quantita = row_data[4]
        prezzo = row_data[9]
        reso = GestoreVendite().reso_prodotto(id_prodotto,codice_vendita,quantita,float(prezzo),id_cliente)
        if(reso == True):
            self.msg_box.setText("Reso del prodotto avvenuto con successo.")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
        else:
            self.msg_box.setText(f"Errore durante l'aggiornamento del wallet: {reso}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()

        row_idx = self.table_widget.currentRow()

        # Rimozione della riga dalla tabella
        self.table_widget.removeRow(row_idx)


    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(f"Data e Ora: {current_time}")


# Metodo principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    window = VistaResoProdotto()
    window.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()