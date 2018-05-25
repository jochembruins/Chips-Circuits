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
python3 chips.py <netlist>
```
Hierbij is \<netlist\> het nummer van de op te lossen netlist (1 t/m 6).

## Dank

* Nicole Silverio - begeleider




### Opbouw algoritmen

De manier waarop een chipcircuit wordt aangelegd is gestructureerd zoals in de afbeelding hieronder weergeven. Allereerst wordt de netlistvolgorde bepaald. Vervolgens wordt er een valide oplossing gevonden vanuit de netlistvolgorde indien mogelijk. Als laatste wordt de valide oplossing verbeterd door één voor één nieuwe wires te leggen met een A*. Hierbij wordt ook het hillclimberalgoritme betrokken.

![structuur algoritmen](https://user-images.githubusercontent.com/36193067/40545743-2f2886fa-602d-11e8-9d22-aab7bc35f6dc.png)

### Netlistvolgorde

De netlist volgorde bepaalt in welke volgorde de wires worden aangelegd. Om de netlist volgorde te bepalen worden de Dalton-methode, Ui-methode en de willekeurige netlist volgorde gebruikt. 
Bij de Dalton-methode wordt de netlist geordend op basis van Manhattan-distance tussen de gates. De bedoeling is dat de wires met kleine Manhattan-distance tussen gates eerder worden gelegd dan wires met een grote Manhattan-distance. 
De Ui-methode ordent de netlist volgorde op gates-positie. Als een wire wordt gelegd tussen gates die relatief veel aan de buitenkant liggen wordt deze wire eerder gelegd dan een wire met gates in het midden van de chip.

### Gewogen A*

De gewogen A* gaat in de netlist één voor één gates neerleggen. Dit algoritme houdt er rekening mee dat een wire niet door gates, eerder gelegde routes of buiten de grid geplaatst wordt. In de gewogen A* zijn de G-costs zodanig aangepast dat een wire zo min mogelijk grenst aan andere gates waarbij de wire niet hoeft te grenzen. Verder zijn de kosten voor het lopen in een hogere z-dimensie relatief hoger. De gewogen A* geeft dus niet de kortste route tussen twee gates. 

Indien het niet mogelijk blijkt dat de netlistvolgorde een valide oplossing geeft in combinatie met A* dan zijn er twee mogelijkheden. Als er geen wire meer gelegd kan worden met meer dan 3 wires te leggen dan wordt de netlistvolgorde willekeurig in zijn geheel geshuffled en wordt de methode opnieuw toegepast. Als er minder dan 4 wires te leggen zijn wordt de netlist volgorde aangepast door de nog te leggen wires als eerste te plaatsen.

### Breakthrough method



### Pure A* in combinatie met hillclimber

Nu er een valide oplossing is gevonden, kan deze oplossing verbeterd worden. Als de wires één voor één opnieuw geplaatst worden met pure A* (de A* met een admissable heuristic en gcost van 1 per stapje die wel de gegarandeerd de kortste route geeft) wordt de oplossing verbeterd. Dit wordt gedaan net zo lang totdat er geen verbetering meer nodig is. Er is dan een lokaal maximum bereikt. 

### experimentatie

De experimentatie die is toegepast is als volgt samen te vatten. Allereerst valt er te testen wat de verschillen in score en eventueel runtime zijn met de verschillende startnetlisten (UI-methode, Dalton-methode, willekeurige netlist). Ook zijn de verschillen in score en runtime te testen tussen de eindscores (verbeterd met pure A*) van breakthrough en gewogen A*. Als laatste wordt er geëxperimenteerd  met het verschil in het verbeteren van de valide oplossing in de volgorde waarin er wires worden teruggelegd. De wires kunnen in willekeurige volgorde verbeterd worden. Ook kan er verbeterd worden door de routebookvolgorde aan te houden. Merk op dat het terugleggen van A* niet slecht n keer (n= netlistlengte) gebeurd maar veel vaker.








