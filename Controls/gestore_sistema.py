import os
import shutil

from pathlib import Path

from PyQt5.QtWidgets import QMessageBox


class GestoreBackup:
    def __init__(self):
        # Ottieni il percorso del desktop dell'utente
        self.desktop_path = Path.home() / "Desktop"
        self.backup_folder = self.desktop_path / "Backup"
        self.data_folder = Path("Dati")
        self.files_to_backup = ["Clienti.pkl", "Dipendenti.pkl", "Prodotti.pkl", "Acquisti.pkl"]
        self.msg_box = QMessageBox()

    def create_backup_folder(self):
        # Crea la cartella Backup se non esiste
        if not self.backup_folder.exists():
            self.backup_folder.mkdir()
            self.msg_box.setText(f"Cartella di backup creata in: {self.backup_folder}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
        else:
            self.msg_box.setText(f"La cartella di backup esiste già in: {self.backup_folder}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()

    def backup_files(self):
        # Crea la cartella di backup
        self.create_backup_folder()

        # Copia ogni file dalla cartella Dati alla cartella Backup
        for file_name in self.files_to_backup:
            source_file = self.data_folder / file_name
            if source_file.exists():
                dest_file = self.backup_folder / file_name
                shutil.copy(source_file, dest_file)
                self.msg_box.setText(f"Backup del file {file_name} completato.")
                self.msg_box.setIcon(QMessageBox.Critical)
                self.msg_box.exec_()
            else:
                self.msg_box.setText(f"File {file_name} non trovato nella cartella 'Dati'.")
                self.msg_box.setIcon(QMessageBox.Critical)
                self.msg_box.exec_()





