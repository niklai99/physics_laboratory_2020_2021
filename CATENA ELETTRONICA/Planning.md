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

![PreAmp Simulazione](./Plots/PreAmp/Preliminary/PreAmp_preliminary_simulation.png)

* Verifico con l'oscilloscopio l'effetto di integrazione della carica e il successivo smorzamento esponenziale. 
* Confronto il valore massimo di tensione atteso con quello misurato.

#### Verifica Linearità

Misuro la tensione massima in uscita al variare della durata dell'impulso in ingresso, cioè al variare della carica
iniettata. Eseguo alcune misure partendo da T = 2&mu;s fino a T = 10&mu;s circa.

Contruisco il grafico V<sub>pre</sub><sup>MAX</sup> vs Q<sub>in</sub> e fitto con una retta per vedere se è lineare.

#### Tempo Caratteristico

Analizzo la fase di scarica del segnale: imposto T = 5&mu;s e acquisisco la forma d'onda con Arduino. Stimo
approssimativamente il lab il tempo caratteristico per vedere che sia ragionevole &rarr; metto il cursore due a livello
asintotico di smorzamento, misuro il massimo e faccio V<sub>pre</sub><sup>MAX</sup> / e &rarr; metto il cursore 1 a
livello V(&tau;) e guardo dove interseca la traccia del segnale &rarr; il tempo t segnato da M Pos in alto a destra è &tau;

#### Risposta in Frequenza (molto importante)

Faccio variare la frequenza tra 10Hz e 1MHz e costruisco il grafico di Bode. Verificare il comportamento da circuito
integratore e filtro passa basso.

Confronto i risultati con la simulazione Spice

![PreAmp Simulazione](./Plots/PreAmp/Preliminary/PreAmp_preliminary_bode_simulation.png)

# Lab Session 25/11/2020

## Planning of the 2nd Day

### SHAPER CR-RC

Assemblo il circuito in figura

![PreAmp Circuito](./Simulations/Shaper/Shaper_circuit.png)

* Imposto sul CH1 del generatore un'onda quadra.
  * Frequenza 100Hz
  * Vlow = 0V
  * Vhigh = 1V 

* SCELGO R<sub>1sh</sub> = R<sub>2sh</sub> TRA 90k&Omega; E 160k&Omega;
* SCELGO C<sub>1sh</sub> = C<sub>2sh</sub> TRA 90pF E 160pF

* Calcolo il tempo caratteristico &tau;<sub>sh</sub> = R<sub>1sh</sub>C<sub>1sh</sub> = R<sub>2sh</sub>C<sub>2sh</sub>

* **EFFETTUO LE SEGUENTI MISURE**
  * Valore del massimo V<sub>sh</sub><sup>MAX</sup> _CHE DEVE ESSERE V<sub>in</sub> / e_
  * Tempo in cui viene assunto il massimo t<sub>sh</sub><sup>MAX</sup> _CHE DEVE ESSERE PROPRIO &tau;<sub>sh</sub>_

* Registro ora una forma d'onda con Arduino

* Studio la risposta in frequenza da 10Hz a 1MHz

#### ATTACCO IL PREAMPLIFICATORE IN INGRESSO ALLO SHAPER

Devo ripristinare le condizioni del PreAmp per verificare che funzioni: IMPULSO QUADRATO T = 5us f = 1kHz Vlow = 0V
Vhigh = -1V

* Prendo nota della tensione massima V<sub>pre</sub><sup>MAX</sup> in uscita dal preamplificatore
* Misuro il massimo V<sub>sh</sub><sup>MAX</sup> del segnale in uscita, il tempo in cui viene raggiunto e il massimo di undershoot
* Calcolo il valore di R<sub>pz</sub> per compensare l'effetto &rarr; R<sub>pz</sub> = &tau;<sub>pre</sub> / C<sub>1sh</sub>
  * Ricordo che, teoricamente, &tau;<sub>pre</sub> = 161.486 +/- 6.493 &mu;s

Posso ora prendere Arduino sia senza sia con Rpz e ho finito per oggi.


# Lab Session 26/11/2020

## Planning of the 3rd Day

### CATENA COMPLETA

Assemblo un semplicissimo amplificatore non invertente per amplificare il segnale che esce dallo shaper. 

* Imposto sul generatore un impulso quadrato di durata T = 10 &mu;s con la solita ampiezza negativa
* Misuro il massimo del segnale in uscita dallo shaper
* Calcolo quanta amplificazione mi serve per avere 2V
* Uso le resistenze per ottenere tale amplificazione

#### Linearità della Catena Elettronica
Acquisisco con Arduino le forme d'onda al variare di T da 2&mu;s a 10&mu;s

* Prendo Vmax per ogni forma d'onda e costruisco il plot Vmax vs Qin come nel caso PreAmp
  
#### Risposta in Frequenza &rarr; THEBODE

#### EFfetto dello Shaping Time

Cambio le resistenza di shaping Rsh1 e Rsh2 con una coppia di valore ridotto in modo da modificare &tau;sh senza però
influenzare la compensazione di pole-zero.

* Acquisisco la forma d'onda con Arduino
  