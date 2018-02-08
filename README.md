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

## Critères

### (TA) Toutes les affectations

Un jeu de test T pour Prog satisfait le critère "toutes les affectations", dénoté TA, si toutes les étiquettes de Labels(Prog,assign) apparaissent au moins une fois dans l’un des chemins d’exécution associés aux données de test σ de T.

#### Notre implémentation TA

### (TD) Toutes les décisions

Un jeu de test T pour Prog satisfait le critère "toutes les décisions", dénoté TD, si toutes les arêtes (u, v) avec Label(u) ∈ Labels(Prog, {if, while}) sont empruntées au moins une fois dans l’un des chemins d’exécution associés aux données de test σ de T.

#### Notre implémentation TD

### (k-TC) Tous les k-Chemins

Un jeu de test T pour Prog satisfait le critère "tous les k- chemins", dénoté k-TC, si pour tous les chemins
ρ de Prog de longueur inférieure ou égale à k, il existe une donnée de test σ de T vérifiant path(Prog, σ) = ρ.

#### Notre implémentation k-TC

### (i-TB) Toutes les i-boucles

Un jeu de test T pour Prog satisfait le critère "toutes les i-boucles", dénoté i-TB, avec i ∈ N si pour tous les chemins ρ pour lesquels les boucles while sont exécutées au plus i fois, il existe une donnée de test σ de T vérifiant path(Prog, σ) = ρ.

> Pour des raisons de simplicité, on utilisera la fonction `simple_loops` de NetworkX, une implémentation d'une fonction similaire ayant déjà été faite dans le projet, et le temps étant plutôt rare.
> Nous n'avons pas implémenté les boucles imbriquées pour des raisons de temps

#### Notre implémentation i-TB

### (TDef) Toutes les définitions


Un jeu de test T pour Prog satisfait le critère "toutes les définitions", dénoté TDef, si pour toutes les variables X de Prog, pour tous les nœuds u de GC(Prog) avec def(u) = {X}, il existe un chemin ρ de la forme μ1.lu.μ2.l′.μ3 avec l = Label(u), X ∈ ref(l′) et ∀l ∈ Labels(μ), X ̸∈ ref(l) pour lequel il existe une donnée de test σ de T vérifiant path(Prog, σ) = ρ.

> Dans la pratique, ce critère ne pourra jamais être rempli à 100%. En effet, les dernières étapes d'un programme sont toujours une assignation avant de retourner la valeur finale. On ne peut pas donc utiliser ces assignations puisque elles donnent directement sur le noeud final. On acceptera donc une valeur de `75%` pour ce critère.

#### Notre implémentation TDef

**Expliquer l'equivalence entre les deux sens, si on itère sur les noeuds et ensuite les variables, ou les variables et ensuite les noeuds. Pour TD, TU, TDU**

### (TU) Toutes les utilisations

Un jeu de test T pour Prog satisfait le critère "toutes les utilisations", dénoté TU, si pour toutes les variables X de Prog, pour tous les nœuds u de CG(Prog) avec def(u) = {X}, pour tous les nœudes v CG(Prog) avec X ∈ ref(v) tel qu’il existe un chemin partiel μ de u à v, sans redéfinition de X, c’est-à-dire vérifiant ∀l ∈ Labels(μ), X ̸∈ ref(l), il existe un chemin ρ de la forme μ1.lu.μ2.l′.μ3 avec lu = Label(u) et lv = Label(v), et ∀l ∈ Labels(μ2), X ̸∈ ref(l). pour lequel il existe une donnée de test σ de T vérifiant path(P rog, σ) = ρ.

> L'idée est de générer tous les chemins possibles entre tous les couples de noeuds dont le premier définit une variable et dont le deuxième la référence sans redéfinition. On génère ensuite les chemins des tests, et on vérifie que pour chaque couple, au moins un des chemins généré est emprunté.

#### Notre implémentation TU

### (TDU) Tous les DU-chemins

Pour deux nœuds u et v, on appelle chemin simple partiel de u à v un chemin u.μ.v de u à v qui passe au plus une fois dans chacune des boucles intermédiaires.

Un jeu de test T pour Prog satisfait le critère "tous les DU-chemins", dénoté TDU, si pour toutes les variables X de Prog, pour tous les nœuds u de CG(Prog) avec def(u) = {X}, pour tous les nœuds v CG(Prog) avec X ∈ ref(v), pour tous les chemins simples partiels μ de u à v, sans redéfinition de X, c’est- à-dire vérifiant ∀l ∈ Labels(μ), X ̸∈ ref(l), il existe un chemin ρ de la forme μ1.lu.μ.l′.μ3 avec lu = Label(u) et lv = Label(v), il existe une donnée de test σ de T vérifiant path(P rog, σ) = ρ.

> L'idée est la même que pour le critère TU, à la différence que cette fois, pour un couple de noeuds, on vérifie que tous les chemins possibles sont couverts par les chemins de test.

#### Notre implémentation TDU

### (TC) Toutes les conditions

Les expressions booléennes utilisées dans les instructions "if" ou "while" sont appelées des décisions. Ces décisions peuvent être décomposées en expressions élémentaires, appelées conditions. Par exemple, la décision
(X ≤0)∧(X =Y +1) est constituée des deux conditions (X ≤ 0) et (X = Y + 1).

Un jeu de test T pour P rog satisfait le critère "toutes conditions", dénoté TC, si pour toutes les conditions c de Prog, il existe une donnée de tests σc qui exécute c à vrai, et une donnée de tests σ¬c qui exécute c à faux.

#### Notre implémentation TC

# TODO

Expliquer que les regex marchent tout le temps car les variables référencées seront toujours entre guillemets

Trouver pour chaque critère des tests qui passent et des tests qui ne passent pas
Comparer les critères entre eux au sens de "plus fort que"
Faire un gros blabla sur les mécanismes d'analyse pour chaque critère

Ajouter l'ensemble non couvert dans les print des critères

1. récupérer les variables
1. Créer un domaine pour chaque variable
1. Restreindre le domaine avec le critère de test
1. Calculer une solution