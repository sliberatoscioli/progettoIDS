import pickle
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.units import mm
from reportlab.lib import colors
import os

class GestoreVendite:

    def __init__(self):
        self.lista_acquisti = []
        self.file_path = 'Dati/Acquisti.pkl'  # Percorso del file nella cartella "Dati"

    # Metodo che restituisce la lista degli acquisti
    def ritorna_lista_acquisti(self):
        try:
            if not os.path.exists(self.file_path):
                print("Il file degli acquisti non esiste.")
                return []

            # Caricamento dei prodotti dal file pickle
            with open(self.file_path, 'rb') as file:
                acquisti = pickle.load(file)

            return acquisti

        except FileNotFoundError:
            print("Il file degli acquisti non è stato trovato.")
            return []

        except pickle.PickleError:
            print("Errore nel caricamento del file pickle degli acquisti.")
            return []

        except Exception as e:
            print(f"Errore imprevisto: {e}")
            return []


    # Metodo per l'aggiunta di un acquisto
    def aggiungi_acquisto(self, acquisto):
        # Si verifica se la cartella "Dati" esiste, altrimenti viene creata
        if not os.path.exists('Dati'):
            os.makedirs('Dati')

        # Caricamento degli acquisti esistenti dal file pickle
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'rb') as file:
                    self.lista_acquisti = pickle.load(file)
            except Exception as e:
                print(f"Errore nel caricamento degli acquisti: {e}")
                return

        # Verifica che l'ID dell'acquisto non sia duplicato
        if any(acq.get_id() == acquisto.get_id() for acq in self.lista_acquisti):
            print("Un acquisto con questo ID esiste già.")
            return

        # Aggiunta del nuovo acquisto alla lista
        self.lista_acquisti.append(acquisto)

        # Salvataggio della lista aggiornata nel file pickle
        try:
            with open(self.file_path, 'wb') as file:
                pickle.dump(self.lista_acquisti, file)
        except Exception as e:
            return e

        return True

    # Metodo che restituisce l'ultimo ID della lista di acquisti
    def ritorna_ultimo_ID_acquisto(self):
        acquisti = self.ritorna_lista_acquisti()
        if not acquisti:
            return 0    #Se la lista è vuota, ID impostato a 0

        # Ricerca dell'ID massimo tra tutti i prodotti
        ultimo_id = max(acquisto.get_id() for acquisto in acquisti)
        return ultimo_id

    # Metodo che crea lo scontrino per il caricamento wallet
    def creaScontrinoWallet(self, telefono, importo, metodoPagamento):
        # Determina il percorso del desktop dell'utente
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # Creazione della cartella 'Scontrino_wallet' sul desktop
        cartella_wallet = os.path.join(desktop_path, 'Scontrino_wallet')
        if not os.path.exists(cartella_wallet):
            os.makedirs(cartella_wallet)

        # Impostazione del nome e del percorso del file PDF
        nome_file = f'Scontrino_{telefono}.pdf'
        percorso_file = os.path.join(cartella_wallet, nome_file)

        larghezza_scontrino = 250  # Larghezza aumentata del PDF
        altezza_scontrino = 500  # Altezza aumentata

        # Creazione del PDF usando ReportLab con le dimensioni personalizzate
        c = canvas.Canvas(percorso_file, pagesize=(larghezza_scontrino, altezza_scontrino))
        c.setFont("Helvetica-Bold", 16)

        # Titolo del PDF
        c.drawString(10, altezza_scontrino - 30, "Ricarica Wallet")

        # Linea di separazione
        c.setLineWidth(0.5)
        c.line(10, altezza_scontrino - 40, larghezza_scontrino - 10,
               altezza_scontrino - 40)  # Linea orizzontale sotto il titolo

        # Font per le altre informazioni
        c.setFont("Helvetica", 12)

        # Data e ora della ricarica
        data_ora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        c.drawString(10, altezza_scontrino - 60, f"Data e Ora: {data_ora}")

        # Linea di separazione sotto la data
        c.line(10, altezza_scontrino - 70, larghezza_scontrino - 10, altezza_scontrino - 70)

        # Informazioni sul PDF
        c.drawString(10, altezza_scontrino - 90, f"Telefono: {telefono}")
        c.drawString(10, altezza_scontrino - 110, f"Importo: {importo} €")
        c.drawString(10, altezza_scontrino - 130, f"Metodo di Pagamento: {metodoPagamento}")

        # Linea di separazione finale
        c.line(10, altezza_scontrino - 140, larghezza_scontrino - 10, altezza_scontrino - 140)

        # Chiudi e salva il PDF
        c.showPage()
        c.save()


    # Metodo per la creazione di uno scontrino fiscale per l'acquisto
    def CreaScontrinoAcquisto(self, prodotti, prezzoSconto, codiceVenditaCompletato):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        # Creazione della cartella per salvare gli scontrini
        cartella_scontrino = os.path.join(desktop_path, 'Scontrino_fiscale')
        if not os.path.exists(cartella_scontrino):
            os.makedirs(cartella_scontrino)

        # Impostazione del nome e del percorso del file PDF
        nome_file = f'Scontrino_{codiceVenditaCompletato}.pdf'
        percorso_file = os.path.join(cartella_scontrino, nome_file)

        # Dimensioni del scontrino
        larghezza_scontrino = 250  # Larghezza del PDF
        altezza_scontrino = 500  # Altezza del PDF

        # Creazione del canvas per il PDF
        c = canvas.Canvas(percorso_file, pagesize=(larghezza_scontrino, altezza_scontrino))

        # Nome del negozio
        c.setFont("Helvetica-Bold", 12)
        c.drawString(80, altezza_scontrino - 30, "Newshop")

        # Indirizzo e numero di telefono del negozio
        c.setFont("Helvetica", 10)
        c.drawString(55, altezza_scontrino - 45, "Corso di Ancona, 123")
        c.drawString(75, altezza_scontrino - 60, "Tel: 071-1234567")

        # Data
        c.setFont("Helvetica", 10)
        c.drawString(70, altezza_scontrino - 80, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Linea di separazione
        c.setFont("Helvetica", 8)
        c.drawString(10, altezza_scontrino - 90, "-" * 80)

        y_position = altezza_scontrino - 110  # Posizione di partenza per i dettagli dei prodotti
        prezzo_totale = 0

        # Iterazione sui prodotti per scrivere i dettagli in una riga
        for prodotto in prodotti:
            id_prodotto = prodotto.get_id_prodotto()
            marca = prodotto.get_marca()
            taglia = prodotto.get_taglia()
            prezzo = float(prodotto.get_prezzo())
            quantita = prodotto.get_quantita()

            # Calcolo del prezzo totale per questo prodotto
            prezzo_prodotto = prezzo * quantita
            prezzo_totale += prezzo_prodotto

            # Creazione della riga del prodotto
            riga_prodotto = f"ID: {id_prodotto} Marca: {marca} Taglia: {taglia} Quantità: {quantita} Prezzo: €{prezzo:.2f}"
            c.drawString(10, y_position, riga_prodotto)
            y_position -= 20  # Aggiornamento della posizione verticale per il prossimo prodotto

        # Linea di separazione
        y_position -= 10
        c.drawString(10, y_position, "-" * 80)

        # Stampa del codice della vendita
        y_position -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(10, y_position, f"Codice Vendita: {codiceVenditaCompletato}")

        # Stampa del prezzo totale
        y_position -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(10, y_position, f"Prezzo Totale: €{prezzo_totale:.2f}")

        # Stampa del prezzo scontato
        y_position -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(10, y_position, f"Prezzo Scontato: {prezzoSconto}")

        # Linea di separazione finale
        y_position -= 20
        c.setFont("Helvetica", 8)
        c.drawString(10, y_position, "-" * 80)

        # Salva e chiudi il PDF
        c.showPage()
        c.save()

        return nome_file

    # Metodo che stampa la lista degli acquisti di un cliente
    def storico_acquisti_cliente(self, ID_cliente):
        lista_acquisti_cliente = []
        lista_acquisti = self.ritorna_lista_acquisti()

        # Iterazione sugli acquisti
        for acquisto in lista_acquisti:
            if acquisto.get_cliente().get_id_cliente() == ID_cliente:
                prodotti = acquisto.get_prodotti()
                for prodotto in prodotti:
                    # Estrazione delle informazioni richieste in una tupla
                    info_acquisto = (
                        prodotto.get_id_prodotto(),
                        prodotto.get_marca(),
                        prodotto.get_prezzo(),
                        prodotto.get_descrizione(),
                        prodotto.get_tipo_prodotto(),
                        acquisto.get_data_acquisto(),
                        prodotto.get_quantita(),
                        acquisto.get_metodo_pagamento()
                    )
                    lista_acquisti_cliente.append(info_acquisto)

        return lista_acquisti_cliente

    # Metodo che restituisce un acquisto
    def ricerca_acquisti(self, codice_acquisto):
        lista_acquisti_ritorna = []
        lista_acquisti = self.ritorna_lista_acquisti()

        for acquisto in lista_acquisti:
            if acquisto.get_codice_vendita() == codice_acquisto:
                # Estrazione delle informazioni rilevanti dall'acquisto
                id_acquisto = acquisto.get_id()
                id_cliente = acquisto.get_cliente().get_id_cliente()
                data_acquisto = acquisto.get_data_acquisto()
                metodo_pagamento = acquisto.get_metodo_pagamento()
                codice_vendita = acquisto.get_codice_vendita()

                # Estrazione delle informazioni da ogni prodotto nell'acquisto
                for prodotto in acquisto.get_prodotti():
                    id_prodotto = prodotto.get_id_prodotto()
                    quantita = prodotto.get_quantita()
                    marca = prodotto.get_marca()
                    colore = prodotto.get_colore()
                    prezzo = prodotto.get_prezzo()
                    descrizione = prodotto.get_descrizione()

                    # Creazione di una tupla con tutte le informazioni
                    acquisto_tuple = (
                        id_acquisto,
                        id_cliente,
                        data_acquisto,
                        id_prodotto,
                        quantita,
                        metodo_pagamento,
                        codice_vendita,
                        marca,
                        colore,
                        prezzo,
                        descrizione
                    )

                    lista_acquisti_ritorna.append(acquisto_tuple)
        return lista_acquisti_ritorna

    # Metodo per il reso di un prodotto
    def reso_prodotto(self, id_prodotto, codice_vendita, quantita, prezzo, id_cliente):
        # Percorso del file per i clienti e gli acquisti
        percorso_file_clienti = os.path.join('Dati', 'Clienti.pkl')
        percorso_file_acquisti = os.path.join('Dati', 'Acquisti.pkl')
        percorso_file_prodotti = os.path.join('Dati', 'Prodotti.pkl')

        # Caricamento dei dati dai file
        with open(percorso_file_clienti, 'rb') as file_clienti:
            lista_clienti = pickle.load(file_clienti)

        with open(percorso_file_acquisti, 'rb') as file_acquisti:
            lista_acquisti = pickle.load(file_acquisti)

        with open(percorso_file_prodotti, 'rb') as file_prodotti:
            lista_prodotti = pickle.load(file_prodotti)


        # Ricerca del cliente per aggiornare il saldo del wallet
        cliente_trovato = None
        for cliente in lista_clienti:
            if cliente.get_id_cliente() == id_cliente:
                cliente_trovato = cliente
                break

        if cliente_trovato:
            # Calcolo del credito da restituire
            wallet_cliente = cliente_trovato.get_saldo_wallet()
            prezzo_wallet = wallet_cliente+quantita * prezzo
            try:
                # Aggiornamento del saldo
                cliente_trovato.set_saldo_wallet(prezzo_wallet)
            except ValueError as e:
                return e # Interrompe l'operazione in caso di errore

        # Ricerca dell'acquisto corrispondente al codice vendita e rimozione del prodotto
        acquisto_trovato = None
        for acquisto in lista_acquisti:
            if acquisto.get_codice_vendita() == codice_vendita:
                acquisto_trovato = acquisto
                break

        if acquisto_trovato:
            # Rimozione del prodotto dall'acquisto
            acquisto_trovato.get_prodotti().remove(
                next(prodotto for prodotto in acquisto_trovato.get_prodotti() if
                     prodotto.get_id_prodotto() == id_prodotto)
            )

        # Ricerca del prodotto e aggiornamento delle giacenza
        prodotto_trovato = None
        for prodotto in lista_prodotti:
            if prodotto.get_id_prodotto() == id_prodotto:
                prodotto_trovato = prodotto
                break

        if prodotto_trovato:
            nuova_giacenza = prodotto_trovato.get_giacenza() + quantita
            prodotto_trovato.aggiorna_giacenza(nuova_giacenza)

        # Salvataggio dei dati aggiornati nei file
        with open(percorso_file_clienti, 'wb') as file_clienti:
            pickle.dump(lista_clienti, file_clienti)

        with open(percorso_file_acquisti, 'wb') as file_acquisti:
            pickle.dump(lista_acquisti, file_acquisti)

        with open(percorso_file_prodotti, 'wb') as file_prodotti:
            pickle.dump(lista_prodotti, file_prodotti)
        return True

    # Metodo per il riepilogo giornaliero delle vendite
    def riepilogo_giornaliero(self):
        lista_acquisti = self.ritorna_lista_acquisti()
        oggi = datetime.now().date()  #data odierna

        try:
            with open('Dati/Clienti.pkl', 'rb') as file:
                lista_clienti = pickle.load(file)
        except (FileNotFoundError, pickle.PickleError):
            lista_clienti = []

        totale_carta_di_credito = 0
        totale_contanti = 0
        totale_saldo_wallet = sum(cliente.get_saldo_wallet() for cliente in lista_clienti) if lista_clienti else 0
        info = []
        quantita_per_tipo = {}  # Dizionario per raccogliere le quantità per tipo di prodotto

        for acquisto in lista_acquisti:
            try:
                # Recupero della data di acquisto come stringa
                data_acquisto_completa = acquisto.get_data_acquisto()
                # Conversione della stringa in un oggetto datetime
                data_acquisto_completa = datetime.strptime(data_acquisto_completa, "%Y-%m-%d %H:%M:%S")
                # Considera solo giorno, mese e anno
                data_solo_giorno_mese_anno = data_acquisto_completa.date()

                # Confronto tra le date
                if data_solo_giorno_mese_anno == oggi:
                    for prodotto in acquisto.get_prodotti():
                        quantita = prodotto.get_quantita()
                        prezzo = float(prodotto.get_prezzo())
                        tot = quantita * prezzo

                        cliente = acquisto.get_cliente()
                        info.append(
                            (cliente.get_nome_cliente(), cliente.get_cognome_cliente(), cliente.get_email_cliente(),
                             cliente.get_telefono_cliente(), cliente.get_saldo_wallet(), prodotto.get_marca(),
                             prodotto.get_taglia(), prodotto.get_colore(), prodotto.get_prezzo(),
                             prodotto.get_tipo_prodotto(), prodotto.get_descrizione(),
                             acquisto.get_data_acquisto(), quantita, acquisto.get_metodo_pagamento()))

                        # Aggiornamento totale per il metodo di pagamento
                        if acquisto.get_metodo_pagamento() == 'CARTA DI CREDITO':
                            totale_carta_di_credito += tot
                        elif acquisto.get_metodo_pagamento() == 'CONTANTI':
                            totale_contanti += tot

                        # Aggiornamento della quantità per tipo di prodotto
                        tipo_prodotto = prodotto.get_tipo_prodotto()
                        if tipo_prodotto in quantita_per_tipo:
                            quantita_per_tipo[tipo_prodotto] += quantita
                        else:
                            quantita_per_tipo[tipo_prodotto] = quantita

            except Exception as e:
                print("Errore durante il processamento dell'acquisto:", e)

        # Creazione di una lista delle quantità totali per tipo di prodotto
        quantita_totale_per_tipo = [(tipo, quantita) for tipo, quantita in quantita_per_tipo.items()]
        path_name = self.crea_pdf_riassunto_giornaliero(info, totale_contanti, totale_carta_di_credito, totale_saldo_wallet, quantita_totale_per_tipo)
        return info, totale_contanti, totale_carta_di_credito, totale_saldo_wallet, quantita_totale_per_tipo, path_name

    # Metodo per la stampa del riepilogo in formato PDF
    def crea_pdf_riassunto_giornaliero(self, dati, totale_contanti, totale_carta_di_credito, totale_saldo_wallet,
                                       vendite_per_tipo):
        # Percorso alla cartella sul desktop
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        cartella_riepiloghi = os.path.join(desktop_path, 'Riepiloghi_giornalieri')

        # Creazione della cartella se non esiste
        if not os.path.exists(cartella_riepiloghi):
            os.makedirs(cartella_riepiloghi)

        # Ricava la data di acquisto dalla data attuale
        data_acquisto = datetime.now().strftime('%Y-%m-%d')

        # Percorso completo per il PDF
        pdf_path = os.path.join(cartella_riepiloghi, f'Riepilogo_{data_acquisto}.pdf')

        # Creazione del PDF
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.setTitle(f"Riepilogo giornaliero del {data_acquisto}")

        width, height = A4
        margin = 20 * mm
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name='Title', fontName='Times-Roman', fontSize=16, spaceAfter=12, alignment=1)
        heading_style = ParagraphStyle(name='Heading', fontName='Times-Bold', fontSize=12, spaceAfter=10, alignment=1)

        # Titolo
        title = Paragraph(f"Riepilogo del giorno {data_acquisto}", title_style)
        title.wrapOn(c, width - 2 * margin, height - 2 * margin)
        title.drawOn(c, margin, height - margin)

        # Linea di "=" dopo il titolo
        c.setFont("Times-Roman", 12)
        num_equals = int((width - 2 * margin) // c.stringWidth("=", "Times-Roman", 12))
        c.drawString(margin, height - 2.5 * margin, "=" * num_equals)

        # Sezione: Informazioni sulle vendite
        heading = Paragraph("Informazioni vendite", heading_style)
        heading.wrapOn(c, width - 2 * margin, height - 2 * margin)
        heading.drawOn(c, margin, height - 3 * margin)

        # Dati per la tabella delle vendite
        table_data = [["Cliente", "Prodotto", "Quantità", "Prezzo", "Metodo Pagamento"]]
        for info in dati:
            cliente = f"{info[0]} {info[1]}"
            prodotto = f"{info[5]} {info[9]} ({info[6]})"
            quantita = info[12]
            prezzo = f"{float(info[8]):.2f} €"
            metodo_pagamento = info[13]
            table_data.append([cliente, prodotto, quantita, prezzo, metodo_pagamento])

        # Creazione della tabella delle informazioni
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
        ]))

        # Riduzione della distanza tra tabelle
        table.wrapOn(c, width - 2 * margin, height - 5 * margin)
        table.drawOn(c, margin, height - 5 * margin - len(table_data) * 16)

        # Calcolo dell'altezza corrente per la posizione successiva
        current_height = height - 5 * margin - len(table_data) * 16

        # Totale incassi
        heading = Paragraph("Totale Incassi", heading_style)
        heading.wrapOn(c, width - 2 * margin, height - 2 * margin)
        heading.drawOn(c, margin, current_height - 1.5 * margin)
        totale_complessivo = totale_contanti + totale_saldo_wallet + totale_carta_di_credito
        table_data_incassi = [
            ["Metodo di Pagamento", "Totale (€)"],
            ["Contanti", f"{totale_contanti:.2f} €"],
            ["Carta di Credito", f"{totale_carta_di_credito:.2f} €"],
            ["Saldo Wallet", f"{totale_saldo_wallet:.2f} €"],
            ["TOTALE COMPLESSIVO", f"{totale_complessivo:.2f} €"]
        ]

        # Creazione della tabella dei totali (bianco e nero)
        table_incassi = Table(table_data_incassi)
        table_incassi.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
        ]))

        current_height -= 2 * margin + len(table_data_incassi) * 16
        table_incassi.wrapOn(c, width - 2 * margin, height - 2 * margin)
        table_incassi.drawOn(c, margin, current_height)

        # Sezione: Vendite per tipo di prodotto
        heading = Paragraph("Vendite per Tipo di Prodotto", heading_style)
        heading.wrapOn(c, width - 2 * margin, height - 2 * margin)
        heading.drawOn(c, margin, current_height - 1.5 * margin)

        table_data_vendite = [["Tipo di Prodotto", "Quantità"]]
        for vendita in vendite_per_tipo:
            table_data_vendite.append([vendita[0], vendita[1]])

        # Creazione della tabella delle vendite per tipo (bianco e nero)
        table_vendite = Table(table_data_vendite)
        table_vendite.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
        ]))

        current_height -= 2 * margin + len(table_data_vendite) * 16
        table_vendite.wrapOn(c, width - 2 * margin, height - 2 * margin)
        table_vendite.drawOn(c, margin, current_height)

        # Linea di "=" alla fine del PDF
        current_height -= 2 * margin
        c.setFont("Times-Roman", 12)
        c.drawString(margin, current_height, "=" * num_equals)

        c.showPage()
        c.save()
        return pdf_path
