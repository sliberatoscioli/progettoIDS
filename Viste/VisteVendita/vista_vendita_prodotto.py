import random
import sys
from datetime import datetime
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
        self.sconto_applicato = 0.0
        self.setWindowTitle("Tabella Prodotto")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2c3e50;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimozione del bordo della finestra
        self.prezzoSconto = 0.0
        main_layout = QVBoxLayout()     # Layout principale

        # Barra del titolo personalizzata con pulsanti
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Titolo della finestra
        self.title_label = QLabel("VENDITA DI CAPI DI ABBIGLIAMENTO", self)
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
        self.quantity_entry.setPlaceholderText("Inserisci quantità")
        self.quantity_entry.setMinimumHeight(40)   # Altezza minima del pulsante
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

        # Tabella aggiunta al layout principale
        main_layout.addWidget(self.table_widget)

        # Form per numero di telefono del cliente
        form_layout2 = QVBoxLayout()

        self.telefono_cliente_entry = QLineEdit(self)
        self.telefono_cliente_entry.setFont(label_font)
        self.telefono_cliente_entry.setStyleSheet("color: white; background-color: #1a1a1a;")
        self.telefono_cliente_entry.setPlaceholderText("Inserisci numero di telefono Cliente")
        self.telefono_cliente_entry.setMinimumHeight(40)
        form_layout2.addWidget(self.telefono_cliente_entry)

        # Bottone per salvataggio delle informazioni aggiuntive
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

        # Bottoni radio per il metodo di pagamento
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

        # Timer per aggiornare la data e l'ora istantaneamente
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

        # Bottoni radio per lo sconto
        discount_group_box = QGroupBox("APPLICA SCONTO")
        discount_group_box.setFont(label_font)
        discount_group_box.setStyleSheet("color: white;")
        discount_layout = QVBoxLayout()

        self.discount_none_radio = QRadioButton("Nessuno")
        self.discount_none_radio.setFont(label_font)
        self.discount_none_radio.setStyleSheet("color: white;")
        self.discount_none_radio.setChecked(True)  # "Nessuno" impostato come defualt
        self.discount_none_radio.toggled.connect(self.applica_sconto)
        discount_layout.addWidget(self.discount_none_radio)

        self.discount_10_radio = QRadioButton("10% SCONTO")
        self.discount_10_radio.setFont(label_font)
        self.discount_10_radio.setStyleSheet("color: white;")
        self.discount_10_radio.toggled.connect(self.applica_sconto)
        discount_layout.addWidget(self.discount_10_radio)

        self.discount_20_radio = QRadioButton("20% SCONTO")
        self.discount_20_radio.setFont(label_font)
        self.discount_20_radio.setStyleSheet("color: white;")
        self.discount_20_radio.toggled.connect(self.applica_sconto)
        discount_layout.addWidget(self.discount_20_radio)

        self.discount_30_radio = QRadioButton("30% SCONTO")
        self.discount_30_radio.setFont(label_font)
        self.discount_30_radio.setStyleSheet("color: white;")
        self.discount_30_radio.toggled.connect(self.applica_sconto)
        discount_layout.addWidget(self.discount_30_radio)

        self.discount_40_radio = QRadioButton("40% SCONTO")
        self.discount_40_radio.setFont(label_font)
        self.discount_40_radio.setStyleSheet("color: white;")
        self.discount_40_radio.toggled.connect(self.applica_sconto)
        discount_layout.addWidget(self.discount_40_radio)

        self.discount_50_radio = QRadioButton("50% SCONTO")
        self.discount_50_radio.setFont(label_font)
        self.discount_50_radio.setStyleSheet("color: white;")
        self.discount_50_radio.toggled.connect(self.applica_sconto)
        discount_layout.addWidget(self.discount_50_radio)

        discount_group_box.setLayout(discount_layout)
        main_layout.addWidget(discount_group_box)

        # Pulsante "Inserisci Nuovo Cliente"
        nuovo_cliente_button = QPushButton("INSERISCI NUOVO CLIENTE", self)
        nuovo_cliente_button.setFont(button_font)
        nuovo_cliente_button.setStyleSheet("color: white; background-color: red;")
        nuovo_cliente_button.setMinimumHeight(50)
        nuovo_cliente_button.clicked.connect(self.open_nuovo_cliente)  # Collega il pulsante al metodo
        main_layout.addWidget(nuovo_cliente_button)

    # Metodo per l'applicazione dello sconto
    def applica_sconto(self):
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

        self.sconto_applicato = discount

        # Calcolo del prezzo totale scontato
        discounted_total = self.total_cost * (1 - discount)
        self.total_cost_label.setText(f"Spesa Totale: €{discounted_total:.2f}")
        self.prezzoSconto = discounted_total

    def enter_clicked(self):
        id_prodotto = self.id_entry.text().strip()
        quantity = self.quantity_entry.text().strip()

        # Controllo dei campi
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

    # Metodo per verificare la disponibiltà del prodotto
    def check_stock_and_load_data(self, id_prodotto_cercato, quantity):
        from Controls.gestore_prodotti import GestoreProdotti
        prodotto_PK = GestoreProdotti()
        prodotti = prodotto_PK.ritorna_prodotto_ID(id_prodotto_cercato)

        if not prodotti:
            QMessageBox.warning(self, "Prodotto non trovato", "Il prodotto con l'ID inserito non esiste.")
            return

        giacenza = prodotti.get_giacenza()

        if quantity > int(giacenza):
            # Messaggio di errore
            QMessageBox.warning(self, "Quantità non disponibile",
                                f"La quantità richiesta ({quantity}) è maggiore della giacenza disponibile ({giacenza}).")
            return

        self.load_data(id_prodotto_cercato, quantity)

    # Metodo per il caricamento dei prodotti
    def load_data(self, id_prodotto_cercato, quantity):
        # Ricerca del prodotto tramite ID
        from Controls.gestore_prodotti import GestoreProdotti
        prodotto_PK = GestoreProdotti()
        prodotto = prodotto_PK.ritorna_prodotto_ID(id_prodotto_cercato)

        if not prodotto:
            return   #Risultati non trovati

        scatola = prodotto.get_scatola()    # Scatola associata al prodotto

        prodotto_tuple = (
            prodotto.get_id_prodotto(),
            prodotto.get_marca(),
            prodotto.get_colore(),
            prodotto.get_prezzo(),
            prodotto.get_taglia(),
            prodotto.get_descrizione(),
            prodotto.get_tipo_prodotto(),
            prodotto.get_giacenza(),
            scatola.get_IDscatola(),
            scatola.get_descrizione_scatola(),
            scatola.get_magazzino_scatola()
        )

        # Se la tabella è vuota, imposta le intestazioni delle colonne
        if self.table_widget.rowCount() == 0:
            self.table_widget.setColumnCount(13)  # impostazione del numero di colonne
            self.table_widget.setHorizontalHeaderLabels(
                ["ID PRODOTTO", "MARCA", "COLORE", "PREZZO", "TAGLIA", "DESCRIZIONE\nPRODOTTO", "TIPO\nPRODOTTO",
                 "GIACENZA", "IDSCATOLA", "DESCRIZIONE\nSCATOLA", "ID MAGAZZINO", "QUANTITÀ",
                 "AZIONE\nRIMUOVI PRODOTTO"])

        product_id = prodotto_tuple[0]

        # Se il prodotto è già presente nella tabella, aggiornamento della quantità
        if product_id in self.product_row_map:
            row = self.product_row_map[product_id]
            current_quantity = int(
                self.table_widget.item(row, 11).text())
            quantity += current_quantity
            self.table_widget.item(row, 11).setText(str(quantity))
            # Aggiorna il costo totale
            self.total_cost += float(prodotto_tuple[3]) * (
                        quantity - current_quantity)  #
            self.update_total_cost()
            return

        # Aggiunta di un nuovo prodotto alla tabella
        row_idx = self.table_widget.rowCount()
        self.table_widget.insertRow(row_idx)

        for col_idx, col_data in enumerate(prodotto_tuple):
            if col_idx < 12:
                item = QTableWidgetItem(str(col_data))
                item.setBackground(Qt.darkCyan)
                self.table_widget.setItem(row_idx, col_idx, item)

        quantity_item = QTableWidgetItem(str(quantity))
        quantity_item.setBackground(Qt.darkCyan)
        self.table_widget.setItem(row_idx, 11, quantity_item)

        action_button = QPushButton("ELIMINA PRODOTTO")
        action_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        action_button.clicked.connect(partial(self.rimuovi_riga, product_id, row_idx, quantity))
        self.table_widget.setCellWidget(row_idx, 12, action_button)

        # Mappa l'ID prodotto all'indice di riga e prezzo
        self.product_row_map[product_id] = row_idx
        self.product_price_map[product_id] = float(prodotto_tuple[3])

        # Aggiornamento del valore totale
        self.total_cost += float(prodotto_tuple[3]) * quantity

        # Visualizzazione del costo totale
        self.update_total_cost()

        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(f"Data e Ora: {current_time}")

    # Metodo per rimuovere la riga dalla tabella
    def rimuovi_riga(self, product_id, row_idx, quantity):
        self.table_widget.removeRow(row_idx)

        # Rimozione della mappatura dell'ID prodotto
        if product_id in self.product_row_map:
            del self.product_row_map[product_id]
            # Sottrai il prezzo del prodotto dalla spesa totale
            self.total_cost -= self.product_price_map.get(product_id, 0.0) * quantity
            # Rimuovi il prezzo dal dizionario
            del self.product_price_map[product_id]

        # Aggiornamento della spesa totale
        self.update_total_cost()

    # Metodo per il salvataggio delle informazioni
    def save_info(self):
        # Controllo dei campi obbligatori
        telefono_cliente = self.telefono_cliente_entry.text().strip()
        metodo_pagamento = self.seleziona_metodo_pagamento()
        self.msg_box = QMessageBox()

        if not telefono_cliente:
            QMessageBox.warning(self, "Campo obbligatorio", "Inserisci il numero di telefono del cliente.")
            return

        if metodo_pagamento == "Nessuno":
            QMessageBox.warning(self, "Metodo di pagamento obbligatorio", "Seleziona un metodo di pagamento.")
            return

        # Controllo affiché il numero di telefono sia composto solo da cifre
        if not telefono_cliente.isdigit():
            QMessageBox.warning(self, "Errore", "Il numero di telefono deve contenere solo cifre.")
            return


        from Attivita.acquisto import Acquisto
        from Controls.gestore_vendite import GestoreVendite
        from Controls.gestore_clienti import GestoreClienti
        from Controls.gestore_prodotti import GestoreProdotti  # Importa il gestore dei prodotti

        cliente = GestoreClienti().cerca_per_telefono(telefono_cliente)


        if not cliente : #Cliente non trovato
            self.msg_box.setText(f"Nessun cliente trovato con numero di telefono {telefono_cliente}.")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
            return

        saldo_wallet = cliente[0].get_saldo_wallet()
        if saldo_wallet is None:
            return

        if saldo_wallet < self.total_cost and metodo_pagamento == "SALDO WALLET":
            QMessageBox.warning(self, "Errore",
                                f"Saldo insufficiente. Il costo totale dell'acquisto è €{self.total_cost:.2f}, "
                                f"ma il saldo del wallet è solo €{saldo_wallet:.2f}.")
            return


        codice = random.randint(10000000, 99999999)
        prodotti = []

        # Raccolta delle informazioni dai widget della tabella
        for row in range(self.table_widget.rowCount()):
            id_prodotto = self.table_widget.item(row, 0).text()
            try:
                quantita = int(self.table_widget.item(row, 11).text())
            except ValueError:
                QMessageBox.warning(self, "Errore",
                                    f"La quantità '{self.table_widget.item(row, 11).text()}' non è valida. Inserisci un numero intero.")
                return

            prodotto = GestoreProdotti().ritorna_prodotto_ID(id_prodotto)  # Recupero del prodotto

            if prodotto:
                # Aggiunta del prodotto all'elenco
                prodotto.set_quantita(quantita)
                prodotti.append(prodotto)
            else:
                QMessageBox.warning(self, "Errore", f"Prodotto con ID '{id_prodotto}' non trovato.")
                return

        if not prodotti:
            QMessageBox.warning(self, "Errore", f"Inserire dei prodotti da acquistare.")
            return

        # Creazione dell'oggetto Acquisto
        id = GestoreVendite().ritorna_ultimo_ID_acquisto() + 1
        acquisto = Acquisto(id,cliente[0],prodotti,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),metodo_pagamento,codice, self.sconto_applicato)

        #Salvataggio acquisti nel gestore vendite
        vendita = GestoreVendite().aggiungi_acquisto(acquisto) #Memorizzazione dell'acquisto nel file
        if(vendita == True):
            self.msg_box.setText(f"Acquisto con ID {acquisto.get_id()} aggiunto con successo.")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
        else:
            self.msg_box.setText(f"Errore nel salvataggio degli acquisti: {vendita}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()

        prezzo_scontato_formattato = f"€{self.prezzoSconto:.2f}"
        scontrino = GestoreVendite().CreaScontrinoAcquisto(prodotti,prezzo_scontato_formattato,acquisto.get_codice_vendita()) #creazione dello scontrino fiscale
        self.msg_box.setText(f"Scontrino creato con successo: {scontrino}")
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.exec_()

        GestoreProdotti().aggiorna_prodotti(prodotti)
        if metodo_pagamento == "SALDO WALLET":
            if self.prezzoSconto != 0:
                GestoreClienti().carica_wallet(telefono_cliente, -self.prezzoSconto, metodo_pagamento)
            else:
                GestoreClienti().carica_wallet(telefono_cliente, -self.total_cost, metodo_pagamento)

    # Metodo per la selezione della modalità di pagamento
    def seleziona_metodo_pagamento(self):
        if self.cash_radio.isChecked():
            return "CONTANTI"
        elif self.credit_card_radio.isChecked():
            return "CARTA DI CREDITO"
        elif self.wallet_radio.isChecked():
            return "SALDO WALLET"
        return "Nessuno"

    def update_total_cost(self):
        self.total_cost_label.setText(f"Spesa Totale: €{self.total_cost:.2f}")

    def open_nuovo_cliente(self):
        from Viste.VisteClienti.vista_inserisci_cliente import InserisciCliente
        self.inserisci_cliente_view = InserisciCliente()
        self.inserisci_cliente_view.resize(500, 600)  # Dimensione della finestra ridotta
        self.inserisci_cliente_view.show()

# Metodo principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    window = VistaVenditaProdotto()
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

