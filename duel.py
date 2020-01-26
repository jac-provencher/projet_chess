import Échec
import e20
a = Échec.echec()
while True:

    a.stratB3()
    print(a)
    b = e20.echec(a.état())
    b.stratW3()
    print(b)
    a = Échec.echec(b.état())
       