import os
import pickle
from PyQt5.QtWidgets import QMessageBox
from Controls.gestore_vendite import GestoreVendite
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
import webbrowser  # Per aprire il PDF



class GestoreClienti:

    def __init__(self):
        self.lista_clienti = []
        self.msg_box = QMessageBox()
        self.file_path = 'Dati/Clienti.pkl'  # Percorso del file nella cartella "Dati"

    def ritorna_lista_clienti(self):
        try:
            # Verifica se il file dei clienti esiste
            if not os.path.exists(self.file_path):
                self.msg_box.setText("Il file dei clienti non esiste.")
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.exec_()
                return []

            # Carica i clienti dal file pickle
            with open(self.file_path, 'rb') as file:
                clienti = pickle.load(file)

            return clienti

        except FileNotFoundError:
            self.msg_box.setText("Il file dei clienti non è stato trovato.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return []

        except pickle.PickleError:
            self.msg_box.setText("Errore nel caricamento del file pickle dei clienti.")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
            return []

        except Exception as e:
            self.msg_box.setText(f"Errore imprevisto: {e}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
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
                self.msg_box.setText(f"Un cliente con il numero di telefono {numero_telefono_nuovo} è già presente.")
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.exec_()
                return

        # Aggiungi il nuovo cliente alla lista
        self.lista_clienti.append(cliente)
        # Salva la lista aggiornata nel file pickle
        try:
            with open(self.file_path, 'wb') as file:
                pickle.dump(self.lista_clienti, file)

        except pickle.PickleError as e:
            self.msg_box.setText(f"Errore durante il salvataggio dei dati: {e}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
            return

        # Mostra il messaggio di conferma
        Nome = cliente.get_nome_cliente()
        Cognome = cliente.get_cognome_cliente()
        self.msg_box.setText(f"Cliente {Nome} {Cognome} aggiunto con successo.")
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.exec_()

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
            self.msg_box.setText(f"Errore durante la creazione del PDF: {e}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()
            return

        # Apertura automatica del PDF
        try:
            webbrowser.open(pdf_name)
        except Exception as e:
            self.msg_box.setText(f"Impossibile aprire il PDF: {e}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()

    def elimina_cliente(self, search_text):
        clienti = self.ritorna_lista_clienti()

        if not clienti:
            self.msg_box.setText("Il file dei clienti è vuoto o non esiste.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

        cliente_trovato = False
        nuova_lista = []
        for cliente in clienti:
            if cliente.get_telefono_cliente() == search_text:
                cliente_trovato = True
                continue  # Salta l'aggiunta di questo cliente alla nuova lista
            nuova_lista.append(cliente)

        if not cliente_trovato:
            self.msg_box.setText(f"Nessun cliente trovato con il numero di telefono {search_text}.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()
            return

        # Salva la lista aggiornata nel file pickle
        with open(self.file_path, 'wb') as file:
            pickle.dump(nuova_lista, file)

        # Mostra il messaggio di conferma
        self.msg_box.setText(f"Cliente con numero di telefono {search_text} rimosso con successo.")
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.exec_()

    # Metodo ricerca cliente per nome
    def cerca_per_nome(self, search_text):
        clienti = self.ritorna_lista_clienti()
        risultati = []

        for cliente in clienti:
            if search_text == cliente.get_nome_cliente():  # Confronta ignorando maiuscole/minuscole
                risultati.append(cliente)

        if not risultati:
            self.msg_box.setText(f"Nessun cliente trovato con il nome '{search_text}'.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

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
            self.msg_box.setText(f"Nessun cliente trovato con ID '{search_text}'.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

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
            self.msg_box.setText(f"Nessun cliente trovato con il telefono '{search_text}'.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

        return risultati

    # Metodo ricerca cliente per codice fiscale
    def cerca_per_codicefiscale(self, search_text):
        clienti = self.ritorna_lista_clienti()
        risultati = []


        for cliente in clienti:
            if search_text == str(cliente.get_codice_fiscale_cliente()):  # Confronta il codice fiscale
                risultati.append(cliente)

        if not risultati:
            self.msg_box.setText(f"Nessun cliente trovato con il codice fiscale '{search_text}'.")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec_()

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
            self.msg_box.setText(f"Nessun cliente trovato con numero di telefono {telefono}.")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()
            return

        # Aggiungi la ricarica al saldo attuale
        nuovo_saldo = cliente_trovato.get_saldo_wallet() + ricarica
        cliente_trovato.set_saldo_wallet(nuovo_saldo)

        try:
            # Salva la lista aggiornata nel file pickle
            with open(self.file_path, 'wb') as file:
                pickle.dump(lista_clienti, file)

            # Messaggio di conferma
            self.msg_box.setText(f"Saldo wallet cliente con telefono {telefono} aggiornato con successo. "
                                 f"Nuovo saldo: € {nuovo_saldo:.2f}.")
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.exec_()

        except pickle.PickleError as e:
            self.msg_box.setText(f"Errore durante il salvataggio del saldo wallet: {e}")
            self.msg_box.setIcon(QMessageBox.Critical)
            self.msg_box.exec_()

        # richiamare metodo crea scontrino saldo_wallet
        Scontrino = GestoreVendite().creaScontrinoWallet(telefono,ricarica,metodo_pagamento)
