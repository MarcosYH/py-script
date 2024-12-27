import os
import shutil
import json
import platform

def cacher_fichier(chemin_fichier):
    systeme = platform.system()
    try:
        if systeme == 'Windows':
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(chemin_fichier, 0x02)
        elif systeme in ['Darwin', 'Linux']:
            nom_fichier = os.path.basename(chemin_fichier)
            dossier = os.path.dirname(chemin_fichier)
            nouveau_chemin = os.path.join(dossier, '.' + nom_fichier)
            os.rename(chemin_fichier, nouveau_chemin)
        print(f"Fichier journal caché sur {systeme}")
    except Exception as e:
        print(f"Erreur lors du masquage du fichier : {e}")

def creer_dossiers(base_path, categories):
    for dossier in categories.keys():
        os.makedirs(os.path.join(base_path, dossier), exist_ok=True)

def deplacer_fichier(chemin_complet, fichier, dossier_source, types_fichiers, journal):
    extension = os.path.splitext(fichier)[1].lower()
    for type_fichier, extensions in types_fichiers.items():
        if extension in extensions:
            destination = os.path.join(dossier_source, type_fichier, fichier)
            try:
                shutil.move(chemin_complet, destination)
                print(f"Déplacé {fichier} vers {type_fichier}")
                journal[fichier] = {"type": type_fichier, "origine": chemin_complet}
            except Exception as e:
                print(f"Erreur lors du déplacement de {fichier} : {e}")
            return True
    return False

def organiser_fichiers():
    dossier_source = os.getcwd()
    types_fichiers = {
        'images': ['.png', '.jpeg', '.jpg', '.svg', '.gif', '.bmp', '.webp', '.tiff', '.raw', '.heic'],
        'documents': ['.docx', '.pdf', '.txt', '.doc', '.rtf', '.odt', '.xlsx', '.csv', '.pptx', '.md'],
        'videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg'],
        'comprimes': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tgz'],
        'torrents': ['.torrent'],
        'executables': ['.exe', '.msi', '.bat', '.sh', '.cmd', '.app', '.bin'],
        'autres': []
    }
    
    journal = {}
    creer_dossiers(dossier_source, types_fichiers)

    fichiers_a_organiser = []
    for fichier in os.listdir(dossier_source):
        chemin_complet = os.path.join(dossier_source, fichier)
        if os.path.isdir(chemin_complet) or fichier in ['organiseur_fichiers.py', 'journal_organisation.json']:
            continue
        if not deplacer_fichier(chemin_complet, fichier, dossier_source, types_fichiers, journal):
            autres_dossier = os.path.join(dossier_source, 'autres', fichier)
            shutil.move(chemin_complet, autres_dossier)
            print(f"Déplacé {fichier} vers 'autres'")
            journal[fichier] = {"type": "autres", "origine": chemin_complet}
            fichiers_a_organiser.append(fichier)
    
    chemin_journal = os.path.join(dossier_source, 'journal_organisation.json')
    with open(chemin_journal, 'w', encoding='utf-8') as f:
        json.dump(journal, f, ensure_ascii=False, indent=4)
    cacher_fichier(chemin_journal)

    if not fichiers_a_organiser:
        with open('tu_tattends_a_quoi.txt', 'w', encoding='utf-8') as f:
            f.write("Tu t'attends à quoi ?")
        print("Aucun fichier organisé. Message humoristique ajouté.")
    print(f"Total de {len(journal)} fichiers organisés.")

if __name__ == "__main__":
    organiser_fichiers()
