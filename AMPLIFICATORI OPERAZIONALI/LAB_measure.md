# Data 1st Lab Session

## 28/10/20 - 29/10/20

### Misura diretta delle resistenze

Ho usato il multimetro _Metrix_ con le pinze 

| Resistenza |      Valore     |      F.S.     |
|:------------:|:-----------------:|:---------------:|
|     R<sub>f</sub>     | 82.462 k&Omega; |  100 k&Omega; |
|     R<sub>1</sub>     | 8.0894 k&Omega; |   10 k&Omega; |
|     R<sub>3</sub>     |  46.54 &Omega;  |    1 k&Omega; |

Notare R<sub>f</sub> > R<sub>1</sub> come richiesto (circa 10 volte più grande!).

Calcolo l'amplificazione attesa: G = - R<sub>f</sub> / R<sub>1</sub> = -10.19383 ~ -10.2 dove il segno meno deriva dalla configurazione invertente
dell'operazionale.

### Misura dell'amplificazione

Applico ora una tensione sinusoidale di frequenza f = 1 kHz: faccio variare l'ampiezza del segnale e registro i massimi e i minimi per entrambi i
segnali V<sub>in</sub> e V<sub>out</sub>

#### Misure dei Massimi

| V<sub>in</sub> |  V<sub>out</sub> | FS V<sub>in</sub> | FS V<sub>out</sub> |    Tensione Generatore |
|:-------------:|:--------------:|:--------:|:------------:|:--------------:|
| 106 mV      | 997 mV       | 50mV   | 324 mV     | 0.20 Vpp     |
| 252 mV      | 2.48 V       | 100 mV | 1.00 V     | 0.50 Vpp     |
| 400 mV      | 4.00 V       | 200 mV | 2.00 V     | 0.80 Vpp     |
| 496 mV      | 4.96 V       | 200 mV | 2.00 V     | 1.00 Vpp     |
| 744 mV      | 7.44 V       | 200 mV | 2.00 V     | 1.50 Vpp     |
| 907 mV      | 8.98 V       | 324 mV | 3.40 V     | 1.80 Vpp     |
| 1.01 V      | 9.93 V       | 324 mV | 3.40 V     | 2.00 Vpp     |
| 1.16 V      | 11.4 V       | 376 mV | 3.80 V     | 2.30 Vpp     |
| 1.29 V      | 13.0 V       | 436 mV | 4.52 V     | 2.60 Vpp     |
| 1.50 V      | 14.4 V       | 480 mV | 4.52 V     | 3.00 Vpp     |

#### Misure dei Minimi

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
| -1.48 V    | - 14.1 V    | 480 mV | 4.52 V     |  3.00 Vpp     |

NOTA: Impostando una tensione sul generatore pari a 3 Vpp inizia a vedersi la saturazione del segnale in uscita!

### Plots

Seguono i plot delle misure dei massimi e delle misure dei minimi, con i rispettivi grafici dei residui.

**NB gli errori devono ancora essere stimati: i plot servono per capire se l'andamento è quello che mi aspetto**

![Plot Max](Plots/opamp_max_plot.png)

![Res Max](Plots/opamp_max_res.png)

![Plot Min](Plots/opamp_min_plot.png)

![Res Min](Plots/opamp_min_res.png)

### Fit Results

**Analisi PROVVISORIA senza tenere conto delle incertezze sulle misure**

I dati inseriti nelle seguenti tabelle sono esattamente quelli restituiti da ROOT, non sono state fatte approssimazioni di alcun tipo fino ad ora.

* #### Massimi
  
| Chi2 | NDf | offset | slope |
|:----:|:----:|:----:|:----:|
|0.241668| 8 | 0.0698892   +/-   0.112246 |  9.77598   +/-   0.124436 |
 
* #### Minimi

| Chi2 | NDf | offset | slope |
|:----:|:----:|:----:|:----:|
|0.569592| 8 |  -0.0731234   +/-   0.172501 |  9.87495   +/-   0.19411  |

