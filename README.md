# Vérification Formelle

## Introduction

Implémentation d'un model-checker pour différents critères et différents tests sur la base d'un graphe de contrôle. Les graphes sont représentés par des instances de `networkx`

```bash
> conda install --yes --file requirements.txt
```

## Programmes

### Prog 1

```python
if x <= 0:
    x = - x
else:
    x = 1 - x

if x >= 1:
    while x < 3:
        x = x + 1
else:
    x = x + 1
```

Pour des raisons de simplification, nous avons parfois ajouté des bouts de code spécifiques à ce programme, notamment pour retirer des chemins impossibles mathématiquement. Ces morceaux sont clairement précisés dans le code, et ne sont pas réplicables à d'autres programmes.

## Partis pris d'implémentation

### Structure du graphe de contrôle

Les graphes de contôle sont implémentés comme des instances de `networkX`, une bibliothèque de graphes pour python. Les différentes informations seront portées par les arêtes, les noeuds n'ayant qu'un identifiant. Chaque arête est de la forme suivante:

```python
""" Arête de décision """
G.add_edge(
    1, # Noeud de départ
    2, # Noeud d'arrivée
    dec=( # Décision
        [ # Liste des conditions
            lambda dic: dic['x'] <= 0
        ],
        lambda a: a # Fonction logique de lien entre les conditions élémentaires
    ),
    cmd=lambda dic: None, # Commande
    cmd_type='if' # Type de commande => Décision
)

""" Arête d'assignation """
G.add_edge(
    2, # Noeud de départ
    4, # Noeud d'arrivée
    dec=( # Décision
        [], # Aucune décision à prendre
        lambda a: True # Fonction vide
    ),
    cmd=lambda dic: dic.update(
        {'x': - dic['x']} # Assignation à la variable 'x'
    ),
    cmd_type='assign' # Type de commande => Asignation
)
```

### Simplifications

* Nous avons choisi de laisser de côté le développement d'un algorithme capable de lire directement un programme écrit en python, d'en calculer l'AST et d'en déduire le graphe de contrôle. Nous partirons directement d'un CFG écrit sous la forme d'une instance de graphe `networkX`.

### Fonctions de parcours et Helpers

Nous avons défini séparément des fonctions redondantes dans notre projet, elles sont toutes situées dans le fichier `common.py`.

#### Subfinder

Cette fonction nous permet de trouver un motif dans une liste. Elle est utilisée lors du traitement des boucles par exemple, pour trouver rapidement les motifs qui se répètent, ou pour identifier su une arête à été utilisée dans un chemin.

#### Shallow Copy

Python travaille par référence dans certains cas, ce qui nécéssite de devoir créer des copies séparée d'objets. Cans certains cas, le module `copy` ne suffit pas, par exemple pour une liste dans un dictionnaire. Si on copie le dictionnaire avec la fonction `copy`, alors un `list.append()` sur la copie agira quand même sur la fonction originale. Pour pallier à ce problème, on implémente la copie propre d'un dictionnaire.

#### Find Vars, Def et Ref

Ces trois fonctions sont au coeur de certains critères. La première est un parser permettant de récupérer le code source des fonctions lambda que l'on utilise dans le CFG, et d'en sortir les informations sur les variables référencées ou définies dans ces fonctions. Pour ce faire, on lit le code source et on extrait les informations avec des expressions régulières.

Def et Ref sont un sucr syntaxique pour accéder plus rapidement aux informations que l'on désire.

#### Loops et Paths

On dispose ensuite d'un ensemble de fonctions pour aider dans l'analyse des boucles et des chemins

* **Compute All Loops :** Cherche toutes les boucles simples présentes dans un graphe. Retourne une liste des chemins correspondants.
* **Is I Loop :** Utilise le détecteur de motifs pour chercher si `i` itérations d'un boucle spécifiée sont présentes dans un chemin passé en argument.
* **Compute All Paths :** Fonction récursive prenant en argument une limite et calculant en BFS tous les chemins de longueur inférieure à la limite, boucles comprises
* **Simple Paths :** Utilise les fonctions précédentes pour retourner une liste de tous les chemins simples, c'est à dire comportant au maximum une itération de chaque boucle.

#### Conditions et Décisions

**Decision :** Exécute une décision contenue dans une arête avec les données contenues dans le dictionnaire passé en argument. Retourne un booléen corespondant à l'application de la fonction d'évaluation aux résultats des différentes conditions.

