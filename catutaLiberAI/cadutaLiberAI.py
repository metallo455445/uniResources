import cv2
import matplotlib.pyplot as plt

# --- MODIFICA SOLO QUESTA SEZIONE ---
# Usiamo i percorsi della versione V2 appena scaricata
config_file = 'ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
frozen_model = 'ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb'
labels_file = 'coco.names'
img_path = 'aplle.jpg' 
# ------------------------------------

# Caricamento del modello
model = cv2.dnn_DetectionModel(frozen_model, config_file)

# Caricamento Labels
classLabels = []
try:
    with open(labels_file, 'rt') as fpt:
        classLabels = fpt.read().rstrip('\n').split('\n')
except FileNotFoundError:
    print("Errore: File coco.names non trovato.")
    exit()

# Parametri standard per MobileNet V2 (simili a V3)
model.setInputSize(300, 300)
model.setInputScale(1.0 / 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

# ... IL RESTO DEL CODICE RIMANE UGUALE ...
img = cv2.imread(img_path)
if img is None:
    print(f"Errore caricamento immagine: {img_path}")
else:
    classIndex, confidence, bbox = model.detect(img, confThreshold=0.5) #da 0.5 a 0.1
    
    # STAMPA DI DEBUG FONDAMENTALE
    print(f"DEBUG: Oggetti rilevati: {len(classIndex)}")

    if len(classIndex) > 0:
        for classInd, conf, boxes in zip(classIndex.flatten(), confidence.flatten(), bbox):
            # 1. Disegna il rettangolo VERDE (0, 255, 0) invece che BLU (255, 0, 0)
            cv2.rectangle(img, boxes, (0, 255, 0), 2)
            
            # Gestione dell'indice (MobileNet V2 su COCO a volte parte da 0, a volte da 1)
            # Se le etichette sembrano sbagliate (es. scambia persona per bicicletta), togli il -1
            label_index = classInd - 1 
            
            if label_index < len(classLabels):
                nome_oggetto = classLabels[label_index]
            else:
                nome_oggetto = f"Obj {classInd}"

            # Testo da stampare sull'immagine
            label_text = f"{nome_oggetto}: {conf:.2f}"
            
            # 2. STAMPA A CONSOLE la posizione e l'oggetto
            x, y, w, h = boxes
            print(f"Trovato: {nome_oggetto} | Confidenza: {conf:.2f} | Posizione: x={x}, y={y}, w={w}, h={h}")

            # Scrive il testo sopra il rettangolo (in verde anche questo)
            cv2.putText(img, label_text, (boxes[0], boxes[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    plt.figure(figsize=(10,10))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    plt.axis('off')
    plt.show()