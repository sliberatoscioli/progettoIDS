class Prodotto:

    def __init__(self, id, scatola, marca, taglia, colore, descrizione, tipo_prodotto, giacenza, prezzo):
        self.id = id
        self.scatola = scatola #OGGETTO SCATOLA
        self.marca = marca
        self.taglia = taglia
        self.colore = colore
        self.descrizione = descrizione
        self.tipo_prodotto = tipo_prodotto
        self.giacenza = giacenza
        self.prezzo = prezzo
        self.quantita = None

    # METODI GETTER E SETTER
    def get_id_prodotto(self):
        return self.id

    def get_scatola(self):
        return self.scatola

    def get_marca(self):
        return self.marca

    def get_taglia(self):
        return self.taglia

    def get_colore(self):
        return self.colore

    def get_descrizione(self):
        return self.descrizione

    def get_tipo_prodotto(self):
        return self.tipo_prodotto

    def get_giacenza(self):
        return self.giacenza

    def get_prezzo(self):
        return self.prezzo

    def get_quantita(self):
        return self.quantita

    def set_giacenza(self):
        self.giacenza = 25

    def set_quantita(self, quantita):
        if quantita > 0:
            self.quantita = quantita
        else:
            raise ValueError("La quantità deve essere maggiore di zero")

    def aggiorna_giacenza(self,quantita):
        self.giacenza = quantita