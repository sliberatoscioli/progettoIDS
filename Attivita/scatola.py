class Scatola:

    def __init__(self, id, descrizione):
        self.id = id
        self.descrizione = "Scatola che contiene: " + descrizione
        self.MAGAZZINO = 1

    # METODI GETTER
    def get_IDscatola(self):
        return self.id

    def get_descrizione_scatola(self):
        return self.descrizione

    def get_magazzino_scatola(self):
        return self.MAGAZZINO