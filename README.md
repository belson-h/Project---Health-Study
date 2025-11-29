# Hälsostudie - Dataanalys

## Projektbeskrivning
Detta projekt är en individuell uppgift i kursen Pythonprogrammering och statistisk dataanalys, där syftet är att analysera (fiktiv) data från en hälsostudie. Analysen utförs i Python med fokus på grundläggande statistik, visualiseringar och simuleringar.

Datasetet innehåller information om deltagarnas ålder, kön, vikt, längd, blodtryck, kolesterolnivå, rökvanor och om de har en viss sjukdom.

## Projektstruktur
- `health_study_dataset.csv` – Dataset med deltagardata  
- `study_report.ipynb` – Hälsorapport
- `helpers.py`- Innehåller uträkningar som stödjer analysen

GitHub-brancher: `main` - Slutrapport, `del1` - Del 1, `del2` - Del 2

## Analys i Del 1
- Beskrivande statistik: medel, median, min och max för numeriska variabler  
- Visualiseringar: översikt över rökning, blodtryck och vikt 
- Simulering: slumpade sjukdomsfall med numpy.random  
- Konfidensintervall för medelvärde av systoliskt blodtryck  
- Hypotesprövning: rökare vs. icke-rökare  

## Analys i Del 2
*Bygger på del 1*:
- Ny struktur: delar av den löpande koden flyttas in i klasser
- Utökad analys: individer med sjukdom och slumpade sjukdomsfall per kön
- Blodtrycksprognos: enkel och multipel regression baserat på ålder och vikt
- Principle Component Analysis (PCA) på numeriska variablar

## Python-version
- Python 3.13.7 (rekommenderas)  
- Viktiga bibliotek: `numpy`, `pandas`, `matplotlib`, `scipy`, `sklearn`, `statsmodels`

## Hur man kör notebooken
1. Klona repository:  
   ```bash
   git clone https://github.com/belson-h/Project---Health-Study.git
2. Installera nödvändiga Python-paket: `pip install -r requirements.txt`
3. Öppna `study_report.ipynb` i Jupyter Notebook.
4. Kör alla celler för att reproducera analys och visualiseringar.
