import Échec
import e20
import jeu_echec
a = jeu_echec.chess()
n = 0
while True:
    try:
        n += 1
        a.autoplay('black')
        print(a)
        b = e20.echec(a.etat)
        b.stratW3()
        print(b)
        a = jeu_echec.chess(b.état())
        
    except Exception as err:
        print(err)
        print(n)
        break

print(n)