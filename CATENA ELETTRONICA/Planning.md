# Lab Session 23/11/2020

## Planning of the 1st Day

### PRE-AMPLIFICATORE

Assembo il circuito in figura

![PreAmp Circuito](./Simulations/PreAmp/PreAmp_circuit.png)

* Imposto sul CH1 del generatore un **impulso** quadrato.
  * Frequenza 1kHz
  * Durata T = 5&mu;s
  * Vlow = 0V
  * Vhigh = -1V _negativo_ (molto importante)

* SCELGO R<sub>in</sub> TRA 45k&Omega; E 85k&Omega;
  * Calcolo Q<sub>in</sub> = T * V / R<sub>in</sub>
* SCELGO C<sub>f, pre</sub> TRA 160pF E 350pF
* SCELGO R<sub>f, pre</sub> TRA 500k&Omega; E 1000k&Omega;
  * Calcolo il tempo caratteristico &tau;<sub>pre</sub> = R<sub>f, pre</sub>  * C<sub>f, pre</sub> atteso
  * Calcolo il valore di tensione massimo V<sub>pre</sub><sup>MAX</sup> = Q<sub>in</sub> / C<sub>f, pre</sub> = ( T * V
    ) / ( R<sub>in</sub> * C<sub>f, pre</sub> ) atteso

Il circuito è un integratore invertente: impostando sul generatore una tensione negativa ottengo in output un segnale
positivo _acquisibile direttamente con Arduino_.

* Simulazione della risposta del circuito raffigurato sopra al segnale impulso negativo:

![PreAmp Simulazione](./Plots/PreAmp_preliminary_simulation.png)

* Verifico con l'oscilloscopio l'effetto di integrazione della carica e il successivo smorzamento esponenziale. 
* Confronto il valore massimo di tensione atteso con quello misurato.

#### Verifica Linearità

Misuro la tensione massima in uscita al variare della durata dell'impulso in ingresso, cioè al variare della carica
iniettata. Eseguo alcune misure partendo da T = 2&mu;s fino a T = 10&mu;s circa.

Contruisco il grafico V<sub>pre</sub><sup>MAX</sup> vs Q<sub>in</sub> e fitto con una retta per vedere se è lineare.

#### Tempo Caratteristico

Analizzo la fase di scarica del segnale: imposto T = 5&mu;s e acquisisco la forma d'onda con Arduino. Stimo
approssimativamente il lab il tempo caratteristico per vedere che sia ragionevole &rarr; come? Tempo di dimezzamento per
qualche tipo di logaritmo o radice di due? 

#### Risposta in Frequenza (molto importante)

Faccio variare la frequenza tra 10Hz e 1MHz e costruisco il grafico di Bode. Verificare il comportamento da circuito
integratore e filtro passa basso.

Confronto i risultati con la simulazione Spice

![PreAmp Simulazione](./Plots/PreAmp_preliminary_bode_simulation.png)