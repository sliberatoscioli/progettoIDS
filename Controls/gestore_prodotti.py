import pickle
import os
from PyQt5.QtWidgets import QMessageBox

class GestoreProdotti:
    def __init__(self):
        self.lista_prodotti = []
        self.msg_box = QMessageBox()
        self.file_path = 'Dati/Prodotti.pkl'  # Percorso del file nella cartella "Dati"

    def ritorna_lista_prodotti(self):
        try:
            if not os.path.exists(self.file_path):
                self.msg_box.setText("Il file dei prodotti non esiste.")
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.exec_()
                return []

            # Carica i prodotti dal file pickle
            with open(self.file_path, 'rb') as file:
                prodotti = pickle.load(file)

            return prodotti

        except FileNotFoundError:
            self.msg_box.setText("Il file dei prodotti non è stato trovato.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return []

        except pickle.PickleError:
            self.msg_box.setText("Errore nel caricamento del file pickle dei prodotti.")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
            return []

        except Exception as e:
            self.msg_box.setText(f"Errore imprevisto: {e}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
            return []

    def aggiungi_prodotto(self, prodotto):
        # Verifica se la cartella "Dati" esiste, altrimenti la crea
        if not os.path.exists('Dati'):
            os.makedirs('Dati')

        # Carica i prodotti esistenti dal file pickle, se esiste
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'rb') as file:
                    self.lista_prodotti = pickle.load(file)
            except Exception as e:
                self.msg_box.setText(f"Errore nel caricamento dei prodotti: {e}")
                self.msg_box.setIcon(QMessageBox.Critical)
                self.msg_box.exec_()
                return

        # Verifica che l'ID del prodotto non sia duplicato
        if any(prod.get_id_prodotto() == prodotto.get_id_prodotto() for prod in self.lista_prodotti):
            self.msg_box.setText("Un prodotto con questo ID esiste già.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

        # Aggiungi il nuovo prodotto alla lista
        self.lista_prodotti.append(prodotto)

        # Salva la lista aggiornata nel file pickle
        try:
            with open(self.file_path, 'wb') as file:
                pickle.dump(self.lista_prodotti, file)
        except Exception as e:
            self.msg_box.setText(f"Errore nel salvataggio dei prodotti: {e}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
            return

        # Mostra il messaggio di conferma
        descrizione = prodotto.get_descrizione()
        self.msg_box.setText(f"{descrizione} aggiunto con successo.")
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.exec_()

    def ritorna_ultimo_IDprodotto(self):
        prodotti = self.ritorna_lista_prodotti()
        if not prodotti:
            # Se la lista è vuota, restituisci 0 come ID predefinito
            return 0

        # Trova l'ID massimo tra tutti i prodotti
        ultimo_id = max(prodotto.get_id_prodotto() for prodotto in prodotti)
        return ultimo_id

    #Metodo ricerca prodotto per ID
    def ritorna_prodotto_ID(self, id_prodotto):
        prodotti = self.ritorna_lista_prodotti()

        for prodotto in prodotti:
            if str(prodotto.get_id_prodotto()) == str(id_prodotto):  # Confronta come stringhe
                return prodotto

        return None  # Restituisce None se non trova nessun prodotto con l'ID specificato

    def elimina_prodotto(self, id_prodotto):
        prodotti = self.ritorna_lista_prodotti()

        if not prodotti:
            self.msg_box.setText("Il file dei prodotti è vuoto o non esiste.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

        nuova_lista = [prod for prod in prodotti if prod.get_id_prodotto() != id_prodotto]

        if len(nuova_lista) == len(prodotti):
            self.msg_box.setText(f"Nessun prodotto trovato con l'ID {id_prodotto}.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

        # Salva la lista aggiornata nel file pickle
        with open(self.file_path, 'wb') as file:
            pickle.dump(nuova_lista, file)

        # Mostra il messaggio di conferma
        self.msg_box.setText(f"Prodotto con ID {id_prodotto} rimosso con successo.")
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.exec_()

    def ritorna_prodotto_giacenza_critica(self):
        # Ricavo la lista dei prodotti
        prodotti = self.ritorna_lista_prodotti()

        # Filtro i prodotti con giacenza inferiore a 10
        prodotti_critici = [prodotto for prodotto in prodotti if int (prodotto.get_giacenza()) < 10]

        return prodotti_critici

    def riassortimento_automatico(self, id_prodotto):

        prodotti = self.ritorna_lista_prodotti()

        if not prodotti:
            self.msg_box.setText("Il file dei prodotti è vuoto o non esiste.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

        prodotto_trovato = None
        for prodotto in prodotti:
            if prodotto.get_id_prodotto() == id_prodotto:
                prodotto_trovato = prodotto
                break

        if prodotto_trovato:
            # Modifica la giacenza del prodotto
            prodotto_trovato.set_giacenza()
            # Salva la lista aggiornata nel file pickle
            with open(self.file_path, 'wb') as file:
                pickle.dump(prodotti, file)
            # Mostra il messaggio di conferma
            self.msg_box.setText(f"Prodotto con ID {id_prodotto} riassortito automaticamente.")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
        else:
            self.msg_box.setText(f"Nessun prodotto trovato con l'ID {id_prodotto}.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

    # Metodo per aggiornare la lista dei prodotti
    def aggiorna_prodotti(self, prodotti_acquistati):
        # Carica la lista di prodotti esistente
        lista_prodotti = self.ritorna_lista_prodotti()

        # Aggiorna la giacenza dei prodotti
        for prodotto_acquistato in prodotti_acquistati:
            id_prodotto = prodotto_acquistato.get_id_prodotto()
            quantita = prodotto_acquistato.get_quantita()

            # Trova il prodotto nella lista
            for p in lista_prodotti:
                if p.get_id_prodotto() == id_prodotto:
                    nuova_giacenza = int(p.get_giacenza()) - quantita  # Aggiorna la giacenza
                    p.aggiorna_giacenza(nuova_giacenza)  # Imposta nuova giacenza
                    break
        # Salva la lista aggiornata di prodotti nel file
        with open(self.file_path, 'wb') as file:
            pickle.dump(lista_prodotti, file)