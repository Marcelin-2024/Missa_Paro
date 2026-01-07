from supabase import create_client

url = "https://orxjqcfrzrurjblytzry.supabase.co"
key = "sb_secret_A5K6_s5CUWU7Q9K8nkrW9A_Wyb8z-ki"
supabase = create_client(url, key)


def ajoute_fidele(nom, gmail, telephone, date):
    # Ajouter une présence test
    data = {
        "nom": nom,
        "email": gmail,
        "telephone": telephone,
        "created_at": date,
    }

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
