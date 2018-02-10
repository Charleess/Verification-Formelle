# Exécution symbolique et test structurel

Compte rendu du projet d'Introduction à la Vérification Formelle de P. le Gall, 2018 Centrale Paris.

## Structure du dossier

L'intégralité du code source est contenu dans le dosser `/src/`. Les fichiers `main.py` et `requirements.txt` permettent l'utilisation directe du programme avec la commande suivante:

```bash
$ pip install -r requirements.txt
$ python main.py -h
```

L'invite de commandes donnera les différentes méthodes utilisables directement en CLI.

## Mode d'emploi

Le tester fonctionne avec les flags suivants:

* `-d` ou `--draw-graph` Draw Graph: Dessine le graphe de contrôle associé au programme dans une nouvelle fenêtre

---
Karim Lasri - Charles Férault