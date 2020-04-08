from tkinter import *
from random import *

# start values

h = 48 * 16
w = 64 * 16

base_v = 64

pole = [['black' for _ in range(48)] for _ in range(64)]

pole_d = [['' for _ in range(48)] for _ in range(64)]

cl_eat = 0

cl_iad = 0

bots = []
cl_b = 0

n_hoda = -1
n_gen = 0


# draw functions

def init_draw():
    for i in range(47):
        conva.create_line(0, i * 16 + 16, w + 1, i * 16 + 16, fill='gray')
    for i in range(63):
        conva.create_line(i * 16 + 16, 0, i * 16 + 16, h + 1, fill='gray')
    for y in range(48):
        for x in range(64):
            pole_d[x][y] = conva.create_polygon((x * 16 + 1, y * 16 + 1),
                                                (x * 16 + 16, y * 16 + 1),
                                                (x * 16 + 16, y * 16 + 16),
                                                (x * 16 + 1, y * 16 + 16),
                                                fill='black')


def draw():
    for x in range(64):
        for y in range(48):
            conva.itemconfig(pole_d[x][y], fill=pole[x][y])


# generating functions

def gen_eat():
    global cl_eat, pole
    while cl_eat < base_v * 2:
        x = randint(0, 63)
        y = randint(0, 47)
        while pole[x][y] != 'black':
            x = randint(0, 63)
            y = randint(0, 47)
        pole[x][y] = 'red'
        cl_eat += 1


def gen_iad():
    global cl_iad, pole
    while cl_iad < base_v:
        x = randint(0, 63)
        y = randint(0, 47)
        while pole[x][y] != 'black':
            x = randint(0, 63)
            y = randint(0, 47)
        pole[x][y] = 'green'
        cl_iad += 1


def gen_steni():
    for i in range(64):
        pole[i][0] = 'gray'
        pole[i][-1] = 'gray'
    for i in range(48):
        pole[0][i] = 'gray'
        pole[-1][i] = 'gray'


def gen_bots():
    global cl_b, pole, bots
    while cl_b < base_v:
        x = randint(0, 63)
        y = randint(0, 47)
        while pole[x][y] != 'black':
            x = randint(0, 63)
            y = randint(0, 47)
        pole[x][y] = 'blue'
        cl_b += 1
        bots += [{'x': x,
                  'y': y,
                  'is_live': True,
                  'energy': 32,
                  'rotate': 0,
                  'c': 0,
                  'gens': [randint(0, 63) for _ in range(64)]}]


def gen_new_b(old_b):
    n_b = []
    for i in old_b:
        for _ in range(8):
            x = randint(0, 63)
            y = randint(0, 47)
            while pole[x][y] != 'black':
                x = randint(0, 63)
                y = randint(0, 47)
            pole[x][y] = 'blue'

            n_b += [{'x': x,
                     'y': y,
                     'is_live': True,
                     'energy': 32,
                     'rotate': 0,
                     'c': 0,
                     'gens': i}]
        n_b[-1]['gens'][randint(0, 63)] = randint(0, 63)
    return n_b


def gen_all():
    gen_eat()
    gen_iad()


# doing functions

def normalise(n_bota, n, r):
    x = bots[n_bota]['x']
    y = bots[n_bota]['y']

    n = (n + r) % 8

    if n == 0:
        return x, y - 1
    if n == 1:
        return x + 1, y - 1
    if n == 2:
        return x + 1, y
    if n == 3:
        return x + 1, y + 1
    if n == 4:
        return x, y + 1
    if n == 5:
        return x - 1, y + 1
    if n == 6:
        return x - 1, y
    if n == 7:
        return x - 1, y - 1


def go_to(n_bota, px, py):
    pole[bots[n_bota]['x']][bots[n_bota]['y']] = 'black'
    pole[px][py] = 'blue'
    bots[n_bota]['x'] = px
    bots[n_bota]['y'] = py


def step(n_bota, n, r):
    global cl_eat, cl_iad, pole, cl_b, bots

    px, py = normalise(n_bota, n, r)

    if pole[px][py] == 'black':
        go_to(n_bota, px, py)
    elif pole[px][py] == 'red':
        cl_eat -= 1
        bots[n_bota]['energy'] += 10
        go_to(n_bota, px, py)
    elif pole[px][py] == 'green':
        bots[n_bota]['energy'] = 0
        pole[bots[n_bota]['x']][bots[n_bota]['y']] = 'green'
        cl_iad += 1
    up_c(n_bota, 2)


def rotate(n_bota):
    if bots[n_bota]['gens'][(bots[n_bota]['c'] + 1) % 64] % 2:
        bots[n_bota]['rotate'] += 1
    else:
        bots[n_bota]['rotate'] -= 1
    bots[n_bota]['rotate'] = bots[n_bota]['rotate'] % 8
    up_c(n_bota, 2)


