# orbitorbit

![Alt text](/funCodes/orbitorbit/sprites/image.png)

Programma per simulare o visualizzare il comportamento di orbite, come ad esempio oggetti in movimento intorno a un corpo centrale.

## Descrizione

Il programma calcola la posizione e la traiettoria di uno o più corpi in orbita, gestendo parametri come la velocità, la distanza e l'attrazione gravitazionale. Riporta inoltre i valori i momento totale e di neergia per verificarne la conservazione (come ci si aspetta dalla teoria). Può essere pensato per studiare il moto orbitale in un contesto fisico semplificato o per rappresentare graficamente il percorso di un corpo celeste.

## Librerie necessarie

- numpy (per i calcoli numerici)
- matplotlib (per la visualizzazione delle orbite)
- scipy (usato per la costante numerica G)

## Come farlo funzionare

All'inerno del codice è presente una lista intorno alla riga 50

```py
# !!! IMPOSTAZIONE DELLA SIMULAZIONE !!!
particelle = [ <...> ]
```

Inserire qui tutte le particelle che si vuole seguendo la seguente sintassi

```py
Particella(
    nome="",             # Inserisci il nome come stringa es. "M1")
    massa=,              # Inserisci il valore della massa (float)
    posizione=(0,0,0),   # Modifica le coordinate (x, y, z)
    velocita=(0,0,0)     # Modifica i vettori velocità (vx, vy, vz)
)
```

Il seguente esempio permette di simulare due corpi:

- un corpo più massivo, centrato nell'origine e inizilmente fermo
- un corpo di massa trascurabile rispetto al primo, ad una distanza di 5[u.a.] dall'origine e con una velocità iniziale da permettergli di fare un'orbita circolare attorno al altro corpo

```py
particelle = [
    Particella("P1", massa=2.0 * 10**12, posizione=(0,0,0), velocita=(0,0,0)), 
    Particella("P2", massa=10.0 * 10**11, posizione=(5.0,0,0), velocita=(0, np.sqrt((constants.G * 2.0 * 10**12) / 5.0), 0))
]
```

## Per i più nerd

Si possono modifiare queste variabili per approfondire il codice (attualmente l'energia ha qualche problema :/)

```py
# Impostazioni grafiche
axis_limits = (-8, 8)

# on/off per visualizzare energia e momento angolare
visualizza_energia = False
visualizza_momento_angolare = False

```