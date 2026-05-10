# Velix v1.0.0

Installation rapide:

```bash
pip install .
velix
```

Publication PyPI:

```bash
python -m build
python -m twine upload dist/*
```

# ⚡ Velix — Trouveur de pseudos

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.0-00d4ff?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/python-3.8+-yellow?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/licence-MIT-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/sites-480+-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OS-Linux%20%7C%20Mac%20%7C%20Windows-blue?style=for-the-badge"/>
</p>

> **Velix** cherche un pseudo sur **480+ sites** en quelques secondes et te dit où ce compte existe.

---

## 🖥️ Aperçu

```
██╗   ██╗███████╗██╗     ██╗██╗  ██╗
██║   ██║██╔════╝██║     ██║╚██╗██╔╝
██║   ██║█████╗  ██║     ██║ ╚███╔╝
╚██╗ ██╔╝██╔══╝  ██║     ██║ ██╔██╗
 ╚████╔╝ ███████╗███████╗██║██╔╝ ██╗
  ╚═══╝  ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝

      Trouveur de pseudos v2.1.0
      Fait par Bachir | github.com/bachir
```

---

## 📦 Installation

### 🐧 Linux / 🍎 macOS

```bash
# 1. Clone le projet
git clone https://github.com/bachir/velix.git
cd velix

# 2. Crée l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installe les dépendances
pip install -r requirements.txt

# 4. Lance !
python3 velix.py
```

### 🪟 Windows

```bash
# 1. Clone le projet
git clone https://github.com/bachir/velix.git
cd velix

# 2. Crée l'environnement virtuel
python -m venv venv
venv\Scripts\activate

# 3. Installe les dépendances
pip install -r requirements.txt

# 4. Lance !
python velix.py
```

---

## 🚀 Utilisation

### Lancement simple (menu interactif)
```bash
python3 velix.py
```

### Toutes les commandes disponibles

| Commande | Description |
|---|---|
| `python3 velix.py bachir` | Recherche directe |
| `python3 velix.py bachir --silent` | Afficher seulement les comptes trouvés |
| `python3 velix.py bachir --html` | Exporter un rapport HTML |
| `python3 velix.py bachir --csv` | Exporter en CSV |
| `python3 velix.py bachir --json` | Exporter en JSON |
| `python3 velix.py bachir --browser` | Ouvrir le rapport dans le navigateur |
| `python3 velix.py bachir --variantes` | Tester bachir_, bachir123, b4ch1r... |
| `python3 velix.py bachir --fast` | Mode rapide (timeout 5s, 30 workers) |
| `python3 velix.py bachir --show-http` | Afficher les codes HTTP |
| `python3 velix.py bachir --no-color` | Désactiver les couleurs |
| `python3 velix.py bachir --categorie 2` | Choisir une catégorie directement |
| `python3 velix.py bachir --filter git` | Filtrer les sites par mot-clé |
| `python3 velix.py bachir --exclude tiktok,reddit` | Exclure des sites |
| `python3 velix.py bachir --output ./resultats` | Choisir le dossier de sauvegarde |
| `python3 velix.py bachir --list-sites` | Voir la liste des sites disponibles |
| `python3 velix.py --historique` | Voir l'historique des recherches |
| `python3 velix.py --version` | Afficher la version |
| `python3 velix.py bachir ali mehdi` | Rechercher plusieurs pseudos d'un coup |

---

## 📂 Catégories disponibles

| # | Catégorie | Nb de sites |
|---|---|---|
| 1 | 🌐 Tous les sites | 480+ |
| 2 | 📱 Réseaux sociaux | 39 |
| 3 | 💻 Développement | 60+ |
| 4 | 🎮 Gaming | 46 |
| 5 | 🎵 Musique | 18 |
| 6 | 🎨 Art & Créatif | 39 |
| 7 | 🔐 Cybersécurité | 12 |
| 8 | 🛍️ Shopping & Finance | 19 |
| 9 | ⭐ Top 50 les plus fiables | 50 |

---

## 📁 Structure du projet

```
velix/
├── velix.py          ← Code principal
├── data.json         ← Base de données des 480+ sites
├── requirements.txt  ← Dépendances Python
├── README.md         ← Documentation
├── LICENSE           ← Licence MIT
└── .gitignore        ← Fichiers ignorés par Git
```

---

## ⚙️ Prérequis

- **Python 3.8+**
- Connexion internet
- Les librairies dans `requirements.txt` :
  - `requests` — requêtes HTTP
  - `requests-futures` — requêtes parallèles (rapide)
  - `colorama` — couleurs dans le terminal

---

## 🎨 Résultats

```
  [+] GitHub                           https://github.com/bachir  312ms
  [+] Reddit                           https://reddit.com/u/bachir  520ms
  [-] TikTok                           Non trouvé
  [!] Instagram                        WAF

  ────────────────────────────────────────────────────
  📊 RÉSUMÉ — bachir
  ────────────────────────────────────────────────────
  ✓ Comptes trouvés   : 12
  ✗ Non trouvés       : 430
  ! Bloqués/Timeout   : 8
  ⏱  Durée            : 24.3s
```

---

## ⚠️ Utilisation légale

Velix est un outil **OSINT légal** — il cherche uniquement des informations **publiquement accessibles** sur Internet.

- ✅ Rechercher son propre pseudo
- ✅ Recherches OSINT légitimes
- ❌ Ne pas utiliser pour harceler ou surveiller des personnes sans leur consentement

---

## 📄 Licence

MIT — Libre d'utilisation, de modification et de distribution.

---

## 🤝 Contribuer

Les contributions sont les bienvenues !

1. Fork le projet
2. Crée une branche (`git checkout -b ma-feature`)
3. Commit tes changements (`git commit -m 'Ajout de ma feature'`)
4. Push (`git push origin ma-feature`)
5. Ouvre une Pull Request
