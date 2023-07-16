<h1 align="center" style="border-botom: none">
  <b>
    🐍 
Modello di Black-Scholes per simulare il prezzo di un'azione🐍     
  </b>
</h1>

Il modello di Black-Sholes è uno dei modelli originali per simulare l'evoluzione del mercato azionario.

## Problema

La modellazione del mercato azionario è un campo molto studiato. Esistono numerosi modelli, ognuno con i suoi vantaggi e svantaggi.

## Soluzione

Uno dei modelli piu usati e semplici è il modello di [Black-Sholes-Merton](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model), che assume che i prezzi di un azzione si evolvono con un processo dall'equazione di [Black-Sholes equation](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation). Questa implementazione simula il prezzo di un'azione nel tempo.

### Input

Parameteri legati alla simulazione di Black-Sholes:
 - `S0`    ... integer, il valore iniziale dell'attivo sottostante.
 - `mu`    ... float, il tasso di drift dell'attivo sottostante.
 - `sigma` ... float, deviazione standard del rendimento dell'attivo sottostante.
 - `T`     ... integer, il tempo massimo di modellazione. Es. se T = 2, il tempo di modellazione va da 0 a 2.
 - `dt`    ... float, lunghezza di ogni sottointervallo. Es. dt=10, ci saranno 10 intervalli di lunghezza 0.1 tra due interi di tempo di modellazione.
 - `rho`   ... float, il coefficiente di correlazione del Brownian motion. Es. rho = 0.4 significa che due  Brownian motions hanno un coefficiente di correlazione di 0.4.

### Output

Ritorno:
 - `prezzo_azzione_simulazione` ... N x 2 Pandas DataFrame con l'indice che representa il tempo di modellazione e i valori come realizzazioni del prezzo dell'attivo sottostante.

## Come iniziare

Modella il prezzo di un'azione che oggi vale 100. Il mercato ha un tasso di interesse privo di rischio annualizzato futuro del 5% e una volatilità annualizzata del 30%. L'utente è interessato a una proiezione del prezzo per i prossimi 10 anni con incrementi di 6 mesi (0,5 anni).

``` python
import pandas as pd
import numpy as np
from typing import Any
from Black_Sholes import simulate_Black_Scholes
print(simulazione_Black_Scholes(100, 0.05, 0.3, 10, 0.5))

    #   [out] = Tempo    Prezzo Azione               
    #       0.0    100.000000
    #       0.5    131.721286
    #       1.0    124.924654
    #       1.5    209.302935
    #       2.0    222.085955
    #       2.5    208.085678
    #       3.0    165.550253
    #       3.5    239.512165
    #       4.0    176.886669
    #       4.5    148.687363
    #       5.0    181.235262
    #       5.5    164.280753
    #       6.0    172.861576
    #       6.5    170.698562
    #       7.0    141.613940
    #       7.5    121.070316
    #       8.0    116.508183
    #       8.5    104.524616
    #       9.0    146.124924
    #       9.5    202.368581
    #       10.0   262.282989
```
## Risk neutral pricing
Questo esempio presenta un test semplice per confermare che gli scenari siano generati in un modo risk neutral, avendo un output di simulazione ESG. Questo test si basa sul fatto che in un contesto risk neutral, esiste una relazione esplicita tra il prezzo di uno strumento finanziario a reddito fisso e i flussi di cassa scontati attesi.

Di seguito è riportato il test di Martingala per l'esempio ipotetico precedente. Per superare il test, i flussi di cassa scontati attesi devono essere uguali al prezzo iniziale dell'azione di 100.

``` python
import numpy as np
from Black_Sholes import simulazione_Black_Scholes

r = 0.05
dt = 0.5
t = 10
S = 100
sigma = 0.3
bank_end = np.exp(t*r) # reddito senza rischio
nIter = 500000
result = np.zeros(nIter)

for iter in range(1,nIter):
    out = simulazione_Black_Scholes(S, r, sigma, t, dt)
    martingale = out.values[-1] / bank_end
    result[iter] = martingale

print(np.mean(result))
#   [out] = 99.8743118539787                

```

