import unittest
import json
import os
from app import App_Web


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = App_Web("testing")
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # 🔐 Clé API depuis Render / environnement local
        self.API_KEY = os.environ.get("API_KEY")

        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.API_KEY
        }

    def tearDown(self):
        self.ctx.pop()

    # ========================
    # FIDELES
    # ========================

    def test_create_fidele(self):
        payload = {
            "nom": "Jean",
            "prenoms": "Kouassi",
            "email": "jean@test.com",
            "password": "password123",
            "telephone": "01020304",
            "diocese": "Abidjan",
            "paroisse": "Saint Pierre"
        }

        response = self.client.post(
            "/api/fideles",
            data=json.dumps(payload),
            headers=self.headers
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json["success"])

    def test_create_fidele_bad_request(self):
        response = self.client.post(
            "/api/fideles",
            data=json.dumps({}),
            headers=self.headers
        )

        self.assertIn(response.status_code, [200, 400])

    # ========================
    # LOGIN
    # ========================

    def test_login_fail(self):
        payload = {
            "email": "inconnu@test.com",
            "password": "wrong"
        }

        response = self.client.post(
            "/api/login",
            data=json.dumps(payload),
            headers=self.headers
        )

        self.assertIn(response.status_code, [401, 400])

    # ========================
    # PAROISSE
    # ========================

    def test_get_paroisse(self):
        response = self.client.get(
            "/api/paroisse/1",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("nom", response.json)

    # ========================
    # MESSES
    # ========================

    def test_get_messes(self):
        response = self.client.get(
            "/api/messes",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    # ========================
    # ANNONCES
    # ========================

    def test_get_annonces(self):
        response = self.client.get(
            "/api/annonces",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

    # ========================
    # INTENTIONS
    # ========================

    def test_create_intention(self):
        payload = {
            "data": {
                "fidele_id": 1,
                "messe_id": 1,
                "type_intention": "Action de grâce"
            }
        }

        response = self.client.post(
            "/api/intentions",
            data=json.dumps(payload),
            headers=self.headers
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json["success"])

    def test_delete_intention(self):
        response = self.client.delete(
            "/api/intentions/1",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

    def test_get_mes_intentions(self):
        response = self.client.get(
            "/api/intentions/mes",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

    def test_get_intentions_validees(self):
        response = self.client.get(
            "/api/intentions/validees",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

    # ========================
    # SYSTEME
    # ========================

    def test_register_push(self):
        payload = {"token": "abc123"}

        response = self.client.post(
            "/api/notifications/registerPush",
            data=json.dumps(payload),
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        payload = {"message": "Bonjour"}

        response = self.client.post(
            "/api/contact",
            data=json.dumps(payload),
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

    def test_post_avis(self):
        payload = {"note": 5, "commentaire": "Très bien"}

        response = self.client.post(
            "/api/avis",
            data=json.dumps(payload),
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
