#!/usr/bin/env python3

# Importation des modules nécessaires
import customtkinter as ctk  # Bibliothèque CustomTkinter pour l'interface graphique
import tkinter as tk         # Module Tkinter de base, utilisé par CustomTkinter
from tkinter import simpledialog, messagebox, filedialog # Fonctions de boîte de dialogue standard
import webbrowser            # Pour ouvrir des liens web dans le navigateur par défaut
import os                    # Pour interagir avec le système d'exploitation (chemins de fichiers, dossiers)
import sys                   # Pour accéder aux paramètres spécifiques du système (ex: PyInstaller)
import json                  # Pour lire et écrire des données au format JSON
from PIL import Image, ImageTk # Pillow pour le traitement des images (icônes)
import requests              # Pour faire des requêtes HTTP (ex: récupérer les favicons)
from io import BytesIO       # Pour manipuler des données binaires en mémoire (favicons)

# --- Configuration initiale de CustomTkinter ---
# Mode d'apparence par défaut (sombre)
DEFAULT_APPEARANCE_MODE = "dark"
# Thème de couleur intégré par défaut pour CustomTkinter
DEFAULT_COLOR_THEME = "blue"

# Thèmes de couleurs intégrés disponibles dans CustomTkinter (simplifié)
AVAILABLE_COLOR_THEMES = ["blue", "green", "dark-blue"]

# --- Chemins des fichiers de configuration dans AppData ---
# Cette fonction détermine le chemin standard pour les données d'application par système d'exploitation.
# Cela permet à l'application de stocker ses fichiers de configuration
# (favoris, paramètres) dans un emplacement approprié pour l'utilisateur,
# évitant ainsi de mélanger les données utilisateur avec les fichiers du script.
def get_app_data_path():
    if sys.platform == "win32":
        # Pour Windows, utilise le dossier LOCALAPPDATA
        return os.path.join(os.environ["LOCALAPPDATA"], "FavMeData")
    elif sys.platform == "darwin": # macOS
        # Pour macOS, utilise Application Support dans la bibliothèque de l'utilisateur
        return os.path.join(os.path.expanduser("~/Library/Application Support"), "FavMeData")
    else: # Linux et autres systèmes basés sur UNIX
        # Pour Linux, utilise le dossier .config (standard XDG Base Directory Specification)
        return os.path.join(os.path.expanduser("~/.config"), "FavMeData")

# Définit le répertoire principal de l'application dans AppData
APP_DATA_DIR = get_app_data_path()
# Crée le dossier FavMeData s'il n'existe pas
os.makedirs(APP_DATA_DIR, exist_ok=True)

# Chemins complets des fichiers de configuration
CONFIG_FILE = os.path.join(APP_DATA_DIR, "favorites_config.json")
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "app_settings.json")

# --- Fonctions de gestion de la persistance des données (JSON) ---
def load_favorites(filename=CONFIG_FILE):
    """
    Charge les favoris (dossiers et sites web) depuis un fichier JSON.
    Gère le cas où le fichier n'existe pas ou est corrompu.
    """
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Retourne les dictionnaires de dossiers et de sites web, ou des dictionnaires vides si absents
                return data.get("folders", {}), data.get("websites", {})
        except json.JSONDecodeError:
            # Affiche un avertissement si le fichier est corrompu
            messagebox.showwarning("Erreur de configuration",
                                   f"Le fichier de configuration des favoris '{filename}' est corrompu ou vide. Les favoris par défaut seront utilisés.")
            return {}, {}
    return {}, {} # Retourne des dictionnaires vides si le fichier n'existe pas

def save_favorites(folders, websites, filename=CONFIG_FILE):
    """
    Sauvegarde les favoris (dossiers et sites web) dans un fichier JSON.
    """
    data = {"folders": folders, "websites": websites}
    with open(filename, 'w', encoding='utf-8') as f:
        # Écrit les données dans le fichier avec un formatage indenté pour la lisibilité
        json.dump(data, f, indent=4)

def load_settings(filename=SETTINGS_FILE):
    """
    Charge les paramètres de l'application (mode d'apparence, thème de couleur) depuis un fichier JSON.
    Gère le cas où le fichier n'existe pas ou est corrompu.
    """
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                return settings
        except json.JSONDecodeError:
            # Affiche un avertissement si le fichier est corrompu
            messagebox.showwarning("Erreur de paramètres",
                                   f"Le fichier de paramètres '{filename}' est corrompu ou vide. Les paramètres par défaut seront utilisés.")
            # Retourne les paramètres par défaut en cas d'erreur
            return {"appearance_mode": DEFAULT_APPEARANCE_MODE, "color_theme": DEFAULT_COLOR_THEME}
    # Retourne les paramètres par défaut si le fichier n'existe pas
    return {"appearance_mode": DEFAULT_APPEARANCE_MODE, "color_theme": DEFAULT_COLOR_THEME}

