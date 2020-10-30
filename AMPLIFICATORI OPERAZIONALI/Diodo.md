# Diodo 

## 30/10

### Materiali Semiconduttori

La corrent totale nel diodo è la somma del contributo di drift e di diffusione

### Diodo a Giunzione p-n

Costruito partendo da un cristallo n-type e drogando intensamente un lato con un accettore in modo che diventi un p-type. Si crea un cristallo di tipo
p-n! Questo porta un forte gradiente di concentrazione e mi aspetto una forte corrente di diffusione!

Gli elettroni quasi liberi tenderanno a migrare nel lato p mentre le lacune verso il lato n &rarr; corrente di drift

L'accumulo di cariche genera allora un campo elettrico, a cui sarà associata una corrente di drift in direzione opposta &rarr; bilancio la corrente di
diffusione e arrivo ad una condizione di equilibrio.

#### Regione di svuotamento

L'estensione della regione svuotata è inversamente proporzionale al drogaggio. Nella pratica spesso c'è una differenza anche di un fattore 100 quindi
approssimativamente la regione svuotata è tutta da una parte!

Ho un blocco di conduzione dovuto ad una barriera potenziale che viene generata naturalmente: la situa peggiora/migliora (a seconda di come metto il
diodo perchè cambia la direzione del campo elettrico esterno) quando attacco il diodo ad un circuito
perchè ci butto dentro un campo elettrico ulteriore!

#### In Polarizzazione Diretta

Collego il polo positivo dalla parte p e il polo negativo dalla parte n: tiro via la barriera di potenziale quindi gli elettroni volano verso la zona
p ma risultano essere minoritari e si accumulano ai lati della giunzione &rarr; situazione di non equilibrio: accumulo con grande gradiente &rarr;
viene innescata la corrente di diffusione!

Le lacune si spostano sul lato n e succede la stessa roba quindi viene innescato nuovamente il processo di diffusione.

_La corrente totale è praticamente tutta corrente di diffusione in prossimità della giunzione e tutta corrente di drift lontano da questa_

Ho una dipendeza complessa dalla temperatura (non lineare), che si ritrova nelle quantità

* V<sub>T</sub> = kT/q 
* I<sub>s</sub>

Applicazione comune: *termometro digitale*

#### In Polarizzazione Inversa

La corrente inversa è associata alla produzione termica di coppie (e<sup>-</sup>, h<sup>+</sup>)

Il fenomeno di breakdown è causato da due meccanismi principali

* Effetto Valanga: aumento della tensiore inversa &rarr; aumento della barriera di potenziale
* Effetto Zener (quantistico): si vede in diodi molto drogati &rarr; effetto tunnel di elttroni di valenza dal lato p direttamente a livello della
  banda di conduzione del lato n generando ulteriori coppie che contribuiscono alla corrente

#### Capacità della Giunzione

In polarizzazione diretta l'accumulo dei portatori minoritari ai bordi della regione di svuotamento determina una carica non nulla sui due lati con
una conseguente capacità C<sub>diff</sub> (capacità di diffusione, dipende dalla corrente che circola nel diodo e può diventare molto grande).

In polarizzazione inversa ho due ditrubuzioni di carica spaziale opposte affaciante &rarr; avrò quindi una capacità C<sub>j</sub> dipendente dal
voltaggio.

