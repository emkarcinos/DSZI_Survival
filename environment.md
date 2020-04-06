# Środowisko agenta
**Skład zespołu:** *Marcin Kostrzewski,* *Mateusz Tylka,* *Michał Czekański,* *Jonathan Spaczyński*  
**Wybrany temat:** *Inteligentny Survival (temat własny)*  
**Wykorzystana technologia:** *Pygame*

## Koncepcja
* *Środowiskiem naszego agenta jest bezludna wyspa*
* *Celem naszego agenta jest przetrwanie jak najdłużej*
* *Na wyspie znajdują się różnorodne elementy, które pomagają lub przeszkadzają przetrwać*
* *Agent ma zasoby, które musi uzupełniać aby przeżyć, np. głód*
* *Agent porusza się w środowisku 20x20*
 
## Struktura projektu
*Plik przedstawiający strukturę katalogów oraz klas:* [structure.pdf](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/master/data/structure.pdf)

## Główne klasy projektu
* [Run.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/Run.py) - plik, względem którego uruchamia się całe środowisko.
* [Game.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/game/Game.py) -
klasa realizacyjna, w niej wywoływane są wszystkie inne główne obiekty, obsługuję główną pętlę aplikacji.
* [Screen.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/game/Screen.py) - reprezentuje obszar okienka, które pojawia się po uruchomieniu, odpowiada za poprawną lokalizację mapy oraz interfejsu użytkownika.
* [Map.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/game/Map.py) - jest to mapa, po której porusza się agent, reprezentowana jest jako macierz o elementach terenu w pliku [map.txt](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/data/mapdata/map.txt),
 renderuje teren oraz jednostki na swój obszar, potrafi też je usuwać.
* [TerrainTile.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/game/TerrainTile.py) - przedstawia element terenu, który jest jedną kratką na mapie 20x20.
* [UI.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/ui/Ui.py) - reprezentuje interfejs użytkownika i obsługuje go, posiada swoje pod elementy.
* [EventMenager.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/game/EventManager.py) - obsługuje zdarzenia występujące na ekranie, takie jak poruszanie się sprite'ów czy wyjście z gry.
* [Entity.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/entities/Entity.py) - przedstawia jednostki występujące na mapie, które w jakiś sposób zachodzą ze sobą w interakcje.
* [Player.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/entities/Player.py) - tworzy agenta, którym na daną chwilę możemy się poruszać i zachodzić w interakcje z innymi jednostkami.
* [Statistics.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/src/entities/Statistics.py) - reprezentuje zasoby agenta, które odpowiednio zwiększają się, lub zmniejszają po interakcji z jakimś elementem.

## Reprezentacja wiedzy
_Wiedzą w naszym projekcie są statystyki agenta, które mowią o tym w jakim stanie toczy się proces przetrwania oraz czas jaki udało się przetrwać.  
Statystyki agenta można zmieniać poprzez interakcję z objektami **entities**, dla przykładu wypicie czystej wody zaspokoi
nasze pragnienie, a zjedzenie królika nasz głód, możemy również odpocząć przy ognisku.
Posiadamy również konsolę, która wypisuje różnorodne zdarzenia i ich skutki, na przykład gry agent coś podniesie. 
W konsoli znajduję się również Timer, który pozwala nam ustalić ile czasu udało się agentowi przetrwać._
![screenshot](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/raw/master/data/images/adventure.png?fbclid=IwAR0lBN3bQIK4-LQuVPw-vTLxBrN3xMTrNjKjcrOp4idzaZvkOwdbYZQRQc0)
### Statystyki
**Health points:** *Punkty życia agenta, gdy pasek spadnie do zera agent umiera.*  
**Hunger:** *Głód agenta, gdy pasek podniesie się do wartości 100, agent umiera.*  
**Stamina:** *Energia agenta, gdy pasek spadnie do zera agent nie może się poruszać.*  
**Thirst:** *Pragnienie agenta, gdy pasek osiągnie maksimum (wartość 100), agent umiera.*  

## Uruchomienie projektu
**Wystarczy uruchomić plik:**python [Run.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/Run.py)

## Poradnik
_Poruszaj się klawiszami **WASD**! Podejdź odpowiednio odwrócony do czystej wody i kliknij **SPACE** aby zaspokoić swoje **pragnienie**! Króliki i różnorodne rośliny zapewnią Tobie **pożywienie**! Odpocznij co jakiś czas w swoim domku przy **ognisku**, aby sprawnie **funkcjonować**! Uważaj na Siebie, **życie** wśród dziczy, bywa brutalne._