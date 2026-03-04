#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9  
#define SS_PIN  10 

MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

// RAM Archivio fissa a 64 blocchi (Max supportato dalla RAM dell'Uno)
byte datiClonati[64][16]; 
bool cartaInMemoria = false; 
byte blocchiSalvati = 0; // Tiene traccia di quanti blocchi abbiamo in pancia

enum StatoSistema { MENU_PRINCIPALE, IN_LETTURA, IN_SCRITTURA, VERIFICA_INFO };
StatoSistema statoAttuale = MENU_PRINCIPALE;

void stampaMenu() {  
  Serial.println(F("$$$$$$\\                            $$\\        $$$$$$\\  $$\\                                         "));
  Serial.println(F("$$  __$$\\                           $$ |      $$  __$$\\ $$ |                                        "));
  Serial.println(F("$$ /  \\__| $$$$$$\\   $$$$$$\\   $$$$$$$ |      $$ /  \\__|$$ | $$$$$$\\  $$$$$$$\\   $$$$$$\\   $$$$$$\\  "));
  Serial.println(F("$$ |       \\____$$\\ $$  __$$\\ $$  __$$ |      $$ |      $$ |$$  __$$\\ $$  __$$\\ $$  __$$\\ $$  __$$\\ "));
  Serial.println(F("$$ |       $$$$$$$ |$$ |  \\__|$$ /  $$ |      $$ |      $$ |$$ /  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \\__|"));
  Serial.println(F("$$ |  $$\\ $$  __$$ |$$ |      $$ |  $$ |      $$ |  $$\\ $$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |      "));
  Serial.println(F("\\$$$$$$  |\\$$$$$$$ |$$ |      \\$$$$$$$ |      \\$$$$$$  |$$ |\\$$$$$$  |$$ |  $$ |\\$$$$$$$\\ $$ |      "));
  Serial.println(F(" \\______/  \\_______|\\__|       \\_______|       \\______/ \\__| \\______/ \\__|  \\__| \\_______|\\__|  "));
  //Serial.println(F("Digita un comando e premi Invio:"));
  Serial.println(F("                                                                                       powered by Theò"));
  Serial.println(F(" [L] - Verifica tipo e capacita' della carta"));
  Serial.println(F(" [R] - Leggi e salva una carta (Doppia Verifica)"));
  if (cartaInMemoria) {
    Serial.println(F(" [W] - Scrivi i dati salvati su una carta vuota"));
    Serial.println(F(" [D] - Mostra i dati attualmente in memoria (Dump)"));
  }
  Serial.println(F("=========================================\n"));
}

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;
  stampaMenu();
}

