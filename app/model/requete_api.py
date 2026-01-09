import requests


def requet_reponse():
    # L'URL du service (ici une API de test)
    url = "https://e-messe.vercel.app/api/paroisse"

    # On effectue la requête
    reponse = requests.get(url)

    # On vérifie si la requête a réussi
    if reponse.status_code == 200:
        # Si le serveur renvoie du JSON, on le transforme en dictionnaire Python
        donnees = reponse.json()
        print("Titre du post :", donnees['data'])
    else:
        print(f"Erreur : {reponse.status_code}")




def requet_envoie(paroisse, diocese, nom_complet, poste, telephone,gmail, password):
    # Données à envoyer sans le champ date
    data = {
        "paroisse": paroisse,
        "diocese": diocese,
        "nom_complet": nom_complet,
        "poste": poste,
        "telephone": telephone,
        "email": gmail,
        "password": password
    }

    try:
        response = requests.post(
            "https://e-messe.vercel.app/api/paroisse",
            json=data
        )

        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.json()}")

    except Exception as e:
        print(f"Erreur : {e}")


def requet_connec(gmail, password):
    # Données à envoyer sans le champ date
    data = {
        "email": gmail,
        "password": password,
    }

    try:
        response = requests.post(
            "https://e-messe.vercel.app/api/login",
            json=data
        )

        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.json()}")

    except Exception as e:
        print(f"Erreur 1: {e}")

requet_reponse()