import Échec
import e20
import jeu_echec
a = Échec.echec()
n = 0
while True:
    try:
        n += 1
        a.stratB4()
        print(a)
        b = e20.echec(a.etat)
        b.stratW3()
        print(b)
        a = Échec.echec(b.état())
    except Exception as e:
        print(e)
        break
print(n)