def save_settings(settings, filename=SETTINGS_FILE):
    """
    Sauvegarde les paramètres de l'application dans un fichier JSON.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # Écrit les paramètres dans le fichier avec un formatage indenté pour la lisibilité
        json.dump(settings, f, indent=4)

# --- Chargement initial des paramètres et application du thème ---
# Charge les paramètres de l'application (mode d'apparence et thème de couleur)
app_settings = load_settings()

# S'assurer que le thème chargé est un thème valide (intégré).
# Si le thème enregistré n'est pas dans la liste des thèmes intégrés, on revient au thème par défaut.
if app_settings["color_theme"] not in AVAILABLE_COLOR_THEMES:
    app_settings["color_theme"] = DEFAULT_COLOR_THEME # Revert au thème par défaut sécurisé
    save_settings(app_settings) # Sauvegarder le paramètre corrigé

# Applique le mode d'apparence (sombre, clair, système)
ctk.set_appearance_mode(app_settings["appearance_mode"])

# Applique le thème de couleur initial
ctk.set_default_color_theme(app_settings["color_theme"])

# --- Chargement initial des favoris ---
favorite_folders, favorite_websites = load_favorites()

# --- Vérification de l'existence des dossiers au démarrage ---
# Cette section vérifie si les chemins de dossiers enregistrés existent toujours sur le système.
print("--- Vérification des chemins de dossiers ---")
# Utilise list() pour itérer sur une copie du dictionnaire, car nous pourrions supprimer des éléments
for name, path in list(favorite_folders.items()):
    print(f"{name} -> {path}")
    if not os.path.exists(path):
        print(f"❌ Le dossier '{name}' n'existe pas au chemin : {path}. Il sera supprimé de la liste.")
        del favorite_folders[name] # Supprime le dossier si le chemin n'est plus valide
    else:
        print(f"✅ Le dossier '{name}' existe.")
print("------------------------------------------\n")
# Sauvegarde les favoris après la vérification pour persister les suppressions
save_favorites(favorite_folders, favorite_websites)

# --- Fonction utilitaire pour obtenir le chemin des ressources (icônes) ---
def get_resource_path(relative_path):
    """
    Retourne le chemin absolu d'une ressource (comme une icône),
    que l'application soit exécutée depuis un script Python ou un exécutable PyInstaller.
    PyInstaller place les ressources dans un dossier temporaire accessible via sys._MEIPASS.
    """
    if hasattr(sys, '_MEIPASS'):
        # Si l'application est compilée avec PyInstaller (mode "frozen")
        return os.path.join(sys._MEIPASS, relative_path)
    # Si l'application est exécutée en tant que script Python (mode "normal")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

# --- Chargement des icônes pour les TITRES de section et les actions (éditer/supprimer) ---
# Utilise un bloc try-except pour gérer les erreurs si les fichiers d'icônes sont manquants.
# Cela permet à l'application de démarrer même sans les icônes.
try:
    # Crée des objets CTkImage à partir des fichiers PNG.
    # get_resource_path assure que le bon chemin est trouvé.
    folder_title_icon = ctk.CTkImage(Image.open(get_resource_path("folder_icon.png")), size=(24, 24))
    web_title_icon = ctk.CTkImage(Image.open(get_resource_path("web_icon.png")), size=(24, 24))
    edit_icon = ctk.CTkImage(Image.open(get_resource_path("edit_icon.png")), size=(16, 16))
    delete_icon = ctk.CTkImage(Image.open(get_resource_path("delete_icon.png")), size=(16, 16))
    settings_icon = ctk.CTkImage(Image.open(get_resource_path("settings_icon.png")), size=(18, 18)) # Nouvelle icône pour les paramètres
    add_icon = ctk.CTkImage(Image.open(get_resource_path("add_icon.png")), size=(18, 18)) # Nouvelle icône pour le bouton "Ajouter un favori"

except FileNotFoundError:
    # Affiche une boîte de message si des icônes sont introuvables
    messagebox.showerror("Erreur d'icône", "Fichiers d'icônes nécessaires ('folder_icon.png', 'web_icon.png', 'edit_icon.png', 'delete_icon.png', 'settings_icon.png', 'add_icon.png') introuvables dans le répertoire du script. Certaines icônes pourraient manquer.")
    # Définit les icônes à None pour éviter d'autres erreurs si elles ne sont pas chargées
    folder_title_icon = None
    web_title_icon = None
    edit_icon = None
    delete_icon = None
    settings_icon = None
    add_icon = None
except Exception as e:
    # Capture toute autre exception lors du chargement des images
    messagebox.showerror("Erreur d'icône", f"Erreur inattendue lors du chargement des icônes : {e}")
    folder_title_icon = None
    web_title_icon = None
    edit_icon = None
    delete_icon = None
    settings_icon = None
    add_icon = None

# --- Fonctions d'action pour les favoris ---
def open_folder(path):
    """Ouvre un dossier en utilisant le programme par défaut du système."""
    try:
        os.startfile(path) # Fonction Windows pour ouvrir des fichiers/dossiers
    except AttributeError:
        # Pour d'autres OS (Linux, macOS), utilise webbrowser.open ou subprocess
        if sys.platform == "darwin": # macOS
            os.system(f"open \"{path}\"")
        else: # Linux
            os.system(f"xdg-open \"{path}\"")
    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Le dossier '{path}' n'a pas été trouvé.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir le dossier : {e}")

def open_website(url):
    """Ouvre un site web dans le navigateur par défaut."""
    try:
        webbrowser.open(url)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir le site web : {e}")

# --- Fonctions pour récupérer les favicons (icônes de site web) ---
def get_favicon_url(url):
    """
    Tente de trouver l'URL du favicon pour un site web donné.
    Priorise les favicons standard (/favicon.ico) ou tente d'analyser la page HTML.
    """
    # 1. Essai de l'emplacement standard du favicon
    if not url.startswith(("http://", "https://")):
        url = "http://" + url # Assure que l'URL a un schéma

    try:
        parsed_url = requests.utils.urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        favicon_url = f"{base_url}/favicon.ico"
        response = requests.head(favicon_url, allow_redirects=True, timeout=3) # Réduit le timeout
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            return favicon_url
    except requests.exceptions.RequestException:
        pass # Ignorer les erreurs et passer à la méthode suivante

    # 2. Si le favicon standard ne fonctionne pas, essayer d'analyser la page HTML (simplifié)
    try:
        response = requests.get(url, timeout=3) # Réduit le timeout
        response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP
        import re
        # Recherche des balises link rel="icon" ou rel="shortcut icon"
        match = re.search(r'<link[^>]+(?:rel=["\'](?:shortcut )?icon["\'][^>]*href=["\']([^"\']+)["\'])', response.text, re.IGNORECASE)
        if match:
            found_url = match.group(1)
            # Si l'URL trouvée est relative, la rendre absolue
            if not found_url.startswith(("http://", "https://")):
                if found_url.startswith("//"):
                    found_url = parsed_url.scheme + ":" + found_url
                else:
                    found_url = base_url + "/" + found_url.lstrip('/')
            return found_url
    except requests.exceptions.RequestException:
        pass

    return None # Retourne None si aucun favicon n'est trouvé

# Cache pour stocker les favicons déjà chargés et éviter de les re-télécharger
favicon_cache = {}

def load_favicon(url, size=(16, 16)):
    """
    Télécharge et redimensionne le favicon d'une URL donnée.
    Retourne un objet CTkImage si le favicon est trouvé, None sinon.
    Utilise un cache pour les favicons déjà téléchargés.
    """
    if url in favicon_cache:
        return favicon_cache[url]

    favicon_url = get_favicon_url(url)
    if favicon_url:
        try:
            response = requests.get(favicon_url, timeout=5)
            response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP
            image_data = BytesIO(response.content)
            img = Image.open(image_data)
            img = img.resize(size, Image.Resampling.LANCZOS) # Redimensionne avec une bonne qualité
            ctk_image = ctk.CTkImage(img, size=size)
            favicon_cache[url] = ctk_image # Ajoute au cache
            return ctk_image
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête pour favicon {favicon_url}: {e}")
        except Exception as e:
            print(f"Erreur de chargement/redimensionnement du favicon pour {url}: {e}")
    return None

# --- Fonctions pour la gestion dynamique des favoris avec CTk Toplevel (fenêtre CustomTkinter) ---
class FavoriteDialog(ctk.CTkToplevel):
    """
    Boîte de dialogue personnalisée pour ajouter ou modifier un favori (dossier ou site web).
    Hérite de ctk.CTkToplevel pour avoir une apparence CustomTkinter et être modale.
    """
    def __init__(self, parent, title, name="", value="", is_folder=True):
        """
        Initialise la boîte de dialogue.
        :param parent: La fenêtre parente (l'application principale).
        :param title: Le titre de la boîte de dialogue.
        :param name: Le nom initial du favori (pour l'édition).
        :param value: La valeur initiale (chemin du dossier ou URL) du favori.
        :param is_folder: Booléen indiquant si c'est un dossier (True) ou un site web (False).
        """
        super().__init__(parent) # Appelle le constructeur de la classe parente
        self.title(title) # Définit le titre de la fenêtre
        self.geometry("400x250") # Définit la taille de la fenêtre
        self.transient(parent) # Fait en sorte que la fenêtre disparaisse si la parente est minimisée
        self.grab_set() # Rend la fenêtre modale (bloque l'interaction avec la fenêtre parente)
        self.resizable(False, False) # Empêche le redimensionnement de la fenêtre
        # Gère la fermeture de la fenêtre par l'utilisateur (bouton X)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        # Variables pour stocker le nom et la valeur du favori
        self.name_var = ctk.StringVar(value=name)
        self.value_var = ctk.StringVar(value=value)
        self.is_folder = is_folder # Stocke le type de favori
        self.result = None # Stockera le résultat de la boîte de dialogue (nom, valeur)

        self.create_widgets() # Crée les éléments de l'interface de la boîte de dialogue

    def create_widgets(self):
        """Crée et organise les widgets (labels, entrées, boutons) dans la boîte de dialogue."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Champ pour le nom du favori
        name_label = ctk.CTkLabel(main_frame, text="Nom :")
        name_label.pack(pady=(0, 5), anchor="w")
        name_entry = ctk.CTkEntry(main_frame, textvariable=self.name_var, width=300)
        name_entry.pack(pady=(0, 10), anchor="w")

        # Champ pour la valeur (chemin ou URL) du favori
        value_label_text = "Chemin du dossier :" if self.is_folder else "URL du site :"
        value_label = ctk.CTkLabel(main_frame, text=value_label_text)
        value_label.pack(pady=(0, 5), anchor="w")
        
        # Frame pour l'entrée de valeur et le bouton "Parcourir" (si c'est un dossier)
        value_input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        value_input_frame.pack(fill="x", pady=(0, 15))

        value_entry = ctk.CTkEntry(value_input_frame, textvariable=self.value_var, width=220)
        value_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        if self.is_folder:
            # Bouton pour ouvrir le sélecteur de dossier si c'est un favori de type dossier
            browse_button = ctk.CTkButton(value_input_frame, text="Parcourir", command=self.browse_folder)
            browse_button.pack(side="right")

        # Frame pour les boutons "Ajouter/Modifier" et "Annuler"
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=0)

        ok_button_text = "Modifier" if self.name_var.get() else "Ajouter"
        ok_button = ctk.CTkButton(button_frame, text=ok_button_text, command=self.on_ok)
        ok_button.pack(side="left", expand=True, padx=(0, 5))

        cancel_button = ctk.CTkButton(button_frame, text="Annuler", command=self.on_cancel)
        cancel_button.pack(side="right", expand=True, padx=(5, 0))

    def browse_folder(self):
        """Ouvre une boîte de dialogue pour sélectionner un dossier."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.value_var.set(folder_selected) # Met à jour la variable avec le chemin sélectionné

    def on_ok(self):
        """
        Gère l'action lorsque l'utilisateur clique sur "Ajouter" ou "Modifier".
        Valide les entrées et stocke le résultat.
        """
        name = self.name_var.get().strip()
        value = self.value_var.get().strip()

        if not name:
            messagebox.showwarning("Entrée manquante", "Veuillez entrer un nom pour le favori.", parent=self)
            return
        if not value:
            messagebox.showwarning("Entrée manquante", f"Veuillez entrer un {'chemin de dossier' if self.is_folder else 'URL de site'} pour le favori.", parent=self)
            return

        self.result = (name, value) # Stocke le nom et la valeur comme résultat
        self.destroy() # Ferme la boîte de dialogue

    def on_cancel(self):
        """Gère l'action lorsque l'utilisateur clique sur "Annuler" ou ferme la fenêtre."""
        self.result = None # Indique qu'aucune action n'a été confirmée
        self.destroy() # Ferme la boîte de dialogue

# --- Fonctions appelant la fenêtre modale FavoriteDialog ---
def add_favorite_entry(is_folder): # Renommé pour éviter la confusion
    """
    Ouvre la boîte de dialogue pour ajouter un nouveau favori.
    :param is_folder: True si c'est un dossier, False si c'est un site web.
    """
    dialog_title = "Ajouter un dossier favori" if is_folder else "Ajouter un site web favori"
    dialog = FavoriteDialog(app, dialog_title, is_folder=is_folder)
    app.wait_window(dialog) # Attend que la boîte de dialogue soit fermée

    if dialog.result:
        name, value = dialog.result
        if is_folder:
            if name in favorite_folders:
                messagebox.showwarning("Nom existant", f"Un dossier favori nommé '{name}' existe déjà. Veuillez choisir un nom différent.")
                return
            favorite_folders[name] = value
        else:
            if name in favorite_websites:
                messagebox.showwarning("Nom existant", f"Un site web favori nommé '{name}' existe déjà. Veuillez choisir un nom différent.")
                return
            favorite_websites[name] = value

        save_favorites(favorite_folders, favorite_websites) # Sauvegarde les changements
        update_view() # Met à jour l'affichage de l'interface

def edit_favorite(old_name, old_value, is_folder):
    """
    Ouvre la boîte de dialogue pour modifier un favori existant.
    :param old_name: L'ancien nom du favori.
    :param old_value: L'ancienne valeur (chemin/URL) du favori.
    :param is_folder: True si c'est un dossier, False si c'est un site web.
    """
    dialog_title = "Modifier le dossier favori" if is_folder else "Modifier le site web favori"
    dialog = FavoriteDialog(app, dialog_title, name=old_name, value=old_value, is_folder=is_folder)
    app.wait_window(dialog) # Attend que la boîte de dialogue soit fermée

    if dialog.result:
        new_name, new_value = dialog.result
        
        # Empêche de modifier si le nouveau nom est vide
        if not new_name:
            messagebox.showwarning("Nom invalide", "Le nom du favori ne peut pas être vide.")
            return

        if is_folder:
            if new_name != old_name and new_name in favorite_folders:
                messagebox.showwarning("Nom existant", f"Un dossier favori nommé '{new_name}' existe déjà. Veuillez choisir un nom différent.")
                return
            # Si le nom a changé, supprime l'ancien et ajoute le nouveau
            if new_name != old_name:
                del favorite_folders[old_name]
            favorite_folders[new_name] = new_value
        else:
            if new_name != old_name and new_name in favorite_websites:
                messagebox.showwarning("Nom existant", f"Un site web favori nommé '{new_name}' existe déjà. Veuillez choisir un nom différent.")
                return
            # Si le nom a changé, supprime l'ancien et ajoute le nouveau
            if new_name != old_name:
                del favorite_websites[old_name]
            favorite_websites[new_name] = new_value

        save_favorites(favorite_folders, favorite_websites) # Sauvegarde les changements
        update_view() # Met à jour l'affichage

def delete_favorite(name, is_folder):
    """
    Supprime un favori après confirmation de l'utilisateur.
    :param name: Le nom du favori à supprimer.
    :param is_folder: True si c'est un dossier, False si c'est un site web.
    """
    type_text = "dossier" if is_folder else "site web"
    if messagebox.askyesno("Confirmer la suppression", f"Êtes-vous sûr de vouloir supprimer le {type_text} favori '{name}' ?"):
        if is_folder:
            del favorite_folders[name]
        else:
            del favorite_websites[name]
        
        save_favorites(favorite_folders, favorite_websites) # Sauvegarde les changements
        update_view() # Met à jour l'affichage

# --- Fonctions de création des boutons (avec boutons Edit/Delete) ---
def create_folder_button(parent_frame, name, path):
    """
    Crée un bouton CustomTkinter pour un dossier favori,
    incluant des boutons pour éditer et supprimer.
    """
    btn_frame = ctk.CTkFrame(parent_frame)
    btn_frame.pack(fill="x", pady=2)

    # Bouton principal pour ouvrir le dossier
    folder_btn = ctk.CTkButton(btn_frame, text=name, command=lambda p=path: open_folder(p), anchor="w")
    folder_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

    # Bouton "Modifier" (avec icône si chargée, sinon texte)
    if edit_icon:
        edit_btn = ctk.CTkButton(btn_frame, text="", image=edit_icon, width=30, command=lambda n=name, v=path: edit_favorite(n, v, True))
        edit_btn.pack(side="left", padx=2)
    else:
        edit_btn = ctk.CTkButton(btn_frame, text="Éditer", width=50, command=lambda n=name, v=path: edit_favorite(n, v, True))
        edit_btn.pack(side="left", padx=2)

    # Bouton "Supprimer" (avec icône si chargée, sinon texte)
    if delete_icon:
        delete_btn = ctk.CTkButton(btn_frame, text="", image=delete_icon, width=30, command=lambda n=name: delete_favorite(n, True))
        delete_btn.pack(side="left", padx=2)
    else:
        delete_btn = ctk.CTkButton(btn_frame, text="Suppr", width=50, command=lambda n=name: delete_favorite(n, True))
        delete_btn.pack(side="left", padx=2)


def create_website_button(parent_frame, name, url):
    """
    Crée un bouton CustomTkinter pour un site web favori,
    incluant un favicon si disponible et des boutons pour éditer et supprimer.
    """
    btn_frame = ctk.CTkFrame(parent_frame)
    btn_frame.pack(fill="x", pady=2)

    # Chargement asynchrone du favicon pour ne pas bloquer l'interface
    favicon_image = load_favicon(url)

    # Bouton principal pour ouvrir le site web (avec favicon si disponible)
    web_btn = ctk.CTkButton(btn_frame, text=name, command=lambda u=url: open_website(u), anchor="w", image=favicon_image, compound="left")
    web_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

    # Bouton "Modifier" (avec icône si chargée, sinon texte)
    if edit_icon:
        edit_btn = ctk.CTkButton(btn_frame, text="", image=edit_icon, width=30, command=lambda n=name, u=url: edit_favorite(n, u, False))
        edit_btn.pack(side="left", padx=2)
    else:
        edit_btn = ctk.CTkButton(btn_frame, text="Éditer", width=50, command=lambda n=name, u=url: edit_favorite(n, u, False))
        edit_btn.pack(side="left", padx=2)

    # Bouton "Supprimer" (avec icône si chargée, sinon texte)
    if delete_icon:
        delete_btn = ctk.CTkButton(btn_frame, text="", image=delete_icon, width=30, command=lambda n=name: delete_favorite(n, False))
        delete_btn.pack(side="left", padx=2)
    else:
        delete_btn = ctk.CTkButton(btn_frame, text="Suppr", width=50, command=lambda n=name: delete_favorite(n, False))
        delete_btn.pack(side="left", padx=2)


# --- Fonctions de mise à jour de l'affichage ---
def toggle_view():
    """Bascule entre l'affichage des dossiers favoris et des sites web favoris."""
    global showing_folders # Déclare qu'on va modifier la variable globale
    showing_folders = not showing_folders # Inverse la valeur
    update_view() # Met à jour l'interface

def update_view():
    """
    Met à jour l'interface utilisateur pour afficher les favoris (dossiers ou sites web)
    en fonction de la variable `showing_folders`.
    """
    # Détruit tous les widgets existants dans les cadres pour les recréer
    for widget in folder_frame.winfo_children():
        widget.destroy()
    for widget in web_frame.winfo_children():
        widget.destroy()

    if showing_folders:
        # Configuration du bouton de bascule pour afficher "Web" (avec icône)
        if web_title_icon: # Utilisation de web_title_icon comme icône pour le bouton "Web"
            toggle_button.configure(text="Web", image=web_title_icon, compound="left")
        else:
            toggle_button.configure(text="Web", image=None, compound="none") # Réinitialise l'image si non trouvée

        folder_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10)) # Affiche le cadre des dossiers
        web_frame.pack_forget() # Cache le cadre des sites web

        # Ajoute un label de titre pour la section des dossiers (avec icône si disponible)
        if folder_title_icon:
            # Centrage du titre "Dossiers Favoris"
            folder_label = ctk.CTkLabel(folder_frame, text="Dossiers Favoris", font=ctk.CTkFont(size=16, weight="bold"),
                                        image=folder_title_icon, compound="left", anchor="center") # Modifié ici
        else:
            # Centrage du titre "Dossiers Favoris"
            folder_label = ctk.CTkLabel(folder_frame, text="Dossiers Favoris", font=ctk.CTkFont(size=16, weight="bold"), anchor="center") # Modifié ici
        folder_label.pack(fill="x", pady=(0, 10))

        # Crée un bouton pour chaque dossier favori
        if favorite_folders:
            sorted_folders = sorted(favorite_folders.items()) # Trie les dossiers par nom
            for name, path in sorted_folders:
                create_folder_button(folder_frame, name, path)
        else:
            # Message si aucun dossier n'est présent
            no_folders_label = ctk.CTkLabel(folder_frame, text="Aucun dossier favori ajouté.", text_color="gray")
            no_folders_label.pack(pady=20)
    else:
        # Configuration du bouton de bascule pour afficher "Dossiers" (avec icône)
        if folder_title_icon: # Utilisation de folder_title_icon comme icône pour le bouton "Dossiers"
            toggle_button.configure(text="Dossiers", image=folder_title_icon, compound="left")
        else:
            toggle_button.configure(text="Dossiers", image=None, compound="none") # Réinitialise l'image si non trouvée

        web_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10)) # Affiche le cadre des sites web
        folder_frame.pack_forget() # Cache le cadre des dossiers

        # Ajoute un label de titre pour la section des sites web (avec icône si disponible)
        if web_title_icon:
            # Centrage du titre "Sites Web Favoris"
            web_label = ctk.CTkLabel(web_frame, text="Sites Web Favoris", font=ctk.CTkFont(size=16, weight="bold"),
                                     image=web_title_icon, compound="left", anchor="center") # Modifié ici
        else:
            # Centrage du titre "Sites Web Favoris"
            web_label = ctk.CTkLabel(web_frame, text="Sites Web Favoris", font=ctk.CTkFont(size=16, weight="bold"), anchor="center") # Modifié ici
        web_label.pack(fill="x", pady=(0, 10))

        # Crée un bouton pour chaque site web favori
        if favorite_websites:
            sorted_websites = sorted(favorite_websites.items()) # Trie les sites web par nom
            for name, url in sorted_websites:
                create_website_button(web_frame, name, url)
        else:
            # Message si aucun site web n'est présent
            no_websites_label = ctk.CTkLabel(web_frame, text="Aucun site web favori ajouté.", text_color="gray")
            no_websites_label.pack(pady=20)

