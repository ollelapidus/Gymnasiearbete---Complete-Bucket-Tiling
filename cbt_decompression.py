
with open("saved.txt", "r") as f:
    bit_string = f.readlines()[0]
number_of_bits = len(bit_string)

pointer = 0
n = 0

def read_n_bits(num):
    global pointer
    global number_of_bits
    if num == 0: return 0
    res = int(bit_string[pointer:pointer+num], 2)
    pointer += num
    return res

rows = read_n_bits(16)
cols = read_n_bits(16)
color_dif_bits = read_n_bits(8)
n = rows * cols

v = [[False]*cols for i in range(rows)]

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



for i in range(n):
    if v[i]: continue
    v[i] = True

    r[i], g[i], b[i] = [read_n_bits(8) for _ in range(3)]

    queue = [i]

    while queue:
        cur = queue.pop(0)
        cur_r, cur_c = path[cur]

        neighbors = neighbor_cells(cur_r, cur_c, v)
        bitset = read_n_bits(len(neighbors))
        # print(len(neighbors))
        # if len(neighbors) == 4: exit()
        if bitset == 0: continue

        for index, nei in enumerate(neighbors):
            if not (bitset & (1 << index)): continue
            nei_r, nei_c = nei
            nei_index = path_to_index[(nei_r, nei_c)]
            v[nei_index] = True

            __ = [None]*3
            for _ in range(3):
                if read_n_bits(1) == 1:
                    __[_] = read_n_bits(color_dif_bits - 1)
                else:
                    __[_] = -read_n_bits(color_dif_bits - 1)

            r[nei_index] = r[cur] + __[0]
            g[nei_index] = g[cur] + __[1]
            b[nei_index] = b[cur] + __[2]

            queue.append(nei_index)

print(pointer, number_of_bits)
print((number_of_bits + 7999) // 8000, "kb")

color_string = f"{rows} {cols}\n"
for i in range(n):
    color_string += f"{r[i]} {g[i]} {b[i]}\n"

with open("decompressed_img.txt", "w") as f:
    f.write(color_string)

# for i in range(n):
#     print(r[i], g[i], b[i])
