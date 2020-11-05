# OpAmp Data Analysis

## Misure Dirette e Amplificazione Attesa

Ho usato il multimetro _Metrix_ con le pinze 

| Resistenza |      Valore     |      F.S.     |
|:------------:|:-----------------:|:---------------:|
|     R<sub>f</sub>     | 82.462 k&Omega; |  100 k&Omega; |
|     R<sub>1</sub>     | 8.0894 k&Omega; |   10 k&Omega; |
|     R<sub>3</sub>     |  46.54 &Omega;  |    1 k&Omega; |

Notare R<sub>f</sub> > R<sub>1</sub> come richiesto (circa 10 volte più grande!).

Calcolo l'amplificazione attesa: G = - R<sub>f</sub> / R<sub>1</sub> = -10.19383 _dove il segno meno deriva dalla configurazione invertente
dell'operazionale_.

Precisione e risoluzione del multimetro Metrix3292 per i fondo-scala utilizzati nell'esperienza

  |        F.S.    | Precisione | Risoluzione |
  |:--------------:|:----------:|:-----------:|
  |1 k&Omega;      | 0.10% + 8  | 0.01 &Omega;|
  |10 k&Omega;     | 0.07% + 8  | 0.1 &Omega; |
  |100 k&Omega;    | 0.07% + 8  | 1 &Omega;   |
  
  Per stimare l'errore sulla misura diretta delle resistenze utilizzo la seguente formula:

  ![Direct measure propagation](LaTeX_equation/resistance_propagation.png)  

  E ottengo dunque

  | Resistenza |      Valore     |      Errore    |
  |:------------:|:-----------------:|:---------------:|
  |     R<sub>f</sub>     | 82.46 k&Omega; |  0.03  k&Omega;|
  |     R<sub>1</sub>     | 8.089 k&Omega; |  0.003 k&Omega;|
  |     R<sub>3</sub>     |  46.54 &Omega;  |  0.05  &Omega;|

  Usando ora le incertezze sulle misure delle resistenze posso stimare l'errore della stima dell'amplificazione attesa. La formula di propagazione è quindi
  
  ![Amplification propagation](LaTeX_equation/amplification_propagation.png) 

  Si trova allora che l'amplificazione attesa è _in modulo_ **G = 10.194 +/- 0.006**.

## Misure con Oscilloscopio

Applico  una tensione sinusoidale di frequenza f = 1 kHz: faccio variare l'ampiezza del segnale e registro i massimi e i minimi per entrambi i
segnali V<sub>in</sub> e V<sub>out</sub>

### Misure dei Massimi

| V<sub>in</sub> |  V<sub>out</sub> | FS V<sub>in</sub> | FS V<sub>out</sub> |    Tensione Generatore |
|:-------------:|:--------------:|:--------:|:------------:|:--------------:|
| 106 mV      | 997 mV       | 50 mV   | 324 mV     | 0.20 Vpp     |
| 252 mV      | 2.48 V       | 100 mV | 1.00 V     | 0.50 Vpp     |
| 400 mV      | 4.00 V       | 200 mV | 2.00 V     | 0.80 Vpp     |
| 496 mV      | 4.96 V       | 200 mV | 2.00 V     | 1.00 Vpp     |
| 744 mV      | 7.44 V       | 200 mV | 2.00 V     | 1.50 Vpp     |
| 907 mV      | 8.98 V       | 324 mV | 3.40 V     | 1.80 Vpp     |
| 1.01 V      | 9.93 V       | 324 mV | 3.40 V     | 2.00 Vpp     |
| 1.16 V      | 11.4 V       | 376 mV | 3.80 V     | 2.30 Vpp     |
| 1.29 V      | 13.0 V       | 436 mV | 4.52 V     | 2.60 Vpp     |
| 1.50 V      | 14.4 V       | 480 mV | 4.52 V     | 3.00 Vpp     |
| 1.61 V      | 14.7 V       | 630 mV | 5.60 V     | 3.20 Vpp     |
| 1.77 V      | 14.7 V       | 660 mV | 5.60 V     | 3.50 Vpp     |

### Misure dei Minimi

