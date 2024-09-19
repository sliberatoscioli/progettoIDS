import os
import shutil
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt

from Viste.VisteClienti.vista_cliente import VistaCliente
from Viste.VisteDipendenti.vista_dipendente import vistaDipendente
from Viste.VisteProdotti.vista_prodotto import VistaProdotto
#from Viste.VistaVendite.Vistavendita import VistaVendita


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
            self.get_colored_button("Gestore Vendite 🛒", "#6A00FF", "#ffffff", self.go_vendita), 1, 1
        )
        grid_layout.addWidget(
            self.get_colored_button("Backup 💾", "#FF8C00", "#ffffff", self.clone_database), 2, 0, 1 ,2
        )

        main_layout.addLayout(grid_layout)

        spacer_bottom = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        self.setLayout(main_layout)

    def get_colored_button(self, title, bg_color, text_color, on_click):
        button = QPushButton(title)
        button.setFont(QFont("Times New Roman", 23, QFont.Bold))
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 100px;
                padding: 100px;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
            """
        )
        button.clicked.connect(on_click)
        return button

    def go_vista_clienti(self):
        self.clienti_window = VistaCliente()
        self.clienti_window.showFullScreen()  # Mostra la finestra a schermo intero
        self.close()

    def go_magazzino(self):
        self.prodotti_window = VistaProdotto()
        self.prodotti_window.showFullScreen()  # Mostra la finestra a schermo intero
        self.close()

    def go_dipendenti(self):
        self.dipendenti_window = vistaDipendente()
        self.dipendenti_window.showFullScreen()  # Mostra la finestra a schermo intero
        self.close()
    def go_vendita(self):
        self.vendita_window = VistaVendita()
        self.vendita_window.showFullScreen()
        self.close()

    def update_clock(self):
        current_time = QTime.currentTime().toString('HH:mm:ss')
        self.clock_label.setText(current_time)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def clone_database(self):
        # Clona il database 'negozio.db' dalla cartella 'Dati' alla cartella 'Backup_DB' situata sul Desktop dell'utente.
        try:
            source_db = os.path.join('Dati', 'negozio.db')

            if not os.path.exists(source_db):
                self.show_error(f"Il file {source_db} non esiste.")
                return
            desktop_path = os.path.join(os.path.expanduser('~'),
                                        'Desktop')  # Ottieni il percorso della cartella Desktop dell'utente
            destination_folder = os.path.join(desktop_path, 'Backup_DB')
            os.makedirs(destination_folder,
                        exist_ok=True)  # Assicurati che la cartella di destinazione esista, altrimenti creala
            destination_db = os.path.join(destination_folder, 'backup_negozio.db')
            shutil.copyfile(source_db, destination_db)  # Copia fisicamente il file del database
            self.show_success(f"Database clonato con successo da {source_db} a {destination_db}.")

        except shutil.SameFileError:
            self.show_error("Il file di origine e destinazione sono uguali. Clonazione non necessaria.")

        except PermissionError:
            self.show_error("Permesso negato. Assicurati di avere i permessi necessari per accedere ai file.")

        except Exception as e:
            self.show_error(f"Errore durante la clonazione del database: {e}")

    def show_error(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Warning)
        error_box.setWindowTitle("Errore Backup")
        error_box.setText(message)
        error_box.exec_()

    def show_success(self, message):
        success_box = QMessageBox()
        success_box.setIcon(QMessageBox.Information)
        success_box.setWindowTitle("Backup Completato")
        success_box.setText(message)
        success_box.exec_()


def main():
    app = QApplication(sys.argv)
    home_window = VistaHome()
    home_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

#COMMIT FINALE