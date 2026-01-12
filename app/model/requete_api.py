import requests



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
            "https://missa-paro.onrender.com/api/paroisse",
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
            "https://missa-paro.onrender.com/api/login",
            json=data
        )

        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.json()}")

    except Exception as e:
        print(f"Erreur 1: {e}")