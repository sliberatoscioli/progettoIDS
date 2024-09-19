import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt



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


class vistaDipendente(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Gestore dipendenti")
        self.setStyleSheet("background-color: #000000;")
        self.setWindowFlags(Qt.FramelessWindowHint)

        header_font = QFont("Times New Roman", 36, QFont.Bold)
        clock_font = QFont("Times New Roman", 24)
        button_font = QFont("Times New Roman", 18)

        main_layout = QVBoxLayout()

        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        spacer_top = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_top)

        header_layout = QVBoxLayout()

        self.store_name_label = QLabel("NEWSHOP\n GESTORE DIPENDENTI", self)
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
        grid_layout.setSpacing(60)

        grid_layout.addWidget(
            self.get_colored_button("Inserisci dipendente 👷", "#4CAF50", "#ffffff", self.go_inserisci_dipendente), 0, 0
        )
        grid_layout.addWidget(
            self.get_colored_button("Rimuovi Dipendente  ❌", "#FF0000", "#ffffff", self.go_rimuovi_cliente), 0, 1
        )
        grid_layout.addWidget(
            self.get_colored_button("Report dipendente  📊‍", "#007BFF", "#ffffff", self.go_report), 1, 0
        )
        grid_layout.addWidget(
            self.get_colored_button("HOME  🏠", "#6A00FF", "#ffffff", self.go_home), 1, 1
        )

        main_layout.addLayout(grid_layout)

        spacer_bottom = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        self.setLayout(main_layout)

    def get_colored_button(self, title, bg_color, text_color, on_click):
        button = QPushButton(title)
        button.setFont(QFont("Times New Roman", 35, QFont.Bold))
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

    def go_inserisci_dipendente(self):
        from Viste.VisteDipendenti.vista_inserisci_dipendente import InserisciDipendente
        self.dipendente = InserisciDipendente()
        self.dipendente.showFullScreen()
        self.close()

    def go_rimuovi_cliente(self):
        from Viste.VisteDipendenti.vista_rimuovi_dipendente import RimuoviDipendente
        self.rimuovi_view = RimuoviDipendente()
        self.rimuovi_view.showFullScreen()
        self.close()

    def go_report(self):
        from Controls.gestore_dipendenti import GestoreDipendenti
        gestore_dipendenti = GestoreDipendenti()
        gestore_dipendenti.report_dipendenti()
    def go_home(self):
        from Viste.vista_home import VistaHome
        self.home_view = VistaHome()
        self.home_view.showFullScreen()
        self.close()

    def update_clock(self):
        current_time = QTime.currentTime().toString('HH:mm:ss')
        self.clock_label.setText(current_time)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

def main():
    app = QApplication(sys.argv)
    home_window = vistaDipendente()
    home_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()