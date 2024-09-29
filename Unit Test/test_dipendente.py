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

   # Metodo che testa l'inserimento del dipendente
    def test_aggiungi_dipendente(self):
        dipendente = Dipendente(
            id=1,
            nome="Nprova",
            cognome="Cprova",
            data_nascita="2003-01-01",
            telefono="1234567890",
            email="prova@univpm.com",
            residenza="Ancona"
        )
        self.gestore.aggiungi_dipendenti(dipendente)

        #Verifiche per l'inserimento corretto del cliente e per la creazione del file
        self.assertEqual(len(self.gestore.lista_dipendenti), 1)
        self.assertEqual(self.gestore.lista_dipendenti[0].get_nome(), "Nprova")
        self.assertTrue(os.path.exists(self.gestore.file_path))

        # Caricamento e verifica dei dati dal file
        with open(self.gestore.file_path, 'rb') as file:
            dipendenti_salvati = pickle.load(file)
            self.assertEqual(len(dipendenti_salvati), 1)
            self.assertEqual(dipendenti_salvati[0].get_nome(), "Nprova")

    # Metodo che testa la rimozione del dipendente
    def test_elimina_dipendente(self):
        dipendente = Dipendente(
            id=1,
            nome="Nprova",
            cognome="Cprova",
            data_nascita="2003-01-01",
            telefono="1234567890",
            email="prova@univpm.com",
            residenza="Ancona"
        )

        self.gestore.aggiungi_dipendenti(dipendente)
        self.assertEqual(len(self.gestore.lista_dipendenti), 1)  #simulazione dell'inserimento

        ID = int(dipendente.get_id())
        self.gestore.rimuovi_dipendenti(ID) #rimozione del dipendente

       # Verifiche riguardo la corretta rimozione del dipendente
        self.assertEqual(len(self.gestore.lista_dipendenti), 0)
        self.assertTrue(os.path.exists(self.gestore.file_path))
        with open(self.gestore.file_path, 'rb') as file:
            dipendenti_salvati = pickle.load(file)
            self.assertEqual(len(dipendenti_salvati), 0)


if __name__ == '__main__':
    unittest.main()
