import os
import pickle
import unittest
from PyQt5.QtWidgets import QApplication

from Attivita.prodotto import Prodotto
from Controls.gestore_prodotti import GestoreProdotti

class TestProdotto(unittest.TestCase):
    def setUp(self):
        self.gestore = GestoreProdotti()
        self.gestore.file_path = 'Dati/TestProdotti.pkl'  # Creazione di un file di test

        if os.path.exists(self.gestore.file_path):   #Rimozione del file, se esiste già
            os.remove(self.gestore.file_path)

    def tearDown(self):
        if os.path.exists(self.gestore.file_path):   #Rimozione del file alla fine di ogni test
            os.remove(self.gestore.file_path)

    # Metodo che testa l'inserimento di un prodotto
    def test_aggiungi_prodotto(self):
        prodotto = Prodotto(
            id=1,
            scatola=None,
            marca="Nike",
            taglia="S",
            colore="Nero",
            descrizione="T-shirt nera a strisce",
            tipo_prodotto="T-shirt",
            giacenza="25",
            prezzo="35.59"
        )
        self.gestore.aggiungi_prodotto(prodotto)  #metodo di inserimento

        #Verifiche per l'inserimento corretto del cliente e per la creazione del file
        self.assertEqual(len(self.gestore.lista_prodotti), 1)
        self.assertEqual(self.gestore.lista_prodotti[0].get_marca(), "Nike")
        self.assertTrue(os.path.exists(self.gestore.file_path))

        # Caricamento e verifica dei dati dal file
        with open(self.gestore.file_path, 'rb') as file:
            prodotti_salvati = pickle.load(file)
            self.assertEqual(len(prodotti_salvati), 1)
            self.assertEqual(prodotti_salvati[0].get_marca(), "Nike")

    # Metodo che testa la rimozione di un prodotto
    def test_elimina_prodotto(self):
        prodotto = Prodotto(
            id=1,
            scatola=None,
            marca="Nike",
            taglia="S",
            colore="Nero",
            descrizione="T-shirt nera a strisce",
            tipo_prodotto="T-shirt",
            giacenza="25",
            prezzo="35.59"
        )

        self.gestore.aggiungi_prodotto(prodotto)  #simulazione di inserimento
        self.assertEqual(len(self.gestore.lista_prodotti), 1)

        self.gestore.elimina_prodotto(prodotto.get_id_prodotto())       # rimozione del prodotto

        # Verifiche riguardo la corretta rimozione del prodotto
        self.assertEqual(len(self.gestore.lista_prodotti), 0)
        with open(self.gestore.file_path, 'rb') as file:
            prodotti_salvati = pickle.load(file)
            self.assertEqual(len(prodotti_salvati), 0)

    def test_elimina_prodotto(self):
        prodotto = Prodotto(
            id=1,
            scatola=None,
            marca="Nike",
            taglia="S",
            colore="Nero",
            descrizione="T-shirt nera a strisce",
            tipo_prodotto="T-shirt",
            giacenza="25",
            prezzo="35.59"
        )

        self.gestore.aggiungi_prodotto(prodotto)
        self.assertEqual(len(self.gestore.lista_prodotti), 1)  # simulazione dell'inserimento

        ID = int(prodotto.get_id_prodotto())
        self.gestore.elimina_prodotto(ID)       # rimozione del prodotto

        # Verifiche riguardo la corretta rimozione del prodotto
        self.assertEqual(len(self.gestore.lista_prodotti), 0)
        self.assertTrue(os.path.exists(self.gestore.file_path))
        with open(self.gestore.file_path, 'rb') as file:
            prodotti_salvati = pickle.load(file)
            self.assertEqual(len(prodotti_salvati), 0)



if __name__ == '__main__':
    unittest.main()
