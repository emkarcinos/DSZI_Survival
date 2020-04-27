# Planowanie ruchu

**Całą implementacje automatycznego poruszania się można znaleźć  
w plikach [AStarNode.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/master/src/AI/AStarNode.py) oraz
 [AutomaticMovement.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/master/src/AI/AutomaticMovement.py).**

## Postęp projektu
Teraz nasz agent ma możliwość automatycznego poruszania się.  
Po wciśnięciu ***u*** nasza postać zacznie zmierzać do losowego obszaru za pomocą algorytmu A*.  
Dodatkowo można kliknąć myszką w element interaktywny (np. jagodę), wtedy pójdziemy do tej jednostki w ten sam sposób.  
Jeśli pole przed agentem będzie zawierało interaktywną jednostkę zostanie ona podniesiona.

## Pętla główna strategii przeszukiwania
**Metoda *a_Star(self)* w [AutomaticMovement.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/master/src/AI/AutomaticMovement.py)**
* Na początku sprawdza czy kolejka jest pusta, jeśli tak zwraca *None*
```        
             while True:
               if fringe.empty():
                   # target is unreachable
                   print("PATH NOT FOUND")
                   return None
```
* Jeśli test spełnienia celu się powiedzie, sprawdzamy dodatkowo czy nasz punkt docelowy nie jest elementem kolizyjnym, jeśli jest, to *cel = cel.parent* i zwracamy ciąg akcji
```
            if self.goalTest(elem.state):
                print("PATH FOUND")
                movesList = []

                if isinstance(self.actualTarget, Entity) or self.actualTarget in self.map.collidables:
                    elem = elem.parent

                while elem.action is not None:
                    movesList.append(elem.action)
                    elem = elem.parent

                movesList.reverse()
                return movesList
```
* Dodajemy dane miejsce do listy *explored*
* Następnie w pętli *for* deklarujemy nowy stan i priorytet zgodnie z funkcją następnika, jego priorytet określamy za pomocą funkcji priorytetu *self.priority*
* Jeśli stan nie jest w kolejce i nie ma go w odwiedzonych polach, umieszczamy go w kolejce  
zgodnie z priorytetem, zapobiegamy też wystąpienia dwóch takich samych priorytetów poprzes *self.testCount += 1*
* A jeśli stan *newNode* należy do kolejki i jakiś inny stan *node* z kolejki posiada od niego większy priorytet, 
to usuwamy z kolejki *node* i dodajemy *newNode*
```
            explored.append(elem)

            for (movement, newState) in self.succesor(elem.state):
                newNode = AStarNode(elem, movement, newState)
                newPriority = self.priority(newNode)

                # Check if state is not in fringe queue ... # ... and is not in explored list
                if not any(newNode.state == node[2].state for node in fringe.queue) \
                        and not any(newNode.state == node.state for node in explored):
                    # there can't be nodes with same priority
                    fringe.put((newPriority, self.testCount, newNode))
                    self.testCount += 1
                # If state is in fringe queue ...
                elif any(newNode.state == node[2].state for node in fringe.queue):
                    node: AStarNode
                    for (pr, count, node) in fringe.queue:
                        # Compare nodes
                        if node.state == newNode.state and node.action == newNode.action:
                            # ... and if it has priority > newPriority
                            if pr > newPriority:
                                # Replace it with new priority
                                fringe.queue.remove((pr, count, node))
                                fringe.put((newPriority, count, node))
                                self.testCount += 1
                                break
```

## Funkcja następnika
**Metoda *succesor(self, elemState)* w [AutomaticMovement.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/master/src/AI/AutomaticMovement.py)**

* Do wynik inicjujemy obrót w lewo i prawo, gdyż to zawsze nasz agent może wykonać
* Sprawdzamy czy jest możliwość ruchu do przodu:
    * Sprawdzamy czy przed nami jest jakaś kolizja, jeśli jest to weryfikujemy
    czy to nie jest nasz cel 
    * Jeśli to jest nasz cel to dodajemy ruch do przodu do wyniku funkcji następnika, jeśli nie to zwracamy jedynie listę z obrotami
```
    def succesor(self, elemState):
        '''
        :param elemState: [x, y, Rotation]
        :return: list of (Movement, NewState)
        '''
        result = [(Movement.ROTATE_R, self.newStateAfterAction(elemState, Movement.ROTATE_R)),
                  (Movement.ROTATE_L, self.newStateAfterAction(elemState, Movement.ROTATE_L))]

        stateAfterForward = self.newStateAfterAction(elemState, Movement.FORWARD)
        if 0 <= stateAfterForward[0] <= self.map.width and 0 <= stateAfterForward[1] <= self.map.height:
            coordsWithUiOffset = [stateAfterForward[0] + self.leftUiWidth, stateAfterForward[1]]
            facingEntity = self.map.getEntityOnCoord(coordsWithUiOffset)

            if facingEntity is not None:
                if isinstance(self.actualTarget, Entity):
                    if facingEntity.id == self.actualTarget.id:
                        result.append((Movement.FORWARD, stateAfterForward))
            elif self.map.collision(coordsWithUiOffset[0], coordsWithUiOffset[1]) and \
                    self.targetCoords[0] == stateAfterForward[0] and self.targetCoords[1] == stateAfterForward[1]:
                result.append((Movement.FORWARD, stateAfterForward))
            elif not self.map.collision(coordsWithUiOffset[0], coordsWithUiOffset[1]):
                result.append((Movement.FORWARD, stateAfterForward))

        return result
```

## Heurystyka
**Metoda *approximateDistanceFromTarget(self, tileX, tileY)* w [AutomaticMovement.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/master/src/AI/AutomaticMovement.py)**
* Oszacowuje koszt dotarcia do celu końcowego z aktualnej pozycji gracza.
* Od tileX i tileY (aktualna pozycja gracza) odejmowana jest pozycja docelowa, zwracana jest wartość zaniżonego kosztu osiągnięcia celu.
```
    def approximateDistanceFromTarget(self, tileX, tileY):
        return abs(tileX - self.targetCoords[0]) + abs(tileY - self.targetCoords[1])
```