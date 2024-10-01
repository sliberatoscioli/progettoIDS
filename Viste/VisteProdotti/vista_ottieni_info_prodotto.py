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


class VistaOttieniInfoProdotto(QMainWindow):

    def __init__(self):
        super().__init__()

        # Impostazioni della finestra
        self.setWindowTitle("Tabella Prodotto")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2c3e50;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimozione del bordo della finestra

        # Layout principale
        main_layout = QVBoxLayout()

        # Barra del titolo personalizzata con pulsanti
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Titolo della finestra
        self.title_label = QLabel("Prodotto Ricercato", self)
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
        self.id_entry = QLineEdit(self)
        label_font = QFont("Arial", 14)
        self.id_entry.setFont(label_font)
        self.id_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.id_entry.setPlaceholderText("Inserisci ID prodotto da ricercare")
        self.id_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        main_layout.addWidget(self.id_entry)

        # Bottone invio
        button_font = QFont("Arial", 14)
        enter_button = QPushButton("Cerca prodotto tramite ID", self)
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

        # Tabella aggiunta al layout principale
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

    def enter_clicked(self):
        try:
            id_prodotto_cercato = self.id_entry.text()  # Mantieni l'ID come stringa
            if not id_prodotto_cercato.isdigit():  # Verifica se l'ID è un numero
                raise ValueError("L'ID deve essere un numero intero")
            id_prodotto_cercato = int(id_prodotto_cercato)  # Converti a intero se necessario
            self.load_data(id_prodotto_cercato)
        except ValueError:
            # Gestisci l'input non valido
            self.id_entry.setStyleSheet("color: red; background-color: #1a1a1a;")
            self.id_entry.setPlaceholderText("Inserisci un ID valido")

    # Metodo per il caricamento delle informazioni
    def load_data(self, id_prodottocercato):
        from Controls.gestore_prodotti import GestoreProdotti

        prodotto = GestoreProdotti().ritorna_prodotto_ID(id_prodottocercato)

        # Si verifica se il prodotto è stato recuperato
        if not prodotto:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(12)
            self.table_widget.setHorizontalHeaderLabels(
                ["ID PRODOTTO", "MARCA", "COLORE", "PREZZO ", "TAGLIA", "DESCRIZIONE\n PRODOTTO", "TIPO\nPRODOTTO",
                 "GIACENZA", "IDSCATOLA", "DESCRIZIONE\nSCATOLA", "ID MAGAZZINO", "AZIONE\nRIMUOVI PRODOTTO"])
            return

        scatola = prodotto.get_scatola()        # Recupero della scatola associata al prodotto

        # Numero di righe e colonne
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(12)

        # Intestazioni delle colonne
        self.table_widget.setHorizontalHeaderLabels(
            ["ID PRODOTTO", "MARCA", "COLORE", "PREZZO ", "TAGLIA", "DESCRIZIONE\n PRODOTTO", "TIPO\nPRODOTTO",
             "GIACENZA", "IDSCATOLA", "DESCRIZIONE\nSCATOLA", "ID MAGAZZINO", "AZIONE\nRIMUOVI PRODOTTO"])

        # Popolamento della tabella con i dati
        self.table_widget.setItem(0, 0, QTableWidgetItem(str(prodotto.get_id_prodotto())))
        self.table_widget.setItem(0, 1, QTableWidgetItem(prodotto.get_marca()))
        self.table_widget.setItem(0, 2, QTableWidgetItem(prodotto.get_colore()))
        self.table_widget.setItem(0, 3, QTableWidgetItem(str(prodotto.get_prezzo())))
        self.table_widget.setItem(0, 4, QTableWidgetItem(prodotto.get_taglia()))
        self.table_widget.setItem(0, 5, QTableWidgetItem(prodotto.get_descrizione()))
        self.table_widget.setItem(0, 6, QTableWidgetItem(prodotto.get_tipo_prodotto()))
        self.table_widget.setItem(0, 7, QTableWidgetItem(str(prodotto.get_giacenza())))
        self.table_widget.setItem(0, 8, QTableWidgetItem(str(scatola.get_IDscatola())))
        self.table_widget.setItem(0, 9, QTableWidgetItem(scatola.get_descrizione_scatola()))
        self.table_widget.setItem(0, 10, QTableWidgetItem(str(scatola.get_magazzino_scatola())))

        # Creazione del pulsante di azione
        action_button = QPushButton("ELIMINA PRODOTTO")
        action_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        action_button.clicked.connect(partial(self.elimina_prodotto, prodotto.get_id_prodotto()))
        self.table_widget.setCellWidget(0, 11, action_button)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(f"Data e Ora: {current_time}")

    # Metodo per l'eliminazione di un prodotto dal file
    def elimina_prodotto(self, prodotto_id):
        from Controls.gestore_prodotti import GestoreProdotti
        self.msg_box = QMessageBox()
        gestore_prodotto = GestoreProdotti()

        # Eliminare il prodotto
        elimina = gestore_prodotto.elimina_prodotto(prodotto_id)
        if(elimina == True):
            self.msg_box.setText(f"Prodotto con ID {prodotto_id} rimosso con successo.")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
        else:
            self.msg_box.setText(f"Nessun prodotto trovato con l'ID {prodotto_id}.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

        # Ricerca e rimozione della riga dalla tabella
        row_count = self.table_widget.rowCount()
        for row in range(row_count):
            item = self.table_widget.item(row, 0)
            if item and item.text() == str(prodotto_id):
                self.table_widget.removeRow(row)
                break

# Metodo principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    window = VistaOttieniInfoProdotto()
    window.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()