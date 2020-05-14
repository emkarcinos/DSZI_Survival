# Sphinx autodoc

Pliki źródłowe do generowania automatycznej dokumentacji kodu za pomocą biblioteki Sphinx.

## Wymagania:
```
Python 3.x
sphinx: 4.x
```

## Ręczne budowanie dokumentacji
Windows: 
```shell
make.bat html
```
Linux/MacOS:
```shell
make html
```

## Automatyczne budowanie dokumentacji w PyCharm
W PyCharmie tworzymy nową konfigurację Python docs -> Sphinx. Jako parametr "input" uswiatiamy ścieżkę do tego folderu,
a output wskazujemy tam, gdzie chcemy otrzymać gotową dokumentację.