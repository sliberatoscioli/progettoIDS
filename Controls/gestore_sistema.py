from PyQt5.QtWidgets import QMessageBox
import os
import shutil

class GestoreBackup:
    def __init__(self):
        # Determina il percorso del desktop dell'utente
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop") # Determina il percorso del desktop dell'utente
        self.backup_folder = os.path.join(self.desktop_path, 'Backup')     # Crea la cartella 'Backup' sul desktop
        self.data_folder = os.path.join(os.getcwd(), "Dati")
        self.files_to_backup = ["Clienti.pkl", "Dipendenti.pkl", "Prodotti.pkl", "Acquisti.pkl"]
        self.msg_box = QMessageBox()

    def backup(self):
        # Crea la cartella 'Backup' se non esiste e copia i file
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)
            self.msg_box.setText(f"Cartella di backup creata in: {self.backup_folder}")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
        else:
            self.msg_box.setText(f"La cartella di backup esiste già in: {self.backup_folder}")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

        # Copia i file dalla cartella Dati alla cartella Backup
        for file_name in self.files_to_backup:
            source_file = os.path.join(self.data_folder, file_name)
            if os.path.exists(source_file):
                dest_file = os.path.join(self.backup_folder, file_name)
                shutil.copy(source_file, dest_file)
                self.msg_box.setText(f"Backup del file {file_name} completato.")
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.exec_()
            else:
                self.msg_box.setText(f"File {file_name} non trovato nella cartella 'Dati'.")
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.exec_()
