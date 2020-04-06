# Środowisko agenta
**Skład zespołu:** *Marcin Kostrzewski,* *Mateusz Tylka,* *Michał Czekański,* *Jonathan Spaczyński*  
**Wybrany temat:** *Inteligentny Survival (temat własny)*  
**Wykorzystana technologia:** *Pygame*

## Koncepcja
* *Środowiskiem naszego agenta jest bezludna wyspa*
* *Celem naszego agenta jest przetrwanie*
* *Na wyspie znajdują się różnorodne elementy, które pomagają lub przeszkadzają przetrwać*
* *Agent ma zasoby, które musi uzupełniać aby przeżyć, np. głód*
* *Agent porusza się w środowisku 20x20*
 
## Struktura projektu
*Plik przedstawiający strukturę katalogów oraz klas:* [structure.pdf](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/data/structure.pdf)

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
*Wiedzą w naszym projekcie są statystyki agenta, które mowią o tym w jakim stanie toczy się proces przetrwania.   
Posiadamy również konsolę, która wypisuje wartości statystyk na ekranie.*  
![screenshot](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/master/data/images/adventure.png)  

## Uruchomienie projektu
**Wystarczy uruchomić plik:** [Run.py](https://git.wmi.amu.edu.pl/s444409/DSZI_Survival/src/development/Run.py)