# Chips & Circuits

Groepsproject voor Heuristieken waarbij wordt gezocht naar de meest optimale manier om gates op een fictieve chip te verbinden.

## Auteurs / Veganboyz

* Noah van Grinsven (Veganboy 1)
* Melle Gelok (Veganboy 2)
* Jochem Bruins (Veganboy 3)

## Aan de slag

### Vereisten

Onze code is volledig geschreven in Python 3. In requirements.txt staat alle packages die nodig zijn om de code succesvol te laten draaien. Installatie is mogelijk met pip. 

```
pip install -r requirements.txt
```

### Structuur

In de hoofdfolder verschillende subfolders:

* Data - Hierin bevinden zich alle datafiles zoals de netlist en de gates
* Scripts - alle scripts die gebruikt worden om het programma te laten draaien
* Presentaties - alle netlists zoals gegeven in de opdracht

### Testen

Voer de volgende command uit om het programma te laten draaien:
```
cd scripts
python3 chips.py
```

#

Lowerbound = x = som directe afstanden wires
Upperbound = x + som die loopt van i = 0 tot lambda over 2i (hierbij is lambda gelijk aan aantal netlists - 1) + 2y
(hierbij is y gates dubbel in netlist)

## Dank

* Nicole Silverio - begeleider




