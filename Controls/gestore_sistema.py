import sqlite3
from PyQt5.QtWidgets import QMessageBox
import os
import shutil

class GestoreSistema:
    def __init__(self):
        # Determina il percorso del desktop dell'utente
        self.percorso_desktop = os.path.join(os.path.expanduser("~"), "Desktop") # Determina il percorso del desktop dell'utente
        self.cartella_backup = os.path.join(self.percorso_desktop, 'Backup')     # Creazione della cartella 'Backup' sul desktop
        self.cartella_dati = os.path.join(os.getcwd(), "Dati")
        self.files_to_backup = ["Clienti.pkl", "Dipendenti.pkl", "Prodotti.pkl", "Acquisti.pkl"]
        self.msg_box = QMessageBox()

    def backup(self):
        # Creazione della cartella 'Backup' se non esiste e copia dei file
        cartella_creata = False
        if not os.path.exists(self.cartella_backup):
            os.makedirs(self.cartella_backup)
            cartella_creata = True

        # Copia i file dalla cartella 'Dati' alla cartella 'Backup'
        files_copiati = []
        for file_name in self.files_to_backup:
            file_sorgente = os.path.join(self.cartella_dati, file_name)
            if os.path.exists(file_sorgente):
                dest_file = os.path.join(self.cartella_backup, file_name)
                shutil.copy(file_sorgente, dest_file)
                files_copiati.append(file_name)

        return cartella_creata, self.cartella_backup, files_copiati

    # Metodo per prelevare username e password
    def preleva_username_password(self):
        db_path = os.path.join(self.cartella_dati, 'utenti.db')  # Percorso del database

        # Creazione del database e aggiunta dell'utente di default 'admin' (se db non esiste)
        if not os.path.exists(db_path):
            # Creazione della cartella 'Dati' se non esiste
            if not os.path.exists(self.cartella_dati):
                os.makedirs(self.cartella_dati)

            # Connessione al nuovo database e creazione della tabella
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS utenti (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')

            # Inserimento dell'utente di default 'admin'
            cursor.execute("INSERT INTO utenti (username, password) VALUES (?, ?)", ('admin', 'admin'))
            conn.commit()
            conn.close()

            # Notifica di creazione database e inserimento utente di default
            self.msg_box.setText("Utente e Password di default 'admin/admin'.")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()

            return [('admin', 'admin')]

        # Se il database esiste, connessione e prelievo dei dati
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT username, password FROM utenti")
            risultati = cursor.fetchall()  # Prelievo di tutti i risultati

            conn.close()

            if risultati:
                return risultati
            else:
                # Se non ci sono utenti nel database, si inserisce 'admin' di default
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO utenti (username, password) VALUES (?, ?)", ('admin', 'admin'))
                conn.commit()
                conn.close()

                self.msg_box.setText("Nessun utente trovato. Aggiunto utente di default: admin/admin")
                self.msg_box.setIcon(QMessageBox.Information)
                self.msg_box.exec_()

                return [('admin', 'admin')]

        except sqlite3.Error as e:
            self.msg_box.setText(f"Errore durante la connessione al database: {str(e)}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
            return None

    # Metodo per modificare le credenziali (username e password)
    def modifica_username_password(self, nuovo_username, nuova_password):
        db_path = os.path.join(self.cartella_dati, 'utenti.db')  # Percorso del database

        # Si verifica se il database esiste
        if not os.path.exists(db_path):
            self.msg_box.setText(f"Database utenti non trovato nella cartella 'Dati'.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

        try:
            # Connessione al database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Aggiornamento dell'unico record nella tabella
            cursor.execute('''
                UPDATE utenti
                SET username = ?, password = ?
                WHERE id = (SELECT id FROM utenti LIMIT 1)
            ''', (nuovo_username, nuova_password))

            # Si verifica se l'aggiornamento ha avuto successo
            if cursor.rowcount == 0:
                self.msg_box.setText("Nessun record trovato per l'aggiornamento.")
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.exec_()
            else:
                self.msg_box.setText(
                    f"Username e password aggiornati con successo a: {nuovo_username}/{nuova_password}")
                self.msg_box.setIcon(QMessageBox.Information)
                self.msg_box.exec_()

            # Salvataggio delle modifiche e chiusura della connessione
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            self.msg_box.setText(f"Errore durante la modifica del database: {str(e)}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()

