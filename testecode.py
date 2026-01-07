import requests


def requet_reponse():
    # L'URL du service (ici une API de test)
    url = "https://e-messe.vercel.app/api/annonces"

    # On effectue la requête
    reponse = requests.get(url)

    # On vérifie si la requête a réussi
    if reponse.status_code == 200:
        # Si le serveur renvoie du JSON, on le transforme en dictionnaire Python
        donnees = reponse.json()
        print("Titre du post :", donnees['data'])
    else:
        print(f"Erreur : {reponse.status_code}")


def requet_envoie():

    # Données à envoyer
    data = {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean@test.com",
        "password": "jhjzeoierejf",
        "telephone": "0123456789"
    }

    # Envoyer POST
    response = requests.post(
        "https://e-messe.vercel.app/api/fideles",  # VOTRE API
        json=data,  # ou data=data pour form

    )

    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}")


if __name__=='__main__':
    requet_envoie()