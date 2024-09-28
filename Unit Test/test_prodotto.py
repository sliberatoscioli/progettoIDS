import os
import pickle
import unittest
from PyQt5.QtWidgets import QApplication

from Attivita.prodotto import Prodotto
from Controls.gestore_prodotti import GestoreProdotti

app = QApplication([])
class TestProdotto(unittest.TestCase):
    def setUp(self):
        self.gestore = GestoreProdotti()
        self.gestore.file_path = 'Dati/TestProdotti.pkl'  # Creazione di un file di test

        if os.path.exists(self.gestore.file_path):   #Rimozione del file, se esiste già
            os.remove(self.gestore.file_path)

    def tearDown(self):
        if os.path.exists(self.gestore.file_path):   #Rimozione del file alla fine di ogni test
            os.remove(self.gestore.file_path)

    def test_aggiungi_dipendenti(self):
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

        # Carica i dati dal file e verifica che contenga il cliente aggiunto
        with open(self.gestore.file_path, 'rb') as file:
            prodotti_salvati = pickle.load(file)
            self.assertEqual(len(prodotti_salvati), 1)
            self.assertEqual(prodotti_salvati[0].get_marca(), "Nike")


if __name__ == '__main__':
    unittest.main()
