A partir du code source, on construit un AST, parsable par l'ordinateur. L'AST est déjà un graphe avec des règles.
On le construit récursivement. 
Le CFG est une autre représentation de l'AST. C'est juste une représentation plus simple pour un programme.
Les numéros des bulles dans le graphe sont grosso modo les lignes dans le code. 
Permet de trouver des erreurs sans exécuter le programme. Par exemple, on peut maintenir une liste des variables définies à un certain moment et trouver des chemins sur le graphe où certaines variables ne sont pas définies quand on arrive à la fin.

Dans le projet on va partir directement du CFG. Il va nous servir à:
1. On se donne un CFG, des critères (propriétés sur le graphe) de tests et des tests. Un test est un dictionnaire variables/valeurs. 

Exemple: "Est-ce qu'on est passé par tous les noeuds assignation ?".

Il faut maintenir en permanence l'endroit où on est dans le CFG et l'état courant. A la fin du test, on donne le chemin qui a été parcouru. Un test est donc un jeu de données, et on l'éxécute en regardant les points qu'on a parcouru. 

Exemple du "Toutes les assignations": On va créer une liste avec tous les sommets par lesquels il faut qu'on passe, et on va faire tourner des tests. A chaque test, on enlève les sommets par lesquels on est passé de la liste. Le but du jeu est d'arriver à une liste vide.

Etapes:
- On prend un jeu de variables assignées
- On exécute le programme
- On regarde ce qui se passe

Deuxième partie du tp, on veut générer un jeu de test qui fait passer un critère. On prend chaque élément de la liste de noeuds par lesquels on veut passer, et on cherche un chemin qui marche. Ca devient tricky lorsque on les enchaîne. Le but est donc de générer automatiquement les contraintes que l'on veut utiliser.



On précise la variable qu'on va utiliser