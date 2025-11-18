# Hälsostudie - Dataanalys

## Projektbeskrivning
Detta projekt är en individuell uppgift i kursen Pythonprogrammering och statistisk dataanalys, där syftet är att analysera (fiktiv) data från en hälsostudie. Analysen utförs i Python med fokus på grundläggande statistik, visualiseringar och simuleringar.

Datasetet innehåller information om deltagarnas ålder, kön, vikt, längd, blodtryck, kolesterolnivå, rökvanor och om de har en viss sjukdom.

## Projektstruktur
- `health_study_dataset.csv` – Dataset med deltagardata  
- `study_report.ipynb` – Jupyter Notebook för del 1 (grundläggande analys och statistik) 

GitHub-brancher: `del1` – Del 1, `del2` – Del 2 (ej påbörjad)

## Analys i Del 1
- Beskrivande statistik: medel, median, min och max för numeriska variabler  
- Visualiseringar: Översikt över rökning, blodtryck och vikt 
- Simulering: slumpade sjukdomsfall med numpy.random  
- Konfidensintervall för medelvärde av systoliskt blodtryck  
- Hypotesprövning: rökare vs. icke-rökare  

## Analys i Del 2
Ej påbörjad

## Python-version
- Python 3.13.7 (rekommenderas)  
- Viktiga bibliotek: `numpy`, `pandas`, `matplotlib`, `scipy`

## Hur man kör notebooken
1. Klona repository:  
   ```bash
   git clone https://github.com/belson-h/Project---Health-Study.git
2. Installera nödvändiga Python-paket: `pip install -r requirements.txt`
3. Öppna `study_report.ipynb` i Jupyter Notebook.
4. Kör alla celler för att reproducera analys och visualiseringar.