| V<sub>in</sub> |  V<sub>out</sub> | FS V<sub>in</sub> | FS V<sub>out</sub> |    Tensione Generatore |
|:-------------:|:--------------:|:--------:|:------------:|:--------------:|
| -102 mV    | -972 mV     | 50mV   | 324 mV     |  0.20 Vpp     |
| -252 mV    | -2.48 V     | 100 mV | 1.00 V     |  0.50 Vpp     |
| -400 mV    | -3.92 V     | 200 mV | 2.00 V     |  0.80 Vpp     |
| -496 mV    | -4.96 V     | 200 mV | 2.00 V     |  1.00 Vpp     |
| -736 mV    | -7.36 V     | 200 mV | 2.00 V     |  1.50 Vpp     |
| -881 mV    | -8.98 V     | 324 mV | 3.40 V     |  1.80 Vpp     |
| -984 mV    | -10.0 V     | 324 mV | 3.40 V     |  2.00 Vpp     |
| -1.13 V    | -11.5 V     | 376 mV | 3.80 V     |  2.30 Vpp     |
| -1.29 V    | -13.0 V     | 436 mV | 4.52 V     |  2.60 Vpp     |
| -1.48 V    | -14.1 V    | 480 mV  | 4.52 V     |  3.00 Vpp     |
| -1.59 V    | -14.8 V    | 630 mV  | 5.60 V     |  3.20 Vpp     |
| -1.72 V    | -14.8 V    | 660 mV  | 5.60 V     |  3.50 Vpp     |

**Impostando una tensione sul generatore pari a 3 Vpp inizia a vedersi la saturazione del segnale in uscita!**

Alle misure di tensione acquisite con i cursori dell'oscilloscopio si associa la seguente incertezza:

![Cursors propagation](LaTeX_equation/cursors_propagation.png)
  
Seguono allora le misure dei massimi e dei minimi con associata l'opportuna incertezza.

### Propagazione dei Massimi
    
| V<sub>in</sub>  (V)  | &sigma;<sub>V<sub>in</sub></sub> (V)|V<sub>out</sub>  (V) | &sigma;<sub>V<sub>out</sub></sub> (V)|
|:--------:|:--------:|:---------:|:----------:|
| 0.106 | 0.003 |  1.00 |   0.02 |
| 0.252 | 0.006 |  2.48 |   0.05 |
| 0.400 | 0.010 |  4.00 |   0.10 |
| 0.496 | 0.011 |  4.96 |   0.11 |
| 0.744 | 0.014 |  7.44 |   0.14 |
| 0.907 | 0.019 |  8.98 |   0.19 |
| 1.01 | 0.02 |  9.9 |   0.2 |
| 1.16 | 0.02 | 11.4 |   0.2 |
| 1.29 | 0.03 | 13.0 |   0.3 |
| 1.50 | 0.03 | 14.4 |   0.3 |
| 1.61 | 0.03 | 14.7 | 0.3 |
| 1.77 | 0.04 | 14.7 | 0.3 |

### Propagazione dei Minimi
  
| V<sub>in</sub>  (V)   | &sigma;<sub>V<sub>in</sub></sub> (V)| V<sub>out</sub>  (V)   | &sigma;<sub>V<sub>out</sub></sub> (V)|
|:--------:|:--------:|:---------:|:----------:|
| -0.102 |  0.003 |  -0.972 |   0.02 |
| -0.252 |  0.006 |  -2.48 |   0.05 |
| -0.400 |  0.010 |  -3.92 |   0.10 |
| -0.496 |  0.011 |  -4.96 |   0.11 |
| -0.736 |  0.014 |  -7.36 |   0.14 |
| -0.881 |  0.019 |  -8.98 |   0.19 |
| -0.98 |  0.02 | -10.0 |   0.2 |
| -1.13 |  0.02 | -11.5 |   0.2 |
| -1.29 |  0.03 | -13.0 |   0.3 |
| -1.48 |  0.03 | -14.1 |   0.3 |
| -1.59 | 0.03 | -14.8 | 0.3 |
| -1.72 | 0.04 | -14.8 | 0.3 |

## Fit Preliminari

