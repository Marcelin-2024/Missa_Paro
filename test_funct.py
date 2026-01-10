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
        response = self.client.get('/page/connection')
        self.assertEqual(response.status_code, 200)
        pass

    def test_validation_inscription(self):
        # 1. Préparation des données simulées (comme si on remplissait le formulaire)
        data_inscription = {
            'paroisse': 'Saint-Pierre',
            'diocese': 'Abidjan',
            'nom_complet': 'Jean Kouassi',
            'poste': 'Fidèle',
            'telephone': '0102030405',
            'gmail': 'jean@gmail.com',
            'password': 'password123'
        }

        # 2. Envoi de la requête POST vers l'URL avec le préfixe /page
        response = self.client.post('/page/valide', data=data_inscription)

        # 3. Vérifications (Assertions)

        # On vérifie que le serveur redirige (302) et non une erreur 404 ou 500
        self.assertEqual(response.status_code, 302)

        # Optionnel : Vérifier que la redirection renvoie bien vers la page de connexion
        self.assertIn('/page/connection', response.location)

        print("✅ Test de validation d'inscription réussi (Redirection vers login)")



if __name__ == '__main__':
    unittest.main()