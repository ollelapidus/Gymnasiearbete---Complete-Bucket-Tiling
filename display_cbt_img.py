from PIL import Image
import numpy as np

rows, cols = [int(i) for i in input().split()]
data = np.zeros((cols, rows, 3), dtype=np.uint8)

for i in range(rows):
    for j in range(cols):
        r, g, b = [int(i) for i in input().split()]
        data[j][i] = [r, g, b]

img = Image.fromarray(data, 'RGB')
img.save('my.png')
img.show()