def do_eat(n_bota, n, r):
    global cl_eat, cl_iad, pole
    px, py = normalise(n_bota, n, r)
    if pole[px][py] == 'red':
        bots[n_bota]['energy'] += 10
        pole[px][py] = 'black'
        cl_eat -= 1
    elif pole[px][py] == 'green':
        pole[px][py] = 'red'
        cl_iad -= 1
        cl_eat += 1
    up_c(n_bota, 2)


def look(n_bota):
    px, py = normalise(n_bota, 0, bots[n_bota]['rotate'])
    if pole[px][py] == 'black':
        up_c(n_bota, 1)
    elif pole[px][py] == 'gray':
        up_c(n_bota, 2)
    elif pole[px][py] == 'red':
        up_c(n_bota, 3)
    elif pole[px][py] == 'green':
        up_c(n_bota, 4)
    elif pole[px][py] == 'blue':
        up_c(n_bota, 5)


def energy(n_bota):
    if bots[n_bota]['energy'] >= bots[n_bota]['gens'][(bots[n_bota]['c'] + 1) % 64]:
        up_c(n_bota, 2)
    else:
        up_c(n_bota, 3)


def up_c(n_bota, c):
    global bots
    bots[n_bota]['c'] += c
    bots[n_bota]['c'] = bots[n_bota]['c'] % 64


def hod_bota(n_bota):
    global cl_b

    for _ in range(16):
        if bots[n_bota]['gens'][bots[n_bota]['c']] == 0:
            step(n_bota, (bots[n_bota]['c'] + 1) // 8, bots[n_bota]['rotate'])
            break

        elif bots[n_bota]['gens'][bots[n_bota]['c']] == 1:
            rotate(n_bota)

        elif bots[n_bota]['gens'][bots[n_bota]['c']] == 2:
            do_eat(n_bota, (bots[n_bota]['c'] + 1) // 8, bots[n_bota]['rotate'])
            break

        elif bots[n_bota]['gens'][bots[n_bota]['c']] == 3:
            look(n_bota)

        elif bots[n_bota]['gens'][bots[n_bota]['c']] == 4:
            energy(n_bota)

        else:
            up_c(n_bota, bots[n_bota]['gens'][bots[n_bota]['c']])

        if bots[n_bota]['energy'] <= 0:
            bots[n_bota]['is_live'] = False
            cl_b -= 1
            if pole[bots[n_bota]['x']][bots[n_bota]['y']] == 'blue':
                pole[bots[n_bota]['x']][bots[n_bota]['y']] = 'black'
            break

    if bots[n_bota]['energy'] <= 0 and bots[n_bota]['is_live']:
        bots[n_bota]['is_live'] = False
        cl_b -= 1
        if pole[bots[n_bota]['x']][bots[n_bota]['y']] == 'blue':
            pole[bots[n_bota]['x']][bots[n_bota]['y']] = 'black'

    bots[n_bota]['energy'] -= 1


is_and = bool(input('Введите пустую строку для новой генерации или что угодно для загрузки\n'))


def do_game():
    global n_hoda, is_and, bots, pole, cl_b, n_gen, cl_eat, cl_iad
    if is_and:
        for i in range(1, 63):
            for j in range(1, 47):
                pole[i][j] = 'black'

        f = open('../gens.txt', mode='r')
        r = f.read().split('\n')
        gens = r[:-2]
        n_gen = int(r[-1])
        f.close()
        for i in range(8):
            gens[i] = [int(j) for j in gens[i].split()]

        bots = gen_new_b(gens)
        is_and = False
        cl_b = 64
        cl_eat = 0
        cl_iad = 0
        n_hoda = -1
        print(f'generation: {n_gen}')
        n_gen += 1

    gen_all()
    n_hoda += 1
    for i in range(64):
        if bots[i]['is_live']:
            hod_bota(i)
        if cl_b == 8:
            is_and = True
            break
    draw()
    print(f'hod: {n_hoda}, cl_b: {cl_b}')
    if is_and:
        f = open('../gens.txt', mode='w')
        for i in bots:
            if i['is_live']:
                f.write(' '.join(str(j) for j in i['gens']) + '\n')
        f.write(str(n_hoda) + '\n')
        f.write(str(n_gen))
        f.close()
    windows.after(1, do_game)


isnt_in_game = True


def game(event):
    global isnt_in_game
    if event.char == ' ' and isnt_in_game:
        isnt_in_game = False
        do_game()


# start

windows = Tk()
conva = Canvas(windows, height=h, width=w, bg='white')

init_draw()
gen_steni()
gen_bots()
gen_all()
draw()

# hod_bota(0)

windows.bind("<KeyPress>", game)

conva.pack()
windows.mainloop()
