import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
                             QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QMessageBox)
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


class VistaRiepilogoGiornaliero(QMainWindow):

    def __init__(self):
        super().__init__()

        # Impostazioni della finestra
        self.setWindowTitle("Riepilogo Totale Giornaliero")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("background-color: #2c3e50;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimozione del bordo della finestra

        # Layout principale
        main_layout = QVBoxLayout()

        # Barra del titolo personalizzata con pulsanti
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Titolo della finestra
        self.title_label = QLabel("Riepilogo totale giornaliero 🛍️️", self)
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

        # Tabella per gli utenti con acquisti
        self.user_table = QTableWidget()
        self.user_table.setStyleSheet("""
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
        main_layout.addWidget(self.user_table)

        # Tabella per la classificazione dei prodotti
        self.category_table = QTableWidget()
        self.category_table.setStyleSheet("""
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
        main_layout.addWidget(self.category_table)

        # Layout per i totali
        totals_layout = QVBoxLayout()
        self.total_label = QLabel("Totali", self)
        self.total_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_label.setStyleSheet("color: #ecf0f1;")
        self.total_label.setAlignment(Qt.AlignCenter)
        totals_layout.addWidget(self.total_label)

        # Etichette per i totali
        self.credit_card_total_label = QLabel(self)
        self.credit_card_total_label.setFont(QFont("Arial", 14))
        self.credit_card_total_label.setStyleSheet("color: #ecf0f1;")
        totals_layout.addWidget(self.credit_card_total_label)

        self.cash_total_label = QLabel(self)
        self.cash_total_label.setFont(QFont("Arial", 14))
        self.cash_total_label.setStyleSheet("color: #ecf0f1;")
        totals_layout.addWidget(self.cash_total_label)

        self.wallet_total_label = QLabel(self)
        self.wallet_total_label.setFont(QFont("Arial", 14))
        self.wallet_total_label.setStyleSheet("color: #ecf0f1;")
        totals_layout.addWidget(self.wallet_total_label)

        self.grand_total_label = QLabel(self)
        self.grand_total_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.grand_total_label.setStyleSheet("color: #ecf0f1;")
        totals_layout.addWidget(self.grand_total_label)

        main_layout.addLayout(totals_layout)

        # Layout per il pulsante
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 50, 0, 0)  # Margini sopra il pulsante
        button_layout.setSpacing(10)

        main_layout.addLayout(button_layout)

        # Widget centrale
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.load_data()

        # Timer per aggiornare la data e l'ora ogni secondo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Aggiorna ogni 1000 millisecondi (1 secondo)
        self.update_time()

    # Metodo per il caricamento dei dati
    def load_data(self):
        from Controls.gestore_vendite import GestoreVendite
        self.msg_box = QMessageBox()
        riepilogo = GestoreVendite()
        info, totale_contanti, totale_carta_di_credito, totale_saldo_wallet, quantita_per_categoria, path_name = riepilogo.riepilogo_giornaliero()

        # Si verifica se i dati sono caricati correttamente
        if info is None:
            self.user_table.setRowCount(0)
            self.user_table.setColumnCount(14)
            self.user_table.setHorizontalHeaderLabels(
                ["NOME", "COGNOME", "EMAIL", "TELEFONO", "SALDO WALLET", "MARCA", "TAGLIA", "COLORE",
                 "PREZZO", "TIPO PRODOTTO", "DESCRIZIONE", "DATA ACQUISTO", "QUANTITA\nACQUISTATA", "METODO PAGAMENTO"])
            self.category_table.setRowCount(0)
            self.category_table.setColumnCount(2)
            self.category_table.setHorizontalHeaderLabels(["TIPO PRODOTTO", "QUANTITA ACQUISTATA"])
            return

        # Popola la tabella degli utenti con acquisti
        self.user_table.setRowCount(len(info))
        self.user_table.setColumnCount(14)
        self.user_table.setHorizontalHeaderLabels(
            ["NOME", "COGNOME", "EMAIL", "TELEFONO", "SALDO WALLET", "MARCA", "TAGLIA", "COLORE",
             "PREZZO", "TIPO PRODOTTO", "DESCRIZIONE", "DATA ACQUISTO", "QUANTITA\nACQUISTATA", "METODO PAGAMENTO"])
        self.user_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        for row_idx, row_data in enumerate(info):
            for col_idx, col_data in enumerate(row_data):
                if col_idx < 14:
                    item = QTableWidgetItem(str(col_data))
                    item.setBackground(Qt.darkCyan)
                    self.user_table.setItem(row_idx, col_idx, item)
        self.user_table.resizeColumnsToContents()
        self.user_table.horizontalHeader().setStretchLastSection(True)

        # Popola la tabella della classificazione dei prodotti
        self.category_table.setRowCount(len(quantita_per_categoria))
        self.category_table.setColumnCount(2)
        self.category_table.setHorizontalHeaderLabels(["TIPO PRODOTTO", "QUANTITA ACQUISTATA"])
        self.category_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        for row_idx, row_data in enumerate(quantita_per_categoria):
            for col_idx, col_data in enumerate(row_data):
                if col_idx < 2:
                    item = QTableWidgetItem(str(col_data))
                    item.setBackground(Qt.darkCyan)
                    self.category_table.setItem(row_idx, col_idx, item)
        self.category_table.resizeColumnsToContents()
        self.category_table.horizontalHeader().setStretchLastSection(True)

        # Aggiornamento delle etichette dei totali
        self.credit_card_total_label.setText(f"1) Totale con Carta di Credito: €{totale_carta_di_credito:.2f}")
        self.cash_total_label.setText(f"2) Totale in Contanti: €{totale_contanti:.2f}")
        self.wallet_total_label.setText(f"3) Totale Saldi Wallet: €{totale_saldo_wallet:.2f}")
        grand_total = totale_carta_di_credito + totale_contanti + totale_saldo_wallet
        self.grand_total_label.setText(f"4) Totale Complessivo: €{grand_total:.2f}")

        self.msg_box.setText(f"Riepilogo giornaliero in PDF generato con successo: {path_name}")
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.exec_()

    # Metodo per aggiornare la data in tempo reale
    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(f"Data e Ora: {current_time}")

# Metodo principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    window = VistaRiepilogoGiornaliero()
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# ULTIMA MODIFICA