Ora faccio due fit separati per massimi e minimi considerando solo gli errori su V<sub>out</sub> al fine di stimare il coefficiente angolare _m_
(_slope_). Questo lo userò poi per proiettare gli errori di V<sub>in</sub> lungo l'asse y: in tal modo potrò sommare quadraticamente i contributi
d'errore di V<sub>out</sub> e V<sub>in</sub>.

**NB: I fit vengono effettuati senza gli outliers, ovvero gli ultimi tre dati presi in saturazione!**

Mostriamo prima di tutto la presenza degli outliers: faccio un plot espolaritvo con tutti i dati, sia massimi sia minimi, con il loro errore sia lungo
x sia lungo y, ed effettuo un fit per osservare l'andamento dei residui.

![All Data EDA](Plots/Report_Plots/opamp_plot_alldata_eda.png)

Si nota chiaramente come gli ultimi tre punti nelle code non rispettino il trend lineare: sono proprio i punti presi in saturazione, che quindi non
verranno considerati nell'analisi successiva.

### Fit Massimi

![Max Preliminary](Plots/Report_Plots/opamp_plot_max_preliminary.png)

| Chi2 | NDf | offset | slope |
|:----:|:----:|:----:|:----:|
| 1.96966 | 7 |-0.0615312   +/-   0.0242261|   10.0251   +/-   0.0941201 |

### Fit Minimi

![Min Preliminary](Plots/Report_Plots/opamp_plot_min_preliminary.png)

| Chi2 | NDf | offset | slope |
|:----:|:----:|:----:|:----:|
| 1.35854 | 7 |0.0675817   +/-   0.0238213|   10.157   +/-   0.0948987 |

![All Preliminary](Plots/Report_Plots/opamp_plot_preliminary.png)

## Proiezione Errori

Ora che ho effettuato i fit preliminari, utilizzo il coefficiente angolare della retta interpolante per proiettare gli errori di V<sub>in</sub> su
V<sub>out</sub>.

![Error projection](LaTeX_equation/error_projection.png)

### Massimi 

| V<sub>in</sub> (V)| &sigma;<sub>V<sub>in</sub></sub> (V)|  V<sub>out</sub>   (V)| &sigma;<sub>V<sub>out, projected</sub></sub> (V)|
|:-------:|:-------:|:-------:|:-------:|
| 0.106 | 0.003 |  1.00 |   0.03 |
| 0.252 | 0.005 |  2.48 |   0.08 |
| 0.400 | 0.010 |  4.00 |   0.14 |
| 0.496 | 0.011 |  4.96 |   0.15 |
| 0.744 | 0.014 |  7.44 |   0.19 |
| 0.907 | 0.019 |  9.0 |   0.3 |
| 1.01 | 0.02 |  10.0 |   0.3 |
| 1.16 | 0.02 | 11.4 |   0.3 |
| 1.29 | 0.03 | 13.0 |   0.4 |

![Max Projected](Plots/Report_Plots/opamp_plot_max_projected.png)

| Chi2 | NDf | offset | slope |
|:----:|:----:|:----:|:----:|
| 0.979322 | 7 |-0.0601178   +/-   0.0383327|   10.0231   +/-   0.135237 |

### Minimi 

| V<sub>in</sub> (V)| &sigma;<sub>V<sub>in</sub></sub> (V)|  V<sub>out</sub>   (V)| &sigma;<sub>V<sub>out, projected</sub></sub> (V)|
|:-------:|:-------:|:-------:|:-------:|
| -0.102 |   0.003 | -0.97 |   0.03 |
| -0.252 |   0.006 | -2.48 |   0.08 |
| -0.400 |   0.010 | -3.92 |   0.14 |
| -0.496 |   0.011 | -4.96 |   0.16 |
| -0.736 |   0.014 | -7.36 |   0.19 |
| -0.881 |   0.019 |  -9.0 |    0.3 |
|  -0.98 |    0.02 | -10.0 |    0.3 |
|  -1.13 |    0.02 | -11.5 |    0.3 |
|  -1.29 |    0.03 | -13.0 |    0.4 |

![Min Projected](Plots/Report_Plots/opamp_plot_min_projected.png)

| Chi2 | NDf | offset | slope |
|:----:|:----:|:----:|:----:|
| 0.6687 | 7 |0.0689833   +/-   0.0379935|   10.1601   +/-   0.136798 |

