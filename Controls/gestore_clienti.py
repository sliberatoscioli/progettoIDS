import os
import pickle
from Controls.gestore_vendite import GestoreVendite
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
import webbrowser  # Per aprire il PDF



class GestoreClienti:

    def __init__(self):
        self.lista_clienti = []
        self.file_path = 'Dati/Clienti.pkl'  # Percorso del file nella cartella "Dati"

    def ritorna_lista_clienti(self):
        try:
            # Verifica se il file dei clienti esiste
            if not os.path.exists(self.file_path):
                return []

            # Carica i clienti dal file pickle
            with open(self.file_path, 'rb') as file:
                clienti = pickle.load(file)

            return clienti

        except FileNotFoundError:
            print("Il file dei clienti non è stato trovato.")
            return []

        except pickle.PickleError:
            print("Errore nel caricamento del file pickle dei clienti.")
            return []

        except Exception as e:
            print(f"Errore imprevisto: {e}")
            return []

    def aggiungi_cliente(self, cliente):
        # Verifica se la cartella "Dati" esiste, altrimenti la crea
        if not os.path.exists('Dati'):
            os.makedirs('Dati')

        # Verifica se il file pickle esiste già
        if os.path.exists(self.file_path):
            try:
                # Carica i clienti esistenti
                with open(self.file_path, 'rb') as file:
                    self.lista_clienti = pickle.load(file)
            except (EOFError, pickle.PickleError):
                # Se il file è vuoto o corrotto, inizializza la lista come vuota
                self.lista_clienti = []

        # Controlla se il numero di telefono è già presente
        numero_telefono_nuovo = cliente.get_telefono_cliente()
        for c in self.lista_clienti:
            if c.get_telefono_cliente() == numero_telefono_nuovo:
                return False

        # Aggiungi il nuovo cliente alla lista
        self.lista_clienti.append(cliente)
        # Salva la lista aggiornata nel file pickle
        try:
            with open(self.file_path, 'wb') as file:
                pickle.dump(self.lista_clienti, file)

        except pickle.PickleError as e:
            print(f"Errore durante il salvataggio dei dati: {e}")
            return

        return True


    def stampa_pdf_clienti(self):
        clienti = self.ritorna_lista_clienti()

        # Percorso per la cartella sul desktop
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        cartella_clienti = os.path.join(desktop_path, 'Lista_clienti_pdf')

        # Crea la cartella se non esiste
        if not os.path.exists(cartella_clienti):
            os.makedirs(cartella_clienti)

        # Percorso completo del file PDF
        pdf_name = os.path.join(cartella_clienti, 'Lista_clienti.pdf')
        doc = SimpleDocTemplate(pdf_name, pagesize=letter)
        elements = []

        # Definizione degli stili per i paragrafi
        title_style = ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=18, alignment=1)
        client_info_style = ParagraphStyle(name='ClientInfoStyle', fontName='Helvetica', fontSize=12)

        # Aggiungi un titolo al documento
        title = Paragraph("Lista Clienti", title_style)
        elements.append(title)
        elements.append(Spacer(1, 50))  # Spazio sotto il titolo

        for cliente in clienti:
            dipendente = cliente.get_dipendente_inserimento()
            dipendente_id = dipendente.get_id() if dipendente else "N/A"  # Gestisce il caso in cui il dipendente sia None
            client_info = (
                f"<b>ID:</b> {cliente.get_id_cliente()}<br/>"
                f"<b>Nome:</b> {cliente.get_nome_cliente()}<br/>"
                f"<b>Cognome:</b> {cliente.get_cognome_cliente()}<br/>"
                f"<b>Data di Nascita:</b> {cliente.get_data_nascita_cliente()}<br/>"
                f"<b>Residenza:</b> {cliente.get_residenza_cliente()}<br/>"
                f"<b>Codice Fiscale:</b> {cliente.get_codice_fiscale_cliente()}<br/>"
                f"<b>Email:</b> {cliente.get_email_cliente()}<br/>"
                f"<b>Telefono:</b> {cliente.get_telefono_cliente()}<br/>"
                f"<b>ID Dipendente:</b> {dipendente_id}<br/>"
                f"<b>Saldo Wallet:</b> € {cliente.get_saldo_wallet():.2f}<br/>"
            )

            # Aggiungi le informazioni del cliente come testo
            client_paragraph = Paragraph(client_info, client_info_style)
            elements.append(client_paragraph)
            elements.append(Spacer(1, 24))  # Spazio tra i clienti
            elements.append(Paragraph("<br/><hr size='1'/>", client_info_style))  # Separatore

        # Generazione del PDF
        try:
            doc.build(elements)
        except Exception as e:
            return False

        # Apertura automatica del PDF
        try:
            webbrowser.open(pdf_name)
            return pdf_name
        except Exception as e:
            print(f"Impossibile aprire il PDF: {e}")

    def elimina_cliente(self, search_text):
        clienti = self.ritorna_lista_clienti()

        if not clienti:
            print("Il file dei clienti è vuoto o non esiste.")
            return

        cliente_trovato = False
        nuova_lista = []
        for cliente in clienti:
            if cliente.get_telefono_cliente() == search_text:
                cliente_trovato = True
                continue  # Salta l'aggiunta di questo cliente alla nuova lista
            nuova_lista.append(cliente)

        if not cliente_trovato:
            return False

        # Salva la lista aggiornata nel file pickle
        with open(self.file_path, 'wb') as file:
            pickle.dump(nuova_lista, file)


    # Metodo ricerca cliente per nome
    def cerca_per_nome(self, search_text):
        clienti = self.ritorna_lista_clienti()
        risultati = []

        for cliente in clienti:
            if search_text == cliente.get_nome_cliente():  # Confronta ignorando maiuscole/minuscole
                risultati.append(cliente)

        if not risultati:
           return False

        return risultati

    # Metedo ricerca cliente per ID
    def cerca_per_ID(self, search_text):
        clienti = self.ritorna_lista_clienti()
        risultati = []

        search_text = str(search_text)

        for cliente in clienti:
            if search_text == str(cliente.get_id_cliente()):  # Assicurati che il confronto sia esatto
                risultati.append(cliente)

        if not risultati:
          return False

        return risultati

    # Metodo che ricerca cliente per numero di telefono
    def cerca_per_telefono(self, search_text):
        clienti = self.ritorna_lista_clienti()
        risultati = []

        search_text = str(search_text)

        for cliente in clienti:
            if search_text == str(cliente.get_telefono_cliente()):  # Confronta il numero di telefono
                risultati.append(cliente)

        if not risultati:
            return False

        return risultati

    # Metodo ricerca cliente per codice fiscale
    def cerca_per_codicefiscale(self, search_text):
        clienti = self.ritorna_lista_clienti()
        risultati = []


        for cliente in clienti:
            if search_text == str(cliente.get_codice_fiscale_cliente()):  # Confronta il codice fiscale
                risultati.append(cliente)

        if not risultati:
          return False

        return risultati

    def carica_wallet(self, telefono, ricarica, metodo_pagamento):
        # Carica i clienti
        lista_clienti = self.ritorna_lista_clienti()

        cliente_trovato = None
        for cliente in lista_clienti:
            if cliente.get_telefono_cliente() == telefono:
                cliente_trovato = cliente
                break

        if cliente_trovato is None:
            return False

        # Aggiungi la ricarica al saldo attuale
        nuovo_saldo = cliente_trovato.get_saldo_wallet() + ricarica
        cliente_trovato.set_saldo_wallet(nuovo_saldo)

        try:
            # Salva la lista aggiornata nel file pickle
            with open(self.file_path, 'wb') as file:
                pickle.dump(lista_clienti, file)
            Scontrino = GestoreVendite().creaScontrinoWallet(telefono, ricarica, metodo_pagamento)
            return nuovo_saldo

        except pickle.PickleError as e:
            print(f"Errore durante il salvataggio del saldo wallet: {e}")
