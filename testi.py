


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

zemljevid = {k: set(v.split()) for k, v in zemljevid.items()} | {k[::-1]: set(v.split()) for k, v in zemljevid.items()}

mali_zemljevid = {(A, B): "robnik bolt",  # 3
                  (A, C): "bolt rodeo pešci",  # 8
                  (C, D): ""}  # 0

mali_zemljevid = {k: set(v.split()) for k, v in mali_zemljevid.items()} | {k[::-1]: set(v.split()) for k, v in mali_zemljevid.items()}

#help func
import numpy as np #np v1.23.5

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

#6 brez list comprehension
def vrednost_povezave(povezava, zemljevid) -> int:
    value = 0
    if povezava in zemljevid:
        keys = zemljevid[povezava]
    else:
        tmp = (povezava[1],povezava[0])
        keys = zemljevid[tmp]

    for el in keys:
        value += points[el]

    return value

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

#7
def najbolj_uporabna(pot, zemljevid):
    skills = []
    tmp = []
    for i in range(len(pot) - 1):
        if (pot[i], pot[i + 1]) in zemljevid:
            skills.append(list(zemljevid[(pot[i], pot[i + 1])]))
        else:
            skills.append(list(zemljevid[(pot[i + 1], pot[i])]))
    for item in skills:
        for subitem in item:
            tmp.append(subitem)
    if tmp == []:
        return None
    return max(tmp, key=tmp.count)
#8
def mozna_pot(pot, zemljevid, vescine):
    skills = vescine
    for i in range(len(pot) - 1):
        removers = {}
        if (pot[i], pot[i + 1]) in zemljevid:
            removers = zemljevid[(pot[i], pot[i + 1])]
        elif (pot[i + 1], pot[i]) in zemljevid:
            removers = zemljevid[(pot[i + 1], pot[i])]
        for item in removers:
            if item in skills:
                skills.remove(item)
            else:
                return False
    return True

def koncna_tocka(pot, zemljevid, vescine): #ta naloga je evil sorcery bullshit
    skills = []
    tmp = []
    newVescine = []
    canQueue = 0
    for item in vescine:
        for i in range(item[1]):
            newVescine.append(item[0])
    for i in range(len(pot) - 1):
        if canQueue == 0:
            if (pot[i], pot[i + 1]) in zemljevid:
                skills.append(zemljevid[(pot[i + 1], pot[i])])
            elif (pot[i +1], pot[i]) in zemljevid:
                skills.append(zemljevid[(pot[i + 1], pot[i])])
            elif (pot[i], pot[i + 1]) or (pot[i +1], pot[i]) not in zemljevid:
                canQueue = i

    if canQueue != 0:
        return pot[canQueue]

    for item in skills:
        for subitem in item:
            tmp.append(subitem)
    my_dict2 = {i: newVescine.count(i) for i in newVescine}
    for item in points:
        if item not in my_dict2:
            my_dict2[item] = 0
    for i in range(len(pot) - 1):
        subtractor = []
        subSubtractor = []
        if (pot[i], pot[i + 1]) in zemljevid:
            temp = zemljevid[(pot[i + 1], pot[i])]
            subtractor.append(temp)
            for item in subtractor:
                for subitem in item:
                    subSubtractor.append(subitem)
            for item in subSubtractor:
                my_dict2[item] -= 1
                if my_dict2[item] < 0 or item not in my_dict2:
                    return pot[i]
    return pot[-1:]

def do_nagrade(pot, zemljevid, meja) -> str:
    value = 0
    for i in range(len(pot) - 1):
        if (pot[i], pot[i + 1]) in zemljevid:
            value += getPoints((pot[i], pot[i + 1]), zemljevid)
        elif (pot[i + 1], pot[i]) in zemljevid:
            value += getPoints((pot[i + 1], pot[i]), zemljevid)
        else:
            return pot[i]
        if value > meja:
            return pot[i]
    return pot[-1:]

#9 (updated 6 z list comprehension in ostalo)

#10
def dosegljive(tocka, zemljevid, vescine):
    return None



import unittest
import ast


