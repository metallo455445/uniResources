# Funzionamento

## Requisiti

- avere python installato
- avere installato le seguenti librerie <br>
    **cv2** ---> pip install opencv-python <br>
    **numpy** ---> pip install numpy <br>
    **matplotlib** ---> pip install matplotlib<br>
    **scipy** ---> pip install scipy<br>
- foto della catenaria
- pazienza

## Come eseguire il programma

### 1. Scaricare il pacchetto

Il programma è formato da due codici python distinti: [catenaria](catenaria.py) e [FITcatenaria](FITcatenaria.py). Conviene scaricare entrambi i codici e metterli nella stessa cartella. <br>

- [catenaria](catenaria.py) prende l'immagine fornita, la ripulisce da errori dovuti alla luce, rileva i bordi e crea un file [coord.txt](coord.txt) dove all'interno inserisce i punti rilevati della catena <br>
- [FITcatenaria](FITcatenaria.py) legge il file [coord.txt](coord.txt) e esegue il FIT restituendo il grafico, i residui e il chi^2 <br>

### 2. Pima esecuzione di [catenaria](catenaria.py)
Come scritto anche nella **prima riga di ogni codice .py** per eseguire il codice bisogna andare sul terminale e inviare il seguente comando

    py catenaria.py <"percorso_file_immagine"> <"N_bordi"> coord.txt

Un esempio di utilizzo di questo comando è il seguente

    py catenaria.py catenaTerraPulita.png 20 coord.txt

In questo caso ho eseguito il codice python nella stessa cartella nel quale è contenuto. La prima volta che viene Runnato [catenaria](catenaria.py) non è importante il valore di *"N_bordi"* (consiglio di metterlo ad 1). <br>
La prima volta che viene eseguito [catenaria](catenaria.py) serve principalmente a capire se si è settato correttamente il comando di esecuzione; se tutto è andato bene verranno aperte diverse finestre di *matplotlib* (molte sono di debugging, non davvero interessanti...), quelle su cui porre l'attenzione sono: "*Tutti i contorni*" e "*Top **n** contorni*" . Il primo mostra in verde tutti i contorni rilevati dal programma, la catena deve essere competamente verde (in caso contrario bisogna cambiare immagine oppure vedere [puliia_approfondita](#migliorare-la-qualità-dei-bordi)); il secondo mostra i *"N_bordi"* più grandi rilevati dal programma (per l'esempio di prima, mostrerà i 20 contorni più grandi). 

### 3. Eseguire per completare la catena
Questo punto è abbastanza autoesplicativo, si continua a inviare il comando

    py catenaria.py <"percorso_file_immagine"> <"N_bordi"> coord.txt

incrementando di volta in volta "*N_bordi*" finchè la finestra "*Top **n** contorni*" non colora di verde tutta la catena

### 4. Pulizia deggli errori
Arrivati a questo punto, molto probabilmente, nella finestra "*Top **n** contorni*" non sarà colorata di verde solo la catena ma anche dei punti extra che ovviamnete costituiscono un errore, bisogna fare quindi pulizia di questi punti.<br>

Se si guarda l'output sul terminale del comando appena inviato si può leggere una voce simile a questa

    ID dei top 9 contorni: [86, 89, 87, 192, 25, 26, 102, 37, 130]

A questo punto si deve andare nel codice di [catenaria](catenaria.py), attono alla riga *181* si leggerà un commento del tipo

    #INCOLLA QUI I getCoord()

dalla riga seguente a questa bisogna richiamare la funzione "*getCoord(Id)*" tante volte quanti sono gli ID di stampati dal teminale e inserendo il valode dell'identificativo all'interno delle parentesi. Seguendo lo stesso esempio

    getCoord(86)
    getCoord(89)
    getCoord(87)
    getCoord(192)
    getCoord(25)
    getCoord(26)
    getCoord(102)
    getCoord(37)
    getCoord(130)

A questo punto bisogna **salvare il codice** e rimandare il comando 

    py catenaria.py <"percorso_file_immagine"> <"N_bordi"> coord.txt

Verranno aperte più finestre rispetto a prima (una per ogni bordo che si sta vedendo), quello che bisogna fare ora è guardare uno ad uno ogni grafico dei singoli contorni (si riconosce perché è di colore rosso e la finestra si chiama come l'ID del contorno che si sta vedendo) e cercare i contorni "sbagliati" (ovvero fuori dalla catena) e segnare (tipo su un pezzo di carta) gli ID di questi contorni.<br>
Una volta fatto questo lavoro per ogni contorno, tornare sul codice python [catenaria](catenaria.py) e eliminare le righe di "*getCoord(ID)*" con gli Id segnati in precedenza (ovvero quelli dei contorni "sbagliati").<br>
Fatto ciò salvare il codice python e rinviare il comando per l'ultima volta, ricontrollare che tutti i bordi siano solo ed esclusivamente della catena e se tutti i check sono andati a buon fine si può passare al seguente punto.

### 5. Fit dei dati
Arrivati a questo punto il file [coord.txt](coord.txt) sarà pieno di dati, è arrivata l'ora di analizzarli.Eseguire sul terminale il seguente codice

    py FITcatenaria.py coord.txt  

Se tutto ha funzionato al meglio si aprirà la finestra con il Fit del grafico della catenaria. <br>
Sul terminale verranno stampate diverse voci tra le quali: "*chi2*" e "*Gradi di libertà*"

# Extra

## Migliorare la qualità dei bordi

Può capitare che quando viene eseguito [catenaria](catenaria.py) nella finestra "*Tutti i bordi*" la catena non venga colorata totalmente di verde, questo vuol dire che il programma non riesce a leggere bene l'immagine (dovuto, nella maggior parte dei casi, alla presenza di oggetti nello sfondo che si "confondono" con la catena). Per ovviare a ciò si può provare a modificare la [riga 67](https://github.com/metallo455445/uniResources/blob/3e8dcdbd2da2447eb01687aafab32d8d6d26af0b/catenaria/catenaria.py#L67) di [catenaria](catenaria.py):

    ret, thresh = cv.threshold(edgesPURE, 127, 255, 0)

modificare la voce "*edgesPURE*" con "*edges*" (nel dettaglio: i bordi vengono rilevati dopo una pulizia attraverso un filtro Gaussiano). Questa tecnica **non funziona il 100% delle volte**, se non dovesse funzionare è necessario cambiare l'immagine di partenza con una meno rumorosa.<br>

*Suggerimenti*<br>
Per evitare il rumore nella foto di partenza mettersi su uno sfondo bianco, è consigliabile utilizzare luci parallele alla fotocamera in modo tale da ridurre le ombre della catena sullo sfondo. Se necessario eliminare le parti pià rumorose attravrso un tool grafico come [photopea](photopea.com)
