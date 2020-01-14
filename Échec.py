import random
import turtle

def tracerpolygone(ronnie, poly):
    "À l'aide de la tortue ronnie, tracer un polygone "
    ronnie.penup()
    ronnie.color('black')
    ronnie.width(3)
    ronnie.goto(poly[0])
    ronnie.pendown()
    for pos in poly[1:]:
        ronnie.goto(pos)
   
class echec:
    def stratW3(self):
        liste = []
        listeval = []
        vali = self.valjeu()
        for x in range(1, 9):
            for y in range(1, 9):
                im = self.etat['white'].get((x, y))
                if im is not None:
                    for i in range(1, 9):
                        for j in range(1, 9):
                            try:
                                pf = (i, j)
                                it = self.etat['black'].get(pf)
                                self.jouer_coupW((x, y), pf)
                                liste += [[(x, y), pf]]
                                if it is None:
                                    listeval += [-self.valcpB3()]
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                    
                                else:
                                    listeval += [self.valjeu()-vali-self.valcpB3()]
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                    self.etat['black'][pf] = it
                                   
                            except EchecError:
                                continue
        if liste != []:
            potentiel = []
            valeur = max(listeval)
            for i, j in enumerate(listeval):
                if j == valeur:
                    potentiel += [liste[i]]
            random.shuffle(potentiel)
            coup = potentiel[0]
            self.jouer_coupW(coup[0], coup[1])
        else:
            if not self.check_echecW():
                raise EchecError('égalité')
            raise EchecError('Échec et mat! (Noirs gagnent)')
    
    def valjeu(self):
        val = 0
        for pos, kind in self.etat['white'].items():
            
            if kind == 'P':
                if pos[1] <= 3:
                    val += 0.1
                val += 1
            elif kind == 'T' or kind == 'C' or kind == 'F':
                val += 3
                if kind == 'T':
                    val += 4
            elif kind == 'Q':
                val += 10
            elif kind == 'K':
                val += 100
        for pos, kind in self.etat['black'].items():
            if kind == 'P':
                if pos[1] >= 6:
                    val -= 0.1
                val -= 1
            elif kind == 'T' or kind == 'C' or kind == 'F':
                val -= 3
                if kind == 'T':
                    val -= 4
            elif kind == 'Q':
                val -= 10
            elif kind == 'K':
                val -= 100
        if self.check_echecB():
            val += 0.5
        if self.check_echecW():
            val -= 0.5
        return val

    def checkmatW(self):
        p = 0
        for x in range(1, 9):
            for y in range(1, 9):
                im = self.etat['white'].get((x, y))
                if im is not None:
                    for i in range(1, 9):
                        for j in range(1, 9):
                            try:
                                pf = (i, j)
                                val = 0
                                it = self.etat['black'].get(pf)
                                self.jouer_coupW((x, y), pf)
                                p += 1
                                if it is None:
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                else:
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                    self.etat['black'][pf] = it
                            except EchecError:
                                continue
        if p > 0:
          return False
        else:
            if not self.check_echecW():
                raise EchecError('égalité')
            raise EchecError('Échec et mat! (Noirs gagnent)')
    
    def checkmatB(self):
        liste = []
        listeval = []
        for x in range(1, 9):
            for y in range(1, 9):
                for i in range(1, 9):
                    for j in range(1, 9):
                        try:
                            pi = (x, y)
                            pf = (i, j)
                            val = 0
                            im = self.etat['black'].get(pi)
                            it = self.etat['white'].get(pf)
                            self.jouer_coupB(pi, pf)
                            liste += [pi, pf]
                            if it is None:
                                self.etat['black'].pop(pf)
                                self.etat['black'][pi] = im
                            else:
                                self.etat['black'].pop(pf)
                                self.etat['black'][pi] = im
                                self.etat['white'][pf] = it
                        except EchecError:
                            continue
        if liste != []:
          return False
        else:
            if not self.check_echecB():
                raise EchecError('égalité')
            raise EchecError('Échec et mat! (Blancs gagnent)')
    
    def valcpW2(self):
        listeval = []
        vali = self.valjeu()
        for x in range(1, 9):
            for y in range(1, 9):
                im = self.etat['white'].get((x, y))
                if im is not None:
                    for i in range(1, 9):
                        for j in range(1, 9):
                            try:
                                pf = (i, j)
                                it = self.etat['black'].get(pf)
                                if it is not None:
                                    self.jouer_coupW((x, y), pf)
                                    vp = self.valjeu() - vali
                                    listeval += [vp]
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                    self.etat['black'][pf] = it
                                else:
                                    self.jouer_coupW((x, y), pf)
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                    listeval+=[0]
                            except EchecError:
                                continue
        if listeval != []:
            return max(listeval)
        return -1000 if self.check_echecW() else 0
    
    def valcpW(self):
        listeval = []
        vali = self.valjeu()
        for x in range(1, 9):
            for y in range(1, 9):
                im = self.etat['white'].get((x, y))
                if im is not None:
                    for i in range(1, 9):
                        for j in range(1, 9):
                            try:
                                pf = (i, j)
                                it = self.etat['black'].get(pf)
                                if it is not None:
                                    self.jouer_coupW((x, y), pf)
                                    vp = self.valjeu() - vali - self.valcpB2()
                                    listeval += [vp]
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                    self.etat['black'][pf] = it
                                else:
                                    self.jouer_coupW((x, y), pf)
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                    listeval+=[0]
                            except EchecError:
                                continue
        if listeval != []:
            return max(listeval)
        return -1000 if self.check_echecW() else 0  
    
    def valcpB3(self):
        listeval = []
        vali = self.valjeu()
        for x in range(1, 9):
            for y in range(1, 9):
                im = self.etat['black'].get((x, y))
                if im is not None:
                    for i in range(1, 9):
                        for j in range(1, 9):
                            try:
                                pf = (i, j)
                                it = self.etat['white'].get(pf)
                                if it is not None:
                                    self.jouer_coupB((x, y), pf)
                                    listeval +=[vali-self.valjeu()-self.valcpW()]  
                                    self.etat['black'].pop(pf)
                                    self.etat['black'][(x, y)] = im
                                    self.etat['white'][pf] = it
                                else:
                                    self.jouer_coupW((x, y), pf)
                                    self.etat['black'].pop(pf)
                                    self.etat['black'][(x, y)] = im
                                    listeval += [0]
                                    
                            except EchecError:
                                continue
        if listeval != []:
            return max(listeval)
        return -1000 if self.check_echecB() else 0
    
    def valcpB2(self):
        listeval = []
        vali = self.valjeu()
        for x in range(1, 9):
            for y in range(1, 9):
                im = self.etat['black'].get((x, y))
                if im is not None:
                    for i in range(1, 9):
                        for j in range(1, 9):
                            try:
                                pf = (i, j)
                                it = self.etat['white'].get(pf)
                                if it is not None:
                                    self.jouer_coupB((x, y), pf)
                                    listeval +=[vali-self.valjeu()]  
                                    self.etat['black'].pop(pf)
                                    self.etat['black'][(x, y)] = im
                                    self.etat['white'][pf] = it
                                else:
                                    self.jouer_coupW((x, y), pf)
                                    self.etat['black'].pop(pf)
                                    self.etat['black'][(x, y)] = im
                                    listeval += [0]
                                    
                            except EchecError:
                                continue
        if listeval != []:
            return max(listeval)
        return -1000 if self.check_echecB() else 0
    
    def valcpB(self):
        listeval = []
        for x in range(1, 9):
            for y in range(1, 9):
                im = self.etat['black'].get((x, y))
                if im is None:
                    break
                for i in range(1, 9):
                    for j in range(1, 9):
                        try:
                            pf = (i, j)
                            val = 0
                            it = self.etat['white'].get(pf)
                            self.jouer_coupB((x, y), pf)
                            
                            if (x, y)[1] == 7 and im == 'P':
                                val += 10
                            if self.check_echecW():
                                val += 1
                            if it == 'P':
                                val += 1
                            elif it == 'T' or it == 'C' or it == 'F':
                                val += 3
                                if it == 'T':
                                    val += 4
                            elif it == 'Q':
                                val += 10
                            listeval += [val]
                        
                            if it is None:
                                self.etat['black'].pop(pf)
                                self.etat['black'][(x, y)] = im
                            else:
                                self.etat['black'].pop(pf)
                                self.etat['black'][(x, y)] = im
                                self.etat['white'][pf] = it
                        except EchecError:
                            continue
        if listeval != []:
            return max(listeval)
        return -100
    
    def stratB2(self):
        if len(self.etat['black']) == 1:
            raise EchecError('les blancs gagnent')
        liste = []
        listeval = []
        for x in range(1, 9):
            for y in range(1, 9):
                for i in range(1, 9):
                    for j in range(1, 9):
                        try:
                            pi = (x, y)
                            pf = (i, j)
                            val = 0
                            im = self.etat['black'].get(pi)
                            it = self.etat['white'].get(pf)
                            self.jouer_coupB(pi, pf)
                            if self.check_echecW():
                                val += 1
                            if it == 'P':
                                val += 1
                            elif it == 'T' or it == 'C' or it == 'F':
                                val += 3
                                if it == 'T':
                                    val += 4
                            elif it == 'Q':
                                val += 10
                            liste += [(pi, pf)]
                            listeval += [val]
                            if it is None:
                                self.etat['black'].pop(pf)
                                self.etat['black'][pi] = im
                            else:
                                self.etat['black'].pop(pf)
                                self.etat['black'][pi] = im
                                self.etat['white'][pf] = it
                        except EchecError:
                            continue
        if liste != []:
            valeur = max(listeval)
            position = listeval.index(valeur)
            coup = liste[position]
            self.jouer_coupB(coup[0], coup[1])
        else:
            if not self.check_echecB():
                raise EchecError('égalité')
            raise EchecError('Échec et math!')
    
    def stratB3(self):
        liste = []
        listeval = []
        vali = self.valjeu()
        for x in range(1, 9):
            for y in range(1, 9):
                im = self.etat['black'].get((x, y))
                if im is not None:
                    for i in range(1, 9):
                        for j in range(1, 9):
                            try:
                                pf = (i, j)
                                it = self.etat['white'].get(pf)
                                self.jouer_coupB((x, y), pf)
                                listeval += [vali - self.valjeu()-self.valcpW()]
                                liste += [[(x, y), pf]]
                                if it is None:
                                    self.etat['black'].pop(pf)
                                    self.etat['black'][(x, y)] = im
                                else:
                                    self.etat['black'].pop(pf)
                                    self.etat['black'][(x, y)] = im
                                    self.etat['white'][pf] = it
                            except EchecError:
                                continue
        if liste != []:
            potentiel = []
            valeur = max(listeval)
            for i, j in enumerate(listeval):
                if j == valeur:
                    potentiel += [liste[i]]
            random.shuffle(potentiel)
            coup = potentiel[0]
            self.jouer_coupB(coup[0], coup[1])
        else:
            if not self.check_echecB():
                raise EchecError('égalité')
            raise EchecError('Échec et mat! (Blancs gagnent)')
    
    def stratW2(self):
        if len(self.etat['white'])+len(self.etat['black']) == 2:
            raise EchecError('égalité')
        liste = []
        listeval = []
        for x in range(1, 9):
            for y in range(1, 9):
                for i in range(1, 9):
                    for j in range(1, 9):
                        try:
                            pi = (x, y)
                            pf = (i, j)
                            val = 0
                            im = self.etat['white'].get(pi)
                            it = self.etat['black'].get(pf)
                            self.jouer_coupW(pi, pf)
                            
                            if im == 'P':
                                val += 0.5
                            if pi[1] == 2 and im == 'P':
                                    val += 10
                            if self.check_echecB():
                                val += 0.5
                            if it == 'P':
                                val += 1
                            elif it == 'T' or it == 'C' or it == 'F':
                                val += 3
                                if it == 'T':
                                    val += 4
                            elif it == 'Q':
                                val += 10
                            val -= self.valcpB()
                            liste += [(pi, pf)]
                            listeval += [val]
                            if it is None:
                                self.etat['white'].pop(pf)
                                self.etat['white'][pi] = im
                            else:
                                self.etat['white'].pop(pf)
                                self.etat['white'][pi] = im
                                self.etat['black'][pf] = it
                        except EchecError:
                            continue
        if liste != []:
            potentiel = []
            valeur = max(listeval)
            for i, j in enumerate(listeval):
                if j == valeur:
                    potentiel += [liste[i]]
            random.shuffle(potentiel)
            coup = potentiel[0]
            self.jouer_coupW(coup[0], coup[1])
        else:
            if not self.check_echecW():
                raise EchecError('égalité')
            raise EchecError('Échec et mat! (Noirs gagnent)')
    
    def check_echecB(self):
        for i in range(1, 9):
            for j in range(1, 9):
                try:
                    for h, k in self.etat['black'].items():
                        if k == 'K':
                            pf = h
                    im = self.etat['white'].get((i, j))
                    if im is None:
                        raise EchecError('pas de pion a cet emplacement')
                    if im == 'P':
                        self.deplacer_pionW((i, j), pf)
                    elif im == 'C':
                        self.deplacer_chevalW((i, j), pf)
                    elif im == 'K':
                        self.deplacer_roiW((i, j), pf)
                    elif im == 'T':
                        self.deplacer_tourW((i, j), pf)
                    elif im == 'F':
                        self.deplacer_fouW((i, j), pf)
                    elif im == 'Q':
                        self.deplacer_dameW((i, j), pf)
                    
                    self.etat['white'][(i, j)] = im
                    self.etat['white'].pop(pf)
                    self.etat['black'][pf] = 'K'
                    return True
                    break
                except EchecError:
                    continue
        return False
    
    def stratW(self):
        if len(self.etat['white']) == 1:
            raise EchecError('les noirs gagnent')
        e = 0
        v = 0                  
        g = 0
        n = list(self.etat['black'].keys())
        q = list(self.etat['white'].keys())
        for pf in n:
            if g == 1:
                break
            for pi in q:
                try:
                    self.jouer_coupW(pi, pf)
                    g = 1 
                    v = 1
                    e = 1
                    break
                except EchecError as err:
                    continue
        if v == 0:
            g = 0
            e = 0
            for b in range(1, 9):
                if g == 1:
                    break
                for c in range(1, 9):
                    if g == 1:
                        break
                    for d in range(1, 9):
                        if g == 1:
                            break
                        for e in range(1, 9):
                            try:
                                self.jouer_coupW((b, c), (d, e) )
                                g = 1
                                e = 1
                                break 
                            except EchecError as err:
                                continue
        if e == 0:
            if not self.check_echecW():
                raise EchecError('Égalité')
            raise EchecError('Échec et math!')
    
    def check_echecW(self):
        for h, k in self.etat['white'].items():
                        if k == 'K':
                            pf = h
        for i in range(1, 9):
            for j in range(1, 9):
                try:
                    im = self.etat['black'].get((i, j))
                    if im is None:
                        raise EchecError('pas de pion a cet emplacement')
                    elif im == 'P':
                        self.deplacer_pionB((i, j), pf)
                    elif im == 'C':
                        self.deplacer_chevalB((i, j), pf)
                    elif im == 'K':
                        self.deplacer_roiB((i, j), pf)
                    elif im == 'T':
                        self.deplacer_tourB((i, j), pf)
                    elif im == 'F':
                        self.deplacer_fouB((i, j), pf)
                    elif im == 'Q':
                        self.deplacer_dameB((i, j), pf)
                    self.etat['black'][(i, j)] = im
                    self.etat['black'].pop(pf)
                    self.etat['white'][pf] = 'K'
                    return True
                    break
                except EchecError:
                    continue
        return False
    
    def stratB(self):
        if len(self.etat['black']) == 1:
            raise EchecError('les blancs gagnent')
        liste = []
        listeval = []
        for x in range(1, 9):
            for y in range(1, 9):
                for i in range(1, 9):
                    for j in range(1, 9):
                        try:
                            pi = (x, y)
                            pf = (i, j)
                            val = 0
                            im = self.etat['black'].get(pi)
                            it = self.etat['white'].get(pf)
                            self.jouer_coupB(pi, pf)
                            if self.check_echecW():
                                val += 1
                            if it == 'P':
                                val += 1
                            elif it == 'T' or it == 'C' or it == 'F':
                                val += 2
                            elif it == 'Q':
                                val += 4
                            liste += [(pi, pf)]
                            listeval += [val]
                            if it is None:
                                self.etat['black'].pop(pf)
                                self.etat['black'][pi] = im
                            else:
                                self.etat['black'].pop(pf)
                                self.etat['black'][pi] = im
                                self.etat['white'][pf] = it
                        except EchecError:
                            continue
        if liste != []:
            valeur = max(listeval)
            position = listeval.index(valeur)
            coup = liste[position]
            self.jouer_coupB(coup[0], coup[1])
        else:
            if not self.check_echecB():
                raise EchecError('égalité')
            raise EchecError('Échec et math!')
    
    def __init__(self, état=None):
        if état is None:
            self.etat = {'white': {(1, 8): 'T', (8, 8): 'T', (2, 8): 'C', (7, 8): 'C', (3, 8): 'F', (6, 8): 'F', (5, 8): 'Q', (4, 8): 'K', (1, 7): 'P', (2, 7): 'P', (3, 7): 'P', (4, 7): 'P', (5, 7): 'P', (6, 7): 'P', (7, 7): 'P', (8, 7): 'P'}, 'black': {(1, 1): 'T', (8, 1): 'T', (2, 1): 'C', (7, 1): 'C', (3, 1): 'F', (6, 1): 'F', (5, 1): 'Q', (4, 1): 'K', (1, 2): 'P', (2, 2): 'P', (3, 2): 'P', (4, 2): 'P', (5, 2): 'P', (6, 2): 'P', (7, 2): 'P', (8, 2): 'P'}}
        else:
            self.etat = état
    
    def état(self):
        return self.etat   
    
    def __str__(self):
        "Afiche le jeu avec un dictionnaire état"
        dicoW = {'K': '♔', 'Q':'♕', 'F':'♗', 'T':'♖', 'C':'♘', 'P':'♙'}
        dicoB = {'K': '♚', 'Q':'♛', 'F':'♝', 'T':'♜', 'C':'♞', 'P':'♟'}
        sui = 3*' '+'-'*31+'\n'
        for i in range(7):
            sui += str(8-i)+' | '+7*'.   '+'. |'+'\n'+'  |                               |'+'\n'
        fin = '1 |' + ' .  '*7 + ' . |'+'\n'+'--|' + '-'*31 + '\n'
        fin2 = '  | 1   2   3   4   5   6   7   8'
        tot = list(sui+fin+fin2)
        for j in self.etat['black'].keys(): 
            tot[(36*(16-2*j[1]))+4*j[0]+35] = dicoB[str(self.etat['black'][j])]
        for j in self.etat['white'].keys(): 
            tot[(36*(16-2*j[1]))+4*j[0]+35] = dicoW[str(self.etat['white'][j])]
        return(''.join(tot))
    
    def jouer_coupW(self, pi, pf):
        l1 = len(self.etat['black'].values())
        it = self.etat['black'].get(pf)
        if 8 >= pf[0] > 0 and 8 >= pf[1] > 0:
            if self.etat['white'].get(pi):
                a = self.etat['white'][pi]
                if a == 'P':
                    self.deplacer_pionW(pi, pf)
                elif a == 'C':
                    self.deplacer_chevalW(pi, pf)
                elif a == 'K':
                    self.deplacer_roiW(pi, pf)
                elif a == 'T':
                    self.deplacer_tourW(pi, pf)
                elif a == 'F':
                    self.deplacer_fouW(pi, pf)
                elif a == 'Q':
                    self.deplacer_dameW(pi, pf)
            else:
                raise EchecError('pas de pion a cette place la')
        else:
            raise EchecError('impossible de sortir du damier')
        l2 = len(self.etat['black'].values())
        if self.check_echecW() is True:
            if l1 == l2:
                self.etat['white'][pi] = a
                self.etat['white'].pop(pf)
                raise EchecError('votre roi est toujours en echec')
            elif l1 != l2:
                self.etat['white'][pi] = a
                self.etat['white'].pop(pf)
                self.etat['black'][pf] = it
                raise EchecError('Votre roi est toujours en échec')
    
    def deplacer_chevalB(self, pi, pf):
        liste = []
        liste += [(pi[0]+2, pi[1]+1)]
        liste += [(pi[0]+2, pi[1]-1)]
        liste += [(pi[0]-2, pi[1]+1)]
        liste += [(pi[0]-2, pi[1]-1)]
        liste += [(pi[0]+1, pi[1]+2)]
        liste += [(pi[0]+1, pi[1]-2)]
        liste += [(pi[0]-1, pi[1]+2)]
        liste += [(pi[0]-1, pi[1]-2)]
        p = 0
        q = 0
        for r in liste:
            if pf == r:
                if self.etat['black'].get(pf):
                    raise EchecError('le coup est invalide')
                    q = 1
                else:    
                    self.etat['black'].pop(pi)
                    self.etat['black'][pf] = 'C'
                    p = 1
                    if self.etat['white'].get(pf):
                        self.etat['white'].pop(pf)
        if p == 0 and q == 0:
            raise EchecError('Le coup est invalide')
    
    def deplacer_roiB(self, pi, pf):
        liste = []
        liste += [(pi[0]+1, pi[1])]
        liste += [(pi[0]-1, pi[1])]
        liste += [(pi[0], pi[1]+1)]
        liste += [((pi[0], pi[1]-1))]
        liste += [(pi[0]+1, pi[1]+1)]
        liste += [((pi[0]+1, pi[1]-1))]
        liste += [(pi[0]-1, pi[1]+1)]
        liste += [((pi[0]-1, pi[1]-1))]         
        p = 0
        q = 0
        for r in liste:   
            if pf == r:
                if self.etat['black'].get(pf):
                    raise EchecError('le coup est invalide')
                    q = 1
                else:
                    self.etat['black'].pop(pi)
                    self.etat['black'][pf] = 'K'
                    p = 1
                    if self.etat['white'].get(pf):
                        self.etat['white'].pop(pf)
        if p == 0 and q == 0:
            raise EchecError('Le coup est invalide')
    
    def deplacer_roiW(self, pi, pf):
        liste = []
        liste += [(pi[0]+1, pi[1])]
        liste += [(pi[0]-1, pi[1])]
        liste += [(pi[0], pi[1]+1)]
        liste += [((pi[0], pi[1]-1))]
        liste += [(pi[0]+1, pi[1]+1)]
        liste += [((pi[0]+1, pi[1]-1))]
        liste += [(pi[0]-1, pi[1]+1)]
        liste += [((pi[0]-1, pi[1]-1))]
        p = 0
        q = 0
        for r in liste:   
            if pf == r:
                if self.etat['white'].get(pf):
                    raise EchecError('le coup est invalide')
                    q = 1
                else:
                    self.etat['white'].pop(pi)
                    self.etat['white'][pf] = 'K'
                    p = 1
                    if self.etat['black'].get(pf):
                        self.etat['black'].pop(pf)
        if p == 0 and q == 0:
            raise EchecError('Le coup est invalide')
    
    def deplacer_chevalW(self, pi, pf):
        liste = []
        liste += [(pi[0]+2, pi[1]+1)]
        liste += [(pi[0]+2, pi[1]-1)]
        liste += [(pi[0]-2, pi[1]+1)]
        liste += [(pi[0]-2, pi[1]-1)]
        liste += [(pi[0]+1, pi[1]+2)]
        liste += [(pi[0]+1, pi[1]-2)]
        liste += [(pi[0]-1, pi[1]+2)]
        liste += [(pi[0]-1, pi[1]-2)]
        p = 0
        q = 0
        for r in liste:
            
            if pf == r:
                if self.etat['white'].get(pf):
                    raise EchecError('le coup est invalide')
                    q = 1
                else:
                    self.etat['white'].pop(pi)
                    self.etat['white'][pf] = 'C'
                    p = 1
                    if self.etat['black'].get(pf):
                        self.etat['black'].pop(pf)
        if p == 0 and q == 0:
            raise EchecError('coup invalide')
    
    def jouer_coupB(self, pi, pf):
        l1 = len(self.etat['white'].values())
        it = self.etat['white'].get(pf)
        if 8 >= pf[0] > 0 and 8 >= pf[1] > 0:
            if self.etat['black'].get(pi):
                a = self.etat['black'][pi]
                if a == 'P':
                    self.deplacer_pionB(pi, pf)
                elif a == 'C':
                    self.deplacer_chevalB(pi, pf)
                elif a == 'K':
                    self.deplacer_roiB(pi, pf)
                elif a == 'T':
                    self.deplacer_tourB(pi, pf)
                elif a == 'F':
                    self.deplacer_fouB(pi, pf)
                elif a == 'Q':
                    self.deplacer_dameB(pi, pf)
            else:
                raise EchecError('pas de pion a cette place la')
        else:
            raise EchecError('impossible de sortir du damier')
        l2 = len(self.etat['white'].values())
        if self.check_echecB() is True:
            if l1 == l2:
                self.etat['black'][pi] = a
                self.etat['black'].pop(pf)
                raise EchecError('Votre roi est toujours en echec')
            elif l1 != l2:
                self.etat['black'][pi] = a
                self.etat['black'].pop(pf)
                self.etat['white'][pf] = it
                raise EchecError('votre roi est toujours en echec')
    
    def deplacer_pionB(self, pi, pf):
        liste = []
        if not self.etat['black'].get((pi[0], pi[1]+1)) and not self.etat['white'].get((pi[0], pi[1]+1)):
            liste += [(pi[0], pi[1]+1)]
            if not self.etat['black'].get((pi[0], pi[1]+2)) and not self.etat['white'].get((pi[0], pi[1]+2)) and pi[1] == 2:
                liste += [(pi[0], pi[1]+2)]
        if self.etat['white'].get((pi[0]+1, pi[1]+1)):
            liste += [(pi[0]+1, pi[1]+1)]
        if self.etat['white'].get((pi[0]-1, pi[1]+1)):
            liste += [(pi[0]-1, pi[1]+1)]
        p = 0
        for r in liste:
            if pf == r:
                self.etat['black'].pop(pi)
                self.etat['black'][pf] = 'P'
                if pf[1] == 8:
                    self.etat['black'][pf] = 'Q'
                p = 1
                if self.etat['white'].get(pf):
                    self.etat['white'].pop(pf)
        if p == 0:
            raise EchecError('coup invalide')
    
    def deplacer_pionW(self, pi, pf):
        liste = []
        if not self.etat['white'].get((pi[0], pi[1]-1)) and not self.etat['black'].get((pi[0], pi[1]-1)):
            liste += [((pi[0], pi[1]-1))]
            if pi[1] == 7 and not self.etat['black'].get((pi[0], pi[1]-2)) and not self.etat['white'].get((pi[0], pi[1]-2)):
                liste += [(pi[0], pi[1]-2)]
        if self.etat['black'].get((pi[0]+1, pi[1]-1)):
            liste += [((pi[0]+1, pi[1]-1))]
        if self.etat['black'].get((pi[0]-1, pi[1]-1)):
            liste += [(pi[0]-1, pi[1]-1)]
        p = 0
        for r in liste:
            if pf == r:
                self.etat['white'].pop(pi)
                self.etat['white'][pf] = 'P'
                if pf[1] == 1:
                    self.etat['white'][pf] = 'Q'
                p = 1
                if self.etat['black'].get(pf):
                    self.etat['black'].pop(pf)
        if p == 0:
            raise EchecError('coup invalide')
    
    def deplacer_tourW(self, pi, pf):
        liste = []
        for i in range(8):
            if pi[1]+i > 7:
                break
            if not self.etat['white'].get((pi[0], pi[1]+i+1)):
                liste += [(pi[0], pi[1]+1+i)]
            if self.etat['black'].get((pi[0], pi[1]+i+1)):
                break
            if self.etat['white'].get((pi[0], pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2:
                break
            if not self.etat['white'].get((pi[0], pi[1]-i-1)):
                liste += [(pi[0], pi[1]-1-i)]
            if self.etat['black'].get((pi[0], pi[1]-i-1)):
                break
            if self.etat['white'].get((pi[0], pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2:
                break
            if not self.etat['white'].get((pi[0]-i-1, pi[1])):
                liste += [(pi[0]-i-1, pi[1])]
            if self.etat['black'].get((pi[0]-i-1, pi[1])):
                break
            if self.etat['white'].get((pi[0]-1-i, pi[1])):
                break
        for i in range(8):
            if pi[0]+i > 7:
                break
            if not self.etat['white'].get((pi[0]+i+1, pi[1])):
                liste += [(pi[0]+i+1, pi[1])]
            if self.etat['black'].get((pi[0]+i+1, pi[1])):
                break
            if self.etat['white'].get((pi[0]+1+i, pi[1])):
                break
        p = 0
        for r in liste:
            if pf == r:
                self.etat['white'].pop(pi)
                self.etat['white'][pf] = 'T'
                p = 1
                if self.etat['black'].get(pf):
                    self.etat['black'].pop(pf)
        if p == 0 :
          raise EchecError('le coup est invalide')
    
    def deplacer_tourB(self, pi, pf):
        liste = []
        for i in range(8):
            if pi[1]+i > 7:
                break
            if not self.etat['black'].get((pi[0], pi[1]+i+1)):
                liste += [(pi[0], pi[1]+1+i)]
            if self.etat['white'].get((pi[0], pi[1]+i+1)):
                break
            if self.etat['black'].get((pi[0], pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2:
                break
            if not self.etat['black'].get((pi[0], pi[1]-i-1)):
                liste += [(pi[0], pi[1]-1-i)]
            if self.etat['white'].get((pi[0], pi[1]-i-1)):
                break
            if self.etat['black'].get((pi[0], pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2:
                break
            if not self.etat['black'].get((pi[0]-i-1, pi[1])):
                liste += [(pi[0]-i-1, pi[1])]
            if self.etat['white'].get((pi[0]-i-1, pi[1])):
                break
            if self.etat['black'].get((pi[0]-1-i, pi[1])):
                break
        for i in range(8):
            if pi[0]+i > 7:
                break
            if not self.etat['black'].get((pi[0]+i+1, pi[1])):
                liste += [(pi[0]+i+1, pi[1])]
            if self.etat['white'].get((pi[0]+i+1, pi[1])):
                break
            if self.etat['black'].get((pi[0]+1+i, pi[1])):
                break
        p = 0
        for r in liste:
            if pf == r:
                self.etat['black'].pop(pi)
                self.etat['black'][pf] = 'T'
                p = 1
                if self.etat['white'].get(pf):
                    self.etat['white'].pop(pf)
        if p == 0 :
          raise EchecError('le coup est invalide')
    
    def deplacer_fouB(self, pi, pf):
        liste = []
        for i in range(8):
            if pi[1]+i > 7 or pi[0]+i > 7 :
                break
            if not self.etat['black'].get((pi[0]+i+1, pi[1]+i+1)):
                liste += [(pi[0]+1+i, pi[1]+1+i)]
            if self.etat['white'].get((pi[0]+1+i, pi[1]+i+1)):
                break
            if self.etat['black'].get((pi[0]+1+i, pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2 or pi[0]+i > 7:
                break
            if not self.etat['black'].get((pi[0]+1+i, pi[1]-i-1)):
                liste += [(pi[0]+1+i, pi[1]-1-i)]
            if self.etat['white'].get((pi[0]+1+i, pi[1]-i-1)):
                break
            if self.etat['black'].get((pi[0]+1+i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]-i < 2:
                break
            if not self.etat['black'].get((pi[0]-i-1, pi[1]-i-1)):
                liste += [(pi[0]-i-1, pi[1]-i-1)]
            if self.etat['white'].get((pi[0]-i-1, pi[1]-i-1)):
                break
            if self.etat['black'].get((pi[0]-1-i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]+i > 7:
                break
            if not self.etat['black'].get((pi[0]-i-1, pi[1]+i+1)):
                liste += [(pi[0]-i-1, pi[1]+i+1)]
            if self.etat['white'].get((pi[0]-i-1, pi[1]+i+1)):
                break
            if self.etat['black'].get((pi[0]-i-1, pi[1]+i+1)):
                break
        p = 0
        for r in liste:
            if pf == r:
                self.etat['black'].pop(pi)
                self.etat['black'][pf] = 'F'
                p = 1
                if self.etat['white'].get(pf):
                    self.etat['white'].pop(pf)
        if p == 0 :
          raise EchecError('le coup est invalide')
    
    def deplacer_fouW(self, pi, pf):
        liste = []
        for i in range(8):
            if pi[1]+i > 7 or pi[0]+i > 7 :
                break
            if not self.etat['white'].get((pi[0]+i+1, pi[1]+i+1)):
                liste += [(pi[0]+1+i, pi[1]+1+i)]
            if self.etat['black'].get((pi[0]+1+i, pi[1]+i+1)):
                break
            if self.etat['white'].get((pi[0]+1+i, pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2 or pi[0]+i > 7:
                break
            if not self.etat['white'].get((pi[0]+1+i, pi[1]-i-1)):
                liste += [(pi[0]+1+i, pi[1]-1-i)]
            if self.etat['black'].get((pi[0]+1+i, pi[1]-i-1)):
                break
            if self.etat['white'].get((pi[0]+1+i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]-i < 2:
                break
            if not self.etat['white'].get((pi[0]-i-1, pi[1]-i-1)):
                liste += [(pi[0]-i-1, pi[1]-i-1)]
            if self.etat['black'].get((pi[0]-i-1, pi[1]-i-1)):
                break
            if self.etat['white'].get((pi[0]-1-i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]+i > 7:
                break
            if not self.etat['white'].get((pi[0]-i-1, pi[1]+i+1)):
                liste += [(pi[0]-i-1, pi[1]+i+1)]
            if self.etat['black'].get((pi[0]-i-1, pi[1]+i+1)):
                break
            if self.etat['white'].get((pi[0]-1-i, pi[1]+i+1)):
                break
        p = 0
        for r in liste:
            if pf == r:
                self.etat['white'].pop(pi)
                self.etat['white'][pf] = 'F'
                p = 1
                if self.etat['black'].get(pf):
                    self.etat['black'].pop(pf)
        if p == 0 :
          raise EchecError('le coup est invalide')
    
    def deplacer_dameW(self, pi, pf):
        liste = []
        for i in range(8):
            if pi[1]+i > 7:
                break
            if not self.etat['white'].get((pi[0], pi[1]+i+1)):
                liste += [(pi[0], pi[1]+1+i)]
            if self.etat['black'].get((pi[0], pi[1]+i+1)):
                break
            if self.etat['white'].get((pi[0], pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2:
                break
            if not self.etat['white'].get((pi[0], pi[1]-i-1)):
                liste += [(pi[0], pi[1]-1-i)]
            if self.etat['black'].get((pi[0], pi[1]-i-1)):
                break
            if self.etat['white'].get((pi[0], pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2:
                break
            if not self.etat['white'].get((pi[0]-i-1, pi[1])):
                liste += [(pi[0]-i-1, pi[1])]
            if self.etat['black'].get((pi[0]-i-1, pi[1])):
                break
            if self.etat['white'].get((pi[0]-1-i, pi[1])):
                break
        for i in range(8):
            if pi[0]+i > 7:
                break
            if not self.etat['white'].get((pi[0]+i+1, pi[1])):
                liste += [(pi[0]+i+1, pi[1])]
            if self.etat['black'].get((pi[0]+i+1, pi[1])):
                break
            if self.etat['white'].get((pi[0]+1+i, pi[1])):
                break
        for i in range(8):
            if pi[1]+i > 7 or pi[0]+i > 7 :
                break
            if not self.etat['white'].get((pi[0]+i+1, pi[1]+i+1)):
                liste += [(pi[0]+1+i, pi[1]+1+i)]
            if self.etat['black'].get((pi[0]+1+i, pi[1]+i+1)):
                break
            if self.etat['white'].get((pi[0]+1+i, pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2 or pi[0]+i > 7:
                break
            if not self.etat['white'].get((pi[0]+1+i, pi[1]-i-1)):
                liste += [(pi[0]+1+i, pi[1]-1-i)]
            if self.etat['black'].get((pi[0]+1+i, pi[1]-i-1)):
                break
            if self.etat['white'].get((pi[0]+1+i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]-i < 2:
                break
            if not self.etat['white'].get((pi[0]-i-1, pi[1]-i-1)):
                liste += [(pi[0]-i-1, pi[1]-i-1)]
            if self.etat['black'].get((pi[0]-i-1, pi[1]-i-1)):
                break
            if self.etat['white'].get((pi[0]-1-i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]+i > 7:
                break
            if not self.etat['white'].get((pi[0]-i-1, pi[1]+i+1)):
                liste += [(pi[0]-i-1, pi[1]+i+1)]
            if self.etat['black'].get((pi[0]-i-1, pi[1]+i+1)):
                break
            if self.etat['white'].get((pi[0]-1-i, pi[1]+i+1)):
                break
        p = 0
        for r in liste:
            if pf == r:
                self.etat['white'].pop(pi)
                self.etat['white'][pf] = 'Q'
                p = 1
                if self.etat['black'].get(pf):
                    self.etat['black'].pop(pf)
        if p == 0 :
          raise EchecError('le coup est invalide')
    
    def deplacer_dameB(self, pi, pf):
        liste = []
        for i in range(8):
            if pi[1]+i > 7:
                break
            if not self.etat['black'].get((pi[0], pi[1]+i+1)):
                liste += [(pi[0], pi[1]+1+i)]
            if self.etat['white'].get((pi[0], pi[1]+i+1)):
                break
            if self.etat['black'].get((pi[0], pi[1]+i+1)):
                break
        for i in range(8):
                if pi[1]-i < 2:
                    break
                if not self.etat['black'].get((pi[0], pi[1]-i-1)):
                    liste += [(pi[0], pi[1]-1-i)]
                if self.etat['white'].get((pi[0], pi[1]-i-1)):
                    break
                if self.etat['black'].get((pi[0], pi[1]-i-1)):
                    break
        for i in range(8):
            if pi[0]-i < 2:
                break
            if not self.etat['black'].get((pi[0]-i-1, pi[1])):
                liste += [(pi[0]-i-1, pi[1])]
            if self.etat['white'].get((pi[0]-i-1, pi[1])):
                break
            if self.etat['black'].get((pi[0]-i-1, pi[1])):
                break
        for i in range(8):
            if pi[0]+i > 7:
                break
            if not self.etat['black'].get((pi[0]+i+1, pi[1])):
                liste += [(pi[0]+i+1, pi[1])]
            if self.etat['white'].get((pi[0]+i+1, pi[1])):
                break
            if self.etat['black'].get((pi[0]+i+1, pi[1])):
                break
        for i in range(8):
            if pi[1]+i > 7 or pi[0]+i > 7 :
                break
            if not self.etat['black'].get((pi[0]+i+1, pi[1]+i+1)):
                liste += [(pi[0]+1+i, pi[1]+1+i)]
            if self.etat['white'].get((pi[0]+1+i, pi[1]+i+1)):
                break
            if self.etat['black'].get((pi[0]+i+1, pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2 or pi[0]+i > 7:
                break
            if not self.etat['black'].get((pi[0]+1+i, pi[1]-i-1)):
                liste += [(pi[0]+1+i, pi[1]-1-i)]
            if self.etat['white'].get((pi[0]+1+i, pi[1]-i-1)):
                break
            if self.etat['black'].get((pi[0]+i+1, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]-i < 2:
                break
            if not self.etat['black'].get((pi[0]-i-1, pi[1]-i-1)):
                liste += [(pi[0]-i-1, pi[1]-i-1)]
            if self.etat['white'].get((pi[0]-i-1, pi[1]-i-1)):
                break
            if self.etat['black'].get((pi[0]-i-1, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]+i > 7:
                break
            if not self.etat['black'].get((pi[0]-i-1, pi[1]+i+1)):
                liste += [(pi[0]-i-1, pi[1]+i+1)]
            if self.etat['white'].get((pi[0]-i-1, pi[1]+i+1)):
                break
            if self.etat['black'].get((pi[0]-i-1, pi[1]+i+1)):
                break
        p = 0
        for r in liste:
            if pf == r:
                self.etat['black'].pop(pi)
                self.etat['black'][pf] = 'Q'
                p = 1
                if self.etat['white'].get(pf):
                    self.etat['white'].pop(pf)
        if p == 0 :
            raise EchecError('le coup est invalide')

class echecX(echec):
    def __init__(self, état=None):
        super().__init__(état)
        joe = turtle.Turtle(visible=None)
        joe.shape(None)
        joe.speed(0)
        n = 25
        for c in range(9):
            tracerpolygone(joe, ((-(8-2*c)*n, -8*n), (-(8-2*c)*n, 8*n)))
            tracerpolygone(joe, ((8*n, -(8-2*c)*n), (-8*n, -(8-2*c)*n)))

        # Screen
        fen = turtle.Screen()
        fen.title('Echec')
        fen.bgcolor('grey')
        fen.setup(width=22*n, height=22*n)

        self.marc = turtle.Turtle(visible=None)
        self.marc.penup()

        # Déplacement de marc
        for a in range(1, 9):
            self.marc.goto(-9*n+a*2*n, 8*n)
            self.marc.write(str(a), align='center', font=('arial', 27, 'bold'))
        for a in range(1, 9):
            self.marc.goto(-9*n, -10*n+3+2*n*a)
            self.marc.write(str(a), align='center', font=('arial', 27, 'bold'))
        self.afficher()

    def afficher(self):
        "permet d'afficher dans un fenetre graphique les actualisation du jeu"
        n = 25
        for i in range(1, 9):
            for j in range(1, 9):
                toto = turtle.Turtle(shape='square')
                toto.penup()
                toto.shapesize(0.075*n)
                toto.color('grey')
                toto.speed(0)
                toto.goto(-9*n + 2*n*(i), -9*n + 2*n*(j))
        for pb in self.etat['black']:
            if self.etat['black'][pb] == 'Q' or self.etat['black'][pb] == 'K' or self.etat['black'][pb] == 'C':
                s = "Fou"
            elif self.etat['black'][pb] == 'P':
                s = 'circle'
            elif self.etat['black'][pb] == 'T' or self.etat['black'][pb] == 'F':
                s = 'square'
            self.pb = turtle.Turtle(shape=s)
            self.pb.penup()
            self.pb.shapesize(0.075*n)
            self.pb.color('black')
            self.pb.speed(0)
            self.pb.goto(-9*n + 2*n*(pb[0]), -9*n + 2*n*(pb[1]))
        for pb in self.etat['white']:
            if self.etat['white'][pb] == 'Q' or self.etat['white'][pb] == 'K' or self.etat['white'][pb] == 'C':
                s = 'triangle'
            elif self.etat['white'][pb] == 'P':
                s = 'circle'
            elif self.etat['white'][pb] == 'T' or self.etat['white'][pb] == 'F':
                s = 'square'
            self.pb = turtle.Turtle(shape=s)
            self.pb.penup()
            self.pb.shapesize(0.075*n)
            self.pb.color('white')
            self.pb.speed(0)
            self.pb.goto(-9*n + 2*n*(pd[0]), -9*n + 2*n*(pb[1]))
class echecXX(echec):
    def __init__(self, état=None):
        super().__init__(état)
        joe = turtle.Turtle(visible=None)
        joe.shape(None)
        joe.speed(0)
        n = 25
        self.fen = turtle.Screen()
        self.fen.title('Echec')
        self.fen.bgcolor('green')
        self.fen.setup(width=22*n, height=22*n)
        self.uu = turtle.Turtle(shape='square')
        self.uu.penup()
        self.uu.shapesize(0.075*n)
        self.uu.color('black')
        self.uu.speed(0)
        self.uu.goto(-9*n + 2*n*(1), -9*n + 2*n*(1))
        self.ud = turtle.Turtle(shape='square')
        self.ud.penup()
        self.ud.shapesize(0.075*n)
        self.ud.color('white')
        self.ud.speed(0)
        self.ud.goto(-9*n + 2*n*(1), -9*n + 2*n*(2))
        self.ut = turtle.Turtle(shape='square')
        self.ut.penup()
        self.ut.shapesize(0.075*n)
        self.ut.color('black')
        self.ut.speed(0)
        self.ut.goto(-9*n + 2*n*(1), -9*n + 2*n*(3))
        self.uq = turtle.Turtle(shape='square')
        self.uq.penup()
        self.uq.shapesize(0.075*n)
        self.uq.color('white')
        self.uq.speed(0)
        self.uq.goto(-9*n + 2*n*(1), -9*n + 2*n*(4))
        self.uc = turtle.Turtle(shape='square')
        self.uc.penup()
        self.uc.shapesize(0.075*n)
        self.uc.color('black')
        self.uc.speed(0)
        self.uc.goto(-9*n + 2*n*(1), -9*n + 2*n*(5))
        self.us = turtle.Turtle(shape='square')
        self.us.penup()
        self.us.shapesize(0.075*n)
        self.us.color('white')
        self.us.speed(0)
        self.us.goto(-9*n + 2*n*(1), -9*n + 2*n*(6))
        self.usp = turtle.Turtle(shape='square')
        self.usp.penup()
        self.usp.shapesize(0.075*n)
        self.usp.color('black')
        self.usp.speed(0)
        self.usp.goto(-9*n + 2*n*(1), -9*n + 2*n*(7))
        self.uh = turtle.Turtle(shape='square')
        self.uh.penup()
        self.uh.shapesize(0.075*n)
        self.uh.color('white')
        self.uh.speed(0)
        self.uh.goto(-9*n + 2*n*(1), -9*n + 2*n*(8))
        self.du = turtle.Turtle(shape='square')
        self.du.penup()
        self.du.shapesize(0.075*n)
        self.du.color('white')
        self.du.speed(0)
        self.du.goto(-9*n + 2*n*(2), -9*n + 2*n*(1))
        self.dd = turtle.Turtle(shape='square')
        self.dd.penup()
        self.dd.shapesize(0.075*n)
        self.dd.color('black')
        self.dd.speed(0)
        self.dd.goto(-9*n + 2*n*(2), -9*n + 2*n*(2))
        self.dt = turtle.Turtle(shape='square')
        self.dt.penup()
        self.dt.shapesize(0.075*n)
        self.dt.color('white')
        self.dt.speed(0)
        self.dt.goto(-9*n + 2*n*(2), -9*n + 2*n*(3))
        self.dq = turtle.Turtle(shape='square')
        self.dq.penup()
        self.dq.shapesize(0.075*n)
        self.dq.color('black')
        self.dq.speed(0)
        self.dq.goto(-9*n + 2*n*(2), -9*n + 2*n*(4))
        self.dc = turtle.Turtle(shape='square')
        self.dc.penup()
        self.dc.shapesize(0.075*n)
        self.dc.color('white')
        self.dc.speed(0)
        self.dc.goto(-9*n + 2*n*(2), -9*n + 2*n*(5))
        self.ds = turtle.Turtle(shape='square')
        self.ds.penup()
        self.ds.shapesize(0.075*n)
        self.ds.color('black')
        self.ds.speed(0)
        self.ds.goto(-9*n + 2*n*(2), -9*n + 2*n*(6))
        self.dsp = turtle.Turtle(shape='square')
        self.dsp.penup()
        self.dsp.shapesize(0.075*n)
        self.dsp.color('white')
        self.dsp.speed(0)
        self.dsp.goto(-9*n + 2*n*(2), -9*n + 2*n*(7))
        self.dh = turtle.Turtle(shape='square')
        self.dh.penup()
        self.dh.shapesize(0.075*n)
        self.dh.color('black')
        self.dh.speed(0)
        self.dh.goto(-9*n + 2*n*(2), -9*n + 2*n*(8))
        self.tu = turtle.Turtle(shape='square')
        self.tu.penup()
        self.tu.shapesize(0.075*n)
        self.tu.color('black')
        self.tu.speed(0)
        self.tu.goto(-9*n + 2*n*(3), -9*n + 2*n*(1))
        self.td = turtle.Turtle(shape='square')
        self.td.penup()
        self.td.shapesize(0.075*n)
        self.td.color('white')
        self.td.speed(0)
        self.td.goto(-9*n + 2*n*(3), -9*n + 2*n*(2))
        self.tt = turtle.Turtle(shape='square')
        self.tt.penup()
        self.tt.shapesize(0.075*n)
        self.tt.color('black')
        self.tt.speed(0)
        self.tt.goto(-9*n + 2*n*(3), -9*n + 2*n*(3))
        self.tq = turtle.Turtle(shape='square')
        self.tq.penup()
        self.tq.shapesize(0.075*n)
        self.tq.color('white')
        self.tq.speed(0)
        self.tq.goto(-9*n + 2*n*(3), -9*n + 2*n*(4))
        self.tc = turtle.Turtle(shape='square')
        self.tc.penup()
        self.tc.shapesize(0.075*n)
        self.tc.color('black')
        self.tc.speed(0)
        self.tc.goto(-9*n + 2*n*(3), -9*n + 2*n*(5))
        self.ts = turtle.Turtle(shape='square')
        self.ts.penup()
        self.ts.shapesize(0.075*n)
        self.ts.color('white')
        self.ts.speed(0)
        self.ts.goto(-9*n + 2*n*(3), -9*n + 2*n*(6))
        self.tsp = turtle.Turtle(shape='square')
        self.tsp.penup()
        self.tsp.shapesize(0.075*n)
        self.tsp.color('black')
        self.tsp.speed(0)
        self.tsp.goto(-9*n + 2*n*(3), -9*n + 2*n*(7))
        self.th = turtle.Turtle(shape='square')
        self.th.penup()
        self.th.shapesize(0.075*n)
        self.th.color('white')
        self.th.speed(0)
        self.th.goto(-9*n + 2*n*(3), -9*n + 2*n*(8))
        self.qu = turtle.Turtle(shape='square')
        self.qu.penup()
        self.qu.shapesize(0.075*n)
        self.qu.color('white')
        self.qu.speed(0)
        self.qu.goto(-9*n + 2*n*(4), -9*n + 2*n*(1))
        self.qd = turtle.Turtle(shape='square')
        self.qd.penup()
        self.qd.shapesize(0.075*n)
        self.qd.color('black')
        self.qd.speed(0)
        self.qd.goto(-9*n + 2*n*(4), -9*n + 2*n*(2))
        self.qt = turtle.Turtle(shape='square')
        self.qt.penup()
        self.qt.shapesize(0.075*n)
        self.qt.color('white')
        self.qt.speed(0)
        self.qt.goto(-9*n + 2*n*(4), -9*n + 2*n*(3))
        self.qq = turtle.Turtle(shape='square')
        self.qq.penup()
        self.qq.shapesize(0.075*n)
        self.qq.color('black')
        self.qq.speed(0)
        self.qq.goto(-9*n + 2*n*(4), -9*n + 2*n*(4))
        self.qc = turtle.Turtle(shape='square')
        self.qc.penup()
        self.qc.shapesize(0.075*n)
        self.qc.color('white')
        self.qc.speed(0)
        self.qc.goto(-9*n + 2*n*(4), -9*n + 2*n*(5))
        self.qs = turtle.Turtle(shape='square')
        self.qs.penup()
        self.qs.shapesize(0.075*n)
        self.qs.color('black')
        self.qs.speed(0)
        self.qs.goto(-9*n + 2*n*(4), -9*n + 2*n*(6))
        self.qsp = turtle.Turtle(shape='square')
        self.qsp.penup()
        self.qsp.shapesize(0.075*n)
        self.qsp.color('white')
        self.qsp.speed(0)
        self.qsp.goto(-9*n + 2*n*(4), -9*n + 2*n*(7))
        self.qh = turtle.Turtle(shape='square')
        self.qh.penup()
        self.qh.shapesize(0.075*n)
        self.qh.color('black')
        self.qh.speed(0)
        self.qh.goto(-9*n + 2*n*(4), -9*n + 2*n*(8))
        self.cu = turtle.Turtle(shape='square')
        self.cu.penup()
        self.cu.shapesize(0.075*n)
        self.cu.color('black')
        self.cu.speed(0)
        self.cu.goto(-9*n + 2*n*(5), -9*n + 2*n*(1))
        self.cd = turtle.Turtle(shape='square')
        self.cd.penup()
        self.cd.shapesize(0.075*n)
        self.cd.color('white')
        self.cd.speed(0)
        self.cd.goto(-9*n + 2*n*(5), -9*n + 2*n*(2))
        self.ct = turtle.Turtle(shape='square')
        self.ct.penup()
        self.ct.shapesize(0.075*n)
        self.ct.color('black')
        self.ct.speed(0)
        self.ct.goto(-9*n + 2*n*(5), -9*n + 2*n*(3))
        self.cq = turtle.Turtle(shape='square')
        self.cq.penup()
        self.cq.shapesize(0.075*n)
        self.cq.color('white')
        self.cq.speed(0)
        self.cq.goto(-9*n + 2*n*(5), -9*n + 2*n*(4))
        self.cc = turtle.Turtle(shape='square')
        self.cc.penup()
        self.cc.shapesize(0.075*n)
        self.cc.color('black')
        self.cc.speed(0)
        self.cc.goto(-9*n + 2*n*(5), -9*n + 2*n*(5))
        self.cs = turtle.Turtle(shape='square')
        self.cs.penup()
        self.cs.shapesize(0.075*n)
        self.cs.color('white')
        self.cs.speed(0)
        self.cs.goto(-9*n + 2*n*(5), -9*n + 2*n*(6))
        self.csp = turtle.Turtle(shape='square')
        self.csp.penup()
        self.csp.shapesize(0.075*n)
        self.csp.color('black')
        self.csp.speed(0)
        self.csp.goto(-9*n + 2*n*(5), -9*n + 2*n*(7))
        self.ch = turtle.Turtle(shape='square')
        self.ch.penup()
        self.ch.shapesize(0.075*n)
        self.ch.color('white')
        self.ch.speed(0)
        self.ch.goto(-9*n + 2*n*(5), -9*n + 2*n*(8))
        self.su = turtle.Turtle(shape='square')
        self.su.penup()
        self.su.shapesize(0.075*n)
        self.su.color('white')
        self.su.speed(0)
        self.su.goto(-9*n + 2*n*(6), -9*n + 2*n*(1))
        self.sd = turtle.Turtle(shape='square')
        self.sd.penup()
        self.sd.shapesize(0.075*n)
        self.sd.color('black')
        self.sd.speed(0)
        self.sd.goto(-9*n + 2*n*(6), -9*n + 2*n*(2))
        self.st = turtle.Turtle(shape='square')
        self.st.penup()
        self.st.shapesize(0.075*n)
        self.st.color('white')
        self.st.speed(0)
        self.st.goto(-9*n + 2*n*(6), -9*n + 2*n*(3))
        self.sq = turtle.Turtle(shape='square')
        self.sq.penup()
        self.sq.shapesize(0.075*n)
        self.sq.color('black')
        self.sq.speed(0)
        self.sq.goto(-9*n + 2*n*(6), -9*n + 2*n*(4))
        self.sc = turtle.Turtle(shape='square')
        self.sc.penup()
        self.sc.shapesize(0.075*n)
        self.sc.color('white')
        self.sc.speed(0)
        self.sc.goto(-9*n + 2*n*(6), -9*n + 2*n*(5))
        self.ss = turtle.Turtle(shape='square')
        self.ss.penup()
        self.ss.shapesize(0.075*n)
        self.ss.color('black')
        self.ss.speed(0)
        self.ss.goto(-9*n + 2*n*(6), -9*n + 2*n*(6))
        self.ssp = turtle.Turtle(shape='square')
        self.ssp.penup()
        self.ssp.shapesize(0.075*n)
        self.ssp.color('white')
        self.ssp.speed(0)
        self.ssp.goto(-9*n + 2*n*(6), -9*n + 2*n*(7))
        self.sh = turtle.Turtle(shape='square')
        self.sh.penup()
        self.sh.shapesize(0.075*n)
        self.sh.color('black')
        self.sh.speed(0)
        self.sh.goto(-9*n + 2*n*(6), -9*n + 2*n*(8))
        self.spu = turtle.Turtle(shape='square')
        self.spu.penup()
        self.spu.shapesize(0.075*n)
        self.spu.color('black')
        self.spu.speed(0)
        self.spu.goto(-9*n + 2*n*(7), -9*n + 2*n*(1))
        self.spd = turtle.Turtle(shape='square')
        self.spd.penup()
        self.spd.shapesize(0.075*n)
        self.spd.color('white')
        self.spd.speed(0)
        self.spd.goto(-9*n + 2*n*(7), -9*n + 2*n*(2))
        self.spt = turtle.Turtle(shape='square')
        self.spt.penup()
        self.spt.shapesize(0.075*n)
        self.spt.color('black')
        self.spt.speed(0)
        self.spt.goto(-9*n + 2*n*(7), -9*n + 2*n*(3))
        self.spq = turtle.Turtle(shape='square')
        self.spq.penup()
        self.spq.shapesize(0.075*n)
        self.spq.color('white')
        self.spq.speed(0)
        self.spq.goto(-9*n + 2*n*(7), -9*n + 2*n*(4))
        self.spc = turtle.Turtle(shape='square')
        self.spc.penup()
        self.spc.shapesize(0.075*n)
        self.spc.color('black')
        self.spc.speed(0)
        self.spc.goto(-9*n + 2*n*(7), -9*n + 2*n*(5))
        self.sps = turtle.Turtle(shape='square')
        self.sps.penup()
        self.sps.shapesize(0.075*n)
        self.sps.color('white')
        self.sps.speed(0)
        self.sps.goto(-9*n + 2*n*(7), -9*n + 2*n*(6))
        self.spsp = turtle.Turtle(shape='square')
        self.spsp.penup()
        self.spsp.shapesize(0.075*n)
        self.spsp.color('black')
        self.spsp.speed(0)
        self.spsp.goto(-9*n + 2*n*(7), -9*n + 2*n*(7))
        self.sph = turtle.Turtle(shape='square')
        self.sph.penup()
        self.sph.shapesize(0.075*n)
        self.sph.color('white')
        self.sph.speed(0)
        self.sph.goto(-9*n + 2*n*(7), -9*n + 2*n*(8))
        self.hu = turtle.Turtle(shape='square')
        self.hu.penup()
        self.hu.shapesize(0.075*n)
        self.hu.color('white')
        self.hu.speed(0)
        self.hu.goto(-9*n + 2*n*(8), -9*n + 2*n*(1))
        self.hd = turtle.Turtle(shape='square')
        self.hd.penup()
        self.hd.shapesize(0.075*n)
        self.hd.color('black')
        self.hd.speed(0)
        self.hd.goto(-9*n + 2*n*(8), -9*n + 2*n*(2))
        self.ht = turtle.Turtle(shape='square')
        self.ht.penup()
        self.ht.shapesize(0.075*n)
        self.ht.color('white')
        self.ht.speed(0)
        self.ht.goto(-9*n + 2*n*(8), -9*n + 2*n*(3))
        self.hq = turtle.Turtle(shape='square')
        self.hq.penup()
        self.hq.shapesize(0.075*n)
        self.hq.color('black')
        self.hq.speed(0)
        self.hq.goto(-9*n + 2*n*(8), -9*n + 2*n*(4))
        self.hc = turtle.Turtle(shape='square')
        self.hc.penup()
        self.hc.shapesize(0.075*n)
        self.hc.color('white')
        self.hc.speed(0)
        self.hc.goto(-9*n + 2*n*(8), -9*n + 2*n*(5))
        self.hs = turtle.Turtle(shape='square')
        self.hs.penup()
        self.hs.shapesize(0.075*n)
        self.hs.color('black')
        self.hs.speed(0)
        self.hs.goto(-9*n + 2*n*(8), -9*n + 2*n*(6))
        self.hsp = turtle.Turtle(shape='square')
        self.hsp.penup()
        self.hsp.shapesize(0.075*n)
        self.hsp.color('white')
        self.hsp.speed(0)
        self.hsp.goto(-9*n + 2*n*(8), -9*n + 2*n*(7))
        self.hh = turtle.Turtle(shape='square')
        self.hh.penup()
        self.hh.shapesize(0.075*n)
        self.hh.color('black')
        self.hh.speed(0)
        self.hh.goto(-9*n + 2*n*(8), -9*n + 2*n*(8))

        self.marc = turtle.Turtle(visible=None)
        self.marc.penup()
        self.marc.speed(0)
        
        b = n*8/20
        self.fen.register_shape("Tour", ((0,2*b/3), (b,b), (b,-b),(0, -2*b/3), (-b,-2*b/3), (-b, -0.4*b), (-3*b/4, -0.4*b),(-3*b/4, -0.4*b/3), (-b, -0.4*b/3), (-b, 0.4*b/3),(-3*b/4, 0.4*b/3),(-3*b/4, 0.4*b), (-b, 0.4*b), (-b,2*b/3)))
        self.fen.register_shape("King", ((b, b/3),(b, -b/3),(b/3, -b/3),(b/3, -b), (-b/3, -b),(-b/3, -b/3),(-b, -b/3),(-b, b/3), (-b/3, b/3),(-b/3, b),(b/3, b),(b/3, b/3),(b, b/3), (0, 0)))
        self.fen.register_shape("Fou", (((b, -b/2),(b, b/2),(0, 0),(-b/2,b/2 ),(-b, 0), (-b/2, -b/2), (0, 0))))
        self.fen.register_shape("Cheval", (((b, -b),(b, b),(0, 2*b/3),(-2*b/3, b/2),(-b, 0), (-b/3, -b),(0, -b), (0, 0))))
        self.fen.register_shape("Dame", (((b, -b),(-b, -b),(b/3, -b/2),(-b, 0),(b/3, b/2), (-b, b),(b, b),(b, -b), (0, 0))))
        self.afficher()
        
    def afficher(self):
        if (1, 1) in self.etat['white'].keys():
            self.uu.color('white')
            if self.etat['white'][(1, 1)] == 'P':
                self.uu.shape('circle')
            elif self.etat['white'][(1, 1)] == 'T':
                self.uu.shape('Tour')
            elif self.etat['white'][(1, 1)] == 'F':
                self.uu.shape("Fou")
            elif self.etat['white'][(1, 1)] == 'C':
                self.uu.shape("Cheval")
            elif self.etat['white'][(1, 1)] == 'Q':
                self.uu.shape("Dame")
            elif self.etat['white'][(1, 1)] == 'K':
                self.uu.shape("King")
        elif (1, 1) in self.etat['black'].keys():
            self.uu.color('black')
            if self.etat['black'][(1, 1)] == 'P':
                self.uu.shape('circle')
            elif self.etat['black'][(1, 1)] == 'T':
                self.uu.shape("Tour")
            elif self.etat['black'][(1, 1)] == 'F':
                self.uu.shape("Fou")
            elif self.etat['black'][(1, 1)] == 'C':
                self.uu.shape("Cheval")
            elif self.etat['black'][(1, 1)] == 'Q':
                self.uu.shape("Dame")
            elif self.etat['black'][(1, 1)] == 'K':
                self.uu.shape("King")
        else:
            self.uu.color('black')
            self.uu.shape('square')
        if (1, 2) in self.etat['white'].keys():
            self.ud.color('white')
            if self.etat['white'][(1, 2)] == 'P':
                self.ud.shape('circle')
            elif self.etat['white'][(1, 2)] == 'T':
                self.ud.shape("Tour")
            elif self.etat['white'][(1, 2)] == 'F':
                self.ud.shape("Fou")
            elif self.etat['white'][(1, 2)] == 'C':
                self.ud.shape("Cheval")
            elif self.etat['white'][(1, 2)] == 'Q':
                self.ud.shape("Dame")
            elif self.etat['white'][(1, 2)] == 'K':
                self.ud.shape("King")
        elif (1, 2) in self.etat['black'].keys():
            self.ud.color('black')
            if self.etat['black'][(1, 2)] == 'P':
                self.ud.shape('circle')
            elif self.etat['black'][(1, 2)] == 'T':
                self.ud.shape("Tour")
            elif self.etat['black'][(1, 2)] == 'F':
                self.ud.shape("Fou")
            elif self.etat['black'][(1, 2)] == 'C':
                self.ud.shape("Cheval")
            elif self.etat['black'][(1, 2)] == 'Q':
                self.ud.shape("Dame")
            elif self.etat['black'][(1, 2)] == 'K':
                self.ud.shape("King")
        else:
            self.ud.color('white')
            self.ud.shape('square')
        if (1, 3) in self.etat['white'].keys():
            self.ut.color('white')
            if self.etat['white'][(1, 3)] == 'P':
                self.ut.shape('circle')
            elif self.etat['white'][(1, 3)] == 'T':
                self.ut.shape("Tour")
            elif self.etat['white'][(1, 3)] == 'F':
                self.ut.shape("Fou")
            elif self.etat['white'][(1, 3)] == 'C':
                self.ut.shape("Cheval")
            elif self.etat['white'][(1, 3)] == 'Q':
                self.ut.shape("Dame")
            elif self.etat['white'][(1, 3)] == 'K':
                self.ut.shape("King")  
        elif (1, 3) in self.etat['black'].keys():
            self.ut.color('black')
            if self.etat['black'][(1, 3)] == 'P':
                self.ut.shape('circle')
            elif self.etat['black'][(1, 3)] == 'T':
                self.ut.shape("Tour")
            elif self.etat['black'][(1, 3)] == 'F':
                self.ut.shape("Fou")
            elif self.etat['black'][(1, 3)] == 'C':
                self.ut.shape("Cheval")
            elif self.etat['black'][(1, 3)] == 'Q':
                self.ut.shape("Dame")
            elif self.etat['black'][(1, 3)] == 'K':
                self.ut.shape("King")
        else:
            self.ut.color('black')
            self.ut.shape('square')
        if (1, 4) in self.etat['white'].keys():
            self.uq.color('white')
            if self.etat['white'][(1, 4)] == 'P':
                self.uq.shape('circle')
            elif self.etat['white'][(1, 4)] == 'T':
                self.uq.shape("Tour")
            elif self.etat['white'][(1, 4)] == 'F':
                self.uq.shape("Fou")
            elif self.etat['white'][(1, 4)] == 'C':
                self.uq.shape("Cheval")
            elif self.etat['white'][(1, 4)] == 'Q':
                self.uq.shape("Dame")
            elif self.etat['white'][(1, 4)] == 'K':
                self.uq.shape("King")       
        elif (1, 4) in self.etat['black'].keys():
            self.uq.color('black')
            if self.etat['black'][(1, 4)] == 'P':
                self.uq.shape('circle')
            elif self.etat['black'][(1, 4)] == 'T':
                self.uq.shape("Tour")
            elif self.etat['black'][(1, 4)] == 'F':
                self.uq.shape("Fou")
            elif self.etat['black'][(1, 4)] == 'C':
                self.uq.shape("Cheval")
            elif self.etat['black'][(1, 4)] == 'Q':
                self.uq.shape("Dame")
            elif self.etat['black'][(1, 4)] == 'K':
                self.uq.shape("King")
        else:
            self.uq.color('white')
            self.uq.shape('square')
        if (1, 5) in self.etat['white'].keys():
            self.uc.color('white')
            if self.etat['white'][(1, 5)] == 'P':
                self.uc.shape('circle')
            elif self.etat['white'][(1, 5)] == 'T':
                self.uc.shape("Tour")
            elif self.etat['white'][(1, 5)] == 'F':
                self.uc.shape("Fou")
            elif self.etat['white'][(1, 5)] == 'C':
                self.uc.shape("Cheval")
            elif self.etat['white'][(1, 5)] == 'Q':
                self.uc.shape("Dame")
            elif self.etat['white'][(1, 5)] == 'K':
                self.uc.shape("King")
        elif (1, 5) in self.etat['black'].keys():
            self.uc.color('black')
            if self.etat['black'][(1, 5)] == 'P':
                self.uc.shape('circle')
            elif self.etat['black'][(1, 5)] == 'T':
                self.uc.shape("Tour")
            elif self.etat['black'][(1, 5)] == 'F':
                self.uc.shape("Fou")
            elif self.etat['black'][(1, 5)] == 'C':
                self.uc.shape("Cheval")
            elif self.etat['black'][(1, 5)] == 'Q':
                self.uc.shape("Dame")
            elif self.etat['black'][(1, 5)] == 'K':
                self.uc.shape("King")
        else:
            self.uc.color('black')
            self.uc.shape('square')
        if (1, 6) in self.etat['white'].keys():
            self.us.color('white')
            if self.etat['white'][(1, 6)] == 'P':
                self.us.shape('circle')
            elif self.etat['white'][(1, 6)] == 'T':
                self.us.shape("Tour")
            elif self.etat['white'][(1, 6)] == 'F':
                self.us.shape("Fou")
            elif self.etat['white'][(1, 6)] == 'C':
                self.us.shape("Cheval")
            elif self.etat['white'][(1, 6)] == 'Q':
                self.us.shape("Dame")
            elif self.etat['white'][(1, 6)] == 'K':
                self.us.shape("King")
        elif (1, 6) in self.etat['black'].keys():
            self.us.color('black')
            if self.etat['black'][(1, 6)] == 'P':
                self.us.shape('circle')
            elif self.etat['black'][(1, 6)] == 'T':
                self.us.shape("Tour")
            elif self.etat['black'][(1, 6)] == 'F':
                self.us.shape("Fou")
            elif self.etat['black'][(1, 6)] == 'C':
                self.us.shape("Cheval")
            elif self.etat['black'][(1, 6)] == 'Q':
                self.us.shape("Dame")
            elif self.etat['black'][(1, 6)] == 'K':
                self.us.shape("King")
        else:
            self.us.color('white')
            self.us.shape('square')
        if (1, 7) in self.etat['white'].keys():
            self.usp.color('white')
            if self.etat['white'][(1, 7)] == 'P':
                self.usp.shape('circle')
            elif self.etat['white'][(1, 7)] == 'T':
                self.usp.shape("Tour")
            elif self.etat['white'][(1, 7)] == 'F':
                self.usp.shape("Fou")
            elif self.etat['white'][(1, 7)] == 'C':
                self.usp.shape("Cheval")
            elif self.etat['white'][(1, 7)] == 'Q':
                self.usp.shape("Dame")
            elif self.etat['white'][(1, 7)] == 'K':
                self.usp.shape("King")
        elif (1, 7) in self.etat['black'].keys():
            self.usp.color('black')
            if self.etat['black'][(1, 7)] == 'P':
                self.usp.shape('circle')
            elif self.etat['black'][(1, 7)] == 'T':
                self.usp.shape("Tour")
            elif self.etat['black'][(1, 7)] == 'F':
                self.usp.shape("Fou")
            elif self.etat['black'][(1, 7)] == 'C':
                self.usp.shape("Cheval")
            elif self.etat['black'][(1, 7)] == 'Q':
                self.usp.shape("Dame")
            elif self.etat['black'][(1, 7)] == 'K':
                self.usp.shape("King")
        else:
            self.usp.color('black')
            self.usp.shape('square')
        if (1, 8) in self.etat['white'].keys():
            self.uh.color('white')
            if self.etat['white'][(1, 8)] == 'P':
                self.uh.shape('circle')
            elif self.etat['white'][(1, 8)] == 'T':
                self.uh.shape("Tour")
            elif self.etat['white'][(1, 8)] == 'F':
                self.uh.shape("Fou")
            elif self.etat['white'][(1, 8)] == 'C':
                self.uh.shape("Cheval")
            elif self.etat['white'][(1, 8)] == 'Q':
                self.uh.shape("Dame")
            elif self.etat['white'][(1, 8)] == 'K':
                self.uh.shape("King")
        elif (1, 8) in self.etat['black'].keys():
            self.uh.color('black')
            if self.etat['black'][(1, 8)] == 'P':
                self.uh.shape('circle')
            elif self.etat['black'][(1, 8)] == 'T':
                self.uh.shape("Tour")
            elif self.etat['black'][(1, 8)] == 'F':
                self.uh.shape("Fou")
            elif self.etat['black'][(1, 8)] == 'C':
                self.uh.shape("Cheval")
            elif self.etat['black'][(1, 8)] == 'Q':
                self.uh.shape("Dame")
            elif self.etat['black'][(1, 8)] == 'K':
                self.uh.shape("King")
        else:
            self.uh.color('white')
            self.uh.shape('square')
        if (2, 1) in self.etat['white'].keys():
            self.du.color('white')
            if self.etat['white'][(2, 1)] == 'P':
                self.du.shape('circle')
            elif self.etat['white'][(2, 1)] == 'T':
                self.du.shape("Tour")
            elif self.etat['white'][(2, 1)] == 'F':
                self.du.shape("Fou")
            elif self.etat['white'][(2, 1)] == 'C':
                self.du.shape("Cheval")
            elif self.etat['white'][(2, 1)] == 'Q':
                self.du.shape("Dame")
            elif self.etat['white'][(2, 1)] == 'K':
                self.du.shape("King")
        elif (2, 1) in self.etat['black'].keys():
            self.du.color('black')
            if self.etat['black'][(2, 1)] == 'P':
                self.du.shape('circle')
            elif self.etat['black'][(2, 1)] == 'T':
                self.du.shape("Tour")
            elif self.etat['black'][(2, 1)] == 'F':
                self.du.shape("Fou")
            elif self.etat['black'][(2, 1)] == 'C':
                self.du.shape("Cheval")
            elif self.etat['black'][(2, 1)] == 'Q':
                self.du.shape("Dame")
            elif self.etat['black'][(2, 1)] == 'K':
                self.du.shape("King")
        else:
            self.du.color('white')
            self.du.shape('square')
        if (2, 2) in self.etat['white'].keys():
            self.dd.color('white')
            if self.etat['white'][(2, 2)] == 'P':
                self.dd.shape('circle')
            elif self.etat['white'][(2, 2)] == 'T':
                self.dd.shape("Tour")
            elif self.etat['white'][(2, 2)] == 'F':
                self.dd.shape("Fou")
            elif self.etat['white'][(2, 2)] == 'C':
                self.dd.shape("Cheval")
            elif self.etat['white'][(2, 2)] == 'Q':
                self.dd.shape("Dame")
            elif self.etat['white'][(2, 2)] == 'K':
                self.dd.shape("King")
        elif (2, 2) in self.etat['black'].keys():
            self.dd.color('black')
            if self.etat['black'][(2, 2)] == 'P':
                self.dd.shape('circle')
            elif self.etat['black'][(2, 2)] == 'T':
                self.dd.shape("Tour")
            elif self.etat['black'][(2, 2)] == 'F':
                self.dd.shape("Fou")
            elif self.etat['black'][(2, 2)] == 'C':
                self.dd.shape("Cheval")
            elif self.etat['black'][(2, 2)] == 'Q':
                self.dd.shape("Dame")
            elif self.etat['black'][(2, 2)] == 'K':
                self.dd.shape("King")
        else:
            self.dd.color('black')
            self.dd.shape('square')
        if (2, 3) in self.etat['white'].keys():
            self.dt.color('white')
            if self.etat['white'][(2, 3)] == 'P':
                self.dt.shape('circle')
            elif self.etat['white'][(2, 3)] == 'T':
                self.dt.shape("Tour")
            elif self.etat['white'][(2, 3)] == 'F':
                self.dt.shape("Fou")
            elif self.etat['white'][(2, 3)] == 'C':
                self.dt.shape("Cheval")
            elif self.etat['white'][(2, 3)] == 'Q':
                self.dt.shape("Dame")
            elif self.etat['white'][(2, 3)] == 'K':
                self.dt.shape("King")       
        elif (2, 3) in self.etat['black'].keys():
            self.dt.color('black')
            if self.etat['black'][(2, 3)] == 'P':
                self.dt.shape('circle')
            elif self.etat['black'][(2, 3)] == 'T':
                self.dt.shape("Tour")
            elif self.etat['black'][(2, 3)] == 'F':
                self.dt.shape("Fou")
            elif self.etat['black'][(2, 3)] == 'C':
                self.dt.shape("Cheval")
            elif self.etat['black'][(2, 3)] == 'Q':
                self.dt.shape("Dame")
            elif self.etat['black'][(2, 3)] == 'K':
                self.dt.shape("King")
        else:
            self.dt.color('white')
            self.dt.shape('square')
        if (2, 4) in self.etat['white'].keys():
            self.dq.color('white')
            if self.etat['white'][(2, 4)] == 'P':
                self.dq.shape('circle')
            elif self.etat['white'][(2, 4)] == 'T':
                self.dq.shape("Tour")
            elif self.etat['white'][(2, 4)] == 'F':
                self.dq.shape("Fou")
            elif self.etat['white'][(2, 4)] == 'C':
                self.dq.shape("Cheval")
            elif self.etat['white'][(2, 4)] == 'Q':
                self.dq.shape("Dame")
            elif self.etat['white'][(2, 4)] == 'K':
                self.dq.shape("King")     
        elif (2, 4) in self.etat['black'].keys():
            self.dq.color('black')
            if self.etat['black'][(2, 4)] == 'P':
                self.dq.shape('circle')
            elif self.etat['black'][(2, 4)] == 'T':
                self.dq.shape("Tour")
            elif self.etat['black'][(2, 4)] == 'F':
                self.dq.shape("Fou")
            elif self.etat['black'][(2, 4)] == 'C':
                self.dq.shape("Cheval")
            elif self.etat['black'][(2, 4)] == 'Q':
                self.dq.shape("Dame")
            elif self.etat['black'][(2, 4)] == 'K':
                self.dq.shape("King")
        else:
            self.dq.color('black')
            self.dq.shape('square')
        if (2, 5) in self.etat['white'].keys():
            self.dc.color('white')
            if self.etat['white'][(2, 5)] == 'P':
                self.dc.shape('circle')
            elif self.etat['white'][(2, 5)] == 'T':
                self.dc.shape("Tour")
            elif self.etat['white'][(2, 5)] == 'F':
                self.dc.shape("Fou")
            elif self.etat['white'][(2, 5)] == 'C':
                self.dc.shape("Cheval")
            elif self.etat['white'][(2, 5)] == 'Q':
                self.dc.shape("Dame")
            elif self.etat['white'][(2, 5)] == 'K':
                self.dc.shape("King")
        elif (2, 5) in self.etat['black'].keys():
            self.dc.color('black')
            if self.etat['black'][(2, 5)] == 'P':
                self.dc.shape('circle')
            elif self.etat['black'][(2, 5)] == 'T':
                self.dc.shape("Tour")
            elif self.etat['black'][(2, 5)] == 'F':
                self.dc.shape("Fou")
            elif self.etat['black'][(2, 5)] == 'C':
                self.dc.shape("Cheval")
            elif self.etat['black'][(2, 5)] == 'Q':
                self.dc.shape("Dame")
            elif self.etat['black'][(2, 5)] == 'K':
                self.dc.shape("King")
        else:
            self.dc.color('white')
            self.dc.shape('square')
        if (2, 6) in self.etat['white'].keys():
            self.ds.color('white')
            if self.etat['white'][(2, 6)] == 'P':
                self.ds.shape('circle')
            elif self.etat['white'][(2, 6)] == 'T':
                self.ds.shape("Tour")
            elif self.etat['white'][(2, 6)] == 'F':
                self.ds.shape("Fou")
            elif self.etat['white'][(2, 6)] == 'C':
                self.ds.shape("Cheval")
            elif self.etat['white'][(2, 6)] == 'Q':
                self.ds.shape("Dame")
            elif self.etat['white'][(2, 6)] == 'K':
                self.ds.shape("King")
        elif (2, 6) in self.etat['black'].keys():
            self.ds.color('black')
            if self.etat['black'][(2, 6)] == 'P':
                self.ds.shape('circle')
            elif self.etat['black'][(2, 6)] == 'T':
                self.ds.shape("Tour")
            elif self.etat['black'][(2, 6)] == 'F':
                self.ds.shape("Fou")
            elif self.etat['black'][(2, 6)] == 'C':
                self.ds.shape("Cheval")
            elif self.etat['black'][(2, 6)] == 'Q':
                self.ds.shape("Dame")
            elif self.etat['black'][(2, 6)] == 'K':
                self.ds.shape("King")
        else:
            self.ds.color('black')
            self.ds.shape('square')
        if (2, 7) in self.etat['white'].keys():
            self.dsp.color('white')
            if self.etat['white'][(2, 7)] == 'P':
                self.dsp.shape('circle')
            elif self.etat['white'][(2, 7)] == 'T':
                self.dsp.shape("Tour")
            elif self.etat['white'][(2, 7)] == 'F':
                self.dsp.shape("Fou")
            elif self.etat['white'][(2, 7)] == 'C':
                self.dsp.shape("Cheval")
            elif self.etat['white'][(2, 7)] == 'Q':
                self.dsp.shape("Dame")
            elif self.etat['white'][(2, 7)] == 'K':
                self.dsp.shape("King")
        elif (2, 7) in self.etat['black'].keys():
            self.dsp.color('black')
            if self.etat['black'][(2, 7)] == 'P':
                self.dsp.shape('circle')
            elif self.etat['black'][(2, 7)] == 'T':
                self.dsp.shape("Tour")
            elif self.etat['black'][(2, 7)] == 'F':
                self.dsp.shape("Fou")
            elif self.etat['black'][(2, 7)] == 'C':
                self.dsp.shape("Cheval")
            elif self.etat['black'][(2, 7)] == 'Q':
                self.dsp.shape("Dame")
            elif self.etat['black'][(2, 7)] == 'K':
                self.dsp.shape("King")
        else:
            self.dsp.color('white')
            self.dsp.shape('square')
        if (2, 8) in self.etat['white'].keys():
            self.dh.color('white')
            if self.etat['white'][(2, 8)] == 'P':
                self.dh.shape('circle')
            elif self.etat['white'][(2, 8)] == 'T':
                self.dh.shape("Tour")
            elif self.etat['white'][(2, 8)] == 'F':
                self.dh.shape("Fou")
            elif self.etat['white'][(2, 8)] == 'C':
                self.dh.shape("Cheval")
            elif self.etat['white'][(2, 8)] == 'Q':
                self.dh.shape("Dame")
            elif self.etat['white'][(2, 8)] == 'K':
                self.dh.shape("King")
        elif (2, 8) in self.etat['black'].keys():
            self.dh.color('black')
            if self.etat['black'][(2, 8)] == 'P':
                self.dh.shape('circle')
            elif self.etat['black'][(2, 8)] == 'T':
                self.dh.shape("Tour")
            elif self.etat['black'][(2, 8)] == 'F':
                self.dh.shape("Fou")
            elif self.etat['black'][(2, 8)] == 'C':
                self.dh.shape("Cheval")
            elif self.etat['black'][(2, 8)] == 'Q':
                self.dh.shape("Dame")
            elif self.etat['black'][(2, 8)] == 'K':
                self.dh.shape("King")
        else:
            self.dh.color('black')
            self.dh.shape('square')
        if (3, 1) in self.etat['white'].keys():
            self.tu.color('white')
            if self.etat['white'][(3, 1)] == 'P':
                self.tu.shape('circle')
            elif self.etat['white'][(3, 1)] == 'T':
                self.tu.shape("Tour")
            elif self.etat['white'][(3, 1)] == 'F':
                self.tu.shape("Fou")
            elif self.etat['white'][(3, 1)] == 'C':
                self.tu.shape("Cheval")
            elif self.etat['white'][(3, 1)] == 'Q':
                self.tu.shape("Dame")
            elif self.etat['white'][(3, 1)] == 'K':
                self.tu.shape("King")
        elif (3, 1) in self.etat['black'].keys():
            self.tu.color('black')
            if self.etat['black'][(3, 1)] == 'P':
                self.tu.shape('circle')
            elif self.etat['black'][(3, 1)] == 'T':
                self.tu.shape("Tour")
            elif self.etat['black'][(3, 1)] == 'F':
                self.tu.shape("Fou")
            elif self.etat['black'][(3, 1)] == 'C':
                self.tu.shape("Cheval")
            elif self.etat['black'][(3, 1)] == 'Q':
                self.tu.shape("Dame")
            elif self.etat['black'][(3, 1)] == 'K':
                self.tu.shape("King")
        else:
            self.tu.color('black')
            self.tu.shape('square')
        if (3, 2) in self.etat['white'].keys():
            self.td.color('white')
            if self.etat['white'][(3, 2)] == 'P':
                self.td.shape('circle')
            elif self.etat['white'][(3, 2)] == 'T':
                self.td.shape("Tour")
            elif self.etat['white'][(3, 2)] == 'F':
                self.td.shape("Fou")
            elif self.etat['white'][(3, 2)] == 'C':
                self.td.shape("Cheval")
            elif self.etat['white'][(3, 2)] == 'Q':
                self.td.shape("Dame")
            elif self.etat['white'][(3, 2)] == 'K':
                self.td.shape("King")
        elif (3, 2) in self.etat['black'].keys():
            self.td.color('black')
            if self.etat['black'][(3, 2)] == 'P':
                self.td.shape('circle')
            elif self.etat['black'][(3, 2)] == 'T':
                self.td.shape("Tour")
            elif self.etat['black'][(3, 2)] == 'F':
                self.td.shape("Fou")
            elif self.etat['black'][(3, 2)] == 'C':
                self.td.shape("Cheval")
            elif self.etat['black'][(3, 2)] == 'Q':
                self.td.shape("Dame")
            elif self.etat['black'][(3, 2)] == 'K':
                self.td.shape("King")
        else:
            self.td.color('white')
            self.td.shape('square')
        if (3, 3) in self.etat['white'].keys():
            self.tt.color('white')
            if self.etat['white'][(3, 3)] == 'P':
                self.tt.shape('circle')
            elif self.etat['white'][(3, 3)] == 'T':
                self.tt.shape("Tour")
            elif self.etat['white'][(3, 3)] == 'F':
                self.tt.shape("Fou")
            elif self.etat['white'][(3, 3)] == 'C':
                self.tt.shape("Cheval")
            elif self.etat['white'][(3, 3)] == 'Q':
                self.tt.shape("Dame")
            elif self.etat['white'][(3, 3)] == 'K':
                self.tt.shape("King")     
        elif (3, 3) in self.etat['black'].keys():
            self.tt.color('black')
            if self.etat['black'][(3, 3)] == 'P':
                self.tt.shape('circle')
            elif self.etat['black'][(3, 3)] == 'T':
                self.tt.shape("Tour")
            elif self.etat['black'][(3, 3)] == 'F':
                self.tt.shape("Fou")
            elif self.etat['black'][(3, 3)] == 'C':
                self.tt.shape("Cheval")
            elif self.etat['black'][(3, 3)] == 'Q':
                self.tt.shape("Dame")
            elif self.etat['black'][(3, 3)] == 'K':
                self.tt.shape("King")
        else:
            self.tt.color('black')
            self.tt.shape('square')
        if (3, 4) in self.etat['white'].keys():
            self.tq.color('white')
            if self.etat['white'][(3, 4)] == 'P':
                self.tq.shape('circle')
            elif self.etat['white'][(3, 4)] == 'T':
                self.tq.shape("Tour")
            elif self.etat['white'][(3, 4)] == 'F':
                self.tq.shape("Fou")
            elif self.etat['white'][(3, 4)] == 'C':
                self.tq.shape("Cheval")
            elif self.etat['white'][(3, 4)] == 'Q':
                self.tq.shape("Dame")
            elif self.etat['white'][(3, 4)] == 'K':
                self.tq.shape("King")       
        elif (3, 4) in self.etat['black'].keys():
            self.tq.color('black')
            if self.etat['black'][(3, 4)] == 'P':
                self.tq.shape('circle')
            elif self.etat['black'][(3, 4)] == 'T':
                self.tq.shape("Tour")
            elif self.etat['black'][(3, 4)] == 'F':
                self.tq.shape("Fou")
            elif self.etat['black'][(3, 4)] == 'C':
                self.tq.shape("Cheval")
            elif self.etat['black'][(3, 4)] == 'Q':
                self.tq.shape("Dame")
            elif self.etat['black'][(3, 4)] == 'K':
                self.tq.shape("King")
        else:
            self.tq.color('white')
            self.tq.shape('square')
        if (3, 5) in self.etat['white'].keys():
            self.tc.color('white')
            if self.etat['white'][(3, 5)] == 'P':
                self.tc.shape('circle')
            elif self.etat['white'][(3, 5)] == 'T':
                self.tc.shape("Tour")
            elif self.etat['white'][(3, 5)] == 'F':
                self.tc.shape("Fou")
            elif self.etat['white'][(3, 5)] == 'C':
                self.tc.shape("Cheval")
            elif self.etat['white'][(3, 5)] == 'Q':
                self.tc.shape("Dame")
            elif self.etat['white'][(3, 5)] == 'K':
                self.tc.shape("King")
        elif (3, 5) in self.etat['black'].keys():
            self.tc.color('black')
            if self.etat['black'][(3, 5)] == 'P':
                self.tc.shape('circle')
            elif self.etat['black'][(3, 5)] == 'T':
                self.tc.shape("Tour")
            elif self.etat['black'][(3, 5)] == 'F':
                self.tc.shape("Fou")
            elif self.etat['black'][(3, 5)] == 'C':
                self.tc.shape("Cheval")
            elif self.etat['black'][(3, 5)] == 'Q':
                self.tc.shape("Dame")
            elif self.etat['black'][(3, 5)] == 'K':
                self.tc.shape("King")
        else:
            self.tc.color('black')
            self.tc.shape('square')
        if (3, 6) in self.etat['white'].keys():
            self.ts.color('white')
            if self.etat['white'][(3, 6)] == 'P':
                self.ts.shape('circle')
            elif self.etat['white'][(3, 6)] == 'T':
                self.ts.shape("Tour")
            elif self.etat['white'][(3, 6)] == 'F':
                self.ts.shape("Fou")
            elif self.etat['white'][(3, 6)] == 'C':
                self.ts.shape("Cheval")
            elif self.etat['white'][(3, 6)] == 'Q':
                self.ts.shape("Dame")
            elif self.etat['white'][(3, 6)] == 'K':
                self.ts.shape("King")
        elif (3, 6) in self.etat['black'].keys():
            self.ts.color('black')
            if self.etat['black'][(3, 6)] == 'P':
                self.ts.shape('circle')
            elif self.etat['black'][(3, 6)] == 'T':
                self.ts.shape("Tour")
            elif self.etat['black'][(3, 6)] == 'F':
                self.ts.shape("Fou")
            elif self.etat['black'][(3, 6)] == 'C':
                self.ts.shape("Cheval")
            elif self.etat['black'][(3, 6)] == 'Q':
                self.ts.shape("Dame")
            elif self.etat['black'][(3, 6)] == 'K':
                self.ts.shape("King")
        else:
            self.ts.color('white')
            self.ts.shape('square')
        if (3, 7) in self.etat['white'].keys():
            self.tsp.color('white')
            if self.etat['white'][(3, 7)] == 'P':
                self.tsp.shape('circle')
            elif self.etat['white'][(3, 7)] == 'T':
                self.tsp.shape("Tour")
            elif self.etat['white'][(3, 7)] == 'F':
                self.tsp.shape("Fou")
            elif self.etat['white'][(3, 7)] == 'C':
                self.tsp.shape("Cheval")
            elif self.etat['white'][(3, 7)] == 'Q':
                self.tsp.shape("Dame")
            elif self.etat['white'][(3, 7)] == 'K':
                self.tsp.shape("King")
        elif (3, 7) in self.etat['black'].keys():
            self.tsp.color('black')
            if self.etat['black'][(3, 7)] == 'P':
                self.tsp.shape('circle')
            elif self.etat['black'][(3, 7)] == 'T':
                self.tsp.shape("Tour")
            elif self.etat['black'][(3, 7)] == 'F':
                self.tsp.shape("Fou")
            elif self.etat['black'][(3, 7)] == 'C':
                self.tsp.shape("Cheval")
            elif self.etat['black'][(3, 7)] == 'Q':
                self.tsp.shape("Dame")
            elif self.etat['black'][(3, 7)] == 'K':
                self.tsp.shape("King")
        else:
            self.tsp.color('black')
            self.tsp.shape('square')
        if (3, 8) in self.etat['white'].keys():
            self.th.color('white')
            if self.etat['white'][(3, 8)] == 'P':
                self.th.shape('circle')
            elif self.etat['white'][(3, 8)] == 'T':
                self.th.shape("Tour")
            elif self.etat['white'][(3, 8)] == 'F':
                self.th.shape("Fou")
            elif self.etat['white'][(3, 8)] == 'C':
                self.th.shape("Cheval")
            elif self.etat['white'][(3, 8)] == 'Q':
                self.th.shape("Dame")
            elif self.etat['white'][(3, 8)] == 'K':
                self.th.shape("King")
        elif (3, 8) in self.etat['black'].keys():
            self.th.color('black')
            if self.etat['black'][(3, 8)] == 'P':
                self.th.shape('circle')
            elif self.etat['black'][(3, 8)] == 'T':
                self.th.shape("Tour")
            elif self.etat['black'][(3, 8)] == 'F':
                self.th.shape("Fou")
            elif self.etat['black'][(3, 8)] == 'C':
                self.th.shape("Cheval")
            elif self.etat['black'][(3, 8)] == 'Q':
                self.th.shape("Dame")
            elif self.etat['black'][(3, 8)] == 'K':
                self.th.shape("King")
        else:
            self.th.color('white')
            self.th.shape('square')
        if (4, 1) in self.etat['white'].keys():
            self.qu.color('white')
            if self.etat['white'][(4, 1)] == 'P':
                self.qu.shape('circle')
            elif self.etat['white'][(4, 1)] == 'T':
                self.qu.shape("Tour")
            elif self.etat['white'][(4, 1)] == 'F':
                self.qu.shape("Fou")
            elif self.etat['white'][(4, 1)] == 'C':
                self.qu.shape("Cheval")
            elif self.etat['white'][(4, 1)] == 'Q':
                self.qu.shape("Dame")
            elif self.etat['white'][(4, 1)] == 'K':
                self.qu.shape("King")
        elif (4, 1) in self.etat['black'].keys():
            self.qu.color('black')
            if self.etat['black'][(4, 1)] == 'P':
                self.qu.shape('circle')
            elif self.etat['black'][(4, 1)] == 'T':
                self.qu.shape("Tour")
            elif self.etat['black'][(4, 1)] == 'F':
                self.qu.shape("Fou")
            elif self.etat['black'][(4, 1)] == 'C':
                self.qu.shape("Cheval")
            elif self.etat['black'][(4, 1)] == 'Q':
                self.qu.shape("Dame")
            elif self.etat['black'][(4, 1)] == 'K':
                self.qu.shape("King")
        else:
            self.qu.color('white')
            self.qu.shape('square')
        if (4, 2) in self.etat['white'].keys():
            self.qd.color('white')
            if self.etat['white'][(4, 2)] == 'P':
                self.qd.shape('circle')
            elif self.etat['white'][(4, 2)] == 'T':
                self.qd.shape("Tour")
            elif self.etat['white'][(4, 2)] == 'F':
                self.qd.shape("Fou")
            elif self.etat['white'][(4, 2)] == 'C':
                self.qd.shape("Cheval")
            elif self.etat['white'][(4, 2)] == 'Q':
                self.qd.shape("Dame")
            elif self.etat['white'][(4, 2)] == 'K':
                self.qd.shape("King")
        elif (4, 2) in self.etat['black'].keys():
            self.qd.color('black')
            if self.etat['black'][(4, 2)] == 'P':
                self.qd.shape('circle')
            elif self.etat['black'][(4, 2)] == 'T':
                self.qd.shape("Tour")
            elif self.etat['black'][(4, 2)] == 'F':
                self.qd.shape("Fou")
            elif self.etat['black'][(4, 2)] == 'C':
                self.qd.shape("Cheval")
            elif self.etat['black'][(4, 2)] == 'Q':
                self.qd.shape("Dame")
            elif self.etat['black'][(4, 2)] == 'K':
                self.qd.shape("King")
        else:
            self.qd.color('black')
            self.qd.shape('square')
        if (4, 3) in self.etat['white'].keys():
            self.qt.color('white')
            if self.etat['white'][(4, 3)] == 'P':
                self.qt.shape('circle')
            elif self.etat['white'][(4, 3)] == 'T':
                self.qt.shape("Tour")
            elif self.etat['white'][(4, 3)] == 'F':
                self.qt.shape("Fou")
            elif self.etat['white'][(4, 3)] == 'C':
                self.qt.shape("Cheval")
            elif self.etat['white'][(4, 3)] == 'Q':
                self.qt.shape("Dame")
            elif self.etat['white'][(4, 3)] == 'K':
                self.qt.shape("King")       
        elif (4, 3) in self.etat['black'].keys():
            self.qt.color('black')
            if self.etat['black'][(4, 3)] == 'P':
                self.qt.shape('circle')
            elif self.etat['black'][(4, 3)] == 'T':
                self.qt.shape("Tour")
            elif self.etat['black'][(4, 3)] == 'F':
                self.qt.shape("Fou")
            elif self.etat['black'][(4, 3)] == 'C':
                self.qt.shape("Cheval")
            elif self.etat['black'][(4, 3)] == 'Q':
                self.qt.shape("Dame")
            elif self.etat['black'][(4, 3)] == 'K':
                self.qt.shape("King")
        else:
            self.qt.color('white')
            self.qt.shape('square')
        if (4, 4) in self.etat['white'].keys():
            self.qq.color('white')
            if self.etat['white'][(4, 4)] == 'P':
                self.qq.shape('circle')
            elif self.etat['white'][(4, 4)] == 'T':
                self.qq.shape("Tour")
            elif self.etat['white'][(4, 4)] == 'F':
                self.qq.shape("Fou")
            elif self.etat['white'][(4, 4)] == 'C':
                self.qq.shape("Cheval")
            elif self.etat['white'][(4, 4)] == 'Q':
                self.qq.shape("Dame")
            elif self.etat['white'][(4, 4)] == 'K':
                self.qq.shape("King")
        elif (4, 4) in self.etat['black'].keys():
            self.qq.color('black')
            if self.etat['black'][(4, 4)] == 'P':
                self.qq.shape('circle')
            elif self.etat['black'][(4, 4)] == 'T':
                self.qq.shape("Tour")
            elif self.etat['black'][(4, 4)] == 'F':
                self.qq.shape("Fou")
            elif self.etat['black'][(4, 4)] == 'C':
                self.qq.shape("Cheval")
            elif self.etat['black'][(4, 4)] == 'Q':
                self.qq.shape("Dame")
            elif self.etat['black'][(4, 4)] == 'K':
                self.qq.shape("King")
        else:
            self.qq.color('black')
            self.qq.shape('square')
        if (4, 5) in self.etat['white'].keys():
            self.qc.color('white')
            if self.etat['white'][(4, 5)] == 'P':
                self.qc.shape('circle')
            elif self.etat['white'][(4, 5)] == 'T':
                self.qc.shape("Tour")
            elif self.etat['white'][(4, 5)] == 'F':
                self.qc.shape("Fou")
            elif self.etat['white'][(4, 5)] == 'C':
                self.qc.shape("Cheval")
            elif self.etat['white'][(4, 5)] == 'Q':
                self.qc.shape("Dame")
            elif self.etat['white'][(4, 5)] == 'K':
                self.qc.shape("King")
        elif (4, 5) in self.etat['black'].keys():
            self.qc.color('black')
            if self.etat['black'][(4, 5)] == 'P':
                self.qc.shape('circle')
            elif self.etat['black'][(4, 5)] == 'T':
                self.qc.shape("Tour")
            elif self.etat['black'][(4, 5)] == 'F':
                self.qc.shape("Fou")
            elif self.etat['black'][(4, 5)] == 'C':
                self.qc.shape("Cheval")
            elif self.etat['black'][(4, 5)] == 'Q':
                self.qc.shape("Dame")
            elif self.etat['black'][(4, 5)] == 'K':
                self.qc.shape("King")
        else:
            self.qc.color('white')
            self.qc.shape('square')
        if (4, 6) in self.etat['white'].keys():
            self.qs.color('white')
            if self.etat['white'][(4, 6)] == 'P':
                self.qs.shape('circle')
            elif self.etat['white'][(4, 6)] == 'T':
                self.qs.shape("Tour")
            elif self.etat['white'][(4, 6)] == 'F':
                self.qs.shape("Fou")
            elif self.etat['white'][(4, 6)] == 'C':
                self.qs.shape("Cheval")
            elif self.etat['white'][(4, 6)] == 'Q':
                self.qs.shape("Dame")
            elif self.etat['white'][(4, 6)] == 'K':
                self.qs.shape("King")
        elif (4, 6) in self.etat['black'].keys():
            self.qs.color('black')
            if self.etat['black'][(4, 6)] == 'P':
                self.qs.shape('circle')
            elif self.etat['black'][(4, 6)] == 'T':
                self.qs.shape("Tour")
            elif self.etat['black'][(4, 6)] == 'F':
                self.qs.shape("Fou")
            elif self.etat['black'][(4, 6)] == 'C':
                self.qs.shape("Cheval")
            elif self.etat['black'][(4, 6)] == 'Q':
                self.qs.shape("Dame")
            elif self.etat['black'][(4, 6)] == 'K':
                self.qs.shape("King")
        else:
            self.qs.color('black')
            self.qs.shape('square')
        if (4, 7) in self.etat['white'].keys():
            self.qsp.color('white')
            if self.etat['white'][(4, 7)] == 'P':
                self.qsp.shape('circle')
            elif self.etat['white'][(4, 7)] == 'T':
                self.qsp.shape("Tour")
            elif self.etat['white'][(4, 7)] == 'F':
                self.qsp.shape("Fou")
            elif self.etat['white'][(4, 7)] == 'C':
                self.qsp.shape("Cheval")
            elif self.etat['white'][(4, 7)] == 'Q':
                self.qsp.shape("Dame")
            elif self.etat['white'][(4, 7)] == 'K':
                self.qsp.shape("King")
        elif (4, 7) in self.etat['black'].keys():
            self.qsp.color('black')
            if self.etat['black'][(4, 7)] == 'P':
                self.qsp.shape('circle')
            elif self.etat['black'][(4, 7)] == 'T':
                self.qsp.shape("Tour")
            elif self.etat['black'][(4, 7)] == 'F':
                self.qsp.shape("Fou")
            elif self.etat['black'][(4, 7)] == 'C':
                self.qsp.shape("Cheval")
            elif self.etat['black'][(4, 7)] == 'Q':
                self.qsp.shape("Dame")
            elif self.etat['black'][(4, 7)] == 'K':
                self.qsp.shape("King")
        else:
            self.qsp.color('white')
            self.qsp.shape('square')
        if (4, 8) in self.etat['white'].keys():
            self.qh.color('white')
            if self.etat['white'][(4, 8)] == 'P':
                self.qh.shape('circle')
            elif self.etat['white'][(4, 8)] == 'T':
                self.qh.shape("Tour")
            elif self.etat['white'][(4, 8)] == 'F':
                self.qh.shape("Fou")
            elif self.etat['white'][(4, 8)] == 'C':
                self.qh.shape("Cheval")
            elif self.etat['white'][(4, 8)] == 'Q':
                self.qh.shape("Dame")
            elif self.etat['white'][(4, 8)] == 'K':
                self.qh.shape("King")
        elif (4, 8) in self.etat['black'].keys():
            self.qh.color('black')
            if self.etat['black'][(4, 8)] == 'P':
                self.qh.shape('circle')
            elif self.etat['black'][(4, 8)] == 'T':
                self.qh.shape("Tour")
            elif self.etat['black'][(4, 8)] == 'F':
                self.qh.shape("Fou")
            elif self.etat['black'][(4, 8)] == 'C':
                self.qh.shape("Cheval")
            elif self.etat['black'][(4, 8)] == 'Q':
                self.qh.shape("Dame")
            elif self.etat['black'][(4, 8)] == 'K':
                self.qh.shape("King")
        else:
            self.qh.color('black')
            self.qh.shape('square')
        if (5, 1) in self.etat['white'].keys():
            self.cu.color('white')
            if self.etat['white'][(5, 1)] == 'P':
                self.cu.shape('circle')
            elif self.etat['white'][(5, 1)] == 'T':
                self.cu.shape("Tour")
            elif self.etat['white'][(5, 1)] == 'F':
                self.cu.shape("Fou")
            elif self.etat['white'][(5, 1)] == 'C':
                self.cu.shape("Cheval")
            elif self.etat['white'][(5, 1)] == 'Q':
                self.cu.shape("Dame")
            elif self.etat['white'][(5, 1)] == 'K':
                self.cu.shape("King")
        elif (5, 1) in self.etat['black'].keys():
            self.cu.color('black')
            if self.etat['black'][(5, 1)] == 'P':
                self.cu.shape('circle')
            elif self.etat['black'][(5, 1)] == 'T':
                self.cu.shape("Tour")
            elif self.etat['black'][(5, 1)] == 'F':
                self.cu.shape("Fou")
            elif self.etat['black'][(5, 1)] == 'C':
                self.cu.shape("Cheval")
            elif self.etat['black'][(5, 1)] == 'Q':
                self.cu.shape("Dame")
            elif self.etat['black'][(5, 1)] == 'K':
                self.cu.shape("King")
        else:
            self.cu.color('black')
            self.cu.shape('square')
        if (5, 2) in self.etat['white'].keys():
            self.cd.color('white')
            if self.etat['white'][(5, 2)] == 'P':
                self.cd.shape('circle')
            elif self.etat['white'][(5, 2)] == 'T':
                self.cd.shape("Tour")
            elif self.etat['white'][(5, 2)] == 'F':
                self.cd.shape("Fou")
            elif self.etat['white'][(5, 2)] == 'C':
                self.cd.shape("Cheval")
            elif self.etat['white'][(5, 2)] == 'Q':
                self.cd.shape("Dame")
            elif self.etat['white'][(5, 2)] == 'K':
                self.cd.shape("King")
        elif (5, 2) in self.etat['black'].keys():
            self.cd.color('black')
            if self.etat['black'][(5, 2)] == 'P':
                self.cd.shape('circle')
            elif self.etat['black'][(5, 2)] == 'T':
                self.cd.shape("Tour")
            elif self.etat['black'][(5, 2)] == 'F':
                self.cd.shape("Fou")
            elif self.etat['black'][(5, 2)] == 'C':
                self.cd.shape("Cheval")
            elif self.etat['black'][(5, 2)] == 'Q':
                self.cd.shape("Dame")
            elif self.etat['black'][(5, 2)] == 'K':
                self.cd.shape("King")
        else:
            self.cd.color('white')
            self.cd.shape('square')
        if (5, 3) in self.etat['white'].keys():
            self.ct.color('white')
            if self.etat['white'][(5, 3)] == 'P':
                self.ct.shape('circle')
            elif self.etat['white'][(5, 3)] == 'T':
                self.ct.shape("Tour")
            elif self.etat['white'][(5, 3)] == 'F':
                self.ct.shape("Fou")
            elif self.etat['white'][(5, 3)] == 'C':
                self.ct.shape("Cheval")
            elif self.etat['white'][(5, 3)] == 'Q':
                self.ct.shape("Dame")
            elif self.etat['white'][(5, 3)] == 'K':
                self.ct.shape("King")  
        elif (5, 3) in self.etat['black'].keys():
            self.ct.color('black')
            if self.etat['black'][(5, 3)] == 'P':
                self.ct.shape('circle')
            elif self.etat['black'][(5, 3)] == 'T':
                self.ct.shape("Tour")
            elif self.etat['black'][(5, 3)] == 'F':
                self.ct.shape("Fou")
            elif self.etat['black'][(5, 3)] == 'C':
                self.ct.shape("Cheval")
            elif self.etat['black'][(5, 3)] == 'Q':
                self.ct.shape("Dame")
            elif self.etat['black'][(5, 3)] == 'K':
                self.ct.shape("King")
        else:
            self.ct.color('black')
            self.ct.shape('square')
        if (5, 4) in self.etat['white'].keys():
            self.cq.color('white')
            if self.etat['white'][(5, 4)] == 'P':
                self.cq.shape('circle')
            elif self.etat['white'][(5, 4)] == 'T':
                self.cq.shape("Tour")
            elif self.etat['white'][(5, 4)] == 'F':
                self.cq.shape("Fou")
            elif self.etat['white'][(5, 4)] == 'C':
                self.cq.shape("Cheval")
            elif self.etat['white'][(5, 4)] == 'Q':
                self.cq.shape("Dame")
            elif self.etat['white'][(5, 4)] == 'K':
                self.cq.shape("King")        
        elif (5, 4) in self.etat['black'].keys():
            self.cq.color('black')
            if self.etat['black'][(5, 4)] == 'P':
                self.cq.shape('circle')
            elif self.etat['black'][(5, 4)] == 'T':
                self.cq.shape("Tour")
            elif self.etat['black'][(5, 4)] == 'F':
                self.cq.shape("Fou")
            elif self.etat['black'][(5, 4)] == 'C':
                self.cq.shape("Cheval")
            elif self.etat['black'][(5, 4)] == 'Q':
                self.cq.shape("Dame")
            elif self.etat['black'][(5, 4)] == 'K':
                self.cq.shape("King")
        else:
            self.cq.color('white')
            self.cq.shape('square')
        if (5, 5) in self.etat['white'].keys():
            self.cc.color('white')
            if self.etat['white'][(5, 5)] == 'P':
                self.cc.shape('circle')
            elif self.etat['white'][(5, 5)] == 'T':
                self.cc.shape("Tour")
            elif self.etat['white'][(5, 5)] == 'F':
                self.cc.shape("Fou")
            elif self.etat['white'][(5, 5)] == 'C':
                self.cc.shape("Cheval")
            elif self.etat['white'][(5, 5)] == 'Q':
                self.cc.shape("Dame")
            elif self.etat['white'][(5, 5)] == 'K':
                self.cc.shape("King")
        elif (5, 5) in self.etat['black'].keys():
            self.cc.color('black')
            if self.etat['black'][(5, 5)] == 'P':
                self.cc.shape('circle')
            elif self.etat['black'][(5, 5)] == 'T':
                self.cc.shape("Tour")
            elif self.etat['black'][(5, 5)] == 'F':
                self.cc.shape("Fou")
            elif self.etat['black'][(5, 5)] == 'C':
                self.cc.shape("Cheval")
            elif self.etat['black'][(5, 5)] == 'Q':
                self.cc.shape("Dame")
            elif self.etat['black'][(5, 5)] == 'K':
                self.cc.shape("King")
        else:
            self.cc.color('black')
            self.cc.shape('square')
        if (5, 6) in self.etat['white'].keys():
            self.cs.color('white')
            if self.etat['white'][(5, 6)] == 'P':
                self.cs.shape('circle')
            elif self.etat['white'][(5, 6)] == 'T':
                self.cs.shape("Tour")
            elif self.etat['white'][(5, 6)] == 'F':
                self.cs.shape("Fou")
            elif self.etat['white'][(5, 6)] == 'C':
                self.cs.shape("Cheval")
            elif self.etat['white'][(5, 6)] == 'Q':
                self.cs.shape("Dame")
            elif self.etat['white'][(5, 6)] == 'K':
                self.cs.shape("King")
        elif (5, 6) in self.etat['black'].keys():
            self.cs.color('black')
            if self.etat['black'][(5, 6)] == 'P':
                self.cs.shape('circle')
            elif self.etat['black'][(5, 6)] == 'T':
                self.cs.shape("Tour")
            elif self.etat['black'][(5, 6)] == 'F':
                self.cs.shape("Fou")
            elif self.etat['black'][(5, 6)] == 'C':
                self.cs.shape("Cheval")
            elif self.etat['black'][(5, 6)] == 'Q':
                self.cs.shape("Dame")
            elif self.etat['black'][(5, 6)] == 'K':
                self.cs.shape("King")
        else:
            self.cs.color('white')
            self.cs.shape('square')
        if (5, 7) in self.etat['white'].keys():
            self.csp.color('white')
            if self.etat['white'][(5, 7)] == 'P':
                self.csp.shape('circle')
            elif self.etat['white'][(5, 7)] == 'T':
                self.csp.shape("Tour")
            elif self.etat['white'][(5, 7)] == 'F':
                self.csp.shape("Fou")
            elif self.etat['white'][(5, 7)] == 'C':
                self.csp.shape("Cheval")
            elif self.etat['white'][(5, 7)] == 'Q':
                self.csp.shape("Dame")
            elif self.etat['white'][(5, 7)] == 'K':
                self.csp.shape("King")
        elif (5, 7) in self.etat['black'].keys():
            self.csp.color('black')
            if self.etat['black'][(5, 7)] == 'P':
                self.csp.shape('circle')
            elif self.etat['black'][(5, 7)] == 'T':
                self.csp.shape("Tour")
            elif self.etat['black'][(5, 7)] == 'F':
                self.csp.shape("Fou")
            elif self.etat['black'][(5, 7)] == 'C':
                self.csp.shape("Cheval")
            elif self.etat['black'][(5, 7)] == 'Q':
                self.csp.shape("Dame")
            elif self.etat['black'][(5, 7)] == 'K':
                self.csp.shape("King")
        else:
            self.csp.color('black')
            self.csp.shape('square')
        if (5, 8) in self.etat['white'].keys():
            self.ch.color('white')
            if self.etat['white'][(5, 8)] == 'P':
                self.ch.shape('circle')
            elif self.etat['white'][(5, 8)] == 'T':
                self.ch.shape("Tour")
            elif self.etat['white'][(5, 8)] == 'F':
                self.ch.shape("Fou")
            elif self.etat['white'][(5, 8)] == 'C':
                self.ch.shape("Cheval")
            elif self.etat['white'][(5, 8)] == 'Q':
                self.ch.shape("Dame")
            elif self.etat['white'][(5, 8)] == 'K':
                self.ch.shape("King")
        elif (5, 8) in self.etat['black'].keys():
            self.ch.color('black')
            if self.etat['black'][(5, 8)] == 'P':
                self.ch.shape('circle')
            elif self.etat['black'][(5, 8)] == 'T':
                self.ch.shape("Tour")
            elif self.etat['black'][(5, 8)] == 'F':
                self.ch.shape("Fou")
            elif self.etat['black'][(5, 8)] == 'C':
                self.ch.shape("Cheval")
            elif self.etat['black'][(5, 8)] == 'Q':
                self.ch.shape("Dame")
            elif self.etat['black'][(5, 8)] == 'K':
                self.ch.shape("King")
        else:
            self.ch.color('white')
            self.ch.shape('square')
        if (6, 1) in self.etat['white'].keys():
            self.su.color('white')
            if self.etat['white'][(6, 1)] == 'P':
                self.su.shape('circle')
            elif self.etat['white'][(6, 1)] == 'T':
                self.su.shape("Tour")
            elif self.etat['white'][(6, 1)] == 'F':
                self.su.shape("Fou")
            elif self.etat['white'][(6, 1)] == 'C':
                self.su.shape("Cheval")
            elif self.etat['white'][(6, 1)] == 'Q':
                self.su.shape("Dame")
            elif self.etat['white'][(6, 1)] == 'K':
                self.su.shape("King")
        elif (6, 1) in self.etat['black'].keys():
            self.su.color('black')
            if self.etat['black'][(6, 1)] == 'P':
                self.su.shape('circle')
            elif self.etat['black'][(6, 1)] == 'T':
                self.su.shape("Tour")
            elif self.etat['black'][(6, 1)] == 'F':
                self.su.shape("Fou")
            elif self.etat['black'][(6, 1)] == 'C':
                self.su.shape("Cheval")
            elif self.etat['black'][(6, 1)] == 'Q':
                self.su.shape("Dame")
            elif self.etat['black'][(6, 1)] == 'K':
                self.su.shape("King")
        else:
            self.su.color('white')
            self.su.shape('square')
        if (6, 2) in self.etat['white'].keys():
            self.sd.color('white')
            if self.etat['white'][(6, 2)] == 'P':
                self.sd.shape('circle')
            elif self.etat['white'][(6, 2)] == 'T':
                self.sd.shape("Tour")
            elif self.etat['white'][(6, 2)] == 'F':
                self.sd.shape("Fou")
            elif self.etat['white'][(6, 2)] == 'C':
                self.sd.shape("Cheval")
            elif self.etat['white'][(6, 2)] == 'Q':
                self.sd.shape("Dame")
            elif self.etat['white'][(6, 2)] == 'K':
                self.sd.shape("King")
        elif (6, 2) in self.etat['black'].keys():
            self.sd.color('black')
            if self.etat['black'][(6, 2)] == 'P':
                self.sd.shape('circle')
            elif self.etat['black'][(6, 2)] == 'T':
                self.sd.shape("Tour")
            elif self.etat['black'][(6, 2)] == 'F':
                self.sd.shape("Fou")
            elif self.etat['black'][(6, 2)] == 'C':
                self.sd.shape("Cheval")
            elif self.etat['black'][(6, 2)] == 'Q':
                self.sd.shape("Dame")
            elif self.etat['black'][(6, 2)] == 'K':
                self.sd.shape("King")
        else:
            self.sd.color('black')
            self.sd.shape('square')
        if (6, 3) in self.etat['white'].keys():
            self.st.color('white')
            if self.etat['white'][(6, 3)] == 'P':
                self.st.shape('circle')
            elif self.etat['white'][(6, 3)] == 'T':
                self.st.shape("Tour")
            elif self.etat['white'][(6, 3)] == 'F':
                self.st.shape("Fou")
            elif self.etat['white'][(6, 3)] == 'C':
                self.st.shape("Cheval")
            elif self.etat['white'][(6, 3)] == 'Q':
                self.st.shape("Dame")
            elif self.etat['white'][(6, 3)] == 'K':
                self.st.shape("King")     
        elif (6, 3) in self.etat['black'].keys():
            self.st.color('black')
            if self.etat['black'][(6, 3)] == 'P':
                self.st.shape('circle')
            elif self.etat['black'][(6, 3)] == 'T':
                self.st.shape("Tour")
            elif self.etat['black'][(6, 3)] == 'F':
                self.st.shape("Fou")
            elif self.etat['black'][(6, 3)] == 'C':
                self.st.shape("Cheval")
            elif self.etat['black'][(6, 3)] == 'Q':
                self.st.shape("Dame")
            elif self.etat['black'][(6, 3)] == 'K':
                self.st.shape("King")
        else:
            self.st.color('white')
            self.st.shape('square')
        if (6, 4) in self.etat['white'].keys():
            self.sq.color('white')
            if self.etat['white'][(6, 4)] == 'P':
                self.sq.shape('circle')
            elif self.etat['white'][(6, 4)] == 'T':
                self.sq.shape("Tour")
            elif self.etat['white'][(6, 4)] == 'F':
                self.sq.shape("Fou")
            elif self.etat['white'][(6, 4)] == 'C':
                self.sq.shape("Cheval")
            elif self.etat['white'][(6, 4)] == 'Q':
                self.sq.shape("Dame")
            elif self.etat['white'][(6, 4)] == 'K':
                self.sq.shape("King")     
        elif (6, 4) in self.etat['black'].keys():
            self.sq.color('black')
            if self.etat['black'][(6, 4)] == 'P':
                self.sq.shape('circle')
            elif self.etat['black'][(6, 4)] == 'T':
                self.sq.shape("Tour")
            elif self.etat['black'][(6, 4)] == 'F':
                self.sq.shape("Fou")
            elif self.etat['black'][(6, 4)] == 'C':
                self.sq.shape("Cheval")
            elif self.etat['black'][(6, 4)] == 'Q':
                self.sq.shape("Dame")
            elif self.etat['black'][(6, 4)] == 'K':
                self.sq.shape("King")
        else:
            self.sq.color('black')
            self.sq.shape('square')
        if (6, 5) in self.etat['white'].keys():
            self.sc.color('white')
            if self.etat['white'][(6, 5)] == 'P':
                self.sc.shape('circle')
            elif self.etat['white'][(6, 5)] == 'T':
                self.sc.shape("Tour")
            elif self.etat['white'][(6, 5)] == 'F':
                self.sc.shape("Fou")
            elif self.etat['white'][(6, 5)] == 'C':
                self.sc.shape("Cheval")
            elif self.etat['white'][(6, 5)] == 'Q':
                self.sc.shape("Dame")
            elif self.etat['white'][(6, 5)] == 'K':
                self.sc.shape("King")
        elif (6, 5) in self.etat['black'].keys():
            self.sc.color('black')
            if self.etat['black'][(6, 5)] == 'P':
                self.sc.shape('circle')
            elif self.etat['black'][(6, 5)] == 'T':
                self.sc.shape("Tour")
            elif self.etat['black'][(6, 5)] == 'F':
                self.sc.shape("Fou")
            elif self.etat['black'][(6, 5)] == 'C':
                self.sc.shape("Cheval")
            elif self.etat['black'][(6, 5)] == 'Q':
                self.sc.shape("Dame")
            elif self.etat['black'][(6, 5)] == 'K':
                self.sc.shape("King")
        else:
            self.sc.color('white')
            self.sc.shape('square')
        if (6, 6) in self.etat['white'].keys():
            self.ss.color('white')
            if self.etat['white'][(6, 6)] == 'P':
                self.ss.shape('circle')
            elif self.etat['white'][(6, 6)] == 'T':
                self.ss.shape("Tour")
            elif self.etat['white'][(6, 6)] == 'F':
                self.ss.shape("Fou")
            elif self.etat['white'][(6, 6)] == 'C':
                self.ss.shape("Cheval")
            elif self.etat['white'][(6, 6)] == 'Q':
                self.ss.shape("Dame")
            elif self.etat['white'][(6, 6)] == 'K':
                self.ss.shape("King")
        elif (6, 6) in self.etat['black'].keys():
            self.ss.color('black')
            if self.etat['black'][(6, 6)] == 'P':
                self.ss.shape('circle')
            elif self.etat['black'][(6, 6)] == 'T':
                self.ss.shape("Tour")
            elif self.etat['black'][(6, 6)] == 'F':
                self.ss.shape("Fou")
            elif self.etat['black'][(6, 6)] == 'C':
                self.ss.shape("Cheval")
            elif self.etat['black'][(6, 6)] == 'Q':
                self.ss.shape("Dame")
            elif self.etat['black'][(6, 6)] == 'K':
                self.ss.shape("King")
        else:
            self.ss.color('black')
            self.ss.shape('square')
        if (6, 7) in self.etat['white'].keys():
            self.ssp.color('white')
            if self.etat['white'][(6, 7)] == 'P':
                self.ssp.shape('circle')
            elif self.etat['white'][(6, 7)] == 'T':
                self.ssp.shape("Tour")
            elif self.etat['white'][(6, 7)] == 'F':
                self.ssp.shape("Fou")
            elif self.etat['white'][(6, 7)] == 'C':
                self.ssp.shape("Cheval")
            elif self.etat['white'][(6, 7)] == 'Q':
                self.ssp.shape("Dame")
            elif self.etat['white'][(6, 7)] == 'K':
                self.ssp.shape("King")
        elif (6, 7) in self.etat['black'].keys():
            self.ssp.color('black')
            if self.etat['black'][(6, 7)] == 'P':
                self.ssp.shape('circle')
            elif self.etat['black'][(6, 7)] == 'T':
                self.ssp.shape("Tour")
            elif self.etat['black'][(6, 7)] == 'F':
                self.ssp.shape("Fou")
            elif self.etat['black'][(6, 7)] == 'C':
                self.ssp.shape("Cheval")
            elif self.etat['black'][(6, 7)] == 'Q':
                self.ssp.shape("Dame")
            elif self.etat['black'][(6, 7)] == 'K':
                self.ssp.shape("King")
        else:
            self.ssp.color('white')
            self.ssp.shape('square')
        if (6, 8) in self.etat['white'].keys():
            self.sh.color('white')
            if self.etat['white'][(6, 8)] == 'P':
                self.sh.shape('circle')
            elif self.etat['white'][(6, 8)] == 'T':
                self.sh.shape("Tour")
            elif self.etat['white'][(6, 8)] == 'F':
                self.sh.shape("Fou")
            elif self.etat['white'][(6, 8)] == 'C':
                self.sh.shape("Cheval")
            elif self.etat['white'][(6, 8)] == 'Q':
                self.sh.shape("Dame")
            elif self.etat['white'][(6, 8)] == 'K':
                self.sh.shape("King")
        elif (6, 8) in self.etat['black'].keys():
            self.sh.color('black')
            if self.etat['black'][(6, 8)] == 'P':
                self.sh.shape('circle')
            elif self.etat['black'][(6, 8)] == 'T':
                self.sh.shape("Tour")
            elif self.etat['black'][(6, 8)] == 'F':
                self.sh.shape("Fou")
            elif self.etat['black'][(6, 8)] == 'C':
                self.sh.shape("Cheval")
            elif self.etat['black'][(6, 8)] == 'Q':
                self.sh.shape("Dame")
            elif self.etat['black'][(6, 8)] == 'K':
                self.sh.shape("King")
        else:
            self.sh.color('black')
            self.sh.shape('square')
        if (7, 1) in self.etat['white'].keys():
            self.spu.color('white')
            if self.etat['white'][(7, 1)] == 'P':
                self.spu.shape('circle')
            elif self.etat['white'][(7, 1)] == 'T':
                self.spu.shape("Tour")
            elif self.etat['white'][(7, 1)] == 'F':
                self.spu.shape("Fou")
            elif self.etat['white'][(7, 1)] == 'C':
                self.spu.shape("Cheval")
            elif self.etat['white'][(7, 1)] == 'Q':
                self.spu.shape("Dame")
            elif self.etat['white'][(7, 1)] == 'K':
                self.spu.shape("King")
        elif (7, 1) in self.etat['black'].keys():
            self.spu.color('black')
            if self.etat['black'][(7, 1)] == 'P':
                self.spu.shape('circle')
            elif self.etat['black'][(7, 1)] == 'T':
                self.spu.shape("Tour")
            elif self.etat['black'][(7, 1)] == 'F':
                self.spu.shape("Fou")
            elif self.etat['black'][(7, 1)] == 'C':
                self.spu.shape("Cheval")
            elif self.etat['black'][(7, 1)] == 'Q':
                self.spu.shape("Dame")
            elif self.etat['black'][(7, 1)] == 'K':
                self.spu.shape("King")
        else:
            self.spu.color('black')
            self.spu.shape('square')
        if (7, 2) in self.etat['white'].keys():
            self.spd.color('white')
            if self.etat['white'][(7, 2)] == 'P':
                self.spd.shape('circle')
            elif self.etat['white'][(7, 2)] == 'T':
                self.spd.shape("Tour")
            elif self.etat['white'][(7, 2)] == 'F':
                self.spd.shape("Fou")
            elif self.etat['white'][(7, 2)] == 'C':
                self.spd.shape("Cheval")
            elif self.etat['white'][(7, 2)] == 'Q':
                self.spd.shape("Dame")
            elif self.etat['white'][(7, 2)] == 'K':
                self.spd.shape("King")
        elif (7, 2) in self.etat['black'].keys():
            self.spd.color('black')
            if self.etat['black'][(7, 2)] == 'P':
                self.spd.shape('circle')
            elif self.etat['black'][(7, 2)] == 'T':
                self.spd.shape("Tour")
            elif self.etat['black'][(7, 2)] == 'F':
                self.spd.shape("Fou")
            elif self.etat['black'][(7, 2)] == 'C':
                self.spd.shape("Cheval")
            elif self.etat['black'][(7, 2)] == 'Q':
                self.spd.shape("Dame")
            elif self.etat['black'][(7, 2)] == 'K':
                self.spd.shape("King")
        else:
            self.spd.color('white')
            self.spd.shape('square')
        if (7, 3) in self.etat['white'].keys():
            self.spt.color('white')
            if self.etat['white'][(7, 3)] == 'P':
                self.spt.shape('circle')
            elif self.etat['white'][(7, 3)] == 'T':
                self.spt.shape("Tour")
            elif self.etat['white'][(7, 3)] == 'F':
                self.spt.shape("Fou")
            elif self.etat['white'][(7, 3)] == 'C':
                self.spt.shape("Cheval")
            elif self.etat['white'][(7, 3)] == 'Q':
                self.spt.shape("Dame")
            elif self.etat['white'][(7, 3)] == 'K':
                self.spt.shape("King")
        elif (7, 3) in self.etat['black'].keys():
            self.spt.color('black')
            if self.etat['black'][(7, 3)] == 'P':
                self.spt.shape('circle')
            elif self.etat['black'][(7, 3)] == 'T':
                self.spt.shape("Tour")
            elif self.etat['black'][(7, 3)] == 'F':
                self.spt.shape("Fou")
            elif self.etat['black'][(7, 3)] == 'C':
                self.spt.shape("Cheval")
            elif self.etat['black'][(7, 3)] == 'Q':
                self.spt.shape("Dame")
            elif self.etat['black'][(7, 3)] == 'K':
                self.spt.shape("King")
        else:
            self.spt.color('black')
            self.spt.shape('square')
        if (7, 4) in self.etat['white'].keys():
            self.spq.color('white')
            if self.etat['white'][(7, 4)] == 'P':
                self.spq.shape('circle')
            elif self.etat['white'][(7, 4)] == 'T':
                self.spq.shape("Tour")
            elif self.etat['white'][(7, 4)] == 'F':
                self.spq.shape("Fou")
            elif self.etat['white'][(7, 4)] == 'C':
                self.spq.shape("Cheval")
            elif self.etat['white'][(7, 4)] == 'Q':
                self.spq.shape("Dame")
            elif self.etat['white'][(7, 4)] == 'K':
                self.spq.shape("King")    
        elif (7, 4) in self.etat['black'].keys():
            self.spq.color('black')
            if self.etat['black'][(7, 4)] == 'P':
                self.spq.shape('circle')
            elif self.etat['black'][(7, 4)] == 'T':
                self.spq.shape("Tour")
            elif self.etat['black'][(7, 4)] == 'F':
                self.spq.shape("Fou")
            elif self.etat['black'][(7, 4)] == 'C':
                self.spq.shape("Cheval")
            elif self.etat['black'][(7, 4)] == 'Q':
                self.spq.shape("Dame")
            elif self.etat['black'][(7, 4)] == 'K':
                self.spq.shape("King")
        else:
            self.spq.color('white')
            self.spq.shape('square')
        if (7, 5) in self.etat['white'].keys():
            self.spc.color('white')
            if self.etat['white'][(7, 5)] == 'P':
                self.spc.shape('circle')
            elif self.etat['white'][(7, 5)] == 'T':
                self.spc.shape("Tour")
            elif self.etat['white'][(7, 5)] == 'F':
                self.spc.shape("Fou")
            elif self.etat['white'][(7, 5)] == 'C':
                self.spc.shape("Cheval")
            elif self.etat['white'][(7, 5)] == 'Q':
                self.spc.shape("Dame")
            elif self.etat['white'][(7, 5)] == 'K':
                self.spc.shape("King")
        elif (7, 5) in self.etat['black'].keys():
            self.spc.color('black')
            if self.etat['black'][(7, 5)] == 'P':
                self.spc.shape('circle')
            elif self.etat['black'][(7, 5)] == 'T':
                self.spc.shape("Tour")
            elif self.etat['black'][(7, 5)] == 'F':
                self.spc.shape("Fou")
            elif self.etat['black'][(7, 5)] == 'C':
                self.spc.shape("Cheval")
            elif self.etat['black'][(7, 5)] == 'Q':
                self.spc.shape("Dame")
            elif self.etat['black'][(7, 5)] == 'K':
                self.spc.shape("King")
        else:
            self.spc.color('black')
            self.spc.shape('square')
        if (7, 6) in self.etat['white'].keys():
            self.sps.color('white')
            if self.etat['white'][(7, 6)] == 'P':
                self.sps.shape('circle')
            elif self.etat['white'][(7, 6)] == 'T':
                self.sps.shape("Tour")
            elif self.etat['white'][(7, 6)] == 'F':
                self.sps.shape("Fou")
            elif self.etat['white'][(7, 6)] == 'C':
                self.sps.shape("Cheval")
            elif self.etat['white'][(7, 6)] == 'Q':
                self.sps.shape("Dame")
            elif self.etat['white'][(7, 6)] == 'K':
                self.sps.shape("King")
        elif (7, 6) in self.etat['black'].keys():
            self.sps.color('black')
            if self.etat['black'][(7, 6)] == 'P':
                self.sps.shape('circle')
            elif self.etat['black'][(7, 6)] == 'T':
                self.sps.shape("Tour")
            elif self.etat['black'][(7, 6)] == 'F':
                self.sps.shape("Fou")
            elif self.etat['black'][(7, 6)] == 'C':
                self.sps.shape("Cheval")
            elif self.etat['black'][(7, 6)] == 'Q':
                self.sps.shape("Dame")
            elif self.etat['black'][(7, 6)] == 'K':
                self.sps.shape("King")
        else:
            self.sps.color('white')
            self.sps.shape('square')
        if (7, 7) in self.etat['white'].keys():
            self.spsp.color('white')
            if self.etat['white'][(7, 7)] == 'P':
                self.spsp.shape('circle')
            elif self.etat['white'][(7, 7)] == 'T':
                self.spsp.shape("Tour")
            elif self.etat['white'][(7, 7)] == 'F':
                self.spsp.shape("Fou")
            elif self.etat['white'][(7, 7)] == 'C':
                self.spsp.shape("Cheval")
            elif self.etat['white'][(7, 7)] == 'Q':
                self.spsp.shape("Dame")
            elif self.etat['white'][(7, 7)] == 'K':
                self.spsp.shape("King")
        elif (7, 7) in self.etat['black'].keys():
            self.spsp.color('black')
            if self.etat['black'][(7, 7)] == 'P':
                self.spsp.shape('circle')
            elif self.etat['black'][(7, 7)] == 'T':
                self.spsp.shape("Tour")
            elif self.etat['black'][(7, 7)] == 'F':
                self.spsp.shape("Fou")
            elif self.etat['black'][(7, 7)] == 'C':
                self.spsp.shape("Cheval")
            elif self.etat['black'][(7, 7)] == 'Q':
                self.spsp.shape("Dame")
            elif self.etat['black'][(7, 7)] == 'K':
                self.spsp.shape("King")
        else:
            self.spsp.color('black')
            self.spsp.shape('square')
        if (7, 8) in self.etat['white'].keys():
            self.sph.color('white')
            if self.etat['white'][(7, 8)] == 'P':
                self.sph.shape('circle')
            elif self.etat['white'][(7, 8)] == 'T':
                self.sph.shape("Tour")
            elif self.etat['white'][(7, 8)] == 'F':
                self.sph.shape("Fou")
            elif self.etat['white'][(7, 8)] == 'C':
                self.sph.shape("Cheval")
            elif self.etat['white'][(7, 8)] == 'Q':
                self.sph.shape("Dame")
            elif self.etat['white'][(7, 8)] == 'K':
                self.sph.shape("King")
        elif (7, 8) in self.etat['black'].keys():
            self.sph.color('black')
            if self.etat['black'][(7, 8)] == 'P':
                self.sph.shape('circle')
            elif self.etat['black'][(7, 8)] == 'T':
                self.sph.shape("Tour")
            elif self.etat['black'][(7, 8)] == 'F':
                self.sph.shape("Fou")
            elif self.etat['black'][(7, 8)] == 'C':
                self.sph.shape("Cheval")
            elif self.etat['black'][(7, 8)] == 'Q':
                self.sph.shape("Dame")
            elif self.etat['black'][(7, 8)] == 'K':
                self.sph.shape("King")
        else:
            self.sph.color('white')
            self.sph.shape('square')
        if (8, 1) in self.etat['white'].keys():
            self.hu.color('white')
            if self.etat['white'][(8, 1)] == 'P':
                self.hu.shape('circle')
            elif self.etat['white'][(8, 1)] == 'T':
                self.hu.shape("Tour")
            elif self.etat['white'][(8, 1)] == 'F':
                self.hu.shape("Fou")
            elif self.etat['white'][(8, 1)] == 'C':
                self.hu.shape("Cheval")
            elif self.etat['white'][(8, 1)] == 'Q':
                self.hu.shape("Dame")
            elif self.etat['white'][(8, 1)] == 'K':
                self.hu.shape("King")
        elif (8, 1) in self.etat['black'].keys():
            self.hu.color('black')
            if self.etat['black'][(8, 1)] == 'P':
                self.hu.shape('circle')
            elif self.etat['black'][(8, 1)] == 'T':
                self.hu.shape("Tour")
            elif self.etat['black'][(8, 1)] == 'F':
                self.hu.shape("Fou")
            elif self.etat['black'][(8, 1)] == 'C':
                self.hu.shape("Cheval")
            elif self.etat['black'][(8, 1)] == 'Q':
                self.hu.shape("Dame")
            elif self.etat['black'][(8, 1)] == 'K':
                self.hu.shape("King")
        else:
            self.hu.color('white')
            self.hu.shape('square')
        if (8, 2) in self.etat['white'].keys():
            self.hd.color('white')
            if self.etat['white'][(8, 2)] == 'P':
                self.hd.shape('circle')
            elif self.etat['white'][(8, 2)] == 'T':
                self.hd.shape("Tour")
            elif self.etat['white'][(8, 2)] == 'F':
                self.hd.shape("Fou")
            elif self.etat['white'][(8, 2)] == 'C':
                self.hd.shape("Cheval")
            elif self.etat['white'][(8, 2)] == 'Q':
                self.hd.shape("Dame")
            elif self.etat['white'][(8, 2)] == 'K':
                self.hd.shape("King")
        elif (8, 2) in self.etat['black'].keys():
            self.hd.color('black')
            if self.etat['black'][(8, 2)] == 'P':
                self.hd.shape('circle')
            elif self.etat['black'][(8, 2)] == 'T':
                self.hd.shape("Tour")
            elif self.etat['black'][(8, 2)] == 'F':
                self.hd.shape("Fou")
            elif self.etat['black'][(8, 2)] == 'C':
                self.hd.shape("Cheval")
            elif self.etat['black'][(8, 2)] == 'Q':
                self.hd.shape("Dame")
            elif self.etat['black'][(8, 2)] == 'K':
                self.hd.shape("King")
        else:
            self.hd.color('black')
            self.hd.shape('square')
        if (8, 3) in self.etat['white'].keys():
            self.ht.color('white')
            if self.etat['white'][(8, 3)] == 'P':
                self.ht.shape('circle')
            elif self.etat['white'][(8, 3)] == 'T':
                self.ht.shape("Tour")
            elif self.etat['white'][(8, 3)] == 'F':
                self.ht.shape("Fou")
            elif self.etat['white'][(8, 3)] == 'C':
                self.ht.shape("Cheval")
            elif self.etat['white'][(8, 3)] == 'Q':
                self.ht.shape("Dame")
            elif self.etat['white'][(8, 3)] == 'K':
                self.ht.shape("King")  
        elif (8, 3) in self.etat['black'].keys():
            self.ht.color('black')
            if self.etat['black'][(8, 3)] == 'P':
                self.ht.shape('circle')
            elif self.etat['black'][(8, 3)] == 'T':
                self.ht.shape("Tour")
            elif self.etat['black'][(8, 3)] == 'F':
                self.ht.shape("Fou")
            elif self.etat['black'][(8, 3)] == 'C':
                self.ht.shape("Cheval")
            elif self.etat['black'][(8, 3)] == 'Q':
                self.ht.shape("Dame")
            elif self.etat['black'][(8, 3)] == 'K':
                self.ht.shape("King")
        else:
            self.ht.color('white')
            self.ht.shape('square')
        if (8, 4) in self.etat['white'].keys():
            self.hq.color('white')
            if self.etat['white'][(8, 4)] == 'P':
                self.hq.shape('circle')
            elif self.etat['white'][(8, 4)] == 'T':
                self.hq.shape("Tour")
            elif self.etat['white'][(8, 4)] == 'F':
                self.hq.shape("Fou")
            elif self.etat['white'][(8, 4)] == 'C':
                self.hq.shape("Cheval")
            elif self.etat['white'][(8, 4)] == 'Q':
                self.hq.shape("Dame")
            elif self.etat['white'][(8, 4)] == 'K':
                self.hq.shape("King")     
        elif (8, 4) in self.etat['black'].keys():
            self.hq.color('black')
            if self.etat['black'][(8, 4)] == 'P':
                self.hq.shape('circle')
            elif self.etat['black'][(8, 4)] == 'T':
                self.hq.shape("Tour")
            elif self.etat['black'][(8, 4)] == 'F':
                self.hq.shape("Fou")
            elif self.etat['black'][(8, 4)] == 'C':
                self.hq.shape("Cheval")
            elif self.etat['black'][(8, 4)] == 'Q':
                self.hq.shape("Dame")
            elif self.etat['black'][(8, 4)] == 'K':
                self.hq.shape("King")
        else:
            self.hq.color('black')
            self.hq.shape('square')
        if (8, 5) in self.etat['white'].keys():
            self.hc.color('white')
            if self.etat['white'][(8, 5)] == 'P':
                self.hc.shape('circle')
            elif self.etat['white'][(8, 5)] == 'T':
                self.hc.shape("Tour")
            elif self.etat['white'][(8, 5)] == 'F':
                self.hc.shape("Fou")
            elif self.etat['white'][(8, 5)] == 'C':
                self.hc.shape("Cheval")
            elif self.etat['white'][(8, 5)] == 'Q':
                self.hc.shape("Dame")
            elif self.etat['white'][(8, 5)] == 'K':
                self.hc.shape("King")
        elif (8, 5) in self.etat['black'].keys():
            self.hc.color('black')
            if self.etat['black'][(8, 5)] == 'P':
                self.hc.shape('circle')
            elif self.etat['black'][(8, 5)] == 'T':
                self.hc.shape("Tour")
            elif self.etat['black'][(8, 5)] == 'F':
                self.hc.shape("Fou")
            elif self.etat['black'][(8, 5)] == 'C':
                self.hc.shape("Cheval")
            elif self.etat['black'][(8, 5)] == 'Q':
                self.hc.shape("Dame")
            elif self.etat['black'][(8, 5)] == 'K':
                self.hc.shape("King")
        else:
            self.hc.color('white')
            self.hc.shape('square')
        if (8, 6) in self.etat['white'].keys():
            self.hs.color('white')
            if self.etat['white'][(8, 6)] == 'P':
                self.hs.shape('circle')
            elif self.etat['white'][(8, 6)] == 'T':
                self.hs.shape("Tour")
            elif self.etat['white'][(8, 6)] == 'F':
                self.hs.shape("Fou")
            elif self.etat['white'][(8, 6)] == 'C':
                self.hs.shape("Cheval")
            elif self.etat['white'][(8, 6)] == 'Q':
                self.hs.shape("Dame")
            elif self.etat['white'][(8, 6)] == 'K':
                self.hs.shape("King")
        elif (8, 6) in self.etat['black'].keys():
            self.hs.color('black')
            if self.etat['black'][(8, 6)] == 'P':
                self.hs.shape('circle')
            elif self.etat['black'][(8, 6)] == 'T':
                self.hs.shape("Tour")
            elif self.etat['black'][(8, 6)] == 'F':
                self.hs.shape("Fou")
            elif self.etat['black'][(8, 6)] == 'C':
                self.hs.shape("Cheval")
            elif self.etat['black'][(8, 6)] == 'Q':
                self.hs.shape("Dame")
            elif self.etat['black'][(8, 6)] == 'K':
                self.hs.shape("King")
        else:
            self.hs.color('black')
            self.hs.shape('square')
        if (8, 7) in self.etat['white'].keys():
            self.hsp.color('white')
            if self.etat['white'][(8, 7)] == 'P':
                self.hsp.shape('circle')
            elif self.etat['white'][(8, 7)] == 'T':
                self.hsp.shape("Tour")
            elif self.etat['white'][(8, 7)] == 'F':
                self.hsp.shape("Fou")
            elif self.etat['white'][(8, 7)] == 'C':
                self.hsp.shape("Cheval")
            elif self.etat['white'][(8, 7)] == 'Q':
                self.hsp.shape("Dame")
            elif self.etat['white'][(8, 7)] == 'K':
                self.hsp.shape("King")
        elif (8, 7) in self.etat['black'].keys():
            self.hsp.color('black')
            if self.etat['black'][(8, 7)] == 'P':
                self.hsp.shape('circle')
            elif self.etat['black'][(8, 7)] == 'T':
                self.hsp.shape("Tour")
            elif self.etat['black'][(8, 7)] == 'F':
                self.hsp.shape("Fou")
            elif self.etat['black'][(8, 7)] == 'C':
                self.hsp.shape("Cheval")
            elif self.etat['black'][(8, 7)] == 'Q':
                self.hsp.shape("Dame")
            elif self.etat['black'][(8, 7)] == 'K':
                self.hsp.shape("King")
        else:
            self.hsp.color('white')
            self.hsp.shape('square')
        if (8, 8) in self.etat['white'].keys():
            self.hh.color('white')
            if self.etat['white'][(8, 8)] == 'P':
                self.hh.shape('circle')
            elif self.etat['white'][(8, 8)] == 'T':
                self.hh.shape("Tour")
            elif self.etat['white'][(8, 8)] == 'F':
                self.hh.shape("Fou")
            elif self.etat['white'][(8, 8)] == 'C':
                self.hh.shape("Cheval")
            elif self.etat['white'][(8, 8)] == 'Q':
                self.hh.shape("Dame")
            elif self.etat['white'][(8, 8)] == 'K':
                self.hh.shape("King")
        elif (8, 8) in self.etat['black'].keys():
            self.hh.color('black')
            if self.etat['black'][(8, 8)] == 'P':
                self.hh.shape('circle')
            elif self.etat['black'][(8, 8)] == 'T':
                self.hh.shape("Tour")
            elif self.etat['black'][(8, 8)] == 'F':
                self.hh.shape("Fou")
            elif self.etat['black'][(8, 8)] == 'C':
                self.hh.shape("Cheval")
            elif self.etat['black'][(8, 8)] == 'Q':
                self.hh.shape("Dame")
            elif self.etat['black'][(8, 8)] == 'K':
                self.hh.shape("King")
        else:
            self.hh.color('black')
            self.hh.shape('square')
class EchecError(Exception):
    pass
# a = echec()
# a.jouer_coupB((7, 2), (7, 3))
# a.jouer_coupB((6, 1), (8, 3))
# print(a)
# print(a.état())
# a.jouer_coupB((8, 3), (6, 1))
# print(a)
# while True:
#     try:
#         a.stratB3()
#         print(a)
#         a.stratW3()
#         print(a)
#     except EchecError as err:
#         print(err)
#         break
# a = echecXX()
# print(a)
# while True:
#     v = 0
#     try:
#         if a.check_echecB():
#             print('Échec !')             
#         c = input('ton coup!')
#         if len(c) != 4:
#             raise RuntimeError('coup invalide')
#         if not int(c):
#             raise RuntimeError('coup invalide')
#         a.jouer_coupB(('+c[0]+', '+c[1]+'), ('+c[2]+', '+c[3]+'))
#         print(a)
#     except ValueError:
#         v = 1
#     except EchecError as err:
#         print(err)
#         v = 1    
#     except RuntimeError as err:
#         print(err)
#         v = 1
#     try:
#         if v == 1:
#             raise RuntimeError
#         if a.check_echecW():
#             print('Echec !')
#         a.stratW2()
#         print(a)
#     except RuntimeError:
#         v = 0
#     except EchecError as err:
#         print(err)
# #         break

# for i in range(10):
#     n=0
#     a = echec()
#     while True:
#         try:
#             a.stratW2()
#             n+=1
#             a.stratB3()
#             n+=1
#         except EchecError as err:
#             print(err)
#             print(n)
#             break
    
# while True:
#     try:
#         a.stratW2()
#         a.afficher()
#         a.stratB3()
#         a.afficher()
#     except EchecError as err:
#         print(err)
#         break
# while True:
#     v = 0
#     try:
#         if a.check_echecB():
#             a.afficher()             
#         c = input('ton coup!')
#         if len(c) != 4:
#             raise RuntimeError('coup invalide')
#         if not int(c):
#             raise RuntimeError('coup invalide')
#         a.jouer_coupB(('+c[0]+', '+c[1]+'), ('+c[2]+', '+c[3]+'))
#         a.afficher()
#     except ValueError:
#         v = 1
#     except EchecError as err:
#         print(err)
#         v = 1    
#     except RuntimeError as err:
#         print(err)
#         v = 1
#     try:
#         if v == 1:
#             raise RuntimeError
#         if a.check_echecW():
#             print('Echec !')
#         a.stratW2()
#         a.afficher()
#     except RuntimeError:
#         v = 0
#     except EchecError as err:
#         print(err)
#         break