class Ocena_06(unittest.TestCase):
    def test01_vrednost_povezave(self):
        self.assertEqual(5, vrednost_povezave((V, R), zemljevid))
        self.assertEqual(10, vrednost_povezave((G, I), zemljevid))
        self.assertEqual(4, vrednost_povezave((R, D), zemljevid))
        self.assertEqual(0, vrednost_povezave((S, P), zemljevid))
        self.assertEqual(11, vrednost_povezave((C, R), zemljevid))

        self.assertEqual(3, vrednost_povezave((A, B), mali_zemljevid))

    def test_02_najboljsa_povezava(self):
        self.assertIn(
            najboljsa_povezava({
                (A, C): {"avtocesta"}, (C, A): {"avtocesta"},  # 10
                (A, B): set("stopnice pešci trava".split()), (A, B): set("stopnice pešci trava".split()), # 12
                (A, D): set("črepinje robnik lonci gravel".split()), (A, D): set("črepinje robnik lonci gravel".split()) # 5
            }),
            {(A, B), (B, A)})

        self.assertIn(najboljsa_povezava(zemljevid), {(C, R), (R, C)})
        self.assertIn(najboljsa_povezava(mali_zemljevid), {(A, C), (C, A)})

    def test_03_vrednost_poti(self):
        self.assertEqual(8, vrednost_poti("ABC", zemljevid))
        self.assertEqual(33, vrednost_poti("ABCRDF", zemljevid))
        self.assertEqual(0, vrednost_poti("SPSPSP", zemljevid))
        self.assertEqual(0, vrednost_poti("M", zemljevid))

        self.assertEqual(8, vrednost_poti("ACDC", mali_zemljevid))


class Ocena_07(unittest.TestCase):
    def test01_najbolj_uporabna(self):
        self.assertEqual("lonci", najbolj_uporabna("ABCRVA", zemljevid))
        self.assertEqual("črepinje", najbolj_uporabna("FGHJ", zemljevid))
        self.assertEqual("gravel", najbolj_uporabna("MNPIG", zemljevid))
        self.assertIn(najbolj_uporabna("VBC", zemljevid), {"lonci", "bolt"})
        self.assertIsNone(najbolj_uporabna("BV", zemljevid))
        self.assertIsNone(najbolj_uporabna("B", zemljevid))
        self.assertIsNone(najbolj_uporabna("T", zemljevid))


