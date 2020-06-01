# Wyznaczanie trasy algorytmem genetycznym
**Autor:** *Mateusz Tylka*  
**Uruchomienie:** *Po parametrze "ga_travel"*
## Cel algorytmu
Celem tego algorytmu jest wyznaczenie optymalnej trasy w zbieraniu ziół o konkretnych pozycjach, które
są generowane losowo. Algorytm decyduje po które zioło udać się najpierw, starając się, aby końcowa suma odległości
pomiędzy odwiedzonymi pozycjami była jak najmniejsza. Gdy agent zbierze wszystkie zioła i dojdzie do ogniska, aby
odpocząć, utworzy również eliksir, który odnowi mu wszystkie statystyki pierwotnego (pełnego) stanu.

## Osobnik Traveling
Osobnik jest to jednostka polegająca ewolucji za pomocą operacji genetycznych. 
W mojej implementacji osobnika reprezentuje obiekt [Traveling.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/wirus_dev/src/AI/GaTravelingForHerbs/Traveling.py). Ten obiekt przechowuje następujące metody:

```python
class Traveling:
    def __init__(self, coords):
        self.coords = coords
        self.fitness = self.evaluate()
```
* W konstruktorze przyjmowany jako parametr jest zestaw koordynatów, który zostaje zapisany jako atrybut, 
następnie tworzymy atrybut reprezentujący sprawność danego osobnika, który jest wynikiem metody określającej
poprawność danej trasy.

```python
def evaluate(self):
    sum = 0
    for i, c in enumerate(self.coords):
        if i + 1 > len(self.coords) - 1:
            break
        nextCoord = self.coords[i + 1]
        # calculate distance
        sum += sqrt((nextCoord[0] - c[0]) ** 2 + (nextCoord[1] - c[1]) ** 2)
    return sum
```
* Metoda **evaluate** odpowiedzialna jest za ocenę osobnika. Liczymy w niej odległość od punktu startu do
pierwszego punktu, następnie odległość między drugim a trzecim miejscem i tak dalej..., aż do końca listy pozycji
ziół z rozważanej trasy. Uzyskane wyniki sumujemy, czyli uzyskujemy długość konretnej drogi.

```python
def crossover(self, parentCoords):
    childCoords = self.coords[1:int(len(self.coords) / 2)]
    for coord in parentCoords.coords:
        if coord not in childCoords and coord not in END_COORD + START_COORD:
            childCoords.append(coord)

        if len(childCoords) == len(parentCoords.coords):
            break
    return Traveling(START_COORD + childCoords + END_COORD)
```
* Metoda **crossover** reprezentuję operację genetyczną krzyżowania osobników. Bierzemy w niej z pierwszego osobnika
część punktów jego trasy (w naszym przypadku połowę) i dobieramy w pętli kolejne koordynaty z drugiego osobnika
tak, aby się one nie powtarzały. Gdy już osiągniemy odpowiednią długość nowego osobnika kończymy pętlę i zwracamy go.

```python
def mutation(self):
    first = randint(1, len(self.coords) - 2)
    second = randint(1, len(self.coords) - 2)
    self.coords[first], self.coords[second] = self.coords[second], self.coords[first]
    self.fitness = self.evaluate()
```
* Ta metoda przedstawia proces mutacji. Polega on po prostu na zamianę miejscami dwóch losowych koordynatów
na trasie.

```python
def __repr__(self):
    return str(self.coords)
```
* Obiekt ten zwracany jest w formie tekstowej listy koordynatów.

## Obiekt GeneticAlgorithm
W pliku [GeneticAlgorithm.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/wirus_dev/src/AI/GaTravelingForHerbs/GeneticAlgorithm.py) znajduje się model selekcji osobników, warunek stopu, oraz główna pętla
algorytmu.

```python
class GeneticAlgorithm:
    def __init__(self, firstPopulation, mutationProbability):
        self.firstPopulation = firstPopulation
        self.mutationProbability = mutationProbability
```
* Obiekt ten przyjmuje pierwszą populację oraz prawdopodobieństwo mutacji jako parametry i zapisuje je
w odpowiednich atrybutach.

```python
def selectionModel(self, generation):
    max_selected = int(len(generation) / 10)
    sorted_by_assess = sorted(generation, key=lambda x: x.fitness)
    return sorted_by_assess[:max_selected]
```

* Model w mojej implementacji opiera się na elitaryzmie - czyli wybraniu pewnej ilości najlepszych chromosomów,
które z pewnością przetrwają do następnej generacji. Definiujemy w niej 10% spośród przyjętej generacji jako parametr.
Sortujemy naszą generację według odległości (metody *evaluate*) czyli wartości atrybutu **fitness**.

```python
def stopCondition(self, i):
    return i == 64
```

* Warunkiem końca algorytmu jest osiągnięcie 64 generacji.

