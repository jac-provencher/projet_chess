import random
import copy
class EchecError(Exception):
    pass
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
                                    if self.check_echecB():
                                        listeval += [0.5-self.valcpB3()]
                                    else:
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
                val += 2
            elif kind == 'T' or kind == 'C' or kind == 'F':
                val += 4
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
                val -= 9
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
                                    if self.check_echecB():
                                        listeval += [0.5]
                                    else:
                                        listeval+=[0]
                                    self.jouer_coupW((x, y), pf)
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                    
                            except EchecError:
                                continue
        if listeval != []:
            return max(listeval)
        return -1000 if self.check_echecW() else -2
    
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
                                    listeval += [self.valjeu() - vali-self.valcpB2()]
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                                    self.etat['black'][pf] = it
                                else:
                                    self.jouer_coupW((x, y), pf)
                                    if self.check_echecB():
                                        listeval += [0.5]
                                    else:
                                        listeval+=[0]
                                    self.etat['white'].pop(pf)
                                    self.etat['white'][(x, y)] = im
                            except EchecError:
                                continue
        if listeval != []:
            return max(listeval)
        return -600 if self.check_echecW() else -20  
    
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
                                    self.jouer_coupB((x, y), pf)
                                    if self.check_echecW():
                                        listeval +=[0.5-self.valcpW()]
                                    else:
                                        listeval += [0]
                                    self.etat['black'].pop(pf)
                                    self.etat['black'][(x, y)] = im
                            except EchecError:
                                continue
        if listeval != []:
            return max(listeval)
        return -1000 if self.check_echecB() else 20
    
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
                                    self.jouer_coupB((x, y), pf)
                                    if self.check_echecW():
                                        listeval+=[0.5]
                                    else:
                                        listeval += [0]
                                    self.etat['black'].pop(pf)
                                    self.etat['black'][(x, y)] = im 
                            except EchecError:
                                continue
        if listeval != []:
            return max(listeval)
        return -400 if self.check_echecB() else 20
    
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
        self.etpass = copy.deepcopy(self.etat)
        self.n = 0
    
    def etatpass(self):
        self.etpass = copy.deepcopy(self.etat)
    
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
        ens = {0}
        ens.add((pi[0]+2, pi[1]+1))
        ens.add((pi[0]+2, pi[1]-1))
        ens.add((pi[0]-2, pi[1]+1))
        ens.add((pi[0]-2, pi[1]-1))
        ens.add((pi[0]+1, pi[1]+2))
        ens.add((pi[0]+1, pi[1]-2))
        ens.add((pi[0]-1, pi[1]+2))
        ens.add((pi[0]-1, pi[1]-2))
        p = 0
        q = 0
        if pf in ens:
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
        ens = {0}
        ens.add((pi[0]+1, pi[1]))
        ens.add((pi[0]-1, pi[1]))
        ens.add((pi[0], pi[1]+1))
        ens.add(((pi[0], pi[1]-1)))
        ens.add((pi[0]+1, pi[1]+1))
        ens.add((pi[0]+1, pi[1]-1))
        ens.add((pi[0]-1, pi[1]+1))
        ens.add((pi[0]-1, pi[1]-1))  
        p = 0
        q = 0
        if pf in ens:
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
        ens = {0}
        ens.add((pi[0]+1, pi[1]))
        ens.add((pi[0]-1, pi[1]))
        ens.add((pi[0], pi[1]+1))
        ens.add(((pi[0], pi[1]-1)))
        ens.add((pi[0]+1, pi[1]+1))
        ens.add((pi[0]+1, pi[1]-1))
        ens.add((pi[0]-1, pi[1]+1))
        ens.add((pi[0]-1, pi[1]-1))
        p = 0
        q = 0
        if pf in ens:
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
        ens = {0}
        ens.add((pi[0]+2, pi[1]+1))
        ens.add((pi[0]+2, pi[1]-1))
        ens.add((pi[0]-2, pi[1]+1))
        ens.add((pi[0]-2, pi[1]-1))
        ens.add((pi[0]+1, pi[1]+2))
        ens.add((pi[0]+1, pi[1]-2))
        ens.add((pi[0]-1, pi[1]+2))
        ens.add((pi[0]-1, pi[1]-2))
        p = 0
        q = 0
        if pf in ens:
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
        ens = {0}
        if not self.etat['black'].get((pi[0], pi[1]+1)) and not self.etat['white'].get((pi[0], pi[1]+1)):
            ens.add((pi[0], pi[1]+1))
            if not self.etat['black'].get((pi[0], pi[1]+2)) and not self.etat['white'].get((pi[0], pi[1]+2)) and pi[1] == 2:
                ens.add((pi[0], pi[1]+2))
        if self.etat['white'].get((pi[0]+1, pi[1]+1)):
            ens.add((pi[0]+1, pi[1]+1))
        if self.etat['white'].get((pi[0]-1, pi[1]+1)):
            ens.add((pi[0]-1, pi[1]+1))
        if pf in ens:
            self.etat['black'].pop(pi)
            self.etat['black'][pf] = 'P'
            if pf[1] == 8:
                self.etat['black'][pf] = 'Q'
            if self.etat['white'].get(pf):
                self.etat['white'].pop(pf)
        else:
            raise EchecError('coup invalide')
    
    def deplacer_pionW(self, pi, pf):
        ens = {0}
        if not self.etat['white'].get((pi[0], pi[1]-1)) and not self.etat['black'].get((pi[0], pi[1]-1)):
            ens.add(((pi[0], pi[1]-1)))
            if pi[1] == 7 and not self.etat['black'].get((pi[0], pi[1]-2)) and not self.etat['white'].get((pi[0], pi[1]-2)):
                ens.add((pi[0], pi[1]-2))
        if self.etat['black'].get((pi[0]+1, pi[1]-1)):
            ens.add(((pi[0]+1, pi[1]-1)))
        if self.etat['black'].get((pi[0]-1, pi[1]-1)):
            ens.add((pi[0]-1, pi[1]-1))
        if pf in ens:
            self.etat['white'].pop(pi)
            self.etat['white'][pf] = 'P'
            if pf[1] == 1:
                self.etat['white'][pf] = 'Q'
                p = 1
            if self.etat['black'].get(pf):
                self.etat['black'].pop(pf)
        else:
            raise EchecError('coup invalide')
    
    def deplacer_tourW(self, pi, pf):
        ens = {0}
        for i in range(8):
            if pi[1]+i > 7:
                break
            if not self.etat['white'].get((pi[0], pi[1]+i+1)):
                ens.add((pi[0], pi[1]+1+i))
            if self.etat['black'].get((pi[0], pi[1]+i+1)):
                break
            if self.etat['white'].get((pi[0], pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2:
                break
            if not self.etat['white'].get((pi[0], pi[1]-i-1)):
                ens.add((pi[0], pi[1]-1-i))
            if self.etat['black'].get((pi[0], pi[1]-i-1)):
                break
            if self.etat['white'].get((pi[0], pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2:
                break
            if not self.etat['white'].get((pi[0]-i-1, pi[1])):
                ens.add((pi[0]-i-1, pi[1]))
            if self.etat['black'].get((pi[0]-i-1, pi[1])):
                break
            if self.etat['white'].get((pi[0]-1-i, pi[1])):
                break
        for i in range(8):
            if pi[0]+i > 7:
                break
            if not self.etat['white'].get((pi[0]+i+1, pi[1])):
                ens.add((pi[0]+i+1, pi[1]))
            if self.etat['black'].get((pi[0]+i+1, pi[1])):
                break
            if self.etat['white'].get((pi[0]+1+i, pi[1])):
                break
        if pf in ens:
            self.etat['white'].pop(pi)
            self.etat['white'][pf] = 'T'
            if self.etat['black'].get(pf):
                self.etat['black'].pop(pf)
        else:
          raise EchecError('le coup est invalide')
    
    def deplacer_tourB(self, pi, pf):
        ens ={0}
        for i in range(8):
            if pi[1]+i > 7:
                break
            if not self.etat['black'].get((pi[0], pi[1]+i+1)):
                ens.add((pi[0], pi[1]+1+i))
            if self.etat['white'].get((pi[0], pi[1]+i+1)):
                break
            if self.etat['black'].get((pi[0], pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2:
                break
            if not self.etat['black'].get((pi[0], pi[1]-i-1)):
                ens.add((pi[0], pi[1]-1-i))
            if self.etat['white'].get((pi[0], pi[1]-i-1)):
                break
            if self.etat['black'].get((pi[0], pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2:
                break
            if not self.etat['black'].get((pi[0]-i-1, pi[1])):
                ens.add((pi[0]-i-1, pi[1]))
            if self.etat['white'].get((pi[0]-i-1, pi[1])):
                break
            if self.etat['black'].get((pi[0]-1-i, pi[1])):
                break
        for i in range(8):
            if pi[0]+i > 7:
                break
            if not self.etat['black'].get((pi[0]+i+1, pi[1])):
                ens.add((pi[0]+i+1, pi[1]))
            if self.etat['white'].get((pi[0]+i+1, pi[1])):
                break
            if self.etat['black'].get((pi[0]+1+i, pi[1])):
                break
        if pf in ens:
            self.etat['black'].pop(pi)
            self.etat['black'][pf] = 'T'
            if self.etat['white'].get(pf):
                self.etat['white'].pop(pf)
        else:
            raise EchecError('le coup est invalide')
    
    def deplacer_fouB(self, pi, pf):
        ens = {0}
        for i in range(8):
            if pi[1]+i > 7 or pi[0]+i > 7 :
                break
            if not self.etat['black'].get((pi[0]+i+1, pi[1]+i+1)):
                ens.add((pi[0]+1+i, pi[1]+1+i))
            if self.etat['white'].get((pi[0]+1+i, pi[1]+i+1)):
                break
            if self.etat['black'].get((pi[0]+1+i, pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2 or pi[0]+i > 7:
                break
            if not self.etat['black'].get((pi[0]+1+i, pi[1]-i-1)):
                ens.add((pi[0]+1+i, pi[1]-1-i))
            if self.etat['white'].get((pi[0]+1+i, pi[1]-i-1)):
                break
            if self.etat['black'].get((pi[0]+1+i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]-i < 2:
                break
            if not self.etat['black'].get((pi[0]-i-1, pi[1]-i-1)):
                ens.add((pi[0]-i-1, pi[1]-i-1))
            if self.etat['white'].get((pi[0]-i-1, pi[1]-i-1)):
                break
            if self.etat['black'].get((pi[0]-1-i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]+i > 7:
                break
            if not self.etat['black'].get((pi[0]-i-1, pi[1]+i+1)):
                ens.add((pi[0]-i-1, pi[1]+i+1))
            if self.etat['white'].get((pi[0]-i-1, pi[1]+i+1)):
                break
            if self.etat['black'].get((pi[0]-i-1, pi[1]+i+1)):
                break
        if pf in ens:
            self.etat['black'].pop(pi)
            self.etat['black'][pf] = 'F'
            if self.etat['white'].get(pf):
                self.etat['white'].pop(pf)
        else:
          raise EchecError('le coup est invalide')
    
    def deplacer_fouW(self, pi, pf):
        ens = {0}
        for i in range(8):
            if pi[1]+i > 7 or pi[0]+i > 7 :
                break
            if not self.etat['white'].get((pi[0]+i+1, pi[1]+i+1)):
                ens.add((pi[0]+1+i, pi[1]+1+i))
            if self.etat['black'].get((pi[0]+1+i, pi[1]+i+1)):
                break
            if self.etat['white'].get((pi[0]+1+i, pi[1]+i+1)):
                break
        for i in range(8):
            if pi[1]-i < 2 or pi[0]+i > 7:
                break
            if not self.etat['white'].get((pi[0]+1+i, pi[1]-i-1)):
                ens.add((pi[0]+1+i, pi[1]-1-i))
            if self.etat['black'].get((pi[0]+1+i, pi[1]-i-1)):
                break
            if self.etat['white'].get((pi[0]+1+i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]-i < 2:
                break
            if not self.etat['white'].get((pi[0]-i-1, pi[1]-i-1)):
                 ens.add((pi[0]-i-1, pi[1]-i-1))
            if self.etat['black'].get((pi[0]-i-1, pi[1]-i-1)):
                break
            if self.etat['white'].get((pi[0]-1-i, pi[1]-i-1)):
                break
        for i in range(8):
            if pi[0]-i < 2 or pi[1]+i > 7:
                break
            if not self.etat['white'].get((pi[0]-i-1, pi[1]+i+1)):
                 ens.add((pi[0]-i-1, pi[1]+i+1))
            if self.etat['black'].get((pi[0]-i-1, pi[1]+i+1)):
                break
            if self.etat['white'].get((pi[0]-1-i, pi[1]+i+1)):
                break
        if pf in ens:
            self.etat['white'].pop(pi)
            self.etat['white'][pf] = 'F'   
            if self.etat['black'].get(pf):
                self.etat['black'].pop(pf)
        else:
          raise EchecError('le coup est invalide')
    
    def deplacer_dameB(self, pi, pf):
        try:
            self.deplacer_tourB(pi, pf)
            self.etat['black'][pf] = 'Q'
        except EchecError:
            try:
                self.deplacer_fouB(pi, pf)
                self.etat['black'][pf] = 'Q'
            except EchecError:
                raise EchecError('le coup est invalide') 
    
    def deplacer_dameW(self, pi, pf):
        try:
            self.deplacer_tourW(pi, pf)
            self.etat['white'][pf] = 'Q'
        except EchecError:
            try:
                self.deplacer_fouW(pi, pf)
                self.etat['white'][pf] = 'Q'
            except EchecError:
                raise EchecError('le coup est invalide') 
# a = echec()
# for i in range(30):
#     a.stratB3()
#     print(a)
# while True:
#     try:
#         a.stratW3()
#         print(a)
#         a.stratB3()
#         print(a)
#     except EchecError as err:
#         print(err)
#         break