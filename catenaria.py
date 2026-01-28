import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import sys

#percorso file coordinate punti della parabola da fittare

coord_path = './lab/coord.txt'
open(coord_path, 'w').close()   #formatta il file delle coord prima di riscrivere


# Ottieni il percorso del file dall'argomento
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    contour_index = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    n_top_countours = int(sys.argv[3]) if len(sys.argv) > 2 else 5
else:
    file = input("Inserisci il nome del file: ")
    file_path = './lab/' + file
    contour_index = 4
    n_top_countours = 5

# Usa file_path ovunque
img = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
assert img is not None, f"file {file_path} could not be read, check file path/integrity"
img = cv.medianBlur(img,5)

ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)

titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]

plt.figure("Correzione impurezze")
for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

#edge detection partendo dall'immagine pura         <---
plt.figure("edge detection pura")
edges = cv.Canny(img, 100, 200)

edgesPURE = edges

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

#edge detection post pulizia dell'adattiva gaussiana
plt.figure("edge detection from gaussian")
edges = cv.Canny(th3, 100, 200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

# edges è già in scala di grigi
ret, thresh = cv.threshold(edgesPURE, 127, 255, 0)          #<--- ho messo qui il pure per evitare sporcizia
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Stampa informazioni sui contorni
print(f"Numero totale di contorni trovati: {len(contours)}")

# Carica l'immagine originale a colori
img_color = cv.imread(file_path)

if img_color is not None and len(contours) > 0:
    # Ordina i contorni per area (dal più grande al più piccolo)
    #contours_sorted = sorted(contours, key=cv.contourArea, reverse=True)           !!<-CHATGPT

    contours_sorted = sorted(
        enumerate(contours),
        key=lambda x: cv.contourArea(x[1]),
        reverse=True
    )
    
    # # Stampa le aree dei primi 10 contorni
    # print("\nAree dei primi 10 contorni (ordinati per dimensione):")
    # for i, cnt in enumerate(contours_sorted[:10]):
    #     area = cv.contourArea(cnt[1])                           ##CHATGPT ha sostituoito cnt con cnt[1]
    #     print(f"Contorno {i}: area = {area:.2f}")
    
    # Disegna TUTTI i contorni
    img_all_contours = img_color.copy()
    cv.drawContours(img_all_contours, contours, -1, (0,255,0), 2)
    
    plt.figure("Tutti i contorni")
    plt.imshow(cv.cvtColor(img_all_contours, cv.COLOR_BGR2RGB))
    plt.title(f'Tutti i {len(contours)} contorni')
    
    # Disegna i primi 5 contorni più grandi (escludendo eventualmente il bordo dell'immagine)
    img_top_contours = img_color.copy()
    # Salta il primo se è troppo grande (potrebbe essere il bordo)
    start_idx = 1 if len(contours_sorted) > 1 and cv.contourArea(contours_sorted[0][1]) > img.shape[0] * img.shape[1] * 0.9 else 0     ##CHAT GPT sostituisce contours_sorted[0] con contours_sorted[0][1]
    
    for i in range(start_idx, min(start_idx + n_top_countours, len(contours_sorted))):                    ## start_idx + 5 sostituito da me coon start_idx + n_top_countours
        cv.drawContours(img_top_contours, [contours_sorted[i][1]], 0, (0,255,0), 3)        ##CHATGPT sostituisce contours_sorted[i] con contours_sorted[i][1]
    
    # top_ids = [                           CHATGPT
    #     contours.index(contours_sorted[i])
    #     for i in range(start_idx, min(start_idx + 5, len(contours_sorted)))
    # ]

    # print("\nID dei top 5 contorni:", top_ids)

    top_ids = [idx for idx, _ in contours_sorted[start_idx:start_idx + n_top_countours]]              ## start_idx + 5 sostituito da me coon start_idx + n_top_countours
    print(f"\nID dei top {n_top_countours} contorni:", top_ids)



    plt.figure(f"Top {n_top_countours} contorni")
    plt.imshow(cv.cvtColor(img_top_contours, cv.COLOR_BGR2RGB))
    plt.title(f'Top {n_top_countours} contorni più grandi')
    
#####    

    # # Se vuoi ancora accedere a un contorno specifico
    # if len(contours) > contour_index:       
    #     cnt = contours[contour_index]                                        #<--|
    #     img_single = img_color.copy()

    #     #ottnego le coordinate di ciascun punto del contorno selezionato
    #     for point in contours[contour_index]:
    #         x = int(point[0][0])
    #         y = int(point[0][1])
    #         p = (x, y)
            
    #         print(f"Coord Point: {p}")
            
    #         # Disegna il cerchio usando la tupla pulita
    #         cv.circle(img_single, p, 2, (255, 0, 0), -1)

    #     cv.drawContours(img_single, [cnt], 0, (0,0,255), 3)                 #commentando questa riga si possono vedere i punti che poi verranno messi nel fit
    #     plt.figure(f"Contorno {contour_index}")
    #     plt.imshow(cv.cvtColor(img_single, cv.COLOR_BGR2RGB))
    #     plt.title(f'Contorno indice {contour_index} (rosso)')

#####
    def getCoord(indiceContornoTarget):
        print(f"Coords di contorno {indiceContornoTarget}")
        if len(contours) > indiceContornoTarget:       
            cnt = contours[indiceContornoTarget]
            img_single = img_color.copy()
            
            # Altezza dell'immagine per l'inversione
            height = img.shape[0] 

            for point in contours[indiceContornoTarget]:
                x_raw = int(point[0][0])
                y_raw = int(point[0][1])
                
                # INVERSIONE ASSE Y
                x = x_raw
                y = height - y_raw  # Ora 0 è il fondo dell'immagine
                
                p_plot = (x_raw, y_raw) # Per il disegno su OpenCV (che vuole ancora l'origine in alto)
                p_calc = (x, y)         # Per il salvataggio su file (piano cartesiano)
                
                #print(f"Coord Originale: ({x_raw}, {y_raw}) -> Corretta: {p_calc}")
                
                with open(coord_path, "a") as f:
                    f.write(f"{p_calc[0]} {p_calc[1]}\n")
                
                # Disegno (usa le coordinate originali altrimenti non vedi i punti sull'immagine)
                cv.circle(img_single, p_plot, 2, (255, 0, 0), -1)

            cv.drawContours(img_single, [cnt], 0, (0,0,255), 3)
            plt.figure(f"Contorno {indiceContornoTarget}")
            plt.imshow(cv.cvtColor(img_single, cv.COLOR_BGR2RGB))
            plt.title(f'Contorno {indiceContornoTarget} (Visualizzazione Standard)')
#####
    getCoord(86)
    getCoord(87)
    getCoord(89)
    getCoord(192)
    getCoord(25)
    getCoord(26)
    getCoord(102)
    getCoord(37)
    getCoord(130)
    getCoord(21)
    getCoord(201)
    #getCoord(206)          #Interferenza
    getCoord(172)
    #getCoord(55)           #Interferenza
    #getCoord(184)          #Interferenza
        
else:
    print("Impossibile caricare l'immagine a colori o nessun contorno trovato")

plt.show()