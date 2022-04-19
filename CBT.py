# COLOR BASED TILING

from PIL import Image
name = input()
img = Image.open("imgs/{}.png".format(name))
imgPixels = img.load() # create the pixel map

rows = img.size[0]
cols = img.size[1]
n = rows*cols

original_size = n * 24
original_kb = (original_size + 7999) // 8000
print("original size:", original_kb, "kb")

pixels = [[None] * cols for i in range(rows)]

for i in range(rows): # for every pixel:
    for j in range(cols):
        currentPixel = imgPixels[i,j]
        pixels[i][j] = currentPixel[:3]

path = []
path_to_index = {}
k = 0
for i in range(rows):
    for j in range(cols):
        path.append((i,j))
        path_to_index[(i,j)] = k
        k += 1

v = [False]*n
r = v[:]
g = v[:]
b = v[:]

for i in range(rows):
    for j in range(cols):
        index = path_to_index[(i,j)]
        r[index] = pixels[i][j][0]
        g[index] = pixels[i][j][1]
        b[index] = pixels[i][j][2]


def neighbor_cells(r, c, visited):
    neighbors = [
        (r + rd, c + cd)
        for rd, cd in
        [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
    ]
    neighbors = [(r, c) for r, c in neighbors
                if (r >= 0 and r < rows and c >= 0 and c < cols
                    and not visited[path_to_index[(r, c)]]
                )]

    return neighbors


# COLOR DIFFERENCE CONSTANT
color_dif_bits = 0
max_abs_color_dif = (1<<(color_dif_bits-1)) - 1
print(max_abs_color_dif)

def make_binary_string(number, bits):
    if bits == 0: return ""
    return str(bin(number))[2:].zfill(bits)

storage = 0
bit_string = ""

bit_string += make_binary_string(rows, 16)
bit_string += make_binary_string(cols, 16)
bit_string += make_binary_string(color_dif_bits, 8)
storage += 32

bucket_count = 0

for i in range(n):
    if v[i]: bucket_count += 1
    if v[i]: continue
    storage += 24
    bit_string += make_binary_string(r[i],8)
    bit_string += make_binary_string(g[i],8)
    bit_string += make_binary_string(b[i],8)

    v[i] = True
    queue = [i]

    while queue:
        cur = queue.pop(0)
        cur_r, cur_c = path[cur]

        neighbor_bitset = 0
        unvisited_neighbors = len(neighbor_cells(cur_r, cur_c, v))

        for index, nei in enumerate(neighbor_cells(cur_r, cur_c, v)):
            nei_r, nei_c = nei
            nei_path_index = path_to_index[(nei_r, nei_c)]

            if (abs(r[nei_path_index] - r[cur]) <= max_abs_color_dif and\
                abs(g[nei_path_index] - g[cur]) <= max_abs_color_dif and\
                abs(b[nei_path_index] - b[cur]) <= max_abs_color_dif):

                neighbor_bitset |= (1<<index)

                queue.append(nei_path_index)

        bit_string += make_binary_string(neighbor_bitset, unvisited_neighbors)
        storage += unvisited_neighbors
        # print(unvisited_neighbors)
        # if unvisited_neighbors == 4: exit()

        for index, nei in enumerate(neighbor_cells(cur_r, cur_c, v)):
            nei_r, nei_c = nei
            nei_path_index = path_to_index[(nei_r, nei_c)]

            if not (neighbor_bitset & (1<<index)):
                continue

            v[nei_path_index] = True


            rd = r[nei_path_index] - r[cur]
            gd = g[nei_path_index] - g[cur]
            bd = b[nei_path_index] - b[cur]

            rstring = ("0" if rd < 0 else "1") + make_binary_string(abs(rd), color_dif_bits-1)
            gstring = ("0" if gd < 0 else "1") + make_binary_string(abs(gd), color_dif_bits-1)
            bstring = ("0" if bd < 0 else "1") + make_binary_string(abs(bd), color_dif_bits-1)

            storage += 3 * color_dif_bits

            if len(rstring) + len(gstring) + len(bstring) != 3 * color_dif_bits:
                print(rstring, gstring, bstring)
                print(len(rstring) + len(gstring) + len(bstring) )
                print(rd, gd, bd)
                print("\n")

            bit_string += rstring + gstring + bstring

with open("saved.txt", "w") as f:
    f.write(bit_string)

def kb(bitsss):
    return (bitsss + 7999) // 8000

print(bucket_count, n)
print("brute:",kb(n*24), "kb")
print("CBT:",kb(storage), "kb")
print(len(bit_string))
