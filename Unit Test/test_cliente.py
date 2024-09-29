import unittest
import os
import pickle
from PyQt5.QtWidgets import QApplication

from Controls.gestore_clienti import GestoreClienti
from Attivita.cliente import Cliente

app = QApplication([])
class TestCliente(unittest.TestCase):
    def setUp(self):
        self.gestore = GestoreClienti()
        self.gestore.file_path = 'Dati/TestClienti.pkl'  # Creazione di un file di test

        if os.path.exists(self.gestore.file_path):   #Rimozione del file, se esiste già
            os.remove(self.gestore.file_path)

    def tearDown(self):
        if os.path.exists(self.gestore.file_path):   #Rimozione del file alla fine di ogni test
            os.remove(self.gestore.file_path)

    # Metodo che testa l'inserimento di un cliente
    def test_aggiungi_cliente(self):
        cliente = Cliente(
            id=1,
            nome="Nprova",
            cognome="Cprova",
            data_nascita="2003-01-01",
            residenza="Ancona",
            codice_fiscale="PRVPRV03P12R345V",
            email="prova@univpm.com",
            dipendente=None,
            telefono="1234567890"
        )
        self.gestore.aggiungi_cliente(cliente)  #metodo di inserimento

        #Verifiche per l'inserimento corretto del cliente e per la creazione del file
        self.assertEqual(len(self.gestore.lista_clienti), 1)
        self.assertEqual(self.gestore.lista_clienti[0].get_nome_cliente(), "Nprova")
        self.assertTrue(os.path.exists(self.gestore.file_path))

        # Caricamento e verifica dei dati dal file
        with open(self.gestore.file_path, 'rb') as file:
            clienti_salvati = pickle.load(file)
            self.assertEqual(len(clienti_salvati), 1)
            self.assertEqual(clienti_salvati[0].get_nome_cliente(), "Nprova")


    # Metodo che testa l'inserimento di un cliente
    def test_elimina_cliente(self):
        cliente = Cliente(
            id=1,
            nome="Nprova",
            cognome="Cprova",
            data_nascita="2003-01-01",
            residenza="Ancona",
            codice_fiscale="PRVPRV03P12R345V",
            email="prova@univpm.com",
            dipendente=None,
            telefono="1234567890"
        )

        self.gestore.aggiungi_cliente(cliente)
        self.assertEqual(len(self.gestore.lista_clienti), 1)  # simulazione dell'inserimento

        self.gestore.elimina_cliente(cliente.get_telefono_cliente())       # rimozione del cliente

        # Verifiche riguardo la corretta rimozione del cliente
        self.assertEqual(len(self.gestore.lista_clienti), 0)
        self.assertTrue(os.path.exists(self.gestore.file_path))
        with open(self.gestore.file_path, 'rb') as file:
            cliente_salvati = pickle.load(file)
            self.assertEqual(len(cliente_salvati), 0)


if __name__ == '__main__':
    unittest.main()
