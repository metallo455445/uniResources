import sys
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Raccogliamo i nomi dei file passati come argomento
    # Esempio comando: python app.py fotoREADME.jpg immagine2.png
    if len(sys.argv) > 1:
        nomi_file = sys.argv[1:] 
    else:
        nomi_file = [] # Nessun file passato
        
    # Passiamo la lista (l'array) direttamente al template, non il codice HTML
    return render_template('index.html', immagini=nomi_file)

if __name__ == '__main__':
    app.run(debug=False)