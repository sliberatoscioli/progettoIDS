class Cliente:

    def __init__(self,id, nome, cognome, data_nascita, residenza, codice_fiscale, email, dipendente, telefono):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.residenza = residenza
        self.codice_fiscale = codice_fiscale
        self.email = email
        self.dipendente = dipendente #Oggetto dipendente
        self.telefono = telefono
        self.saldo_wallet = 0.0

    #Metodi di classe

    def get_id_cliente(self):
        return self.id

    def get_nome_cliente(self):
        return self.nome

    def get_cognome_cliente(self):
        return self.cognome

    def get_data_nascita_cliente(self):
        return self.data_nascita

    def get_residenza_cliente(self):
        return self.residenza

    def get_codice_fiscale_cliente(self):
        return self.codice_fiscale

    def get_email_cliente(self):
        return self.email

    def get_dipendente_inserimento(self):
        return self.dipendente

    def get_telefono_cliente(self):
        return self.telefono

    def get_saldo_wallet(self):
        return self.saldo_wallet