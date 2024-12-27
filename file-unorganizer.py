import os
import shutil
import json

def restaurer_fichiers():
    # Obtenir le dossier courant
    dossier_source = os.getcwd()
    
    # Chemins des dossiers à restaurer
    dossiers_a_restaurer = ['images', 'documents', 'videos', 'comprimes', 'torrents', 'executables']
    
    # Fichiers journaux possibles
    fichiers_journal = ['journal_organisation.json', '.journal_organisation.json']
    
    # Trouver le fichier journal
    chemin_journal = None
    for fichier in fichiers_journal:
        chemin_potentiel = os.path.join(dossier_source, fichier)
        if os.path.exists(chemin_potentiel):
            chemin_journal = chemin_potentiel
            break
    
    # Vérifier si le fichier journal existe
    if not chemin_journal:
        print("Aucun journal de déplacement trouvé. Impossible de restaurer.")
        return
    
    # Charger le journal des déplacements
    with open(chemin_journal, 'r', encoding='utf-8') as f:
        journal = json.load(f)
    
    # Restaurer chaque fichier
    fichiers_restaures = 0
    for dossier in dossiers_a_restaurer:
        chemin_dossier = os.path.join(dossier_source, dossier)
        
        # Vérifier si le dossier existe
        if not os.path.exists(chemin_dossier):
            continue
        
        # Parcourir les fichiers du dossier
        for fichier in os.listdir(chemin_dossier):
            chemin_fichier = os.path.join(chemin_dossier, fichier)
            
            # Vérifier si le fichier est dans le journal
            if fichier in journal:
                # Restaurer à l'emplacement d'origine
                destination = os.path.join(dossier_source, fichier)
                
                # Vérifier les conflits
                if os.path.exists(destination):
                    base, ext = os.path.splitext(fichier)
                    compteur = 1
                    while os.path.exists(destination):
                        nouveau_nom = f"{base}({compteur}){ext}"
                        destination = os.path.join(dossier_source, nouveau_nom)
                        compteur += 1
                
                shutil.move(chemin_fichier, destination)
                print(f"Restauré {fichier} vers {destination}")
                fichiers_restaures += 1
    
    # Supprimer les dossiers de catégories
    for dossier in dossiers_a_restaurer:
        chemin_dossier = os.path.join(dossier_source, dossier)
        if os.path.exists(chemin_dossier) and not os.listdir(chemin_dossier):
            os.rmdir(chemin_dossier)
    
    # Supprimer le fichier "tu_tattends_a_quoi.txt" s'il existe
    fichier_texte = os.path.join(dossier_source, 'tu_tattends_a_quoi.txt')
    if os.path.exists(fichier_texte):
        os.remove(fichier_texte)
    
    # Supprimer le journal uniquement après une restauration réussie
    os.remove(chemin_journal)
    
    print(f"Restauration terminée. {fichiers_restaures} fichiers restaurés.")

def main():
    restaurer_fichiers()

if __name__ == "__main__":
    main()
