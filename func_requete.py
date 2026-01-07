import os
import json
from supabase import create_client
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv



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
            service_account_info = json.loads(service_account_env)
            cred = credentials.Certificate(service_account_info)
        else:
            cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()


def creer_utilisateur(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password,
        )
        print(f"✅ Utilisateur créé avec succès : {user.uid}")
        return user.uid
    except Exception as e:
        print(f"❌ Erreur lors de la création : {e}")
        return None


def ajoute_fidele(nom, gmail, password, telephone, date):
    # Ajouter une présence test
    uid = creer_utilisateur(gmail, password)


    if uid:
        data = {
            "id": uid,
            "nom": nom,
            "email": gmail,
            "telephone": telephone,
            "created_at": date,
        }
        ajoute_fidele_compl('fidele', uid, data)
        response = supabase.table("fidele").insert(data).execute()
        print(response)


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
