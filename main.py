# main.py

import sys
from PyQt5.QtWidgets import QApplication
from Viste.vista_login import LoginForm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_form = LoginForm()  # Crea un'istanza di LoginForm
    login_form.showFullScreen()  # Mostra la finestra in modalità a schermo intero
    sys.exit(app.exec_())  # Avvia il loop dell'applicazione
