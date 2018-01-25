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

if x >= 1:
    while x < 10:
        x = x + 1
else:
    x = x + 1
```

## Critères

### (TA) Toutes les affectations

Un jeu de test T pour Prog satisfait le critère "toutes les affectations", dénoté TA, si toutes les étiquettes de Labels(Prog,assign) apparaissent au moins une fois dans l’un des chemins d’exécution associés aux données de test σ de T.

### (TD) Toutes les décisions

Un jeu de test T pour Prog satisfait le critère "toutes les décisions", dénoté TD, si toutes les arêtes (u, v) avec Label(u) ∈ Labels(Prog, {if, while}) sont empruntées au moins une fois dans l’un des chemins d’exécution associés aux données de test σ de T.

### (k-TC) Tous les k-Chemins

Un jeu de test T pour Prog satisfait le critère "tous les k- chemins", dénoté k-TC, si pour tous les chemins
ρ de Prog de longueur inférieure ou égale à k, il existe une donnée de test σ de T vérifiant path(Prog, σ) = ρ.

### (i-TB) Toutes les i-boucles

Un jeu de test T pour Prog satisfait le critère "toutes les i-boucles", dénoté i-TB, avec i ∈ N si pour tous les chemins ρ pour lesquels les boucles while sont exécutées au plus i fois, il existe une donnée de test σ de T vérifiant path(Prog, σ) = ρ.

### (TDef) Toutes les définitions

Un jeu de test T pour Prog satisfait le critère "toutes les définitions", dénoté TDef, si pour toutes les variables X de Prog, pour tous les nœuds u de GC(Prog) avec def(u) = {X}, il existe un chemin ρ de la forme μ1.lu.μ2.l′.μ3 avec l = Label(u), X ∈ ref(l′) et ∀l ∈ Labels(μ), X ̸∈ ref(l) pour lequel il existe une donnée de test σ de T vérifiant path(Prog, σ) = ρ.

### (TU) Toutes les utilisations

Un jeu de test T pour Prog satisfait le critère "toutes les utilisations", dénoté TU, si pour toutes les variables X de Prog, pour tous les nœuds u de CG(Prog) avec def(u) = {X}, pour tous les nœudes v CG(Prog) avec X ∈ ref(v) tel qu’il existe un chemin partiel μ de u à v, sans redéfinition de X, c’est-à-dire vérifiant ∀l ∈ Labels(μ), X ̸∈ ref(l), il existe un chemin ρ de la forme μ1.lu.μ2.l′.μ3 avec lu = Label(u) et lv = Label(v), et ∀l ∈ Labels(μ2), X ̸∈ ref(l). pour lequel il existe une donnée de test σ de T vérifiant path(P rog, σ) = ρ.

### (TDU) Tous les DU-chemins

Pour deux nœuds u et v, on appelle chemin simple partiel de u à v un chemin u.μ.v de u à v qui passe au plus une fois dans chacune des boucles intermédiaires.

Un jeu de test T pour Prog satisfait le critère "tous les DU-chemins", dénoté TDU, si pour toutes les variables X de Prog, pour tous les nœuds u de CG(Prog) avec def(u) = {X}, pour tous les nœuds v CG(Prog) avec X ∈ ref(v), pour tous les chemins simples partiels μ de u à v, sans redéfinition de X, c’est- à-dire vérifiant ∀l ∈ Labels(μ), X ̸∈ ref(l), il existe un chemin ρ de la forme μ1.lu.μ.l′.μ3 avec lu = Label(u) et lv = Label(v), il existe une donnée de test σ de T vérifiant path(P rog, σ) = ρ.

### (TC) Toutes les conditions

Les expressions booléennes utilisées dans les instructions "if" ou "while" sont appelées des décisions. Ces décisions peuvent être décomposées en expressions élémentaires, appelées conditions. Par exemple, la décision
(X ≤0)∧(X =Y +1) est constituée des deux conditions (X ≤ 0) et (X = Y + 1).

Un jeu de test T pour P rog satisfait le critère "toutes conditions", dénoté TC, si pour toutes les conditions c de Prog, il existe une donnée de tests σc qui exécute c à vrai, et une donnée de tests σ¬c qui exécute c à faux.