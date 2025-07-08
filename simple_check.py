import psycopg2

try:
    conn = psycopg2.connect(host='localhost', database='sac', user='postgres', password='postgres')
    cursor = conn.cursor()
    
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'individus' AND table_schema = 'sge_cre'")
    columns = cursor.fetchall()
    
    print("Colonnes de la table individus:")
    for col in columns:
        print(f"  - {col[0]}")
    
    column_names = [col[0] for col in columns]
    if 'actif' in column_names:
        print("La colonne 'actif' existe")
    else:
        print("La colonne 'actif' n'existe pas")
    
    conn.close()
    
except Exception as e:
    print(f"Erreur: {e}") 