import psycopg2

try:
    conn = psycopg2.connect(host='localhost', database='sac', user='postgres', password='postgres')
    cursor = conn.cursor()
    
    # Vérifier les contraintes du domaine role_ind
    cursor.execute("""
        SELECT conname, pg_get_constraintdef(oid) 
        FROM pg_constraint 
        WHERE conname = 'role_ind_check'
    """)
    
    constraints = cursor.fetchall()
    print("Contraintes sur role_ind:")
    for constraint in constraints:
        print(f"  {constraint[0]}: {constraint[1]}")
    
    # Vérifier les valeurs possibles dans le domaine
    cursor.execute("""
        SELECT enumlabel 
        FROM pg_enum 
        WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'role_ind')
        ORDER BY enumsortorder
    """)
    
    roles = cursor.fetchall()
    print("\nRôles autorisés:")
    for role in roles:
        print(f"  - {role[0]}")
    
    # Vérifier les rôles existants dans la table
    cursor.execute("SELECT DISTINCT role FROM sge_cre.individus")
    existing_roles = cursor.fetchall()
    print("\nRôles existants dans la table:")
    for role in existing_roles:
        print(f"  - {role[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"Erreur: {e}") 