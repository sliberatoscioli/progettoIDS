# main.py
import sys
from PyQt5.QtWidgets import QApplication
from Viste.vista_login import LoginForm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_form = LoginForm()  # Creazione di un'istanza di LoginForm
    login_form.showFullScreen()  # Finestra in modalità a schermo intero
    sys.exit(app.exec_())  # Avvio dell'applicazione
