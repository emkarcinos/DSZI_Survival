# DSZI_Survival

Projekt symulatora agenta surwiwalowego w dzikim środowisku, przygotowywany na przedmiot *Sztuczna Inteligencja*.
Skład zespołu:
- Jonatan Spaczyński
- Mateusz Tylka
- Michał Czekański
- Marcin Kostrzewski

## Wymagania
```
Python 3.x
pygame: 1.9.x
```
## Uruchomienie
Projekt można uruchomić w dwóch trybach, które podajemy jako parametry:
* test: Wizualne środowisko agenta, którym możemy sami prouszać
* ga: Uruchomienie algorytmu genetycznego w tle. Musimy dodatkowo jako kolejny
parametr podać ilość iteracji dla algorytmu. Możemy dodać -t, jeżeli
chcemy uruchomić algorytm w wielu wątkach (Nie działa zbyt dobrze)
```
$ python Run.py {test|ga} [iter] [-t]
```
## Konfiguracja
Plik z konfiguracją znajduje w ```data/config/mainConfig.json```.

## Sterowanie
* Poruszanie się: *WASD*
* A*: ***u*** lub click myszką w jednostkę (np; królik)
* Interakcja: *SPACJA*