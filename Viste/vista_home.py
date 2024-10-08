import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel, QMessageBox, QGridLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt

from Viste.VisteClienti.vista_cliente import VistaCliente
from Viste.VisteDipendenti.vista_dipendente import vistaDipendente
from Viste.VisteProdotti.vista_prodotto import VistaProdotto
from Viste.VisteVendita.vista_vendita import VistaVendita


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


class VistaHome(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Gestore Negozio")
        self.setStyleSheet("background-color: black;")
        self.setWindowFlags(Qt.FramelessWindowHint)

        header_font = QFont("Times New Roman", 30, QFont.Bold)
        clock_font = QFont("Times New Roman", 24)
        button_font = QFont("Times New Roman", 18)

        main_layout = QVBoxLayout()

        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        spacer_top = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_top)

        header_layout = QVBoxLayout()

        self.store_name_label = QLabel("NEWSHOP\n Home View", self)
        self.store_name_label.setFont(header_font)
        self.store_name_label.setStyleSheet("color: white;")
        self.store_name_label.setAlignment(Qt.AlignCenter)

        self.clock_label = QLabel(self)
        self.clock_label.setFont(clock_font)
        self.clock_label.setStyleSheet("color: #bdbdbd;")
        self.clock_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(self.store_name_label)
        header_layout.addWidget(self.clock_label)

        main_layout.addLayout(header_layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)

        self.update_clock()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(40)

        grid_layout.addWidget(
            self.get_colored_button("Gestore Clienti 🧑‍💼", "#4CAF50", "#ffffff", self.go_vista_clienti), 0, 0
        )
        grid_layout.addWidget(
            self.get_colored_button("Gestore Magazzino 📦", "#FF0000", "#ffffff", self.go_magazzino), 0, 1
        )
        grid_layout.addWidget(
            self.get_colored_button("Gestore Dipendenti 👷‍", "#007BFF", "#ffffff", self.go_dipendenti), 1, 0
        )
        grid_layout.addWidget(
            self.get_colored_button("Gestore Vendite 🛒", "#4B0082", "#ffffff", self.go_vendita), 1, 1
        )
        grid_layout.addWidget(
            self.get_colored_button("Backup 💾", "#FF8C00", "#ffffff", self.go_backup), 2, 0, 1, 2
        )

        main_layout.addLayout(grid_layout)

        spacer_bottom = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        self.setLayout(main_layout)

    def get_colored_button(self, title, bg_color, text_color, on_click):
        button = QPushButton(title)
        button.setFont(QFont("Times New Roman", 30, QFont.Bold))
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 80px;
                padding: 80px;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
            """
        )
        button.clicked.connect(on_click)
        return button

    def go_vista_clienti(self):
        self.clienti_window = VistaCliente()     #Collegamento alla vista clienti
        self.clienti_window.showFullScreen()
        self.close()

    def go_magazzino(self):
        self.prodotti_window = VistaProdotto()     #Collegamento alla vista prodotti
        self.prodotti_window.showFullScreen()
        self.close()

    def go_dipendenti(self):
        self.dipendenti_window = vistaDipendente()   #Collegamento alla vista dipendenti
        self.dipendenti_window.showFullScreen()
        self.close()

    def go_vendita(self):
        self.vendita_window = VistaVendita()   #Collegamento alla vista vendita
        self.vendita_window.showFullScreen()
        self.close()

    def go_backup(self):
        from Controls.gestore_sistema import GestoreSistema
        gestore = GestoreSistema()
        cartella_creata, cartella_backup, files_copiati = gestore.backup()
        self.msg_box = QMessageBox()

        # Crea un messaggio di conferma sul backup
        if cartella_creata:
            self.msg_box.setText(f"Cartella di backup creata in: {cartella_backup}\n")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

        else:
            self.msg_box.setText(f"La cartella di backup esiste già in: {cartella_backup}\n")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

        if files_copiati:
            self.msg_box.setText(f"Backup dei seguenti file completato:\n" + "\n".join(files_copiati))
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
        else:
            self.msg_box.setText("Nessun file trovato per il backup.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

    def update_clock(self):
        current_time = QTime.currentTime().toString('HH:mm:ss')
        self.clock_label.setText(current_time)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

# Metodo principale per avviare l'applicazione
def main():
    app = QApplication(sys.argv)
    home_window = VistaHome()
    home_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

