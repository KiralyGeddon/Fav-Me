# Fav-Me ✨ - Votre Gestionnaire de Favoris Personnel

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![PyInstaller](https://img.shields.io/badge/Packaging-PyInstaller-orange.svg)
![Installer](https://img.shields.io/badge/Installer-InnoSetup-lightgrey.svg)
![License](https://img.shields.io/badge/License-No%20License-red.svg)

Bienvenue sur **Fav-Me**, votre application de bureau intuitive pour gérer et accéder rapidement à vos dossiers et sites web favoris. Fini les recherches fastidieuses ! Organisez tout en un seul endroit pratique et stylé.

## 🚀 Table des Matières

-   [Fav-Me ✨ - Votre Gestionnaire de Favoris Personnel](#fav-me---votre-gestionnaire-de-favoris-personnel)
-   [🚀 Table des Matières](#-table-des-matières)
-   [🌟 À Propos de Fav-Me](#-à-propos-de-fav-me)
-   [💡 Fonctionnalités Clés](#-fonctionnalités-clés)
-   [📸 Aperçu](#-aperçu)
-   [📦 Technologies Utilisées](#-technologies-utilisées)
-   [🚀 Démarrage Rapide](#-démarrage-rapide)
    -   [Prérequis](#prérequis)
    -   [Installation](#installation)
    -   [Exécuter le Script Python](#exécuter-le-script-python)
    -   [Construire l'Exécutable (.exe) avec PyInstaller](#construire-lexécutable-exe-avec-pyinstaller)
-   [📦 Versions Distribuées](#-versions-distribuées)
    -   [Exécutable Autonome](#exécutable-autonome)
    -   [Installateur Windows (Inno Setup)](#installateur-windows-inno-setup)
-   [🖥️ Utilisation](#️-utilisation)
-   [🗂️ Stockage des Données et Paramètres](#️-stockage-des-données-et-paramètres)
-   [🤝 Contribution](#-contribution)
-   [✉️ Contact](#️-contact)


## 🌟 À Propos de Fav-Me

**Fav-Me** est une application de bureau légère et élégante conçue pour simplifier votre navigation quotidienne. Que ce soit pour accéder rapidement à un dossier de projet fréquemment utilisé ou pour lancer votre site web préféré, Fav-Me met tout à portée de main.

Construite avec `CustomTkinter` pour une interface utilisateur moderne et personnalisable, elle offre une expérience fluide et agréable. Vos favoris et vos préférences de thème sont sauvegardés automatiquement, pour que vous retrouviez votre environnement de travail exactement comme vous l'avez laissé.

## 💡 Fonctionnalités Clés

* **📁 Gestion des Dossiers Favoris :**
    * Ajoutez n'importe quel dossier de votre système de fichiers.
    * Ouvrez les dossiers directement via l'explorateur (Windows) ou le Finder (macOS).
    * Modifiez facilement le nom ou le chemin d'un dossier existant.
    * Supprimez les dossiers devenus obsolètes.
    * Vérification automatique de l'existence des chemins de dossiers au démarrage.

* **🌐 Gestion des Sites Web Favoris :**
    * Enregistrez vos URLs préférées.
    * Ouvrez les sites web dans votre navigateur par défaut.
    * **Récupération automatique des Favicons** : L'application tente de télécharger et d'afficher l'icône de chaque site web pour une identification visuelle rapide.
    * Modifiez l'URL ou le nom d'un site web.
    * Supprimez les sites web de votre liste.

* **🔄 Bascule Rapide :**
    * Passez instantanément de la vue des dossiers à la vue des sites web grâce à un bouton dédié.

* **🎨 Thèmes Personnalisables :**
    * Choisissez entre les modes d'apparence **Sombre**, **Clair** ou **Système**.
    * Sélectionnez votre couleur d'accentuation préférée parmi les thèmes CustomTkinter disponibles (`blue`, `green`, `dark-blue`).

* **💾 Persistance des Données :**
    * Tous vos favoris et vos paramètres de thème sont automatiquement sauvegardés dans des fichiers JSON.

* **✨ Interface Intuitive :**
    * Design épuré et facile à utiliser grâce à CustomTkinter.
    * Icônes dédiées pour chaque action (ajouter, modifier, supprimer, paramètres).

## 📸 Aperçu

## 📸 Aperçu

* **Écran principal - Vue Dossiers :**
    ![Favoris Dossiers](https://github.com/KiralyGeddon/Fav-Me/blob/main/images/1.png)
   
* **Écran principal - Vue Sites Web (avec favicons) :**
    ![Favoris Websites](https://github.com/KiralyGeddon/Fav-Me/blob/main/images/2.png)
   
* **Fenêtre d'ajout/édition de favori :**
    ![Ajout de Favori](https://github.com/KiralyGeddon/Fav-Me/blob/main/images/3.png)
   
    ![Ajout de Dossier Favori](https://github.com/KiralyGeddon/Fav-Me/blob/main/images/4.png)

    ![Ajout de Site Web Favori](https://github.com/KiralyGeddon/Fav-Me/blob/main/images/5.png)

* **Fenêtre des paramètres de thème :**
    ![Theme Settings](https://github.com/KiralyGeddon/Fav-Me/blob/main/images/6.png)
    
* **Mode Clair :**
    ![Light Mode](https://github.com/KiralyGeddon/Fav-Me/blob/main/images/7.png)


## 📦 Technologies Utilisées

* **[Python](https://www.python.org/)** - Langage de programmation
* **[CustomTkinter](https://customtkinter.tomsons.de/)** - Bibliothèque GUI moderne pour Tkinter
* **[Pillow (PIL Fork)](https://python-pillow.org/)** - Pour le traitement des images (icônes, favicons)
* **[Requests](https://requests.readthedocs.io/en/latest/)** - Pour les requêtes HTTP (téléchargement des favicons)
* **[PyInstaller](https://pyinstaller.org/en/stable/)** - Pour compiler l'application en exécutable autonome
* **[Inno Setup](https://jrsoftware.org/isinfo.php)** - Pour créer un installateur Windows convivial

## 🚀 Démarrage Rapide

Suivez ces étapes pour faire fonctionner Fav-Me sur votre machine locale.

### Prérequis

Assurez-vous d'avoir Python 3.x installé sur votre système.

### Installation

1.  **Clonez le dépôt** (ou téléchargez le fichier `fav-v2.1.py` et les icônes) :
    ```bash
    git clone [https://github.com/KiralyGeddon/Fav-Me](https://github.com/KiralyGeddon/Fav-Me)
    cd Fav-Me/script # Accédez au répertoire du projet
    ```

2.  **Installez les dépendances Python :**
    ```bash
    pip install customtkinter Pillow requests
    ```

### Exécuter le Script Python

Pour lancer l'application directement depuis le script Python :

```bash
python fav-v2.1.py


