# Planowanie ruchu

**Całą implementacje automatycznego poruszania się można znaleźć  
w plikach [AStarNode.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/master/src/AI/AStarNode.py) oraz
 [AutomaticMovement.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/master/src/AI/AutomaticMovement.py).**
 
## Pętla główna strategii przeszukiwania

* Na początku sprawdza czy kolejka jest pusta, jeśli tak zwraca *None*
* Jeśli test spełnienia celu się powiedzie, sprawdzamy dodatkowo czy nasz punkt docelowy nie jest elementem kolizyjnym, jeśli jest, to *cel = cel.parent* i zwracamy ciąg akcji
* Dodajemy dane miejsce do listy *explored*
* Następnie w pętli *for* deklarujemy nowy stan i priorytet zgodnie z funkcją następnika, jego priorytet określamy za pomocą funkcji priorytetu *self.priority*
* Jeśli stan nie jest w kolejce i nie ma go w odwiedzonych polach, umieszczamy go w kolejce  
zgodnie z priorytetem, zapobiegamy też wystąpienia dwóch takich samych priorytetów poprzes *self.testCount += 1*
* A jeśli stan *newNode* należy do kolejki i jakiś inny stan *node* z kolejki posiada od niego większy priorytet, 
to usuwamy z kolejki *node* i dodajemy *newNode*

## Funkcja następnika

* Do wynik inicjujemy obrót w lewo i prawo, gdyż to zawsze nasz agent może wykonać
* Sprawdzamy czy jest możliwość ruchu do przodu:
    * Sprawdzamy czy przed nami jest jakaś kolizja  jeśli jest to weryfikujemy
    czy to nie jest nasz cel, jeśli jest to dodajemy ruch do przodu do wyniku funkcji następnika, jeśli nie to zwracamy jedynie listę z obrotami

## Heurystyka

* Oszacowuje koszt dotarcia do celu końcowego z aktualnej pozycji gracza.
* Opisana metodą approximateDistanceFromTarget(self, tileX, tileY) w pliku AutomaticMovement.py
* Od tileX i tileY (aktualna pozycja gracza) odejmowana jest pozycja docelowa, zwracana jest wartość zaniżonego kosztu osiągnięcia celu.