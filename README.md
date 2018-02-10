# Exécution symbolique et test structurel

Compte rendu du projet d'Introduction à la Vérification Formelle de P. le Gall, 2018 Centrale Paris.

## Structure du dossier

L'intégralité du code source est contenu dans le dosser `/src/`. Les fichiers `main.py` et `requirements.txt` permettent l'utilisation directe du programme avec la commande suivante:

```bash
$ pip install -r requirements.txt #Avec PIP
$ conda install --yes --file requirements.txt #Avec Conda
$ python main.py -h #Pour obtenir l'aide
```

L'invite de commandes donnera les différentes méthodes utilisables directement en CLI.

## Mode d'emploi

Le tester fonctionne avec les flags suivants:

* `-d` ou `--draw-graph` Draw Graph: Dessine le graphe de contrôle associé au programme dans une nouvelle fenêtre. Default=False

* `-t` ou `--test` Test: Précise que l'on souhaite tester des critères. Default=False
* `-tc` ou `--criteria` Criteria to test: Précise les critères à tester. Default=ALL
* `-ts` ou `--test-set` Sets of test: Précise les valeurs des tests à exécuter. Le format est une suite de dictionnaires dans des listes. Default=Range(-15, 15)

* `-g` ou `--generate` Generate Tests: Précise que l'on souhaite générer des sets de test. Default=False
* `-gc` ou `--generate-criteria` Generate Criteria: Précise les critères pour lesquels on veut générer des tests. Default=ALL
* `-gr` ou `--generate-range` Generate Range: Précise le domaine de recherche pour la génération des tests. Default=15

**Exemples**:

Tester les critères `TA` et `TD` pour x valant -1, 2 ou 5

```bash
$ python main.py -t -tc TA TD -ts "{'x': -1}" "{'x': 2}" "{'x': 5}"
```

Générer des jeux de critère pour `i-TB` et `TDef` en cherchant dans un espace de [-20, 20]
```bash
$ python main.py -g -gc i-TB TDef -gr 20
```

Il est bien entendu possible de mixer tests et génération.

---
Karim Lasri - Charles Férault