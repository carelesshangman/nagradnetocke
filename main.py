A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, R, S, T, U, V = "ABCDEFGHIJKLMNOPRSTUV"

zemljevid = {
    (A, B): "gravel trava",
    (A, V): "pešci lonci",
    (B, C): "bolt lonci",
    (B, V): "",
    (C, R): "stopnice pešci lonci",
    (D, F): "stopnice pešci",
    (D, R): "pešci",
    (E, I): "trava lonci",
    (F, G): "trava črepinje",
    (G, H): "črepinje pešci",
    (G, I): "avtocesta",
    (H, J): "robnik bolt",
    (I, M): "avtocesta",
    (I, P): "gravel",
    (I, R): "stopnice robnik",
    (J, K): "",
    (J, L): "gravel bolt",
    (K, M): "stopnice bolt",
    (L, M): "robnik pešci",
    (M, N): "rodeo",
    (N, P): "gravel",
    (O, P): "gravel",
    (P, S): "",
    (R, U): "trava pešci",
    (R, V): "pešci lonci",
    (S, T): "robnik trava",
    (T, U): "gravel trava",
    (U, V): "robnik lonci trava"
}

zemljevid2 = {
                (A, C): {"avtocesta"}, (C, A): {"avtocesta"},  # 10
                (A, B): set("stopnice pešci trava".split()), (A, B): set("stopnice pešci trava".split()), # 12
                (A, D): set("črepinje robnik lonci gravel".split()), (A, D): set("črepinje robnik lonci gravel".split()) # 5
            }

points = {"črepinje": 1,
"robnik": 1,
"lonci": 1,
"gravel": 2,
"bolt": 2,
"rodeo": 2,
"trava": 3,
"pešci": 4,
"stopnice": 6,
"avtocesta": 10}

def getPoints(item, zemljevid) -> int: #item -> (A,B) example
    value = 0

    if item in zemljevid:
        keys = zemljevid[item]
    else:
        tmp = (item[1], item[0])
        keys = zemljevid[tmp]

    for el in keys:#.split(" "):
        value += points[el]

    return value


def vrednost_povezave(povezava, zemljevid) -> int:
    value = 0
    if povezava in zemljevid:
        keys = zemljevid[povezava]
    else:
        tmp = (povezava[1],povezava[0])
        keys = zemljevid[tmp]

    for el in keys.split(" "):
        value += points[el]

    return value


def vrednost_povezave_inOne(povezava, zemljevid) -> int:
    value = 0
    for i in range(2):
        value += points[next(iter(zemljevid[povezava] if povezava in zemljevid else zemljevid[(povezava[1], povezava[0])].split(" ")))]
    return value
    #return points[next(iter(zemljevid[povezava] if povezava in zemljevid else zemljevid[(povezava[1],povezava[0])].split(" ")))]

def najboljsa_povezava(zemljevid) -> (str, str):
    bestValue = [0, None]
    for i, el in enumerate(zemljevid):
        if getPoints(el, zemljevid) > bestValue[0]:
            bestValue = [getPoints(el, zemljevid), el]

    bestPath = (bestValue[1])
    #bestPath.append((bestValue[1][1],bestValue[1][0]))
    return (bestPath)

def vrednost_poti(pot, zemljevid) -> int:
    value = 0
    for i in range(len(pot)-1):
        tmp = (pot[i], pot[i+1])
        skills = zemljevid[tmp]
        for item in skills:
            value += points[item]
    return value

print(vrednost_povezave((V, R), zemljevid))
print(vrednost_povezave_inOne((V, R), zemljevid))