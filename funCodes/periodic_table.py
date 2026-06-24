import os
# Diciamo a OpenCV di usare X11 senza lamentarsi
os.environ["QT_QPA_PLATFORM"] = "xcb"

import cv2
import time
import sys

timer = 5

if sys.orig_argv[2] == 0:
    timer = 5
else:
    timer = sys.orig_argv[2]
    
timer = float(timer)

# 1. Carica l'immagine (inserisci il percorso corretto della tua immagine)
percorso_immagine = '/home/matteo/Documenti/uni/lab/funCodes/notatableatall.jpeg'
immagine = cv2.imread(percorso_immagine)

def mostra():
    # 2. Crea la finestra e mostra l'immagine
    cv2.imshow('Flash', immagine)

    # 3. Aspetta il tempo minimo possibile (1 millisecondo)
    # cv2.waitKey(1) permette al sistema di renderizzare la finestra,
    # aspetta 1 millisecondo, e poi passa all'istruzione successiva.
    cv2.waitKey(200) 

    # 4. Chiude subito la scheda/finestra
    cv2.destroyAllWindows()

# Controlla se l'immagine è stata caricata correttamente
if immagine is None:
    print("Errore: Immagine non trovata.")
else:
    mostra()
    while True:
        start_time = time.time()

        while time.time() - start_time < timer:
            pass
        mostra()