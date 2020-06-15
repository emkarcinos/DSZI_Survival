# DSZI_Survival
Przetrwanie na bezludnej wyspie.

## Podprojekty w DSZI_Survival:
* Genetic Algorithm Affinities
* Genetic Algorithm Travelling
* Neural Networks - recognizing food images
* Decision Tree - deciding whether go for food, water or rest.

## Wykorzystanie podprojektów przez agenta

### Decision Tree
W trakcie działania programu drzewo decyzyjne pomaga agentowi-rozbitkowi podjąć decyzję, 
czy powinien on w danej chwili:
 * zbierać pożywienie
 * pójść po wodę
 * odpocząć przy ognisku
 
### Neural Network
W trakcie działania programu sieć neuronowa pomaga podjąć decyzję czy znalezione pożywienie jest jadalne
czy nie. W przypadku, w którm agent się pomyli dochodzi do zatrucia i do końca gry.
Na bezludnej wyspie znajdują się tylko dwa rodzaje owoców:
 * Jabłka
 * Gruszki
 
 Celem agenta jest przetrwanie jak najdłużej.
 
### Genetic Algorithm Travelling
Po uruchomieniu aplikacji algorytm genetyczny wyznacza optymalną trasę/kolejność do zebrania ziół,
dzięki którym jego statystyki zresetują się do początkowego pozytywnego poziomu. Optymalna ścieżka
do zebrania ziół jest potrzebna, aby agent nie stracił zbyt wielu statystyk przed wykonaniem zadania.