```python
def run(self):
    population = self.firstPopulation
    population.sort(key=lambda x: x.fitness)
    populationLen = len(population)
    i = 0
    while True:
        selected = self.selectionModel(population)
        newPopulation = selected.copy()
        while len(newPopulation) != populationLen:
            child = choice(population).crossover(choice(population))
            if random() <= self.mutationProbability:
                child.mutation()
            newPopulation.append(child)

        population = newPopulation
        theBestMatch = min(population, key=lambda x: x.fitness)
        print("Generation: {} S: {} fitness: {}".format(i+1, theBestMatch, theBestMatch.fitness))

        i += 1
        if self.stopCondition(i):
            return str(theBestMatch)
```
* W metodzie **run** zaimplementowana jest główna pętla algorytmu
genetycznego. Na początku wskazujemy pierwszą populację i sortujemy ją według dopasowania **fitness**,
a następnie obliczamy długość populacji i deklarujemy iterator pętli, która przebiega w następujących krokach;
    * Wybieramy najlepszych osobników według modelu selekcji (metody **selectionModel**)
    * Tworzymy nową populację z najlepszych wybranych osobników, jednak do pełnej populacji brakuje nam kilku chromosomów
    * Dopełniamy do pełnej liczności populacji, poprzez operację krzyżowania (metoda **crossover**), oraz
    ewentualną mutację (metodą **mutation**).
    * Wybieramy najlepszego osobnika z populacji po minimalnej odległości, oraz wyświetlamy wynik.
    * Przeprowadzamy w ten sposób kolejną generację dopóki nie będzie ich 64.
    
```python
def listOfTravel(self):
    strTravel = self.run()
    import ast
    return ast.literal_eval(strTravel)
```

* Ta metoda, odpowiada za uruchomienie algorytmu oraz zwrócenie najlepszego wyniku w postaci listy koordynatów
(nie jako string).

## Inicjalizacja pierwszej populacji i uruchomienie algorytmu

Uruchamiając projekt za pomocą [Run.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/wirus_dev/Run.py) z użyciem parametru **ga_travel**, projekt uruchomi się tak jak w przypadku
testowej wersji z dodatkiem kodu (znajduje się on w [Game.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/wirus_dev/src/game/Game.py)) zaprezentowanego poniżej;

```python
    # Generate random travel list
    self.travelCoords = random.sample(self.map.movableList(), 10)
    import ast
    self.travelCoords = ast.literal_eval(str(self.travelCoords))

    # Insert herbs on random travel coordinates
    self.map.insertHerbs(self.travelCoords)

    # Initialize genetic algorithm
    firstGeneration = [Traveling(START_COORD + sample(self.travelCoords, len(self.travelCoords)) + END_COORD) for _
                       in range(100)]
    mutationProbability = float(0.1)
    ga = GeneticAlgorithm(firstGeneration, mutationProbability)
    self.movementList = ga.listOfTravel()

    # Define list of entities which player should pass to collect herbs
    self.entityToVisitList = []
    for i in self.movementList:
        self.entityToVisitList.append(self.map.getEntityOnCoord(i))

    # Remove first element, because start coordinates is None
    self.entityToVisitList.remove(self.entityToVisitList[0])

    self.screen.ui.console.printToConsole("First generation: " + str(firstGeneration[0]))
    self.screen.ui.console.printToConsole("The best generation: " + str(self.entityToVisitList))

    self.mainLoop()
```

* Generujemy losową listę 10 koordynatów na mapie wolnych od entity za pomocą metody **map.movableList()** i konwertujemy
ją na normalną listę (nie *string*). 
* Umieszczamy entity ziół w miejscach wygenerowanych koordynatów.
* Tworzymy pierwszą generację w postaci 100-elementowej listy, za pomocą konstruktora obiektu **Traveling** o koordynatach ziół plus startowa pozycja gracza
i pozycja ogniska, gdzie agent będzie w stanie sporządzić miksturę odnawiającą jego statystyki.
* Deklarujemy algorytm genetyczny przekazując pierwszą generację oraz prawdopodobieństwo mutacji wynoszące 10%
* Tworzymy listę kordynatów na których będziemy się poruszać, gdzie jej wartość co zwrócona lista przez
metodę **ga.listOfTravel()**
* Aby udać się po odpowiednie cele, tworzymy listę entity, które musimy zebrać, wykorzystując przy tym
wcześniej stworzoną listę **movementList** oraz metodę **map.getEntityOnCoord**.
* Usuwamy z listy **entityToVisitList** pierwszy element, gdyż jest to startowa pozycja gracza, na której nie
ma żadnego entity.

## Poruszanie się
*Zdefiniowane jest w pliku/klasie [EventManager.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/wirus_dev/src/game/EventManager.py).*

```python
    if keys[pygame.K_t]:  # Handle traveling movement to collect herbs
        if self.player.movementTarget is None and self.iterator <= 10:
            target = self.game.entityToVisitList[self.iterator]
            self.player.gotoToTarget(target, self.game.map)
            self.iterator += 1

    if self.player.herbs > self.takenHerbs:  # Console log when player collect herb
        self.game.screen.ui.console.printToConsole("Ziele zebrane! Ilość: " + str(self.player.herbs))
        self.takenHerbs = self.player.herbs

    if self.player.readyToCrafting:  # Console log and reset statistics because of collect all herbs
        self.game.screen.ui.console.printToConsole("Eliksir został utworzony i spożyty!")
        self.player.statistics.set_hp(100)
        self.player.statistics.set_stamina(100)
        self.player.statistics.set_thirst(-100)
        self.player.statistics.set_hunger(-100)
        self.player.readyToCrafting = False
```
Po kliknięciu przycisku **t** agent uda się po kolejne ziele do zebranie w
kolejce za pomocą algorytmu **A***. Obok jest również zaimplementowane wypisywanie ilości zebranych ziół,
oraz odnawianie statystyk po spożyciu eliksiru.