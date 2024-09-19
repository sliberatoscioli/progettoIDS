import random
import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QLineEdit, QGroupBox, QRadioButton, QMessageBox
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


class VistaVenditaProdotto(QMainWindow):

    def __init__(self):
        super().__init__()

        # Impostazioni della finestra
        self.setWindowTitle("Tabella Prodotto")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2c3e50;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimuove il bordo della finestra
        self.prezzoSconto = 0.0
        # Layout principale
        main_layout = QVBoxLayout()

        # Barra del titolo personalizzata con pulsanti
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Titolo della finestra
        self.title_label = QLabel("Prodotti inseriti nella vendita", self)
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
        form_layout = QHBoxLayout()

        self.id_entry = QLineEdit(self)
        label_font = QFont("Arial", 14)
        self.id_entry.setFont(label_font)
        self.id_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.id_entry.setPlaceholderText("Inserisci ID prodotto")
        self.id_entry.setMinimumHeight(40)  # Altezza minima del campo di input
        form_layout.addWidget(self.id_entry)

        self.quantity_entry = QLineEdit(self)
        self.quantity_entry.setFont(label_font)
        self.quantity_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.quantity_entry.setPlaceholderText("Inserisci Quantità")
        self.quantity_entry.setMinimumHeight(40)
        form_layout.addWidget(self.quantity_entry)

        # Bottone invio
        button_font = QFont("Arial", 14)
        enter_button = QPushButton("Cerca prodotto e aggiungi alla vendita", self)
        enter_button.setFont(button_font)
        enter_button.setStyleSheet("color: white; background-color: purple;")
        enter_button.setMinimumHeight(50)  # Altezza minima del pulsante
        enter_button.clicked.connect(self.enter_clicked)
        form_layout.addWidget(enter_button)

        main_layout.addLayout(form_layout)

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

        # Aggiungi la tabella al layout principale
        main_layout.addWidget(self.table_widget)

        # Form per numero di telefono del cliente
        form_layout2 = QVBoxLayout()

        self.telefono_cliente_entry = QLineEdit(self)
        self.telefono_cliente_entry.setFont(label_font)
        self.telefono_cliente_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.telefono_cliente_entry.setPlaceholderText("Inserisci Numero di Telefono Cliente")
        self.telefono_cliente_entry.setMinimumHeight(40)
        form_layout2.addWidget(self.telefono_cliente_entry)

        # Bottone per salvare informazioni aggiuntive
        save_button = QPushButton("ACQUISTA", self)
        save_button.setFont(button_font)
        save_button.setStyleSheet("color: white; background-color: green;")
        save_button.setMinimumHeight(50)
        save_button.clicked.connect(self.save_info)
        form_layout2.addWidget(save_button)

        main_layout.addLayout(form_layout2)

        # Spazio per la visualizzazione della spesa totale
        self.total_cost_label = QLabel("Spesa Totale: €0.00", self)
        self.total_cost_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.total_cost_label.setStyleSheet("color: #ecf0f2;")
        self.total_cost_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.total_cost_label)

        # Aggiungi il gruppo di bottoni radio per il metodo di pagamento
        payment_group_box = QGroupBox("TIPO PAGAMENTO")
        payment_group_box.setFont(label_font)
        payment_group_box.setStyleSheet("color: white;")
        payment_layout = QVBoxLayout()

        self.cash_radio = QRadioButton("CONTANTI")
        self.cash_radio.setFont(label_font)
        self.cash_radio.setStyleSheet("color: white;")
        payment_layout.addWidget(self.cash_radio)

        self.credit_card_radio = QRadioButton("CARTA DI CREDITO")
        self.credit_card_radio.setFont(label_font)
        self.credit_card_radio.setStyleSheet("color: white;")
        payment_layout.addWidget(self.credit_card_radio)

        self.wallet_radio = QRadioButton("SALDO WALLET")
        self.wallet_radio.setFont(label_font)
        self.wallet_radio.setStyleSheet("color: white;")
        payment_layout.addWidget(self.wallet_radio)

        payment_group_box.setLayout(payment_layout)
        main_layout.addWidget(payment_group_box)

        # Widget centrale
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Timer per aggiornare la data e l'ora ogni secondo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Aggiorna ogni 1000 millisecondi (1 secondo)
        self.update_time()

        # Mappa degli ID prodotto agli indici di riga e prezzi
        self.product_row_map = {}
        self.product_price_map = {}
        # Variabile per tenere traccia del costo totale
        self.total_cost = 0.0

        discount_group_box = QGroupBox("APPLICA SCONTO")
        discount_group_box.setFont(label_font)
        discount_group_box.setStyleSheet("color: white;")
        discount_layout = QVBoxLayout()

        # Radio Button per lo sconto
        discount_group_box = QGroupBox("APPLICA SCONTO")
        discount_group_box.setFont(label_font)
        discount_group_box.setStyleSheet("color: white;")
        discount_layout = QVBoxLayout()

        self.discount_none_radio = QRadioButton("Nessuno")
        self.discount_none_radio.setFont(label_font)
        self.discount_none_radio.setStyleSheet("color: white;")
        self.discount_none_radio.setChecked(True)  # Default to "Nessuno"
        self.discount_none_radio.toggled.connect(self.apply_discount)
        discount_layout.addWidget(self.discount_none_radio)

        self.discount_10_radio = QRadioButton("10% SCONTO")
        self.discount_10_radio.setFont(label_font)
        self.discount_10_radio.setStyleSheet("color: white;")
        self.discount_10_radio.toggled.connect(self.apply_discount)
        discount_layout.addWidget(self.discount_10_radio)

        self.discount_20_radio = QRadioButton("20% SCONTO")
        self.discount_20_radio.setFont(label_font)
        self.discount_20_radio.setStyleSheet("color: white;")
        self.discount_20_radio.toggled.connect(self.apply_discount)
        discount_layout.addWidget(self.discount_20_radio)

        self.discount_30_radio = QRadioButton("30% SCONTO")
        self.discount_30_radio.setFont(label_font)
        self.discount_30_radio.setStyleSheet("color: white;")
        self.discount_30_radio.toggled.connect(self.apply_discount)
        discount_layout.addWidget(self.discount_30_radio)

        self.discount_40_radio = QRadioButton("40% SCONTO")
        self.discount_40_radio.setFont(label_font)
        self.discount_40_radio.setStyleSheet("color: white;")
        self.discount_40_radio.toggled.connect(self.apply_discount)
        discount_layout.addWidget(self.discount_40_radio)

        self.discount_50_radio = QRadioButton("50% SCONTO")
        self.discount_50_radio.setFont(label_font)
        self.discount_50_radio.setStyleSheet("color: white;")
        self.discount_50_radio.toggled.connect(self.apply_discount)
        discount_layout.addWidget(self.discount_50_radio)

        discount_group_box.setLayout(discount_layout)
        main_layout.addWidget(discount_group_box)

    def apply_discount(self):
        if self.discount_none_radio.isChecked():
            discount = 0.0
        elif self.discount_10_radio.isChecked():
            discount = 0.10
        elif self.discount_20_radio.isChecked():
            discount = 0.20
        elif self.discount_30_radio.isChecked():
            discount = 0.30
        elif self.discount_40_radio.isChecked():
            discount = 0.40
        elif self.discount_50_radio.isChecked():
            discount = 0.50

        # Calculate the discounted total cost
        discounted_total = self.total_cost * (1 - discount)
        self.total_cost_label.setText(f"Spesa Totale: €{discounted_total:.2f}")
        self.prezzoSconto = discounted_total

    def enter_clicked(self):
        id_prodotto = self.id_entry.text().strip()
        quantity = self.quantity_entry.text().strip()

        # Controllo se i campi sono vuoti
        if not id_prodotto or not quantity:
            QMessageBox.warning(self, "Campi obbligatori", "Per favore, riempi tutti i campi prima di procedere.")
            return

        try:
            id_prodotto_cercato = int(id_prodotto)
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("La quantità deve essere maggiore di zero.")
            self.check_stock_and_load_data(id_prodotto_cercato, quantity)
        except ValueError:
            # Gestione dell'input non intero o della quantità non valida
            self.id_entry.setStyleSheet("color: red; background-color: #1a1a1a;")
            self.id_entry.setPlaceholderText("Inserisci un ID e una quantità validi")

    def check_stock_and_load_data(self, id_prodotto_cercato, quantity):
        from Attivita.prodotto import Prodotto
        prodottoDB = Prodotto()
        prodotti = prodottoDB.Ottieni_info_prodotto(id_prodotto_cercato)

        if not prodotti:
            # Se non ci sono risultati, non fare nulla
            QMessageBox.warning(self, "Prodotto non trovato", "Il prodotto con l'ID inserito non esiste.")
            return

        giacenza = prodotti[0][7]  # Supponendo che la giacenza sia nella colonna 7 dell'array `prodotti`

        if quantity > giacenza:
            # Mostra un messaggio di errore se la quantità richiesta è maggiore della giacenza
            QMessageBox.warning(self, "Quantità non disponibile",
                                f"La quantità richiesta ({quantity}) è maggiore della giacenza disponibile ({giacenza}).")
            return

        self.load_data(id_prodotto_cercato, quantity)

    def load_data(self, id_prodotto_cercato, quantity):
        # Connessione al database SQLite
        from Attivita.prodotto import Prodotto
        prodottoDB = Prodotto()
        prodotti = prodottoDB.Ottieni_info_prodotto(id_prodotto_cercato)

        if not prodotti:
            # Se non ci sono risultati, non fare nulla
            return

        # Se la tabella è vuota, imposta le intestazioni delle colonne
        if self.table_widget.rowCount() == 0:
            self.table_widget.setColumnCount(13)  # Imposta il numero corretto di colonne (inclusa la colonna Quantità)
            self.table_widget.setHorizontalHeaderLabels(
                ["ID PRODOTTO", "MARCA", "COLORE", "PREZZO", "TAGLIA", "DESCRIZIONE\nPRODOTTO", "TIPO\nPRODOTTO",
                 "GIACENZA", "IDSCATOLA", "DESCRIZIONE\nSCATOLA", "ID MAGAZZINO", "QUANTITÀ",
                 "AZIONE\nRIMUOVI PRODOTTO"])

        # Aggiungi nuove righe alla tabella per i prodotti cercati
        for row_data in prodotti:
            product_id = row_data[0]
            # Se il prodotto è già presente nella tabella, aggiorna la quantità
            if product_id in self.product_row_map:
                row = self.product_row_map[product_id]
                current_quantity = int(
                    self.table_widget.item(row, 11).text())  # Supponiamo che la quantità sia nella colonna 11
                quantity += current_quantity
                self.table_widget.item(row, 11).setText(str(quantity))  # Aggiorna la quantità
                # Aggiorna il costo totale
                self.total_cost += float(row_data[3]) * quantity
                self.update_total_cost()
                return

            # Aggiungi nuovo prodotto alla tabella
            row_idx = self.table_widget.rowCount()
            self.table_widget.insertRow(row_idx)

            for col_idx, col_data in enumerate(row_data):
                if col_idx < 12:  # Assicurati di non superare il numero di colonne
                    item = QTableWidgetItem(str(col_data))
                    item.setBackground(Qt.darkCyan)
                    self.table_widget.setItem(row_idx, col_idx, item)

            quantity_item = QTableWidgetItem(str(quantity))
            quantity_item.setBackground(Qt.darkCyan)
            self.table_widget.setItem(row_idx, 11, quantity_item)

            action_button = QPushButton("ELIMINA PRODOTTO")
            action_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
            action_button.clicked.connect(partial(self.perform_action1, product_id, row_idx, quantity))
            self.table_widget.setCellWidget(row_idx, 12, action_button)

            # Mappa l'ID prodotto all'indice di riga e prezzo
            self.product_row_map[product_id] = row_idx
            self.product_price_map[product_id] = float(row_data[3])  # Prezzo del prodotto

            # Aggiorna la spesa totale
            self.total_cost += float(row_data[3]) * quantity

        # Aggiorna la visualizzazione della spesa totale
        self.update_total_cost()

        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(f"Data e Ora: {current_time}")

    def perform_action1(self, product_id, row_idx, quantity):
        # Rimuovi la riga dalla tabella
        self.table_widget.removeRow(row_idx)
        # Rimuovi la mappatura dell'ID prodotto
        if product_id in self.product_row_map:
            del self.product_row_map[product_id]
            # Sottrai il prezzo del prodotto dalla spesa totale
            self.total_cost -= self.product_price_map.get(product_id, 0.0) * quantity
            # Rimuovi il prezzo dal dizionario
            del self.product_price_map[product_id]

        # Aggiorna la visualizzazione della spesa totale
        self.update_total_cost()

    def save_info(self):
        # Controllo dei campi obbligatori
        telefono_cliente = self.telefono_cliente_entry.text().strip()
        metodo_pagamento = self.get_selected_payment_method()

        if not telefono_cliente:
            QMessageBox.warning(self, "Campo obbligatorio", "Inserisci il numero di telefono del cliente.")
            return

        if metodo_pagamento == "Nessuno":
            QMessageBox.warning(self, "Metodo di pagamento obbligatorio", "Seleziona un metodo di pagamento.")
            return

        from Attivita.acquisto import Acquisto
        from Attivita.cliente import Cliente
        cliente = Cliente()

        saldo_wallet = cliente.ritorna_wallet(telefono_cliente)
        if saldo_wallet is None:
            return

        if saldo_wallet < self.total_cost and metodo_pagamento == "SALDO WALLET":
            QMessageBox.warning(self, "Errore",
                                f"Saldo insufficiente. Il costo totale dell'acquisto è €{self.total_cost:.2f}, ma il saldo del wallet è solo €{saldo_wallet:.2f}.")
            return

        Acquisto = Acquisto()
        codice = random.randint(10000000, 99999999)
        products = []

        # Raccolta delle informazioni dai widget della tabella
        for row in range(self.table_widget.rowCount()):
            product_info = {
                'id_prodotto': self.table_widget.item(row, 0).text(),
                'marca': self.table_widget.item(row, 1).text(),
                'colore': self.table_widget.item(row, 2).text(),
                'prezzo': self.table_widget.item(row, 3).text(),
                'taglia': self.table_widget.item(row, 4).text(),
                'descrizione_prodotto': self.table_widget.item(row, 5).text(),
                'tipo_prodotto': self.table_widget.item(row, 6).text(),
                'giacenza': self.table_widget.item(row, 7).text(),
                'id_scatola': self.table_widget.item(row, 8).text(),
                'descrizione_scatola': self.table_widget.item(row, 9).text(),
                'id_magazzino': self.table_widget.item(row, 10).text(),
                'quantita': self.table_widget.item(row, 11).text(),
            }
            products.append(product_info)

        # Inserimento delle informazioni di acquisto per ogni prodotto
        for product in products:
            id_prodotto = product['id_prodotto']
            try:
                quantita = int(product['quantita'])  # Converti quantita in intero
            except ValueError:
                QMessageBox.warning(self, "Errore",
                                    f"La quantità '{product['quantita']}' non è valida. Inserisci un numero intero.")
                return

            Acquisto.inserisci_acquisto(
                telefono_cliente,  # Numero di telefono del cliente
                id_prodotto,  # ID del prodotto
                quantita,  # Quantità acquistata
                metodo_pagamento,  # Metodo di pagamento
                str(codice)  # Codice generato per l'acquisto
            )

        Acquisto.CreaScontrinoAcquisto(products, self.prezzoSconto, str(codice))


    def get_selected_payment_method(self):
        if self.cash_radio.isChecked():
            return "CONTANTI"
        elif self.credit_card_radio.isChecked():
            return "CARTA DI CREDITO"
        elif self.wallet_radio.isChecked():
            return "SALDO WALLET"
        return "Nessuno"

    def update_total_cost(self):
        self.total_cost_label.setText(f"Spesa Totale: €{self.total_cost:.2f}")


def main():
    app = QApplication(sys.argv)
    window = VistaVenditaProdotto()
    window.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

#ULTIMA MODIFICA

