# DSZI_Survival - Drzewa Decyzyjne
### Autor: Michał Czekański

## Cel zastosowania w projekcie
W projekcie DSZI_Survival drzewo decyzyjne użyte jest do podejmowania decyzji przez agenta, rozbitka na bezludnej wyspie,
jaką czynność wykonać w danej chwili. 

Czy:
* zdobyć pożywienie
* udać się do źródła wody
* odpocząć przy ognisku

## Opis drzewa decyzyjnego

* **Drzewo decyzyjne** to drzewo reprezentujące jakąś funkcję, Boolowską w najprostszym przypadku.
* Drzewo decyzyjne jako **argument** przyjmuje obiekt - sytuację opisaną za pomocą zestawu **atrybutów**
* **Wierzchołek** drzewa decyzyjnego odpowiada testowi jednego z atrybutów (np. IsMonday)
* Każda **gałąź** wychodząca z wierzchołka jest oznaczona możliwą wartością testu z wierzchołka (np. True)
* **Liść** zawiera wartość do zwrócenia (**decyzję, wybór**), gdy liść ten zostanie osiągnięty (np. ShopType.Grocery)


## Metoda uczenia - Algorytm ID3

Metoda użyta do uczenia drzewa decyzyjnego to metoda **indukcyjnego uczenia drzewa decyzyjnego**.

### Działanie ID3 
* Definiujemy atrybuty, które będą posiadały przykłady służące do uczenia drzewa (**atrybuty**)

```python
class AttributeDefinition:
    def __init__(self, id, name: str, values: List):
        self.id = id
        self.name = name
        self.values = values

class Attribute:
    def __init__(self, attributeDefinition: AttributeDefinition, value):
        self.attributeDefinition = attributeDefinition
        self.value = value
```
* Tworzymy przykłady z wykorzystaniem atrybutów (**przykłady**)

```python
class DecisionTreeExample:
    def __init__(self, classification, attributes: List[Attribute]):
        self.attributes = attributes
        self.classification = classification
```
* Ustalamy domyślną wartość do zwrócenia przez drzewo - **klasa domyślna**
* Następnie postępujemy indukcyjnie:
    * Jeżeli liczba przykładów == 0: zwracamy wierzchołek oznaczony klasą domyślną
    * Jeżeli wszystkie przykłady są tak samo sklasyfikowane: zwracamy wierzchołek oznacz. tą klasą
    * Jeżeli liczba atrybutów == 0: zwracamy wierzchołek oznacz. klasą, którą posiada większość przykładów
    * W przeciwnym wypadku **wybieramy atrybut** A (o wyborze atrybutu poniżej) i czynimy go korzeniem drzewa T
    * **nowa_klasa_domyślna** = wierzchołek oznaczony klasą, która jest przypisana największej liczbie przykładów
    * Dla każdej wartości W atrybutu A:
        * nowe_przykłady = przykłady, dla których atrybut A przyjmuje wartość W
        * Dodajemy do T krawędź oznaczoną przez wartość W, która prowadzi do wierzchołka zwróconego przez wywołanie indukcyjne:
        *treelearn(nowe_przykłady, atrybuty−A, nowa_klasa_domyślna)*
    * Zwróć drzewo T
 ```python
class DecisionTree(object):
    def __init__(self, root):
        self.root = root
        self.branches = []
        self.branchesNum = 0
```

### Wybór atrybutu
W trakcie uczenia drzewa decyzyjnego chcemy wybrać jak najlepszy atrybut, dzięki któremu możliwie jak najszybciej będziemy mogli sklasyfikować podane przykłady.

Miarą porównawczą atrybutów będzie **zysk informacji** dla danego atrybutu (**information gain**).

Atrybut o największym zysku zostanie wybrany.

**Implementacja**

```python
def chooseAttribute(attributes: List[AttributeDefinition], examples: List[DecisionTreeExample], classifications):
    bestAttribute = None
    bestAttributeGain = -1

    for attribute in attributes:
        attrInformationGain = calculateInformationGain(attribute, classifications, examples)
        if attrInformationGain > bestAttributeGain:
            bestAttribute = attribute
            bestAttributeGain = attrInformationGain

    return bestAttribute
```


#### Obliczanie zysku informacji
(Wszelkie obliczenia wedle wzorów podanych na zajęciach)
* I(C) - Obliczamy zawartość informacji dla zbioru możliwych klasyfikacji
* E(A) - Obliczamy ilość informacji potrzebną do zakończenia klasyfikacji po sprawdzeniu atrybutu
* **G(A)** - **Przyrost informacji dla atrybutu A** = I(C) - E(A)

**Implementacja**

