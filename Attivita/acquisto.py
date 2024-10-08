class Acquisto:

    def __init__(self, id, cliente, prodotti, data_acquisto, metodo_pagamento, codice_vendita, sconto):
        self.id = id
        self.cliente = cliente  #Oggetto di tipo Cliente
        self.prodotti = prodotti  # Una lista di oggetti Prodotto
        self.data_acquisto = data_acquisto
        self.metodo_pagamento = metodo_pagamento
        self.codice_vendita = "ACQ" + str(codice_vendita)
        self.sconto = sconto

    # METODI GETTER
    def get_id(self):
        return self.id

    def get_cliente(self):
        return self.cliente

    def get_prodotti(self):
        return self.prodotti

    def get_data_acquisto(self):
        return self.data_acquisto

    def get_metodo_pagamento(self):
        return self.metodo_pagamento

    def get_codice_vendita(self):
        return self.codice_vendita

    def get_sconto(self):
        return self.sconto