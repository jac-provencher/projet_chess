import Échec
import e20
a = Échec.echec()
n = 0
while True:
    try:
        n += 1
        a.stratB3()
        print(a)
        b = e20.echec(a.état())
        b.stratW3()
        print(b)
        a = Échec.echec(b.état())
        
    except Exception as err:
        print(err)
        print(n)
        break

print(n)