**Conditions :** Retourne une liste contenant le résultat de l'évaluation de chaque condition avec les données passées en argument.

#### Browsers

Les dernières fonctions sont les deux algorithmes de parcours de graphe que nous utilisons pour calculer les chemins empruntés par le programme lors de l'évaluation d'une donnée de test. Le premier fait un parcours simple, et stocke à chaque fois le noeud par lequel il est passé dans une liste retournée à la fin. Le second est légèrement plus lent, et maintient un dictionnaire contenant les noeuds qui ont été traversé, et pour chaque noeud, une liste des valeurs de toutes les variables en sortant du noeud.

## Critères

### (TA) Toutes les affectations

Un jeu de test T pour Prog satisfait le critère "toutes les affectations", dénoté TA, si toutes les étiquettes de Labels(Prog,assign) apparaissent au moins une fois dans l’un des chemins d’exécution associés aux données de test σ de T.

#### Notre implémentation TA

L'idée est de passer par chaque arête d'affectation au moins une fois avec le jeu de test.

Nous avons cherché, parmi les arêtes du graphe, lesquelles étaient étiquetées "assign", puis nous avons généré les chemins induits par chaque ensemble de valeurs initiales du jeu de test, et nous avons cherché les arêtes dans les chemins générés.

*Pourcentage de couverture :* Le pourcentage de couverture de ce test est la proportion d'arêtes d'affectation effectivement empruntées.

### (TD) Toutes les décisions

Un jeu de test T pour Prog satisfait le critère "toutes les décisions", dénoté TD, si toutes les arêtes (u, v) avec Label(u) ∈ Labels(Prog, {if, while}) sont empruntées au moins une fois dans l’un des chemins d’exécution associés aux données de test σ de T.

#### Notre implémentation TD

L'idée est de parcourir le graphe à la recherche d'arêtes de décision. 

La décision est le résultat de l'évaluation logique des différentes conditions contenues sur l'arête. On peut donc montrer que dans un graphe de contrôle, deux arêtes de décision partant du même noeud sont forcément antinomiques l'une de l'autre. ainsi, le critère "Toutes les décision" peut se ramener à "Pour chaque arête de décision, il existe au moins un chemin de test qui passe par cette arête.

On parcourt donc cotre graphe en stockant les arêtes portant une condition, on génère l'ensemble des chenins pour nos tests. Il suffit alors de chercher dans les chemins si on a effectivement toutes les arêtes de décision.

*Pourcentage de couverture :* Le pourcentage de couverture de ce test est la proportion d'arêtes de décision effectivement empruntées.

### (k-TC) Tous les k-Chemins

Un jeu de test T pour Prog satisfait le critère "tous les k- chemins", dénoté k-TC, si pour tous les chemins
ρ de Prog de longueur inférieure ou égale à k, il existe une donnée de test σ de T vérifiant path(Prog, σ) = ρ.

> Pour procéder, nous avons défini une fonction récursive permettant de calculer les chemins de longueur inférieure ou égale à k, et nous avons comparé ces chemins à ceux générés par le jeu de test.

#### Notre implémentation k-TC

L'idée est de générer tous les chemins possibles de longueur inférieure ou égale à k, et de vérifier que les chemins du jeu de test incluent bien ces chemins.

Nous avons défini une fonction récursive qui ajoute au noeud courant les chemins de longueur inférieure ou égale à k-1 de chacun de ses successeurs.

*Pourcentage de couverture :* Le pourcentage de couverture de ce test est la proportion de chemins de longueur inférieure ou égale à k ayant été parcourus par rapport au nombre total de ces chemins.


### (i-TB) Toutes les i-boucles

Un jeu de test T pour Prog satisfait le critère "toutes les i-boucles", dénoté i-TB, avec i ∈ N si pour tous les chemins ρ pour lesquels les boucles while sont exécutées au plus i fois, il existe une donnée de test σ de T vérifiant path(Prog, σ) = ρ.

> Pour des raisons de simplicité, on utilisera la fonction `simple_loops` de NetworkX, une implémentation d'une fonction similaire ayant déjà été faite dans le projet, et le temps étant plutôt rare.
> Ce critère contient certaines implémentations spécifiques au programme utilisé. Nous avons mis *en dur* certaines modifications à apporter aux chemins possibles pour retirer ceux qui sont mathématiquement impossibles.
> Nous n'avons pas tenu compte des boucles imbriquées pour des raisons de temps.

