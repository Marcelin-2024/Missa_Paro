import unittest
from app import App_Web # Assurez-vous que c'est bien votre fonction de création d'app

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

if __name__ == '__main__':
    unittest.main()