# Exécution symbolique et test structurel

Compte rendu du projet d'Introduction à la Vérification Formelle de P. le Gall, 2018 Centrale Paris.

## Structure du dossier

L'intégralité du code source est contenu dans le dosser `/src/`. Les fichiers `main.py` et `requirements.txt` permettent l'utilisation directe du programme avec la commande suivante:

```bash
$ pip install -r requirements.txt
$ python main.py -ra
```

## Mode d'emploi

Le tester fonctionne avec les flags suivants:

* `-ra` Run All: Run all the tests on predefined test sets. This can be useful to test the integrity of the tester

---
Karim Lasri - Charles Férault