#### Notre implémentation i-TB

L'idée de ce test sera de générer tous les chemins possibles allant de l'entrée à la sortie -- c'est à dire représentant bien un exécution du programme -- et de vérifier que les chemins de test incluent bien ces chemins.

On calcule donc la taille maximale d'un graphe comportant des i-boucles, et on utilise ce résultat comme borne supérieure pour notre générateur de chemin. On retire ensuite les chemins mathématiquement impossibles, non représentatifs pour le test, et on génère les chemins de test pour comparer.

*Pourcentage de couverture :* Le pourcentage de couverture de ce test est la proportion de chemins ayant été parcourus par rapport au nombre de chemins théoriques à parcourir.

### (TDef) Toutes les définitions

Un jeu de test T pour Prog satisfait le critère "toutes les définitions", dénoté TDef, si pour toutes les variables X de Prog, pour tous les nœuds u de GC(Prog) avec def(u) = {X}, il existe un chemin ρ de la forme μ1.lu.μ2.l′.μ3 avec l = Label(u), X ∈ ref(l′) et ∀l ∈ Labels(μ), X ̸∈ ref(l) pour lequel il existe une donnée de test σ de T vérifiant path(Prog, σ) = ρ.

> Dans la pratique, on ne peut garantir que ce critère soit rempli à 100% pour certains programmes. En effet, il peut y avoir des assignations sur les dernières arêtes, comme dans le programme donné à titre d'exemple. On ne peut pas donc utiliser ces assignations puisque elles donnent directement sur le noeud final. On acceptera donc une valeur de `75%` pour ce critère.

#### Notre implémentation TDef

On commence par chercher dans le graphe tous les noeuds qui définissent une variable. Pour cela, nous avons implémenté une méthode Def retournant les variables définies en une arête. Ensuite, nous cherchons dans les chemins générés par le jeu de test les noeuds précédents. Lorsque nous en trouvons un, nous cherchons dans la suite du chemin un noeud qui référence la variable. Lorsque nous trouvons un tel noeud, nous retirons le noeud de définition de l'ensemble à couvrir.

Remarque : Notons qu'un noeud ne peut définir qu'une seule variable. Ainsi, même si la formulation de l'énoncé est sous la forme "pour toutes les variables X de Prog, pour tous les nœuds u de GC(Prog) avec def(u) = {X}", il est équivalent d'itérer d'abord sur tous les noeuds u de CG(Prog) avec def(u) non vide puis sur les variables (en l'occurence la variable) définies en ce noeud. En fait, il y a une bijection entre l'ensemble des couples (variable définie, noeud définissant la variable) et (noeud définissant une variable, variable qu'il définit), puisqu'il suffit de permuter les deux éléments. Cet ordre sera également utilisé dans les critères suivants.

*Pourcentage de couverture :* Le pourcentage de couverture de ce test est la proportion d'arêtes ayant défini une variable dont au moins un chemin de test passe par cette arête et utilise cette variable, par rapport au nombre d'arêtes définissant une variable.

### (TU) Toutes les utilisations

Un jeu de test T pour Prog satisfait le critère "toutes les utilisations", dénoté TU, si pour toutes les variables X de Prog, pour tous les nœuds u de CG(Prog) avec def(u) = {X}, pour tous les nœudes v CG(Prog) avec X ∈ ref(v) tel qu’il existe un chemin partiel μ de u à v, sans redéfinition de X, c’est-à-dire vérifiant ∀l ∈ Labels(μ), X ̸∈ ref(l), il existe un chemin ρ de la forme μ1.lu.μ2.l′.μ3 avec lu = Label(u) et lv = Label(v), et ∀l ∈ Labels(μ2), X ̸∈ ref(l). pour lequel il existe une donnée de test σ de T vérifiant path(P rog, σ) = ρ.

> L'idée est de générer tous les chemins possibles entre tous les couples de noeuds dont le premier définit une variable et dont le deuxième la référence sans redéfinition. On génère ensuite les chemins des tests, et on vérifie que pour chaque couple, au moins un des chemins généré est emprunté.

#### Notre implémentation TU

