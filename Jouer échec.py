import turtle
import Échec as e
import copy
class echecclic(e.echecXX):
    def __init__(self, état=None):
        super().__init__(état)
        n=25
        self.pio = None
        self.cou = None
        self.fond = turtle.Turtle(visible=None)
        self.fond.penup()
        self.fond.speed(0)
        self.fond.goto(9*n, 9*n)
        self.fond.pendown()
        self.fond.pensize(20)
        self.fond.color('brown')
        self.fond.goto(9*n, -9*n)
        self.fond.goto(-9*n, -9*n)
        self.fond.goto(-9*n, 9*n)
        self.fond.goto(9*n, 9*n)
        self.fond.penup()
        self.leave = turtle.Turtle(shape='square')
        self.leave.penup()
        self.leave.shapesize(0.09*n)
        self.leave.color('red')
        self.leave.speed(0)
        self.leave.goto(-9*n + 2*n*(9), -9*n + 2*n*(9))
        self.R = turtle.Turtle(shape='square')
        self.R.penup()
        self.R.shapesize(0.09*n)
        self.R.color('yellow')
        self.R.speed(0)
        self.R.goto(-9*n, -9*n + 2*n*(9))
        self.U = turtle.Turtle(shape='square')
        self.U.penup()
        self.U.shapesize(0.09*n)
        self.U.color('blue')
        self.U.speed(0)
        self.U.goto(-9*n,-9*n)
        self.fond.goto(-9*n + 2*n*(9), -10*n + 2*n*(9))
        self.fond.color('black')
        self.fond.write('X',align='center', font=('arial', 30, 'normal'))
        self.fond.goto(-9*n, -10*n + 2*n*(9))
        self.fond.write('R',align='center', font=('arial', 30, 'normal'))
        self.fond.goto(-9*n, -10*n)
        self.fond.write('U',align='center', font=('arial', 30, 'normal'))
        self.marc.goto(0,-10*n)
        self.etpass = None
         
    def pion(self, x, y):
        self.marc.clear()
        
        if self.check_echecW() is True:
            self.marc.write('Échec!',align='center', font=('arial', 20, 'normal'))
        n=25
        if 8*n<x<10*n and 8*n<y<10*n:
            self.terminerpartie()
        elif -10*n<x<-8*n and -8*n>y>-10*n:
            self.undo()
        elif -10*n<x<-8*n and 8*n<y<10*n:
            self.recommencer()
        elif self.pio == None:
            vx=None
            vy=None
            
            if 0<x<=2*n:
                vx=5
            elif 2*n<x<=2*2*n:
                vx=6
            elif 2*2*n<x<=2*3*n:
                vx=7
            elif 2*3*n<x<=2*4*n:
                vx=8
            elif -2*n<x<=0:
                vx=4
            elif -4*n<x<=-2*n:
                vx=3
            elif -2*3*n<x<=-2*2*n:
                vx=2
            elif -2*4*n<x<=-2*3*n:
                vx=1
            if 0<y<=2*n:
                vy=5
            elif 2*n<y<=2*2*n:
                vy=6
            elif 2*2*n<y<=2*3*n:
                vy=7
            elif 2*3*n<y<=2*4*n:
                vy=8
            elif -2*n<y<=0:
                vy=4
            elif -2*2*n<y<=-2*n:
                vy=3
            elif -2*3*n<y<=-2*2*n:
                vy=2
            elif -2*4*n<y<=-2*3*n:
                vy=1
            self.pio = (vx, vy)
        else:
            vx=None
            vy=None
            if 0<x<=2*n:
                vx=5
            elif 2*n<x<=2*2*n:
                vx=6
            elif 2*2*n<x<=2*3*n:
                vx=7
            elif 2*3*n<x<=2*4*n:
                vx=8
            elif -2*n<x<=0:
                vx=4
            elif -4*n<x<=-2*n:
                vx=3
            elif -2*3*n<x<=-2*2*n:
                vx=2
            elif -2*4*n<x<=-2*3*n:
                vx=1
            if 0<y<=2*n:
                vy=5
            elif 2*n<y<=2*2*n:
                vy=6
            elif 2*2*n<y<=2*3*n:
                vy=7
            elif 2*3*n<y<=2*4*n:
                vy=8
            elif -2*n<y<=0:
                vy=4
            elif -2*2*n<y<=-2*n:
                vy=3
            elif -2*3*n<y<=-2*2*n:
                vy=2
            elif -2*4*n<y<=-2*3*n:
                vy=1
            self.marc.clear()
            if self.pio != None and vy != None and vx != None:
                self.cou = (vx, vy)
                p = 0
                try:
                    self.etatpass()
                    self.jouer_coupB(self.pio, self.cou)
                except e.EchecError as err:
                    self.marc.write(err,align='center', font=('arial', 20, 'normal'))
                    self.pio = None
                    self.cou = None
                    p+=1
                if p != 1:
                    try:
                        self.afficher()
                        self.stratW3()
                        self.afficher()
                        self.checkmatW()
                        if self.check_echecB() is True:
                            if self.checkmatB() is True:
                                self.marc.write('Échec et mat!',align='center', font=('arial', 20, 'normal'))
                            else:
                                self.marc.write('Échec!',align='center', font=('arial', 20, 'normal'))
                    except e.EchecError as err:
                        self.marc.write(err,align='center', font=('arial', 20, 'normal'))
                        
                        
                    
            self.pio = None
            self.cou = None
    
    def etatpass(self):
        self.etpass = copy.deepcopy(self.etat)
    
    def jouer(self):
            self.fen.onscreenclick(btn=1, fun=self.pion)
            self.fen.mainloop()
    
    def terminerpartie(self):
        raise SystemExit
    
    def undo(self):
        self.etat = self.etpass
        self.marc.clear()
        self.afficher()
    
    def recommencer(self):
        self.etat = {'white': {(1, 8): 'T', (8, 8): 'T', (2, 8): 'C', (7, 8): 'C', (3, 8): 'F', (6, 8): 'F', (5, 8): 'Q', (4, 8): 'K', (1, 7): 'P', (2, 7): 'P', (3, 7): 'P', (4, 7): 'P', (5, 7): 'P', (6, 7): 'P', (7, 7): 'P', (8, 7): 'P'}, 'black': {(1, 1): 'T', (8, 1): 'T', (2, 1): 'C', (7, 1): 'C', (3, 1): 'F', (6, 1): 'F', (5, 1): 'Q', (4, 1): 'K', (1, 2): 'P', (2, 2): 'P', (3, 2): 'P', (4, 2): 'P', (5, 2): 'P', (6, 2): 'P', (7, 2): 'P', (8, 2): 'P'}}
        self.marc.clear()
        self.afficher()
a = echecclic()
a.jouer()




