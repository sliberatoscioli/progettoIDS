import pickle
import os
import webbrowser
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from Controls.gestore_clienti import GestoreClienti


class GestoreDipendenti:

    def __init__(self):
        self.lista_dipendenti = []
        self.file_path = 'Dati/Dipendenti.pkl'  # Percorso del file nella cartella "Dati"

    # Metodo per l'aggiunta di un nuovo dipendente
    def aggiungi_dipendenti(self, dipendente):
        # Verifica se la cartella "Dati" esiste, altrimenti la crea
        if not os.path.exists('Dati'):
            os.makedirs('Dati')

        # Verifica se il file pickle esiste già
        if os.path.exists(self.file_path):
            # Caricamento dei dipendenti esistenti
            with open(self.file_path, 'rb') as file:
                self.lista_dipendenti = pickle.load(file)

        numero_telefono_nuovo = dipendente.get_telefono()
        for c in self.lista_dipendenti:
            if c.get_telefono() == numero_telefono_nuovo:
                return False
        # Aggiunta del nuovo dipendente alla lista
        self.lista_dipendenti.append(dipendente)

        # Salvataggio della lista aggiornata nel file pickle
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.lista_dipendenti, file)

        return True

    # Metodo per la rimozione del dipendente
    def rimuovi_dipendenti(self, IDdipendente):
        # Verifica se il file pickle esiste
        if not os.path.exists(self.file_path):
            return

        # Caricamento dei dipendenti esistenti
        with open(self.file_path, 'rb') as file:
            self.lista_dipendenti = pickle.load(file)

        # Ricerca e rimozione del dipendente con l'ID specificato
        dipendente_trovato = False
        nuova_lista = []
        for dipendente in self.lista_dipendenti:
            if dipendente.get_id() == IDdipendente:
                dipendente_trovato = True
            else:
                nuova_lista.append(dipendente)

        self.lista_dipendenti = nuova_lista

        if not dipendente_trovato:
            return

        # Salvataggio della lista aggiornata nel file pickle
        with open(self.file_path, 'wb') as file:
            pickle.dump(nuova_lista, file)
        return True

    # Metodo che restituisce la lista dei dipendenti
    def ritorna_lista_dipendenti(self):
        try:
            # Verifica se il file dei dipendenti esiste
            if not os.path.exists(self.file_path):
                print("Il file dei dipendenti non esiste.")
                return []

            # Caricamento dei dipendenti dal file pickle
            with open(self.file_path, 'rb') as file:
                dipendenti = pickle.load(file)

            return dipendenti

        except FileNotFoundError:
            print("Il file dei dipendenti non esiste.")
            return []

        except pickle.PickleError:
            print("Il file dei dipendenti non esiste.")
            return []

    # Metodo che restituisce un dipendente dato il suo ID
    def ritorna_dipendente_per_id(self, id):
        dipendenti = self.ritorna_lista_dipendenti()

        # Ricerca del dipendente con l'ID specificato
        for dipendente in dipendenti:
            if dipendente.get_id() == id:
                return dipendente
        return None

    # Metodo che verifica l'esistenza del dipendente
    def esiste_dipendente(self, IDdipendente):
        # Verifica se il file pickle esiste
        if not os.path.exists(self.file_path):
            print("Il file dei dipendenti non esiste.")
            return False

        # Caricamento dei dipendenti esistenti
        with open(self.file_path, 'rb') as file:
            dipendenti = pickle.load(file)

        # Controlla se esiste un dipendente con l'ID specificato
        for dipendente in dipendenti:
            if dipendente.get_id() == IDdipendente:
                return 1

        return 0

    # Metodo che stampa un report dei dipendenti
    def report_dipendenti(self):
        # Caricamento della lista dei clienti
        lista_clienti = GestoreClienti().ritorna_lista_clienti()

        # Verifica se il file dei dipendenti esiste
        if not os.path.exists(self.file_path):
            return False

        # Caricamento dei dipendenti esistenti
        with open(self.file_path, 'rb') as file:
            dipendenti = pickle.load(file)

        # Creazione della cartella report
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        cartella_report = os.path.join(desktop_path, 'Report_Dipendenti_pdf')
        if not os.path.exists(cartella_report):
            os.makedirs(cartella_report)

        # Creazione data
        data_corrente = datetime.now().strftime('%Y-%m-%d')

        # Percorso completo del file PDF
        pdf_name = os.path.join(cartella_report, f"report_dipendenti_{data_corrente}.pdf")
        doc = SimpleDocTemplate(pdf_name, pagesize=letter)
        elements = []

        # Preparazione dei dati per la tabella
        data = [["ID", "Nome", "Cognome", "Data \n Nascita", "Telefono", "Email", "Residenza", "Numero Clienti \n Inseriti"]]

        for dipendente in dipendenti:
            dipendente_id = dipendente.get_id()
            numero_clienti = sum(
                1 for cliente in lista_clienti if cliente.get_dipendente_inserimento().get_id() == dipendente_id)

            # Aggiunta delle informazioni alla tabella
            data.append([
                dipendente.get_id(),
                dipendente.get_nome(),
                dipendente.get_cognome(),
                dipendente.get_data_nascita(),
                dipendente.get_telefono(),
                dipendente.get_email(),
                dipendente.get_residenza(),
                numero_clienti
            ])

        # Creazione della tabella
        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)
        elements.append(table)

        # Generazione del PDF
        try:
            doc.build(elements)
        except Exception as e:
            print(f"Errore durante la generazione del PDF: {e}")
            return

        # Apertura automatica del PDF
        try:
            webbrowser.open(pdf_name)
            return pdf_name

        except Exception as e:
            print(f"Impossibile aprire il PDF: {e}")