On commence par récupérer tous les noeuds qui définissent des variables, et tous les noeuds qui en référencent. On itère ensuite sur tous les noeuds de définition, et on cherche tous les noeuds suivants qui référencent les variables définies. On calcule ensuite tous les chemins simples -- c'est à dire sans boucles -- entre ces couples de points. Si on croise un noeud qui redéfinit la variable entre temps, on retire le chemin de la liste.

Après avoir exécuté cet algorithme sur tous les noeuds de définition, on obtient une liste comprenant tout les chemins entre deux noeuds. On stocke cette information sous la force d'une liste indexée par le noeud de départ et le noeud d'arrivée, de cette façon, on a tous les chemins possibles entre deux noeuds, sans redéfinition, et pratique à utiliser. Il suffit maintenant de générer tous les chemins découlant de nos tests, et de vérifier si on retrouve bien au moins un des chemins de nos listes, ceci pour chaque liste. *In fine*, si pour chaque liste on retrouve au moins un des chemins dans un des tests, alors le critère est satisfait.

**NB:** Ce critère ne peut pas être satisfait à 100% de part sa définition. En effet, un programme termine forcément par une assignation dans une des arêtes. Ainsi, cette assignation n'a pas de noeud fils, et ne pourra jamais être utilisée. C'est pourquoi dans notre cas, le test termine avec une couverture de 75%, car le noeud 6 donne directement sur le noeud 8, qui n'a pas d'enfants puisque il est la fin du programme.

*Pourcentage de couverture :* L'ensemble à couvrir ici est l'ensemble des couples d'arêtes u où u définit une variable. Pour chacune de ces arêtes, le test de couverture porte sur les arêtes v utilisant la variable sans redéfinition préalable. Le pourcentage de couverture de ce test est la proportion de arêtes de définition qui sont couvertes par un des chemins de test, au sens du critère précédent.

### (TDU) Tous les DU-chemins

Pour deux nœuds u et v, on appelle chemin simple partiel de u à v un chemin u.μ.v de u à v qui passe au plus une fois dans chacune des boucles intermédiaires.

Un jeu de test T pour Prog satisfait le critère "tous les DU-chemins", dénoté TDU, si pour toutes les variables X de Prog, pour tous les nœuds u de CG(Prog) avec def(u) = {X}, pour tous les nœuds v CG(Prog) avec X ∈ ref(v), pour tous les chemins simples partiels μ de u à v, sans redéfinition de X, c’est- à-dire vérifiant ∀l ∈ Labels(μ), X ̸∈ ref(l), il existe un chemin ρ de la forme μ1.lu.μ.l′.μ3 avec lu = Label(u) et lv = Label(v), il existe une donnée de test σ de T vérifiant path(P rog, σ) = ρ.

> L'idée est la même que pour le critère TU, à la différence que cette fois, pour un couple de noeuds (définition et première utilisation après cette définition), on vérifie que tous les chemins possibles sont couverts par les chemins de test.

#### Notre implémentation TDU

L'implémentation est très similaire à la précédente, mais elle a cela de différent que, au lieu de tester des couples d'arêtes u, v, on teste pour ces couples chaque chemin simple reliant u à v sans redéfinition.

Le test est le même que précédemment, nous stockons pour chaque arête de définition, toutes les premières arêtes d'utilisation et une liste de chemins simples les reliant. Si on retrouve tous ces chemins simples pour toutes les arêtes d'utilisation dans les chemins de test, nous retirons l'arête de définition des arêtes à couvrir.

*Pourcentage de couverture :* Le pourcentage de couverture de ce test est la proportion de noeuds de définition qui n'ont pas été évaluées à vrai et à faux au moins une fois.

### (TC) Toutes les conditions

Les expressions booléennes utilisées dans les instructions "if" ou "while" sont appelées des décisions. Ces décisions peuvent être décomposées en expressions élémentaires, appelées conditions. Par exemple, la décision
(X ≤0)∧(X =Y +1) est constituée des deux conditions (X ≤ 0) et (X = Y + 1).

Un jeu de test T pour P rog satisfait le critère "toutes conditions", dénoté TC, si pour toutes les conditions c de Prog, il existe une donnée de tests σc qui exécute c à vrai, et une donnée de tests σ¬c qui exécute c à faux.

#### Notre implémentation TC

Ce critère est une version plus complexe du critère TD. Au lieu de regarder simplement si la décision totale est bien empruntée dans les deux cas `True` et `False`, on va décomposer les décisions en conditions élémentaires, et vérifier que chacune de ces conditions est bien évaluée une fois à `True` et une fois à `False`.

