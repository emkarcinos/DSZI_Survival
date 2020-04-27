#Planowanie ruchu
**Całą implementacje automatycznego poruszania się można znaleźć  
w plikach [AStarNode.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/Al/AStarNode.py) oraz
 [AutomaticMovement.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/Al/AutomaticMovement.py).**
##Pętla główna strategii przeszukiwania
* Na początku sprawdza czy kolejka jest pusta, jeśli tak zwraca *None*
* Jeśli test spełnienia celu się powiedzie, sprawdzamy dodatkowo czy nasz punkt docelowy nie jest elementem kolizyjnym, jeśli jest, to *cel = cel.parent* i zwracamy ciąg akcji
* Umieszczamy cel docelowy w tej iteracji w liście odwiedzonych pól
* Następnie w pętli *for* deklarujemy nowy stan i priorytet zgodnie z funkcją następnika
* Jeśli stan nie jest w kolejce i nie ma go w odwiedzonych polach, umieszczamy go w kolejce  
zgodnie z priorytetem, zapobiegamy też wystąpienia dwóch takich samych priorytetów poprzes *self.testCount += 1*
* A jeśli stan *newNode* należy do kolejki i jakiś inny stan *node* z kolejki posiada od niego większy priorytet, 
to usuwamy z kolejki *node* i dodajemy *newNode*
##Funkcja następnika

##Heurystyka