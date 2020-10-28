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

