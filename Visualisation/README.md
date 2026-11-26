# carte — Visualisation du TP3 « Vitesse Spatiale » (8INF259 A26)

Affiche en 2D la carte des planètes et, en option :
- le ou les chemins écrits par `?2` et `?3` (fichiers de route) ;
- les secteurs écrits par `!S` (fichier de secteurs) : chaque planète prend la
  couleur de son secteur, les planètes isolées sont en gris.

Le type de chaque fichier est reconnu à son premier mot-clé (`ROUTE` ou `SECTEURS`).
Le programme ne fait aucun calcul : il affiche uniquement le contenu des fichiers
(formats : section 4 de l'énoncé).

Le premier argument est **toujours le fichier de planètes**, suivi des fichiers
de route ou de secteurs (facultatifs). Plusieurs routes peuvent être
superposées ; un seul fichier de secteurs à la fois.
Touches : `N` affiche ou masque les noms des planètes, `Échap` quitte.

Exemples fournis dans `exemples/` : système de 20 planètes en 3 nations
(`Planetes_20_nations.txt`, trajet Delta_1 → Omega_1), produits par la solution
avec le système du lot d'exemples `Exemples/Lot_20`.

Tous les exemples utilisent le vaisseau VITT-MOD-Z150 (capacité 150) :

| Fichier | Contenu |
|---|---|
| `1_court_Z150.txt` | `?2` sans conflit : long détour par l'est (Sigma_3 → Omega_3) |
| `1_cout_Z150.txt` | `?3` sans conflit : quitte le plus court chemin à Sigma_5 (par Omega_4) |
| `1_secteurs_Z150.txt` | `!S` sans conflit : 2 secteurs (Delta_3 isolée) |
| `3_court_Z150.txt` | `?2` après `/ Delta Omega` et `/ Sigma Omega` : aucune route (`CHEMIN 0`) |
| `3_secteurs_Z150.txt` | `!S` après les deux conflits : 3 secteurs (Omega séparée) |

---

## 1. Lancer avec Python

Il faut Python 3 (la version Windows de python.org inclut tkinter). Aucune
autre librairie n'est nécessaire.

```text
python carte.py PLANETES.txt                         (carte seule)
python carte.py PLANETES.txt FICHIER [FICHIER ...]   (routes et/ou secteurs)
```

Exemples, à lancer depuis le dossier `Visualisation` :

```text
python carte.py exemples/Planetes_20_nations.txt
python carte.py exemples/Planetes_20_nations.txt exemples/1_court_Z150.txt exemples/1_cout_Z150.txt
python carte.py exemples/Planetes_20_nations.txt exemples/1_secteurs_Z150.txt exemples/1_court_Z150.txt
python carte.py exemples/Planetes_20_nations.txt exemples/3_secteurs_Z150.txt exemples/3_court_Z150.txt
```

## 2. Transformer le script Python en exécutable

On utilise **PyInstaller**, qui regroupe dans un seul `.exe` le script,
l'interpréteur Python et tkinter.

```text
python -m pip install pyinstaller
python -m PyInstaller --onefile --name carte carte.py
```

- L'exécutable est créé dans `dist/carte.exe` (environ 11 Mo). On peut le
  déplacer où l'on veut.
- Les dossiers `build/`, `dist/` et le fichier `carte.spec` sont des fichiers
  de travail : on peut les supprimer une fois `carte.exe` récupéré.
- L'exécutable est propre à Windows 64 bits ; il faut le reconstruire après
  toute modification de `carte.py`.

## 3. Lancer avec l'exécutable

`carte.exe` fonctionne **sans que Python soit installé**. On l'utilise
exactement comme le script, dans un terminal (invite de commandes ou
PowerShell) :

```text
carte.exe PLANETES.txt                         (carte seule)
carte.exe PLANETES.txt FICHIER [FICHIER ...]   (routes et/ou secteurs)
```

Exemples, depuis le dossier `Visualisation` :

```text
carte.exe exemples\Planetes_20_nations.txt
carte.exe exemples\Planetes_20_nations.txt exemples\1_court_Z150.txt exemples\1_cout_Z150.txt
carte.exe exemples\Planetes_20_nations.txt exemples\1_secteurs_Z150.txt exemples\1_court_Z150.txt
carte.exe exemples\Planetes_20_nations.txt exemples\3_secteurs_Z150.txt exemples\3_court_Z150.txt
```

Remarques :
- Le démarrage prend une ou deux secondes : l'exécutable se décompresse
  d'abord dans un dossier temporaire.
- Une fenêtre de console accompagne la carte : elle affiche les messages
  d'erreur (fichier introuvable, format invalide). On peut l'ignorer.
- Windows SmartScreen ou l'antivirus peut avertir au premier lancement, car
  l'exécutable n'est pas signé : choisir « Informations complémentaires »
  puis « Exécuter quand même ».
- Un double-clic sur `carte.exe` ne suffit pas : il faut lui passer au moins le
  fichier de planètes en argument. Glisser-déposer le seul fichier de planètes
  sur `carte.exe` dans l'Explorateur affiche la carte seule.
