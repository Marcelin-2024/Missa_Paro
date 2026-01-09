import os
import json
from supabase import create_client
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv
import requests


# Trouve cette clé dans : Console Firebase > Paramètres du projet > Clé API Web
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
load_dotenv()

# --- Supabase ---
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

if url and key:
    supabase = create_client(url, key)
    print("✅ Supabase connecté !")
else:
    print("⚠️ Attention: SUPABASE_URL ou KEY manquante")

# --- Firebase ---
def init_firebase():
    if not firebase_admin._apps:
        service_account_env = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
        if service_account_env:
            # Correction pour les sauts de ligne dans la clé privée Vercel
            service_account_info = json.loads(service_account_env)
            if "private_key" in service_account_info:
                service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
            cred = credentials.Certificate(service_account_info)
        else:
            cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()


def creer_utilisateur(email, password):
    # ON INITIALISE ICI AUSSI pour être sûr que 'auth' fonctionne
    init_firebase()
    try:
        user = auth.create_user(email=email, password=password)
        print(f"✅ Utilisateur créé : {user.uid}")
        return user.uid
    except Exception as e:
        print(f"❌ Erreur Auth Firebase : {e}")
        raise e  # On lève l'erreur pour qu'elle soit vue par l'API


def ajoute_fidele(nom, diocese,paroisse,gmail, password, telephone, date):
    # 1. Création du compte Auth (initialise Firebase au passage)
    uid = creer_utilisateur(gmail, password)

    if uid:
        data1 = {
            "nom": nom,
            "email": gmail,
            "telephone": telephone,
            "Diocèse" : diocese,
            "paroisse" : paroisse,
        }
        data = {
            "nom": nom,
            "email": gmail,
            "telephone": telephone,
            "created_at": date,
        }

        # 2. Ajout dans Firestore
        ajoute_fidele_compl('fidele', uid, data1)

        # 3. Ajout dans Supabase
        if url and key:
            try:
                supabase.table("fidele").insert(data).execute()
                print("✅ Ajouté à Supabase")
            except Exception as e:
                print(f"❌ Erreur Supabase : {e}")



def connecter_utilisateur(email, password):
    """
    Vérifie l'email et le mot de passe auprès de Firebase.
    Retourne l'ID utilisateur (uid) et le jeton (idToken) si succès.
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if response.status_code == 200:
            print(f"✅ Connexion réussie : {data['localId']}")
            return {
                "status": "success",
                "uid": data['localId'],
                "idToken": data['idToken']
            }
        else:
            # Gestion des erreurs (ex: EMAIL_NOT_FOUND, INVALID_PASSWORD)
            message_erreur = data.get('error', {}).get('message', 'Erreur de connexion')
            print(f"❌ Échec connexion : {message_erreur}")
            return {"status": "error", "message": message_erreur}

    except Exception as e:
        print(f"❌ Erreur réseau lors de la connexion : {e}")
        return {"status": "error", "message": str(e)}


def ajoute_intention(fidele_id, messe_id, type_intention, date):
    # Ajouter une présence test
    data = {
        "fidele_id": fidele_id,
        "messe_id": messe_id,
        "type_intention": type_intention,
        "statut": "en attente",
        "created_at": date,
    }

    response = supabase.table("intention_messe").insert(data).execute()
    print(response)


def ajoute_fidele_compl(user, uid, data):
    try:
        db = init_firebase()

        # Test d'écriture dans Firestore
        doc_ref = db.collection(user).document(uid)
        doc_ref.set(data)

        print("✅ Document écrit avec succès dans Firebase !")
    except Exception as e:
        print(f"❌ Erreur : {e}")
