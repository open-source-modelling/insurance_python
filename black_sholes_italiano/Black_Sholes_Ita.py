import numpy as np
import pandas as pd

def simulazione_Black_Scholes(S0, mu, sigma, T, dt) -> pd.DataFrame:
    """Simula una serie temporale di prezzi delle azioni utilizzando il modello log-normale di Black-Scholes.

    Argomenti:
        S0 (int): Valore iniziale dell'attivo sottostante.
        mu (float): Tasso di drift dell'attivo sottostante.
        sigma (float): Deviazione standard del rendimento dell'attivo sottostante.
        T (int): Tempo massimo di modellazione.
        dt (float): Lunghezza di ogni sottointervallo.

    Returns:
        pd.DataFrame: DataFrame N x 2 con l'indice che representa il tempo di modellazione e i valori come realizzazioni del prezzo dell'attivo sottostante.

    Esempio:
        Modella il prezzo di un'azione che vale oggi 100. Il mercato ha un tasso di interesse privo di rischio annualizzato futuro del 5% e una volatilità annualizzata del 30%. L'utente è interessato a una proiezione del prezzo per i prossimi 10 anni con incrementi di 6 mesi (0,5 anni).

        import pandas as pd
        import numpy as np
        simulate_Black_Scholes(100, 0.05, 0.3, 10, 0.5)

        Output:
               Prezzo Azione
        Tempo
        0.0     100.000000
        0.5     131.721286
        1.0     124.924654
        1.5     209.302935
        2.0     222.085955
        ...     ...
        9.5    202.368581
        10.0   262.282989

    Riferimento:
        Per ulteriori informazioni, consulta: https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
    """
    
    N = int(T / dt)

    time, delta_t = np.linspace(0, T, num = N+1, retstep = True)
    
    S = np.exp((mu - sigma ** 2 / 2) * dt + sigma * np.random.normal(0, np.sqrt(dt), size= N))
    S = np.hstack([1, S])
    S = S0* S.cumprod(axis=0)

    dict = {'Tempo' : time, 'Prezzo Azione' : S}

    prezzo_azzione_simulazione = pd.DataFrame.from_dict(data = dict)
    prezzo_azzione_simulazione.set_index('Tempo', inplace = True)

    return prezzo_azzione_simulazione
