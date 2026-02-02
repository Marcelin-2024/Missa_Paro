from module_fidele import creer_utilisateur, post_fidele_compl, url, key, supabase


def ajoute_paroisse(nom_complet, diocese,paroisse,gmail,poste , password, telephone, date):
    # 1. Création du compte Auth (initialise Firebase au passage)
    uid = creer_utilisateur(gmail, password)

    if uid:
        data1 = {
            "id": uid,  # IMPORTANT : On force l'ID dans Supabase pour qu'il soit identique à Firebase
            "paroisse": paroisse,
            "diocese": diocese,
            "nom_complet": nom_complet,
            "poste": poste,
            "telephone": telephone,
            "email": gmail,
        }
        data = {
            "nom": nom_complet,
            "email": gmail,
            "telephone": telephone,
            "created_at": date,
        }

        # 2. Ajout dans Firestore
        post_fidele_compl('paroisse', uid, data1)

        # 3. Ajout dans Supabase
        if url and key:
            try:
                supabase.table("paroisse").insert(data).execute()
                print("✅ Ajouté à Supabase")
            except Exception as e:
                print(f"❌ Erreur Supabase : {e}")