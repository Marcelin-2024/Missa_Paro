import os
import json
from supabase import create_client
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv
import requests

# 1. On charge le .env en premier (pour le développement local)
load_dotenv()

# 2. On récupère les variables après le chargement
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

# --- Vérification Supabase ---
if url and key:
    supabase = create_client(url, key)
    print("✅ Supabase connecté !")
else:
    print("⚠️ Attention: SUPABASE_URL ou KEY manquante")

# --- La fonction init_firebase est correcte ---
def init_firebase():
    if not firebase_admin._apps:
        try:
            service_account_env = os.environ.get("FIREBASE_SERVICE_ACCOUNT")

            if service_account_env:
                service_account_info = json.loads(service_account_env)
                if "private_key" in service_account_info:
                    service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
                cred = credentials.Certificate(service_account_info)
                firebase_admin.initialize_app(cred)

            # Priorité 2 : Fichier physique (Uniquement si la variable est absente)
            else:
                cert_path = "serviceAccountKey.json"
                if os.path.exists(cert_path):
                    cred = credentials.Certificate(cert_path)
                    firebase_admin.initialize_app(cred)
                else:
                    # Si on ne trouve rien, on affiche une erreur claire sans faire planter le serveur
                    print("❌ Erreur critique : Aucun identifiant Firebase trouvé (Variable ou Fichier JSON)")
                    return None

        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation Firebase : {e}")
            return None

    return firestore.client()


# Initialisation sécurisée
db = None
try:
    db = init_firebase()
    if db:
        print("✅ Firebase connecté !")
except Exception:
    pass

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
    uid = creer_utilisateur(gmail, password)  # Récupère l'ID de Firebase

    if uid:
        data = {
            "id": uid,  # IMPORTANT : On force l'ID dans Supabase pour qu'il soit identique à Firebase
            "nom": nom,
            "email": gmail,
            "telephone": telephone,
            "created_at": date,
        }
        data = {
            "nom": nom,
            "email": gmail,
            "telephone": telephone,
            "created_at": date,
        }

        # 2. Ajout dans Firestore
        post_fidele_compl('fidele', uid, data1)

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
                "email": email,
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





def post_fidele_compl(user, uid, data):
    try:
        db = init_firebase()
        # Test d'écriture dans Firestore
        doc_ref = db.collection(user).document(uid)
        doc_ref.set(data)

        print("✅ Document écrit avec succès dans Firebase !")
    except Exception as e:
        print(f"❌ Erreur : {e}")



# --- FONCTIONS DE COMMUNICATION ---

# 1. Récupérer les infos d'une paroisse (Firestore ou Supabase selon ton choix)
def get_paroisse_db(paroisse_id):
    # Exemple avec Supabase
    try:
        response = supabase.table("paroisses").select("*").eq("id", paroisse_id).single().execute()
        return response.data
    except Exception as e:
        print(f"❌ Erreur get_paroisse : {e}")
        return None

# 2. Récupérer les messes (Supabase)
def get_messes_db():
    try:
        # On peut filtrer pour ne prendre que les messes futures
        response = supabase.table("messes").select("*").order("date").execute()
        return response.data
    except Exception as e:
        print(f"❌ Erreur get_messes : {e}")
        return []

# 3. Récupérer les annonces (Supabase)
def get_annonces_db():
    try:
        response = supabase.table("annonces").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"❌ Erreur get_annonces : {e}")
        return []

def post_intention(fidele_id, messe_id, objet_intention,detail_intention, date):
    # Ajouter une présence test
    data = {
        "fidele_id": fidele_id,
        "messe_id": messe_id,
        "objet_intention": objet_intention,
        "detail_intention":detail_intention,
        "statut": "en attente",
        "created_at": date,
    }

    response = supabase.table("intention_messe").insert(data).execute()
    return response.data

# 4. Modifier une intention (Supabase)
def update_intention_db(intention_id, nouveau_type_intention,nouveau_objet_intention):
    try:
        response = supabase.table("intention_messe").update({
            "type_intention": nouveau_type_intention,
            "objet_intention": nouveau_objet_intention
        }).eq("id", intention_id).execute()
        return response.data
    except Exception as e:
        print(f"❌ Erreur update_intention : {e}")
        return False

# 5. Supprimer une intention (Supabase)
def delete_intention_db(intention_id):
    try:
        response = supabase.table("intention_messe").delete().eq("id", intention_id).execute()
        return response.data
    except Exception as e:
        print(f"❌ Erreur delete_intention : {e}")
        return False

# 6. Récupérer les intentions d'un fidèle spécifique (Supabase)
def get_mes_intentions_db(fidele_id):
    try:
        response = supabase.table("intention_messe").select("*").eq("fidele_id", fidele_id).execute()
        return response.data
    except Exception as e:
        print(f"❌ Erreur get_mes_intentions : {e}")
        return []

# 7. Récupérer les intentions validées pour l'affichage public (Supabase)
def get_intentions_validees_db():
    try:
        response = supabase.table("intention_messe").select("*").eq("statut", "validé").execute()
        return response.data
    except Exception as e:
        print(f"❌ Erreur get_intentions_validees : {e}")
        return []

# 8. Ajouter un Avis/Feedback (Firestore - plus simple pour les logs textuels)
def ajoute_avis_db(uid, note, commentaire):
    try:
        db = init_firebase()
        data = {
            "uid": uid,
            "note": note,
            "commentaire": commentaire,
            "timestamp": datetime.now().isoformat()
        }
        db.collection("avis").add(data)
        print("✅ Avis enregistré dans Firestore")
        return True
    except Exception as e:
        print(f"❌ Erreur avis : {e}")
        return False

# 9. Enregistrer un Token Push (Firestore)
def save_push_token(uid, token):
    try:
        db = init_firebase()
        db.collection("fidele").document(uid).update({
            "push_token": token
        })
        return True
    except Exception as e:
        print(f"❌ Erreur token push : {e}")
        return False