# --- Classe pour la boîte de dialogue des paramètres de thème ---
class ThemeSettingsDialog(ctk.CTkToplevel):
    """
    Boîte de dialogue modale pour permettre à l'utilisateur de configurer
    le mode d'apparence (sombre/clair/système) et le thème de couleur.
    """
    def __init__(self, parent, current_appearance_mode, current_color_theme):
        """
        Initialise la boîte de dialogue des paramètres.
        :param parent: La fenêtre parente (l'application principale).
        :param current_appearance_mode: Le mode d'apparence actuel.
        :param current_color_theme: Le thème de couleur actuel.
        """
        super().__init__(parent)
        self.title("Paramètres du Thème")
        self.geometry("300x280")
        self.transient(parent) # Rendre la fenêtre modale par rapport à la parente
        self.grab_set()        # Bloquer les interactions avec la fenêtre parente
        self.resizable(False, False) # Empêcher le redimensionnement
        self.protocol("WM_DELETE_WINDOW", self.on_cancel) # Gérer la fermeture par le bouton X

        self.selected_appearance_mode = current_appearance_mode
        self.selected_color_theme = current_color_theme

        self.create_widgets() # Crée les éléments de l'interface

    def create_widgets(self):
        """Crée et organise les widgets dans la boîte de dialogue des paramètres."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Section pour le mode d'apparence
        mode_label = ctk.CTkLabel(main_frame, text="Mode d'apparence :")
        mode_label.pack(pady=(0, 5), anchor="w")

        self.mode_var = ctk.StringVar(value=self.selected_appearance_mode)
        mode_options = ["dark", "light", "system"]
        for mode in mode_options:
            # Boutons radio pour choisir le mode
            rb = ctk.CTkRadioButton(main_frame, text=mode.capitalize(), variable=self.mode_var, value=mode)
            rb.pack(pady=2, anchor="w")
        
        # Section pour la couleur d'accentuation (thème)
        color_label = ctk.CTkLabel(main_frame, text="Couleur d'accentuation :")
        color_label.pack(pady=(10, 5), anchor="w")

        self.color_combobox = ctk.CTkComboBox(main_frame, values=AVAILABLE_COLOR_THEMES, variable=ctk.StringVar(value=self.selected_color_theme), width=150)
        self.color_combobox.pack(pady=(0, 15), anchor="w")

        # Cadre pour les boutons "Appliquer" et "Annuler"
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=0)

        ok_button = ctk.CTkButton(button_frame, text="Appliquer", command=self.on_apply)
        ok_button.pack(side="left", expand=True, padx=(0, 5))

        cancel_button = ctk.CTkButton(button_frame, text="Annuler", command=self.on_cancel)
        cancel_button.pack(side="right", expand=True, padx=(5, 0))

    def on_apply(self):
        """
        Gère l'action lorsque l'utilisateur clique sur "Appliquer" dans les paramètres de thème.
        Applique les nouveaux paramètres et les sauvegarde.
        """
        new_mode = self.mode_var.get()
        new_color = self.color_combobox.get() # Utiliser .get() sur le combobox

        # Applique le mode d'apparence choisi
        ctk.set_appearance_mode(new_mode)
        # Applique le thème de couleur choisi (toujours un thème intégré)
        ctk.set_default_color_theme(new_color)

        # Met à jour les paramètres de l'application et les sauvegarde
        app_settings["appearance_mode"] = new_mode
        app_settings["color_theme"] = new_color
        save_settings(app_settings)

        # Forcer le rafraîchissement de l'interface pour appliquer les changements de thème
        app.update_idletasks()
        app.update()
        self.destroy() # Ferme la boîte de dialogue

    def on_cancel(self):
        """Gère l'action lorsque l'utilisateur clique sur "Annuler" ou ferme la fenêtre."""
        self.destroy() # Ferme la boîte de dialogue


def open_theme_settings_dialog():
    """Ouvre la boîte de dialogue des paramètres de thème."""
    # Passe les paramètres actuels à la boîte de dialogue pour qu'ils soient pre-sélectionnés
    dialog = ThemeSettingsDialog(app, app_settings["appearance_mode"], app_settings["color_theme"])
    app.wait_window(dialog) # Attend que la boîte de dialogue soit fermée

# --- Nouvelle boîte de dialogue pour choisir le type de favori à ajouter ---
class AddFavoriteChoiceDialog(ctk.CTkToplevel):
    """
    Boîte de dialogue modale pour permettre à l'utilisateur de choisir
    s'il veut ajouter un dossier ou un site web favori.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ajouter un favori")
        self.geometry("280x150")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.choice = None # Stockera True pour dossier, False pour web, None si annulé

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(main_frame, text="Quel type de favori souhaitez-vous ajouter ?")
        label.pack(pady=(0, 15))

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        folder_button = ctk.CTkButton(button_frame, text="Dossier", command=self.choose_folder)
        folder_button.pack(side="left", expand=True, padx=(0, 5))

        web_button = ctk.CTkButton(button_frame, text="Site Web", command=self.choose_website)
        web_button.pack(side="right", expand=True, padx=(5, 0))

    def choose_folder(self):
        self.choice = True
        self.destroy()

    def choose_website(self):
        self.choice = False
        self.destroy()

    def on_cancel(self):
        self.choice = None
        self.destroy()

