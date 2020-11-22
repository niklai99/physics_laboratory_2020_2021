# Lab Session 23/11/2020

## Planning of the 1st Day

### PRE-AMPLIFICATORE

Assembo il circuito in figura

![PreAmp Circuito](./Simulations/PreAmp/PreAmp_circuit.png)

* Imposto sul CH1 del generatore un **impulso** quadrato.
  * Frequenza 1kHz
  * Durata 5&mu;s
  * Vlow = 0V
  * Vhigh = -1V _negativo_ (molto importante)

* SCELGO R<sub>in</sub> TRA 45k&Omega; E 85k&Omega;
  * Calcolo Q<sub>in</sub> = &Delta;t * V / R<sub>in</sub>
* SCELGO C<sub>f, pre</sub> TRA 160pF E 350pF
* SCELGO R<sub>f, pre</sub> TRA 500k&Omega; E 1000k&Omega;
  * Calcolo il tempo caratteristico &tau;<sub>pre</sub> = R<sub>f, pre</sub>  * C<sub>f, pre</sub> atteso
  * Calcolo il valore di tensione massimo V<sub>pre</sub><sup>MAX</sup> atteso

Il circuito è un integratore invertente: impostando sul generatore una tensione negativa ottengo in output un segnale
positivo _acquisibile direttamente con Arduino_.

* Simulazione della risposta del circuito raffigurato sopra al segnale impulso negativo:

![PreAmp Simulazione](./Plots/PreAmp_preliminary_simulation.png)

* Verifico con l'oscilloscopio l'effetto di integrazione della carica e il successivo smorzamento esponenziale. 
* Confronto il valore massimo di tensione atteso con quello misurato.