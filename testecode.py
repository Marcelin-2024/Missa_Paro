resultat = {
    "status": "success",
    "email": "email@exemple.com",
    "uid": "uid_de_l_utilisateur",
    "idToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
# Vérifier le statut
resultat =resultat
if resultat["status"] == "success":
    print("Connexion réussie ✅")

    # Récupérer les infos
    email = resultat["email"]
    uid = resultat["uid"]
    idToken = resultat["idToken"]

    print(f"Email : {email}")
    print(f"UID : {uid}")
    print(f"Token : {idToken}")
else:
    print("Erreur de connexion")
