import pygame
from more_itertools import tail
from jeu_echec import ChessError, chess
import e20

pygame.init()

class display(e20.echec):

    def __init__(self):
        super().__init__()

        # Caractéristiques de la fenêtre
        pygame.display.set_caption("Échecs")
        self.dx = 104
        self.boardHeight = 696
        self.boardWidth = 696
        self.squareX, self.squareY = self.boardWidth//8, self.boardHeight//8
        self.screen = pygame.display.set_mode((self.boardWidth + self.dx, self.boardHeight))
        self.screen.fill((104, 103, 98))

        # Images
        self.board = pygame.image.load("board.png")
        self.contour = pygame.image.load("contour.png")
        self.circle = pygame.image.load("circle.png")
        self.pieces = {
        'black':
        {
        'P': pygame.image.load("pion_noir.png"),
        'T': pygame.image.load("tour_noir.png"),
        'F': pygame.image.load("fou_noir.png"),
        'Q': pygame.image.load("reine_noir.png"),
        'K': pygame.image.load("roi_noir.png"),
        'C': pygame.image.load("cheval_noir.png")
        },
        'white':
        {
        'P': pygame.image.load("pion_blanc.png"),
        'T': pygame.image.load("tour_blanc.png"),
        'F': pygame.image.load("fou_blanc.png"),
        'Q': pygame.image.load("reine_blanc.png"),
        'K': pygame.image.load("roi_blanc.png"),
        'C': pygame.image.load("cheval_blanc.png")
        }
        }

        # Suivi des clicks
        self.boardClickPosition = [(0, 0), (0, 0)]
        self.cursorPosition = None

        # Fonctions anonymes pour les positions
        self.windowToBoard = lambda position: (position[0]//self.squareX+1, 8-position[1]//self.squareY)
        self.boardToWindow = lambda position: ((position[0]-1)*self.squareX, self.boardHeight - (position[1])*self.squareY)
        self.getLastPositions = lambda positions: list(tail(2, positions))
        self.scaleX = lambda index: self.boardWidth + (index // 5) * ((self.boardWidth // 8) // 3)
        self.scaleY = lambda index: (index % 5) * ((self.boardHeight // 8) // 3) + (self.boardHeight // 8) // 10

        # Boolean values
        self.showMove = True
        self.button = {True: pygame.image.load("on.png"), False: pygame.image.load("off.png")}

        # Importation de sons
        self.moveSound = pygame.mixer.Sound("moveSound.wav")
        self.buttonSound = pygame.mixer.Sound("switchSound.wav")
        self.gagnant = pygame.mixer.Sound("gagnant.wav")
        self.perdant = pygame.mixer.Sound("perdant.wav")
        self.mauvaisc = pygame.mixer.Sound("pourri.wav")
        self.echeccc = pygame.mixer.Sound("echec_1_.wav")
        
        

    def redrawScreen(self, screen):
        """
        Méthode qui regénère la fenêtre à chaque loop
        """
        screen.blit(self.board, (0, 0))

        # Positions des pions
        for color, positions in self.etat.items():
            for position, piece in positions.items():
                pos = self.boardToWindow(position)
                screen.blit(self.pieces[color][piece], pos)

        # # Show les deplacements et attaques valides
        # if self.cursorPosition in self.etat['white'] and self.showMove:
        #     for move in self.moveGenerator(self.etat, 'white', self.cursorPosition):
        #         pos = self.boardToWindow(move)
        #         screen.blit(self.contour, pos)
        #     for attack in self.killGenerator(self.etat, 'white', self.cursorPosition):
        #         pos = self.boardToWindow(attack)
        #         screen.blit(self.circle, pos)

        # Update button state
        position = (self.boardWidth, (self.boardHeight-55)//2)
        screen.blit(self.button[self.showMove], position)

        # # Display les pions mangés
        # for color, pions in self.pawnKilled.items():
        #     for i, pion in enumerate(pions):
        #         pawnScaled = pygame.transform.scale(self.pieces[color][pion], (self.squareX//3, self.squareY//3))
        #         screen.blit(pawnScaled, (self.scaleX(i), self.scaleY(i)))

        pygame.display.update()

    def isClicked(self, button, clickPosition):
        x, y = clickPosition
        middleY, dy = self.boardHeight/2, 59/2
        booleanDico = {
        'showMove': self.boardWidth <= x <= self.boardWidth + self.dx and middleY - dy <= y <= middleY + dy
        }
        if booleanDico['showMove']:
            self.showMove = not self.showMove
            self.buttonSound.play()

partie = display()
running = True
turn = 'black'
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseClick = partie.windowToBoard(event.pos)
            partie.isClicked('showMove', event.pos)
            partie.boardClickPosition.append(mouseClick)
            try:
                partie.checkmatB()
            except:
                partie.perdant.play()
            try:
                pos1, pos2 = partie.getLastPositions(partie.boardClickPosition)
                partie.jouer_coupB(pos1, pos2)
                partie.moveSound.play()
            except e20.EchecError:
                turn = 'black'
                continue
            else:
                turn = 'white'
            if turn == 'white':
                try:
                    partie.redrawScreen(partie.screen)
                    l1 = len(partie.état()['black'])
                    partie.stratW3()
                    partie.moveSound.play()
                    if l1>len(partie.état()['black']):
                        partie.mauvaisc.play()
                    
                    elif partie.check_echecB():
                        partie.echeccc.play()
                    turn = 'black'
                except e20.EchecError:
                    partie.gagnant.play()

                
                

    partie.cursorPosition = partie.windowToBoard(pygame.mouse.get_pos())

    partie.redrawScreen(partie.screen)


pygame.quit()