class Ocena_08(unittest.TestCase):
    def test_01_mozna_pot(self):
        # Ni povezave I->A
        self.assertFalse(mozna_pot("DFGIAB", zemljevid, set("stopnice avtocesta pešci trava črepinje rodeo".split())))
        # Ta se da
        self.assertTrue(mozna_pot("DFGI", zemljevid, set("stopnice avtocesta pešci trava črepinje rodeo".split())))
        # Ne zna čez črepinje (F->G)
        self.assertFalse(mozna_pot("DFGI", zemljevid, set("stopnice avtocesta pešci trava rodeo".split())))
        # Dvakrat po travi
        self.assertFalse(mozna_pot("DFGIE", zemljevid, set("stopnice avtocesta pešci trava črepinje rodeo".split())))
        # Dvakrat med peščci
        self.assertFalse(mozna_pot("RDFGI", zemljevid, set("stopnice avtocesta pešci trava črepinje rodeo".split())))
        # Ne zahteva veščin
        self.assertTrue(mozna_pot("SP", zemljevid, set()))
        # Pot dolžine 0 je seveda možna
        self.assertTrue(mozna_pot("T", zemljevid, set()))
        self.assertTrue(mozna_pot("T", zemljevid, set("stopnice avtocesta pešci trava črepinje rodeo gravel lonci".split())))

        self.assertTrue(mozna_pot("SPNMIE", zemljevid, set("stopnice avtocesta pešci trava črepinje rodeo gravel lonci".split())))
        self.assertTrue(mozna_pot("SPNMIE", zemljevid, set("stopnice avtocesta pešci trava črepinje rodeo gravel lonci robnik".split())))
        # Dvakrat po travi
        self.assertFalse(mozna_pot("TSPNMIE", zemljevid, set("stopnice avtocesta pešci trava črepinje rodeo gravel lonci robnik".split())))

    def test_02_koncna_tocka(self):
        # zmanjka loncev
        self.assertEqual(R, koncna_tocka("ABCRVBCRV", zemljevid, {("gravel", 1), ("trava", 1), ("bolt", 3), ("lonci", 5), ("stopnice", 10), ("pešci", 10)}))
        # zmanjka gravelov
        self.assertEqual(P, koncna_tocka("SPNMIPNML", zemljevid, {("gravel", 2), ("rodeo", 2), ("avtocesta", 1)}))
        # nima robnika in pešcev
        self.assertEqual(M, koncna_tocka("SPNMIPNML", zemljevid, {("gravel", 3), ("rodeo", 2), ("avtocesta", 1)}))
        # nima robnika
        self.assertEqual(M, koncna_tocka("SPNMIPNML", zemljevid, {("gravel", 3), ("rodeo", 2), ("avtocesta", 1), ("pešci", 2)}))
        # nima pešcev
        self.assertEqual(M, koncna_tocka("SPNMIPNML", zemljevid, {("gravel", 3), ("rodeo", 2), ("avtocesta", 1), ("robnik", 2)}))
        # ni povezave N -> E
        self.assertEqual(N, koncna_tocka("SPNMIPNEML", zemljevid, {("gravel", 3), ("rodeo", 2), ("avtocesta", 1), ("robnik", 2)}))

        self.assertEqual(P, koncna_tocka("SP", zemljevid, {("gravel", 3), ("rodeo", 2), ("avtocesta", 1), ("robnik", 2)}))
        self.assertEqual(P, koncna_tocka("SP", zemljevid, set()))
        self.assertEqual(P, koncna_tocka("P", zemljevid, {("gravel", 3), ("rodeo", 2), ("avtocesta", 1), ("robnik", 2)}))
        self.assertEqual(P, koncna_tocka("P", zemljevid, set()))

    def test_03_do_nagrade(self):
        self.assertEqual(R, do_nagrade("ABCRIMNPSTU", zemljevid, 20))
        self.assertEqual(I, do_nagrade("ABCRIMNPSTU", zemljevid, 30))
        self.assertEqual(N, do_nagrade("ABCRIMNPSTU", zemljevid, 39))
        self.assertEqual(S, do_nagrade("ABCRIMNPSTU", zemljevid, 40))
        self.assertEqual(U, do_nagrade("ABCRIMNPSTU", zemljevid, 50))

        # ni povezave A -> C
        self.assertEqual(A, do_nagrade("ACRIMNPSTU", zemljevid, 50))

        self.assertEqual(M, do_nagrade("MNPOPNMKJHGFDRCBA", zemljevid, 1))
        self.assertEqual(O, do_nagrade("MNPOPNMKJHGFDRCBA", zemljevid, 6))
        self.assertEqual(J, do_nagrade("MNPOPNMKJHGFDRCBA", zemljevid, 20))
        self.assertEqual(C, do_nagrade("MNPOPNMKJHGFDRCBA", zemljevid, 58))
        self.assertEqual(A, do_nagrade("MNPOPNMKJHGFDRCBA", zemljevid, 100))

class Ocena_09(unittest.TestCase):
    def test_00_enovrsticne(self):
        functions = {
            elm.name: elm
            for elm in ast.parse(open(__file__, "r", encoding="utf-8").read()).body
            if isinstance(elm, ast.FunctionDef)}

        dovoljene_funkcije = set("vrednost_povezave najboljsa_povezava vrednost_poti najbolj_uporabna "
                                 "mozna_pot koncna_tocka do_nagrade naslednje_tocke dosegljive dosegljive_n naj_vescine".split())
        for func in functions:
            self.assertIn(func, dovoljene_funkcije, f"\nFunkcija {func} ni dovoljena.")

        for func in (vrednost_povezave, najboljsa_povezava, vrednost_poti, naslednje_tocke):
            body = functions[func.__code__.co_name].body
            self.assertEqual(len(body), 1, "\nFunkcija ni dolga le eno vrstico")
            self.assertIsInstance(body[0], ast.Return, "\nFunkcija naj bi vsebovala le return")

    def test_01_naslednje_tocke(self):
        self.assertEqual({S, P, O, N, I}, naslednje_tocke({P}, zemljevid, {"gravel"}))
        self.assertEqual({S, P, O, N, I}, naslednje_tocke({P}, zemljevid, {"gravel", "rodeo"}))
        self.assertEqual({N, M, P}, naslednje_tocke({N}, zemljevid, {"gravel", "rodeo"}))
        self.assertEqual({N, M}, naslednje_tocke({N}, zemljevid, {"rodeo"}))

        self.assertEqual({V, A, B, R, F, D}, naslednje_tocke({V, F}, zemljevid, set("pešci stopnice lonci rodeo".split())))
        self.assertEqual({V, A, B, R, F, D, P, S}, naslednje_tocke({V, F, P}, zemljevid, set("pešci stopnice lonci rodeo".split())))
        self.assertEqual({V, A, B, R, F, D, P, S}, naslednje_tocke({V, F, P}, zemljevid, set("pešci stopnice lonci rodeo".split())))
        self.assertEqual({V, A, B, R, F, D, P, S, O, N, I}, naslednje_tocke({V, F, P}, zemljevid, set("pešci stopnice lonci rodeo gravel".split())))