```python
def calculateInformationGain(attribute: AttributeDefinition, classifications, examples: List[DecisionTreeExample]):
    return calculateEntropy(classifications, examples) - calculateRemainder(attribute, examples, classifications)
```

## Opis implementacji
### Definicje atrybutów:
* Głód: **[0, 1/4); [1/4, 1/2); [1/2, 3/4); [3/4, 1]**
* Pragnienie: **[0, 1/4); [1/4, 1/2); [1/2, 3/4); [3/4, 1]**
* Energia: **[0, 1/4); [1/4, 1/2); [1/2, 3/4); [3/4, 1]**
* Odległość od jedzenia: **[0, 3); [3, 8); [8, 15); [15, max)**
* Odległość od źródła wody: **[0, 3); [3, 8); [8, 15); [15, max)**
* Odległość od miejsca spoczynku: **[0, 3); [3, 8); [8, 15); [15, max)**
* Odległość pomiędzy wodą a jedzeniem: **[0, 3); [3, 8); [8, 15); [15, max)**

```python
class PlayerStatsValue(Enum):
    ZERO_TO_QUARTER = 0
    QUARTER_TO_HALF = 1
    HALF_TO_THREE_QUARTERS = 2
    THREE_QUARTERS_TO_FULL = 3

class DistFromObject(Enum):
    LT_3 = 0
    GE_3_LT_8 = 1
    GE_8_LT_15 = 2
    GE_15 = 3
```
### Uczenie drzewa

```python
def inductiveDecisionTreeLearning(examples: List[DecisionTreeExample], attributes: List[AttributeDefinition], default,
                                  classifications)
```

### Zwracanie decyzji przez drzewo
```python
def giveAnswer(self, example: DecisionTreeExample):
    if self.branchesNum == 0:
        return self.root

    for attr in example.attributes:
        if attr.attributeDefinition.id == self.root.id:
            for branch in self.branches:
                if branch.label == attr.value:
                    return branch.subtree.giveAnswer(example)
```

### Wybór celu dla agenta
```python
def pickEntity(self, player, map, pickForGa=False):
    foods = map.getInteractablesByClassifier(Classifiers.FOOD)
    waters = map.getInteractablesByClassifier(Classifiers.WATER)
    rests = map.getInteractablesByClassifier(Classifiers.REST)

    playerStats = DTPlayerStats.dtStatsFromPlayerStats(player.statistics)

    # Get waters sorted by distance from player
    dtWaters: List[DTSurvivalInteractable] = []
    for water in waters:
        dtWater = DTSurvivalInteractable.dtInteractableFromInteractable(water, player.x, player.y)
        dtWaters.append(dtWater)
    dtWaters.sort(key=lambda x: x.accurateDistanceFromPlayer)
    nearestDtWater = dtWaters[0]

    # Get foods sorted by distance from player
    dtFoods: List[DTSurvivalInteractable] = []
    for food in foods:
        dtFood = DTSurvivalInteractable.dtInteractableFromInteractable(food, player.x, player.y)
        dtFoods.append(dtFood)

    dtFoods.sort(key=lambda x: x.accurateDistanceFromPlayer)
    # If there is no food on map return nearest water.
    try:
        nearestDtFood = dtFoods[0]
    except IndexError:
        return nearestDtWater.interactable

    # Get rest places sorted by distance from player
    dtRestPlaces: List[DTSurvivalInteractable] = []
    for rest in rests:
        dtRest = DTSurvivalInteractable.dtInteractableFromInteractable(rest, player.x, player.y)
        dtRestPlaces.append(dtRest)
    dtRestPlaces.sort(key=lambda x: x.accurateDistanceFromPlayer)
    nearestDtRest = dtRestPlaces[0]

    currentSituation = SurvivalDTExample(None, playerStats.hungerAmount, playerStats.thirstAmount,
                                         playerStats.staminaAmount,
                                         nearestDtFood.dtDistanceFromPlayer, nearestDtWater.dtDistanceFromPlayer,
                                         nearestDtRest.dtDistanceFromPlayer,
                                         nearestDtFood.getDtDistanceFromOtherInteractable(nearestDtWater.interactable))

    treeDecision, choice = self.__pickEntityAfterTreeDecision__(currentSituation,
                                                                dtFoods,
                                                                dtRestPlaces,
                                                                dtWaters)
    return choice.interactable
```

## Zestaw uczący, zestaw testowy

### Zestaw uczący

Zestaw uczący był generowany poprzez tworzenie losowych przykładów i zapytanie użytkownika o klasyfikację, a następnie zapisywany do pliku.

### Zestaw testowy

Przy testowaniu drzewa podajemy ile procent wszystkich, wcześniej wygenerowanych przykładów mają być przykłady testowe.