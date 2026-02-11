import numpy as np
import time

word = "Hello World!"
comp = np.array([''] * len(word))
stop = False
i = 0

while not stop:
    n = np.random.randint(0, 129)
    if n == 10:
        n = 56
    char = chr(n)
    if char != '':
        comp[i] = char
        time.sleep(0.01)
        print(''.join(comp))
        if char == word[i]:   
            i += 1
            if i >= len(word):
                stop = True