### Commenti

Il coefficiente angolare delle rette è leggermente più piccolo dell'amplificazione che mi aspettavo: forse rimuovendo il punto in saturazione viene
meglio! 

Dai residui si vede palesemente che il punto in saturazione non rispetta l'andamento lineare degli altri punti.

L'offset della retta è """"compatibile con lo zero"""" quindi si può pensare di effettuare un fit con un solo parametro del tipo *y = mx* per ottenere
maggiori informazioni sul coefficiente angolare.

I chi2 non sono significativi in quanto non sono stati presi in considerazioni gli errori sulle misure.

### Propagazione degli Errori

* #### Misure dirette delle Resistenze
  
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

* #### Stima dell'Amplificazione attesa

  Usando ora le incertezze sulle misure delle resistenze posso stimare l'errore della stima dell'amplificazione attesa. La formula di propagazione è quindi
  
  ![Amplification propagation](LaTeX_equation/amplification_propagation.png) 

  Si trova allora che l'amplificazione attesa è _in modulo_ **G = 10.194 +/- 0.006**.

* #### Misure con i Cursori

  Alle misure _di tensione_ acquisite con i cursori dell'oscilloscopio si associa la seguente incertezza:

  ![Cursors propagation](LaTeX_equation/cursors_propagation.png)

  * ##### Massimi

    | Vin    | Vout    | FS Vin | FS Vout | err Vin | err Vout |
    |--------|---------|--------|---------|---------|----------|
    | 0,1060 |  0,9970 |  0,050 |   0,324 |  0,0026 |   0,0198 |
    | 0,2520 |  2,4800 |  0,100 |   1,000 |  0,0055 |   0,0546 |
    | 0,4000 |  4,0000 |  0,200 |   2,000 |  0,0100 |   0,1000 |
    | 0,4960 |  4,9600 |  0,200 |   2,000 |  0,0109 |   0,1092 |
    | 0,7440 |  7,4400 |  0,200 |   2,000 |  0,0137 |   0,1373 |
    | 0,9070 |  8,9800 |  0,324 |   3,400 |  0,0188 |   0,1914 |
    | 1,0100 |  9,9300 |  0,324 |   3,400 |  0,0199 |   0,2017 |
    | 1,1600 | 11,4000 |  0,376 |   3,800 |  0,0230 |   0,2288 |
    | 1,2900 | 13,0000 |  0,436 |   4,520 |  0,0260 |   0,2659 |
    | 1,5000 | 14,4000 |  0,480 |   4,520 |  0,0296 |   0,2817 |


  * ##### Minimi
  
    | Vin     | Vout     | FS Vin | FS Vout | err Vin | err Vout |
    |---------|----------|--------|---------|---------|----------|
    | -0,1020 |  -0,6750 |  0,050 |   0,324 |  0,0025 |   0,0164 |
    | -0,2520 |  -2,4800 |  0,100 |   1,000 |  0,0055 |   0,0546 |
    | -0,4000 |  -3,9200 |  0,200 |   2,000 |  0,0100 |   0,0993 |
    | -0,4960 |  -4,9600 |  0,200 |   2,000 |  0,0109 |   0,1092 |
    | -0,7360 |  -7,3600 |  0,200 |   2,000 |  0,0136 |   0,1363 |
    | -0,8810 |  -8,9800 |  0,324 |   3,400 |  0,0185 |   0,1914 |
    | -0,9840 | -10,0000 |  0,324 |   3,400 |  0,0196 |   0,2025 |
    | -1,1300 | -11,5000 |  0,376 |   3,800 |  0,0227 |   0,2299 |
    | -1,2900 | -13,0000 |  0,436 |   4,520 |  0,0260 |   0,2659 |
    | -1,4800 | -14,1000 |  0,480 |   4,520 |  0,0294 |   0,2782 |