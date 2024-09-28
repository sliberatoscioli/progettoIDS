import os
import pickle
import unittest
from PyQt5.QtWidgets import QApplication

from Attivita.dipendente import Dipendente
from Controls.gestore_dipendenti import GestoreDipendenti

app = QApplication([])
class TestDipendente(unittest.TestCase):
    def setUp(self):
        self.gestore = GestoreDipendenti()
        self.gestore.file_path = 'Dati/TestDipendenti.pkl'  # Creazione di un file di test

        if os.path.exists(self.gestore.file_path):   #Rimozione del file, se esiste già
            os.remove(self.gestore.file_path)

    def tearDown(self):
        if os.path.exists(self.gestore.file_path):   #Rimozione del file alla fine di ogni test
            os.remove(self.gestore.file_path)

    def test_aggiungi_dipendenti(self):
        dipendente = Dipendente(
            id=1,
            nome="Nprova",
            cognome="Cprova",
            data_nascita="2003-01-01",
            telefono="1234567890",
            email="prova@univpm.com",
            residenza="Ancona"
        )
        self.gestore.aggiungi_dipendenti(dipendente)  #metodo di inserimento

        #Verifiche per l'inserimento corretto del cliente e per la creazione del file
        self.assertEqual(len(self.gestore.lista_dipendenti), 1)
        self.assertEqual(self.gestore.lista_dipendenti[0].get_nome(), "Nprova")
        self.assertTrue(os.path.exists(self.gestore.file_path))

        # Carica i dati dal file e verifica che contenga il cliente aggiunto
        with open(self.gestore.file_path, 'rb') as file:
            dipendenti_salvati = pickle.load(file)
            self.assertEqual(len(dipendenti_salvati), 1)
            self.assertEqual(dipendenti_salvati[0].get_nome(), "Nprova")


if __name__ == '__main__':
    unittest.main()