def open_add_favorite_choice_dialog():
    """Ouvre la boîte de dialogue pour choisir le type de favori à ajouter."""
    dialog = AddFavoriteChoiceDialog(app)
    app.wait_window(dialog)
    if dialog.choice is not None:
        add_favorite_entry(dialog.choice)

# --- Interface principale de l'application ---
app = ctk.CTk() # Crée la fenêtre principale de l'application CustomTkinter
app.title("Fav-Me -- v2.1") # Définit le titre de la fenêtre (mis à jour la version)
app.geometry("400x600") # Définit la taille initiale de la fenêtre
app.minsize(350, 500) # Définit la taille minimale de la fenêtre

# --- Barre supérieure avec boutons de contrôle ---
top_frame = ctk.CTkFrame(app)
top_frame.pack(fill="x", padx=10, pady=5)

# Bouton pour ouvrir les paramètres de thème (avec icône si disponible)
if settings_icon:
    theme_button = ctk.CTkButton(top_frame, text="", image=settings_icon, command=open_theme_settings_dialog, width=40)
    theme_button.pack(side="right", padx=5)
else:
    theme_button = ctk.CTkButton(top_frame, text="Thème", command=open_theme_settings_dialog)
    theme_button.pack(side="right", padx=5)

# Bouton pour basculer entre l'affichage des dossiers et des sites web
# La configuration de l'icône et du texte se fera dans update_view()
toggle_button = ctk.CTkButton(top_frame, text="", command=toggle_view, compound="left")
toggle_button.pack(side="left", padx=5)