class Ocena_10(unittest.TestCase):
    def test_01_dosegljivo(self):
        self.assertEqual({N, S, P, O, I}, dosegljive(N, zemljevid, {"gravel"}))
        self.assertEqual({N, S, P, O, I, G, M}, dosegljive(N, zemljevid, {"gravel", "avtocesta"}))
        self.assertEqual({N, S, P, O, I, G, M}, dosegljive(N, zemljevid, {"gravel", "avtocesta", "rodeo"}))
        self.assertEqual({N, S, P, O, I, M}, dosegljive(N, zemljevid, {"gravel", "rodeo"}))

        self.assertEqual({H, J, L, K, M, N}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt".split())))
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta".split())))
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F, V, A, B, C}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta lonci".split())))
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F, V, A, B, C, U, E}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta lonci trava".split())))
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F, V, A, B, C, U, E}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta lonci trava črepinje".split())))
        # zdaj je dosegljivo vse
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F, V, A, B, C, U, E, S, T, P, O}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta lonci trava črepinje gravel".split())))


class Ocena_11(unittest.TestCase):
    def test_01_dosegljive_n(self):
        self.assertEqual({S, P, O, N, I}, dosegljive_n(P, zemljevid, 2))
        self.assertEqual({T, S, P, O, I, M, N}, dosegljive_n(P, zemljevid, 4))
        self.assertEqual({T, S, P, O, I, E, M, N}, dosegljive_n(P, zemljevid, 6))
        self.assertEqual({T, S, P, O, I, E, M, N}, dosegljive_n(P, zemljevid, 8))
        self.assertEqual({T, S, P, O, I, E, M, N, L, U, R}, dosegljive_n(P, zemljevid, 9))
        self.assertEqual({S, P}, dosegljive_n(P, zemljevid, 0))
        self.assertEqual({S, P}, dosegljive_n(P, zemljevid, 1))
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F, V, A, B, C, U, E, S, T, P, O}, dosegljive_n(A, zemljevid, 1000))


class Ocena_12(unittest.TestCase):
    def test_01_naj_vescine(self):
        self.assertEqual(({'lonci', 'pešci'}, 5), naj_vescine("A", zemljevid, 2))
        self.assertEqual(({"lonci", "stopnice", "pešci"}, 7), naj_vescine("A", zemljevid, 3))
        self.assertEqual(({'trava', 'gravel', 'lonci', 'robnik'}, 11), naj_vescine("A", zemljevid, 4))

        self.assertEqual(({'gravel', 'avtocesta'}, 7), naj_vescine("I", zemljevid, 2))
        self.assertEqual(({'gravel', 'avtocesta'}, 7), naj_vescine("P", zemljevid, 2))
        self.assertEqual(({'gravel'}, 5), naj_vescine("P", zemljevid, 1))
        self.assertEqual(({'lonci', 'robnik', 'gravel', 'trava'}, 11), naj_vescine("P", zemljevid, 4))

        self.assertEqual(({'gravel', "bolt"}, 3), naj_vescine("L", zemljevid, 2))
        self.assertEqual(({'stopnice', 'bolt', 'gravel', 'avtocesta'}, 10), naj_vescine("L", zemljevid, 4))


if "__main__" == __name__:
    unittest.main()