Notre graphe de contrôle stocke les décisions sous la forme d'une liste de conditions, ainsi qu'une fonction faisant le lien entre ces différentes conditions. L'idée sera donc de récupérer l'ensemble des arêtes de condition, et d'extraire de ces arêtes les conditions à tester.

L'étape de parcours du graphe avec des tests est légèrement différente pour ce critère, en effet, il ne faut pas stocker uniquement le chemin que l'on a emprunté, mais aussi les valeurs des différentes variables à chaque étape. On va donc changer notre parcours, et au lieu de renvoyer une liste des noeuds par lesquels on est passé, on va renvoyé un dictionnaire avec en clé les noeuds, et en valeur une liste des valeurs des variables lorsque on est passé par ce noeud. Notons qu'on peut passer plusiseurs fois par le même noeud avec des valeurs différentes.

Pour chaque condition, on va alors regarder dans le résultat du parcours de graphe si on l'a évalué à vrai et à faux au moins une fois. Le cas échéant, on la retire des conditions à tester pour les étapes suivantes.

*Pourcentage de couverture :* Le pourcentage de couverture de ce test est la proportion de conditions à tester qui n'ont pas été évaluées à vrai et à faux au moins une fois.

## Relations entre les critères

Le critère "tous les DU-chemins" est plus fort que le critère "toutes les utilisations", qui lui même serait plus fort que le critère "toutes les définitions" si sa formulation était la suivante :
"Un jeu de test T pour Prog satisfait le critère "toutes les définitions", dénoté TDef, si pour toutes les variables X de Prog, pour tous les nœuds u de CG(Prog) avec def(u) = {X}, tels qu'il existe un nœuds v CG(Prog) avec X ∈ ref(v) sans redéfinition de X, c’est- à-dire vérifiant ∀l ∈ Labels(μ), X ̸∈ ref(l), il existe un chemin ρ de la forme μ1.lu.μ.l′.μ3 avec lu = Label(u) et lv = Label(v), pour lequel il existe une donnée de test σ de T vérifiant path(P rog, σ) = ρ."
Enfin, le critère "toutes les définitions" tel que donné dans l'énoncé est plus fort que le critère "toutes les affectations", puisqu'un chemin passant par un noeud de définition puis par un noeud d'utilisation passe par le noeud de définition.

Le critère "toutes les décisions" n'est pas plus fort que le critère "toutes les 1-boucles", car il ne suffit pas de s'assurer que l'on passe par une boucle while pour affirmer que tous les chemins passant au plus 1 fois par la boucle while sont couverts. Il existe des programmes qui ne peuvent vérifier cette condition
On peut en exhiber un exemple :
 si x < 0 :
    x = x - 3
 tant que x < 0
    x : x+1


## Génération de tests

Pour la génération de tests, nous avons raisonné en termes d'ensembles. Pour chaque critère, nous déduisons un ensemble à couvrir (ensemble de noeuds, de chemins, ou d'expressions booléennes) et nous calculons l'ensemble des éléments couverts par chaque assignation de variables initiale. Pour calculer cette couverture, il est suggéré de calculer le prédicat de chemin pour les chemins à couvrir. Néanmoins, les méthodes développées pour tester les critères permettent de déduire cette couverture. En effet, pour chaque affectation, elles testent des égalités entre les chemins à couvrir et le chemin découlant de l'exécution du programme avec l'affectation. Ces égalités sont équivalentes à des satisfiabilités de formules booléennes par une assignation de variables. Une fois déterminés les éléments couverts par chaque affectation de variable, nous cherchons la couverture la plus petite de l'ensemble des valeurs à couvrir. Pour cela, il n'y a pas de résolution exacte car c'est un problème NP-complet, mais nous utilisons la méthode gloutonne, qui en fournit une approximation à un facteur logarithmique près. Ainsi nous déterminons un jeu de tests avec le soucis de sa taille.

# TODO

Trouver pour chaque critère des tests qui passent et des tests qui ne passent pas
Comparer les critères entre eux au sens de "plus fort que" en illustrant par des programmes pour l'infirmation de certains "plus fort que"

1. récupérer les variables
1. Créer un domaine pour chaque variable
1. Restreindre le domaine avec le critère de test
1. Calculer une solution