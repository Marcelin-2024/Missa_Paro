# serveur.py - SOLUTION TEMPORAIRE
from supabase import create_client, Client

# Mettez vos valeurs directement (À REMPLACER)
SUPABASE_URL = "https://orxjqcfrzrurjblytzry.supabase.co"
SUPABASE_KEY = "sb_publishable_4nt0GGGNPWEY0-izLVtS1A_buw480u9"

# Supprimez les vérifications d'environnement
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("Connexion établie!")