# --- Cadre pour le bouton "Ajouter un favori" centré ---
add_button_frame = ctk.CTkFrame(app, fg_color="transparent")
add_button_frame.pack(fill="x", pady=5) # Ajout du cadre et centrage

# Bouton "Ajouter un favori" avec icône et texte, centré
if add_icon:
    add_button = ctk.CTkButton(add_button_frame, text="Ajouter un favori", image=add_icon, compound="left",
                               command=open_add_favorite_choice_dialog)
else:
    add_button = ctk.CTkButton(add_button_frame, text="Ajouter un favori",
                               command=open_add_favorite_choice_dialog)
add_button.pack(expand=True) # Utilise expand=True pour le centrer dans add_button_frame

# --- Section pour les dossiers favoris ---
# Cadre défilant pour contenir les boutons des dossiers
folder_frame = ctk.CTkScrollableFrame(app, label_text="")

# --- Section pour les sites web favoris ---
# Cadre défilant pour contenir les boutons des sites web
web_frame = ctk.CTkScrollableFrame(app, label_text="")

# --- Affichage initial ---
# Variable globale pour savoir quel type de favoris est actuellement affiché
showing_folders = True
update_view() # Appelle la fonction pour afficher les favoris au démarrage

# --- Lancement de l'application ---
app.mainloop()