void loop() {
  // 1. GESTIONE COMANDI SERIALI
  if (Serial.available() > 0 && statoAttuale == MENU_PRINCIPALE) {
    char comando = Serial.read();
    comando = toupper(comando);

    if (comando == 'L') {
      statoAttuale = VERIFICA_INFO;
      Serial.println(F(">>> INFO CARTA. Avvicina una carta qualsiasi..."));
    }
    else if (comando == 'R') {
      statoAttuale = IN_LETTURA;
      Serial.println(F(">>> MODALITA' LETTURA. Avvicina la carta originale..."));
    } 
    else if (comando == 'W' && cartaInMemoria) {
      statoAttuale = IN_SCRITTURA;
      Serial.println(F(">>> MODALITA' SCRITTURA. Avvicina la carta vuota..."));
    }
    else if (comando == 'D' && cartaInMemoria) {
      Serial.println(F(">>> DATI IN MEMORIA:"));
      for(byte b = 1; b < blocchiSalvati; b++) { 
        if ((b + 1) % 4 == 0) continue; 
        Serial.print(F("Blocco ")); Serial.print(b < 10 ? "0" : ""); Serial.print(b); Serial.print(F(": "));
        for(byte i = 0; i < 16; i++) {
          Serial.print(datiClonati[b][i] < 0x10 ? " 0" : " ");
          Serial.print(datiClonati[b][i], HEX);
        }
        Serial.println();
      }
      stampaMenu();
    }
    while(Serial.available()) Serial.read(); 
  }

  if (statoAttuale == MENU_PRINCIPALE) return;

  // 2. LETTURA RFID
  if ( ! mfrc522.PICC_IsNewCardPresent() || ! mfrc522.PICC_ReadCardSerial() ) {
    return;
  }

  MFRC522::StatusCode status;
  MFRC522::PICC_Type tipoCarta = mfrc522.PICC_GetType(mfrc522.uid.sak);

  // --- ESECUZIONE VERIFICA INFO [L] ---
  if (statoAttuale == VERIFICA_INFO) {
    Serial.print(F("Tipo di chip rilevato: "));
    Serial.println(mfrc522.PICC_GetTypeName(tipoCarta));

    if (tipoCarta == MFRC522::PICC_TYPE_MIFARE_1K) {
      Serial.println(F("Capacita': 1K (64 blocchi). Supporto COMPLETO."));
    } else if (tipoCarta == MFRC522::PICC_TYPE_MIFARE_4K) {
      Serial.println(F("Capacita': 4K (256 blocchi). ATTENZIONE: La RAM di Arduino puo' tenere solo i primi 64 blocchi!"));
    } else if (tipoCarta == MFRC522::PICC_TYPE_MIFARE_UL) {
      Serial.println(F("Capacita': Ultralight. Struttura a pagine non supportata dal cloner."));
    } else {
      Serial.println(F("Capacita': Sconosciuta."));
    }

    statoAttuale = MENU_PRINCIPALE;
    stampaMenu();
  }

  // --- ESECUZIONE LETTURA [R] ---
  else if (statoAttuale == IN_LETTURA) {
    
    // Determiniamo quanti blocchi leggere in base alla carta e alla RAM
    if (tipoCarta == MFRC522::PICC_TYPE_MIFARE_1K) {
      blocchiSalvati = 64;
    } else if (tipoCarta == MFRC522::PICC_TYPE_MIFARE_4K) {
      Serial.println(F("[AVVISO] Carta 4K rilevata. Leggero' solo i primi 64 blocchi per limiti di memoria."));
      blocchiSalvati = 64;
    } else {
      Serial.println(F("[ERRORE] Formato carta non supportato per questa clonazione."));
      statoAttuale = MENU_PRINCIPALE;
      stampaMenu();
      return;
    }

    bool successoTotale = true;
    byte buffer1[18], buffer2[18];
    byte dimensione = 18;

    for (byte blocco = 0; blocco < blocchiSalvati; blocco++) {
      status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blocco, &key, &(mfrc522.uid));
      if (status != MFRC522::STATUS_OK) {
        Serial.print(F("Errore Auth Blocco ")); Serial.println(blocco);
        successoTotale = false; break; 
      }

      dimensione = 18;
      status = mfrc522.MIFARE_Read(blocco, buffer1, &dimensione);
      if (status != MFRC522::STATUS_OK) { successoTotale = false; break; }

      dimensione = 18;
      status = mfrc522.MIFARE_Read(blocco, buffer2, &dimensione);
      if (status != MFRC522::STATUS_OK) { successoTotale = false; break; }

      bool bloccoValido = true;
      for (byte i = 0; i < 16; i++) {
        if (buffer1[i] != buffer2[i]) bloccoValido = false;
        datiClonati[blocco][i] = buffer1[i]; 
      }

      if (!bloccoValido) {
        Serial.print(F("ERRORE: Incongruenza dati al blocco ")); Serial.println(blocco);
        successoTotale = false; break;
      }
    }

    if (successoTotale) {
      Serial.println(F("[OK] Lettura completata e salvata in RAM!"));
      cartaInMemoria = true;
    } else {
      Serial.println(F("[FALLITO] Errore di lettura."));
    }
    
    statoAttuale = MENU_PRINCIPALE;
    stampaMenu();
  }

  // --- ESECUZIONE SCRITTURA [W] ---
  else if (statoAttuale == IN_SCRITTURA) {
    bool successoTotale = true;

    for (byte blocco = 1; blocco < blocchiSalvati; blocco++) {
      if ((blocco + 1) % 4 == 0) continue; 

      status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blocco, &key, &(mfrc522.uid));
      if (status != MFRC522::STATUS_OK) { successoTotale = false; break; }

      status = mfrc522.MIFARE_Write(blocco, datiClonati[blocco], 16);
      if (status != MFRC522::STATUS_OK) { successoTotale = false; break; }
    }

    if (successoTotale) Serial.println(F("[OK] Clonazione avvenuta con successo!"));
    else Serial.println(F("[FALLITO] Scrittura interrotta. Controlla che la carta sia formattata con la chiave corretta."));

    statoAttuale = MENU_PRINCIPALE;
    stampaMenu();
  }

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
  delay(1000); 
}