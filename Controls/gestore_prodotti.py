import pickle
import os

class GestoreProdotti:
    def __init__(self):
        self.lista_prodotti = []
        self.file_path = 'Dati/Prodotti.pkl'  # Percorso del file nella cartella "Dati"

    # Metodo che restituisce la lista dei prodotti
    def ritorna_lista_prodotti(self):
        try:
            if not os.path.exists(self.file_path):
                print("Il file dei prodotti non esiste.")
                return []

            # Caricamento dei prodotti dal file pickle
            with open(self.file_path, 'rb') as file:
                prodotti = pickle.load(file)

            return prodotti

        except FileNotFoundError:
            print("Il file dei prodotti non è stato trovato.")
            return []

        except pickle.PickleError:
            print("Errore nel caricamento del file pickle dei prodotti.")
            return []

        except Exception as e:
            print(f"Errore imprevisto: {e}")
            return []

    # Metodo per l'aggiunta di un prodotto
    def aggiungi_prodotto(self, prodotto):
        # Si verifica se la cartella "Dati" esiste, altrimenti viene creata
        if not os.path.exists('Dati'):
            os.makedirs('Dati')

        # Caricamento dei prodotti esistenti dal file pickle
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'rb') as file:
                    self.lista_prodotti = pickle.load(file)
            except Exception as e:
                print(f"Errore nel caricamento dei prodotti: {e}")
                return

        # Verifica che l'ID del prodotto non sia duplicato
        if any(prod.get_id_prodotto() == prodotto.get_id_prodotto() for prod in self.lista_prodotti):
            print("Un prodotto con questo ID esiste già.")
            return

        # Aggiunta del nuovo prodotto alla lista
        self.lista_prodotti.append(prodotto)

        # Salvataggio della lista aggiornata nel file pickle
        try:
            with open(self.file_path, 'wb') as file:
                pickle.dump(self.lista_prodotti, file)
                return True
        except Exception as e:
            return e


    # Metodo che restituisce l'ultimo ID salvato
    def ritorna_ultimo_IDprodotto(self):
        prodotti = self.ritorna_lista_prodotti()
        if not prodotti:
            return 0  #Se la lista è vuota, ID impostato a zero

        # Ricerca dell'ID massimo tra tutti i prodotti
        ultimo_id = max(prodotto.get_id_prodotto() for prodotto in prodotti)
        return ultimo_id

    # Metodo ricerca prodotto per ID
    def ritorna_prodotto_ID(self, id_prodotto):
        prodotti = self.ritorna_lista_prodotti()

        for prodotto in prodotti:
            if str(prodotto.get_id_prodotto()) == str(id_prodotto):  # Confronta come stringhe
                return prodotto

        return None  # Nessun prodotto trovato

    # Metodo per l'eliminazione di un prodotto
    def elimina_prodotto(self, id_prodotto):
        prodotti = self.ritorna_lista_prodotti()

        if not prodotti:
            print("Il file dei prodotti è vuoto o non esiste.")
            return

        nuova_lista = [prod for prod in prodotti if prod.get_id_prodotto() != id_prodotto]

        if len(nuova_lista) == len(prodotti):
            return False

        self.lista_prodotti = nuova_lista

        # Salvataggio della lista aggiornata nel file pickle
        with open(self.file_path, 'wb') as file:
            pickle.dump(nuova_lista, file)
            return True

    # Metodo che restituisce i prodotti con giacenza critica (<10)
    def ritorna_prodotto_giacenza_critica(self):
        prodotti = self.ritorna_lista_prodotti()

        # Ricerca dei prodotti con giacenza inferiore a 10
        prodotti_critici = [prodotto for prodotto in prodotti if int (prodotto.get_giacenza()) < 5]

        return prodotti_critici

    # Metodo per riassortire la giacenza dei prodotti critici
    def riassortimento_automatico(self, id_prodotto):

        prodotti = self.ritorna_lista_prodotti()

        if not prodotti:
            print("Il file dei prodotti è vuoto o non esiste.")
            return

        prodotto_trovato = None
        for prodotto in prodotti:
            if prodotto.get_id_prodotto() == id_prodotto:
                prodotto_trovato = prodotto
                break

        if prodotto_trovato:
            # Modifica della giacenza del prodotto
            prodotto_trovato.set_giacenza()
            # Salvataggio della lista aggiornata nel file pickle
            with open(self.file_path, 'wb') as file:
                pickle.dump(prodotti, file)
                return True
        else:
            return False

    # Metodo per aggiornare la lista dei prodotti
    def aggiorna_prodotti(self, prodotti_acquistati):
        # Caricamento della lista di prodotti esistente
        lista_prodotti = self.ritorna_lista_prodotti()

        # Aggiornamento della giacenza dei prodotti
        for prodotto_acquistato in prodotti_acquistati:
            id_prodotto = prodotto_acquistato.get_id_prodotto()
            quantita = prodotto_acquistato.get_quantita()

            # Ricerca del prodotto nella lista
            for p in lista_prodotti:
                if p.get_id_prodotto() == id_prodotto:
                    nuova_giacenza = int(p.get_giacenza()) - quantita
                    p.aggiorna_giacenza(nuova_giacenza)
                    break
        # Salvataggio della lista aggiornata di prodotti nel file
        with open(self.file_path, 'wb') as file:
            pickle.dump(lista_prodotti, file)