from supabase import create_client
from datetime import datetime

url = "https://orxjqcfrzrurjblytzry.supabase.co"
key = "sb_secret_A5K6_s5CUWU7Q9K8nkrW9A_Wyb8z-ki"  # Ta clé secrète du backend

supabase = create_client(url, key)

# Ajouter une présence test
data = {
    "nom": "Jean Kouamé",
    "email": "jean@gmail.com",
}

response = supabase.table("presences").insert(data).execute()
print(response)
