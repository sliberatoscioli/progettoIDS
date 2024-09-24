from PyQt5.QtWidgets import QMessageBox
import os
import shutil

class GestoreBackup:
    def __init__(self):
        # Determina il percorso del desktop dell'utente
        self.percorso_desktop = os.path.join(os.path.expanduser("~"), "Desktop") # Determina il percorso del desktop dell'utente
        self.cartella_backup = os.path.join(self.percorso_desktop, 'Backup')     # Crea la cartella 'Backup' sul desktop
        self.cartella_dati = os.path.join(os.getcwd(), "Dati")
        self.files_to_backup = ["Clienti.pkl", "Dipendenti.pkl", "Prodotti.pkl", "Acquisti.pkl"]
        self.msg_box = QMessageBox()

    # Metodo per il backup dei file
    def backup(self):
        # Crea la cartella 'Backup' se non esiste e copia i file
        if not os.path.exists(self.cartella_backup):
            os.makedirs(self.cartella_backup)
            self.msg_box.setText(f"Cartella di backup creata in: {self.cartella_backup}")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
        else:
            self.msg_box.setText(f"La cartella di backup esiste già in: {self.cartella_backup}")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

        # Copia i file dalla cartella Dati alla cartella Backup
        for file_name in self.files_to_backup:
            file_sorgente = os.path.join(self.cartella_dati, file_name)  #percorso originario
            if os.path.exists(file_sorgente):
                dest_file = os.path.join(self.cartella_backup, file_name) #percorso finale
                shutil.copy(file_sorgente, dest_file)
                self.msg_box.setText(f"Backup del file {file_name} completato.")
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.exec_()
            else:
                self.msg_box.setText(f"File {file_name} non trovato nella cartella 'Dati'.")
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.exec_()
