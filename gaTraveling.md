# Wyznaczanie trasy algorytmem genetycznym
**Autor:** *Mateusz Tylka*  

## Cel algorytmu
Celem tego algorytmu jest wyznaczenie optymalnej trasy w zbieraniu ziół o konkretnych pozycjach, które
są generowane losowo. Algorytm decyduje po które zioło udać się najpierw, starając się, aby końcowa suma odległości
pomiędzy odwiedzonymi pozycjami była jak najmniejsza.

## Osobnik Traveling
Osobnik jest to jednostka polegająca ewolucji za pomocą operacji genetycznych. 
W mojej implementacji osobnika reprezentuje obiekt [Traveling.py](). Ten obiekt przechowuje następujące metody:

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
W pliku [GeneticAlgorithm.py]() znajduje się model selekcji osobników, warunek stopu, oraz główna pętla
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