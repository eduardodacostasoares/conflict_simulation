<p align="center">
  <img src="assets/header.png" alt="Team Sprint Demo — Médiation de conflit" width="100%">
</p>

<h1 align="center">Conflict Simulation</h1>

<p align="center">
  Un jeu interactif où <strong>vous êtes le médiateur</strong> d'un conflit en milieu de travail.
</p>

<p align="center">
  <a href="README.md">English</a> · <strong>Français</strong> · <a href="README.pt-BR.md">Português</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="Streamlit" src="https://img.shields.io/badge/built%20with-Streamlit-FF4B4B">
</p>

---

## Table des matières

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Comment jouer](#comment-jouer)
- [Démarrage](#démarrage)
- [Structure du projet](#structure-du-projet)
- [Créer votre propre scénario](#créer-votre-propre-scénario)
- [Contribuer](#contribuer)
- [Licence](#licence)
- [Auteur](#auteur)

## À propos

**Conflict Simulation** est un petit jeu de rôle qui s'exécute dans le navigateur, développé avec [Streamlit](https://streamlit.io/). Il vous place au cœur d'une discussion tendue entre deux collègues et vous demande d'apaiser la situation, un message à la fois.

Le scénario inclus, **« Demo Deadline Conflict »** (conflit autour de l'échéance d'une démo), se déroule le jour d'une démonstration devant les parties prenantes :

- **Alex** a promis une démo du tableau de bord pour aujourd'hui et se sent pris au dépourvu.
- **Sam** refuse de livrer quelque chose de défectueux après que les exigences ont changé trois fois.

Votre rôle est de les amener vers un plan commun et réaliste, sans prendre parti. C'est une façon simple de pratiquer la médiation et la communication : écoute active, reformulation, entente sur la portée du travail et établissement de règles de collaboration claires.

> **Remarque :** l'interface et les dialogues du jeu sont actuellement en anglais.

## Fonctionnalités

- 🎭 **Choix de médiation à embranchements** — trois réponses possibles à chaque tour, chacune avec un impact différent.
- 📊 **Indicateurs en temps réel** — suivez l'évolution de la tension et de la confiance de chaque personne envers vous après chaque décision.
- 💬 **Transcription de style messagerie** — toute la conversation s'affiche avec les avatars d'Alex, de Sam et le vôtre.
- 🏁 **Conditions de victoire et de défaite** — désamorcez le conflit… ou regardez-le dégénérer.
- 🔄 **Boutons Recommencer et Terminer** — rejouez pour tester d'autres stratégies.
- 🧩 **Scénario piloté par les données** — dialogues, pointage et règles se trouvent dans un seul dictionnaire Python : vous pouvez écrire votre propre scénario sans toucher à la logique du jeu.

## Comment jouer

1. Lisez ce que disent Alex et Sam au tour actuel.
2. Choisissez l'un des trois messages de médiation (**A**, **B** ou **C**).
3. Votre choix met à jour les indicateurs, puis le tour suivant commence.

Le jeu compte **8 tours** au total. Chaque choix est évalué en arrière-plan :

| Qualité du choix | Tension | Confiance (Alex) | Confiance (Sam) |
|------------------|:-------:|:----------------:|:---------------:|
| Meilleur         | −15     | +10              | +10             |
| Moyen            | −5      | +3               | +3              |
| Mauvais          | +10     | −5               | −5              |

Vous commencez avec une **tension de 50** et une **confiance de 55** pour chaque personne. Toutes les valeurs restent entre 0 et 100.

L'état de la partie est vérifié après chaque choix :

- ✅ **Vous gagnez** lorsque la tension est **inférieure ou égale à 20** et que la confiance d'Alex **et** de Sam est **supérieure ou égale à 70**.
- ❌ **Vous perdez** lorsque la tension atteint **85 ou plus**, ou que la confiance de **l'une ou l'autre** personne tombe à **20 ou moins**.
- Si aucune de ces situations ne se produit, la partie se termine après le dernier tour et affiche vos statistiques finales.

> **Astuce :** les bonnes réponses de médiation restent généralement neutres, clarifient ce dont chaque personne a réellement besoin et transforment la discussion en ententes concrètes et partagées.

## Démarrage

### Prérequis

- [Python](https://www.python.org/downloads/) 3.9 ou plus récent
- `pip`

### Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/eduardodacostasoares/conflict_simulation.git
cd conflict_simulation

# 2. (Facultatif) Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate        # Sous Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

### Lancer l'application

```bash
streamlit run app.py
```

Streamlit ouvrira le jeu dans votre navigateur, généralement à l'adresse <http://localhost:8501>.

> **Remarque :** lancez la commande depuis le dossier racine du projet — l'application charge ses images depuis le dossier `assets/` à l'aide de chemins relatifs.
>
> Si vous obtenez une erreur mentionnant `chat_message` ou `use_container_width`, votre version de Streamlit est trop ancienne. Mettez-la à jour avec `pip install --upgrade streamlit`.

## Structure du projet

```
conflict_simulation/
├── app.py              # Application Streamlit : données du scénario, logique du jeu et interface
├── requirements.txt    # Dépendances Python
└── assets/             # Images utilisées par l'application
    ├── header.png      # Bannière affichée en haut de la page
    ├── alex.png        # Avatar d'Alex
    ├── sam.png         # Avatar de Sam
    ├── mediator.png    # Votre avatar (le médiateur)
    └── good.png
```

## Créer votre propre scénario

Tout le contenu du jeu est défini dans le dictionnaire `SCENARIO`, au début du fichier `app.py` :

| Clé              | Ce qu'elle contrôle                                                          |
|------------------|------------------------------------------------------------------------------|
| `title`          | Titre de la page, affiché dans le navigateur et en haut de l'application     |
| `initial_state`  | Valeurs de départ de la tension et de la confiance                           |
| `scoring`        | Effet de chaque niveau (`best`, `medium`, `bad`) sur les indicateurs         |
| `end_conditions` | Seuils de victoire et de défaite                                             |
| `turns`          | La liste des tours : ce que disent Alex et Sam, et les trois choix proposés  |

Chaque tour suit cette structure :

```python
{
    "alex": "Ce que dit Alex à ce tour.",
    "sam": "Ce que dit Sam à ce tour.",
    "choices": [
        {"id": "A", "text": "Un message de médiation.", "grade": "best"},
        {"id": "B", "text": "Une autre option.",        "grade": "medium"},
        {"id": "C", "text": "Une mauvaise option.",     "grade": "bad"},
    ],
},
```

Modifiez les dialogues, ajoutez ou retirez des tours, ou ajustez le pointage et les seuils pour créer un nouveau défi. Pour changer l'apparence des personnages, remplacez les images du dossier `assets/`.

## Contribuer

Les contributions, les idées et les nouveaux scénarios sont les bienvenus !

1. Faites un fork du dépôt.
2. Créez une branche pour votre modification : `git checkout -b mon-nouveau-scenario`
3. Validez vos changements : `git commit -m "Ajout d'un nouveau scénario"`
4. Poussez la branche : `git push origin mon-nouveau-scenario`
5. Ouvrez une pull request.

Vous avez trouvé un bogue ou avez une suggestion ? [Ouvrez une issue](https://github.com/eduardodacostasoares/conflict_simulation/issues).

## Licence

Aucune licence n'a encore été définie pour ce projet. Tant qu'aucune licence n'est ajoutée, tous les droits sont réservés à l'auteur. Veuillez communiquer avec l'auteur avant de réutiliser le code.

## Auteur

**Eduardo da Costa Soares** — [@eduardodacostasoares](https://github.com/eduardodacostasoares)

Si le projet vous a plu, pensez à lui donner une ⭐ sur GitHub !
