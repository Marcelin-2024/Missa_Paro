import requests

url = "https://missa-paro.onrender.com/api/fideles"  # Change l'URL si nécessaire

data = {
    "nom": "Kouassi",
    "prenoms": "Jean Marc",
    "email": "jeanmarc@gmail.com",
    "password": "123456",
    "telephone": "0700000000",
    "diocese": "Abidjan",
    "paroisse": "Saint Jean"
}

response = requests.post(url, json=data)

print("Status code :", response.status_code)
print("Réponse :", response.json())