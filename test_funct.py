import unittest
from app import App_Web # Assurez-vous que c'est bien votre fonction de création d'app
from func_requete import ajoute_fidele_compl


class TestURLs(unittest.TestCase):
    """Tests pour toutes les URLs de l'application"""

    def setUp(self):
        """Configuration lancée AVANT chaque test"""
        # Note : On suppose que connecte_bp() retourne une instance de Flask(app)
        self.app = App_Web('testing')
        self.app.config['SERVER_NAME'] = 'localhost.test'
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        """Nettoyage APRÈS chaque test"""
        self.ctx.pop()

    # --- AJOUTEZ VOS TESTS CI-DESSOUS ---

    def test_accueil_status_code(self):
        """Vérifie que la page d'accueil répond avec un code 200 (OK)"""
        # Remplacez 'index' par le nom de votre route principale
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_ma_page_specifique(self):
        """Un autre exemple de test"""
        # Si vous utilisez url_for, assurez-vous que les routes sont enregistrées
        response = self.client.get('/page/connect')
        self.assertEqual(response.status_code, 200)
        pass

    def test_ajoute_fidele_firestore(self):
        """Test de l'écriture Firestore avec paramètres"""
        # On définit des valeurs de test
        collection_test = "users_test"
        id_test = "id_marcelin_001"
        date = "10 : 00"

        try:
            # On appelle la fonction avec les deux arguments
            ajoute_fidele_compl(user=collection_test, uid=id_test, data=date)
            # Si on arrive ici sans erreur, le test est réussi
        except Exception as e:
            self.fail(f"L'écriture a échoué : {e}")


if __name__ == '__main__':
    unittest.main()