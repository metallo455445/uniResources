data_file = "/home/matteo/uni/lab esperienza 1/0209_000092/0209_000092_data.csv"

times = []
temps = []
pins = []

with open(data_file, "r") as f:
    for riga in f:
        riga = riga.strip()
        # salta i commenti
        if riga.startswith("#") or not riga:
            continue

        # dividi i valori
        pin, t, temp = riga.split(",")

        pins.append(int(pin.strip()))
        times.append(float(t.strip()))
        temps.append(float(temp.strip()))

print("Esempio:")
print(times[:5], temps[:5], pins[:5])