![Min Projected](Plots/Report_Plots/opamp_plot_projected.png)

Siccome la compatibilità tra i due coefficienti angolari è _ottima_, **&lambda; = 0.7**, procedo con un fit del dataset unificato con sia massimi che minimi.

## Fit Dataset Unificato

Ometto il dataset unificato perchè basta andarsi a guardare quelli sopra (con errori proiettati).

![All Projected](Plots/Report_Plots/opamp_plot_all_projected.png)

L'andamento dei residui non mi piace molto, sembra avere una specie di andamento parabolico. Eppure il coefficiente angolare del fit dei massimi e
quello dei minimi erano molto compatibili! Si nota anche che il nuovo coefficiente angolare è visibilmente diverso dai due coefficienti angolari
separati: probabilmente c'è qualche sistematica sotto!

_Ipotizzo che il problema stia nell'intercetta, e che quindi le due rette siano sfasate (abbiano un leggero offset). Per eliminare questo errore di
offset, che assumo costante su tutte le misure, provo ad effettuare un'analisi delle misure picco picco facilmente computabili come
V<sub>out</sub><sup>max</sup> - V<sub>out</sub><sup>min</sup> e V<sub>in</sub><sup>max</sup> - V<sub>in</sub><sup>min</sup>_.

## Dataset Picco-Picco

Partendo dalle misure effettuate in laboratorio ed all'errore ad esse associato, assembo il dataset di grandezze picco-picco. Successivamente effettuo
un fit preliminare per ricavare il coefficiente angolare e proiettare l'errore in modo analogo ai dataset precedenti.

### Data

| Vpp<sub>in</sub> (V)   | &sigma;<sub>Vpp<sub>in</sub></sub> (V) | Vpp<sub>out</sub> (V)   | &sigma;<sub>Vpp<sub>out</sub></sub> (V) |
|:-------:|:-------:|:-------:|:-------:|
| 0.208 |   0.004 |  1.97 |    0.03 |
| 0.504 |   0.008 |  4.96 |    0.08 |
| 0.800 |   0.014 |  7.92 |    0.14 |
| 0.992 |   0.015 |  9.92 |    0.16 |
| 1.480 |   0.019 | 14.8 |    0.2 |
| 1.79 |   0.03 | 18.0 |    0.3 |
| 1.99 |   0.03 | 19.9 |    0.3 |
| 2.29 |   0.03 | 22.9 |    0.3 |
| 2.58 |   0.04 | 26.0 |    0.4 |

### Fit Preliminare

![Piccopicco Preliminary](Plots/Report_Plots/opamp_plot_pp_preliminary.png)

| Chi2 | NDf | offset | slope |
|:----:|:----:|:----:|:----:|
| 0.294132 | 7 |-0.129779   +/-   0.0339771|   10.0921   +/-   0.0668321 |

### Proiezione Errori

| Vpp<sub>in</sub> (V)   | &sigma;<sub>Vpp<sub>in</sub></sub> (V) | Vpp<sub>out</sub> (V)   | &sigma;<sub>Vpp<sub>out, projected</sub></sub> (V) |
|:-------:|:-------:|:-------:|:-------:|
| 0.208 |   0.004 |  1.97 |    0.05 |
| 0.504 |   0.008 |  4.96 |    0.11 |
| 0.800 |   0.014 |  7.9 |    0.2 |
| 0.992 |   0.015 |  9.9 |    0.2 |
| 1.480 |   0.019 | 14.8 |    0.3 |
| 1.79 |   0.03 | 18.0 |    0.4 |
| 1.99 |   0.03 | 19.9 |    0.4 |
| 2.29 |   0.03 | 22.9 |    0.5 |
| 2.58 |   0.04 | 26.0 |    0.5 |

### Fit

![Piccopicco Projected](Plots/Report_Plots/opamp_plot_pp_projected.png)

| Chi2 | NDf | offset | slope |
|:----:|:----:|:----:|:----:|
| 0.147273 | 7 |-0.129672   +/-   0.0539787|   10.0921   +/-   0.0961865 |

Si nota come ora i residui siano ben distribuiti, nonostante le barre d'errore siano veramente enormi...

## Simulazioni MonteCarlo

