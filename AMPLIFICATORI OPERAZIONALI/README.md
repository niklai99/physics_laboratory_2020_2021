# Planning 1st Lab Session

## 28/10/20 - 29/10/20

### Materiale e Strumentazione

* Circuito integrato TL082C &rarr; 2 amplificatori operazionali
* Resistenze e condensatori
* Alimentatore di tensione continua stabilizzato con 2 uscite tra 0 e 20 V e una fissa a 5 V
* Generatore di funzioni Tektronix AFG 1022
* Oscilloscopio digitale Tektronix TBS 1102B
* Multimetro digitale Metrix e Agilent
* Scheda Arduino Due

  **NB: USARE LE SONDE**

### Alimentazione dell'Operazionale

Collego l'operazionale alle alimentazioni

* V<sub>cc</sub> = +15 V
* V<sub>ee</sub> = -15 V

Collego due capacità da C = 0.1 $\mu$F tra le alimentazioni degli operazionali e la massa (però vicine all'operazionale!).

### 1) Funzione di Trasferimento per un amplificatore INVERTENTE

* Misuro con il multimetro le resistenze in dotazione, usando R<sub>f</sub> > R<sub>1</sub>!
* Assemblo il seguente circuito

<img src="LTSpice_Simulation/OpAmp/circuit_image.png" alt="Circuito" width="300"/>


