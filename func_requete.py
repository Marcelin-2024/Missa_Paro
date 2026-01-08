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


def ajoute_fidele(nom,prenoms, diocese,paroisse,gmail, password, telephone, date):
    # 1. Création du compte Auth (initialise Firebase au passage)
    uid = creer_utilisateur(gmail, password)

    if uid:
        data1 = {
            "nom": nom + " " + prenoms,
            "email": gmail,
            "telephone": telephone,
            "Diocèse" : diocese,
            "paroisse" : paroisse,
            "created_at": date,
        }
        data = {
            "nom": nom +" "+ prenoms,
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
