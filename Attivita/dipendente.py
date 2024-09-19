class Dipendente:

    def __init__(self, id, nome, cognome, data_nascita, telefono, email, residenza):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.telefono = telefono
        self.email = email
        self.residenza = residenza
        self.MAGAZZINO = 1

    # METODI GETTER
    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def get_cognome(self):
        return self.cognome

    def get_data_nascita(self):
        return self.data_nascita

    def get_telefono(self):
        return self.telefono

    def get_email(self):
        return self.email

    def get_residenza(self):
        return self.residenza

    def get_magazzino(self):
        return self.MAGAZZINO