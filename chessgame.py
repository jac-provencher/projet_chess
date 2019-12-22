
class ChessError(Exception):
    """
    Crée un nouveau type d'erreur, soit ChessError.
    """

class Chess:

    def __init__(self, player1, player2):
        """
        Initialiser un nouvel état de partie
        Accepte en argument le nom de deux joueurs en str

        :raise ChessError: si un des deux joueurs n'est pas une str
        """
        self.player1 = player1
        self.player2 = player2
        self.etat = {
                'black': {
                    (1, 7): ['P', []], (2, 7): ['P', []], (3, 7): ['P', []], (4, 7): ['P', []],
                    (5, 7): ['P', []], (6, 7): ['P', []], (7, 7): ['P', []], (8, 7): ['P', []],
                    (1, 8): ['T', []], (8, 8): ['T', []], (2, 8): ['C', []], (7, 8): ['C', []],
                    (3, 8): ['F', []], (6, 8): ['F', []], (5, 8): ['K', []], (4, 8): ['Q', []]
                        },
                'white': {
                    (1, 2): ['P', []], (2, 2): ['P', []], (3, 2): ['P', []], (4, 2): ['P', []],
                    (5, 2): ['P', []], (6, 2): ['P', []], (7, 2): ['P', []], (8, 2): ['P', []],
                    (1, 1): ['T', []], (8, 1): ['T', []], (2, 1): ['C', []], (7, 1): ['C', []],
                    (3, 1): ['F', []], (6, 1): ['F', []], (4, 1): ['K', []], (5, 1): ['Q', []]
                        }
                    }

    def __str__(self):
        """
        :returns: la chaine de caractère représentant l'état de jeu actuelle
        """
        # Construction du damier
        d1 = [[' ' for _ in range(35)] for _ in range(15)]
        for i, ligne in enumerate(d1[::2]):
            ligne[0] = str(8 - i)
            for n in range(4, 35, 4):
                ligne[n] = '.'
        d2 = []
        for ligne in d1:
            ligne[2] = ligne[34] = '|'
            d2 += ligne + ['\n']

        # Position des joueurs
        for positions in self.state().values():
            for pos, liste in positions.items():
                x, y = pos
                d2[36*(16-2*y)+4*x] = liste[0]

        # Affiche du damier
        title = "Chessgame"
        debut = ['   ', '-'*31, '\n']
        end = ['--|', '-'*31, '\n', '  | ', '   '.join(str(n) for n in range(1, 9))]

        return f"{title:^37}" + '\n' + ''.join(debut + d2 + end) + '\n' + f"White: {self.player1}" + '\n' + f"Black: {self.player2}"

    def move(self, color, piece, pos1, pos2):
        """
        Méthode permettant de déplacer le pion 'piece' situé à
        la position pos1 vers la position pos2.

        :Argument: une color, une piece, sa position (pos1) et sa nouvelle position (pos2)

        :raise ChessError: si aucun pion ne se trouve à la position pos1
        :raise ChessError: si pos2 n'est pas un coup valide pour le pion 'piece'

        :modifie: l'état de partie
        """
        positions_pions = [[position for position in positions.keys()] for positions in self.state().values()]
        positions_pions = positions_pions[0] + positions_pions[1]
        coup_valide = self.state()[color][pos1][1]

        # Traitement d'erreurs
        if color not in ['black', 'white']:
            raise ChessError("Cette couleur n'existe pas aux échecs.")
        elif piece not in ['P', 'K', 'F', 'Q', 'C', 'T']:
            raise ChessError("Ce type de pion n'existe pas")
        elif pos1 not in positions_pions:
            raise ChessError("Aucun pion ne se trouve à cette position.")
        elif pos2 not in coup_valide:
            raise ChessError("Ce déplacement est invalide.")

        # Appel de la bonne méthode
        if piece == 'P':
            self.__pion(color=color, pos1=pos1, pos2=pos2, action='move')
        elif piece == 'K':
            self.__roi(color=color, pos1=pos1, pos2=pos2, action='move')
        elif piece == 'F':
            self.__fou(color=color, pos1=pos1, pos2=pos2, action='move')
        elif piece == 'Q':
            self.__reine(color=color, pos1=pos1, pos2=pos2, action='move')
        elif piece == 'C':
            self.__cheval(color=color, pos1=pos1, pos2=pos2, action='move')
        elif piece == 'T':
            self.__tour(color=color, pos1=pos1, pos2=pos2, action='move')

    def play(self, color):
        """
        Méthode permettant de jouer un coup valide pour
        l'état actuelle de jeu (pour le moment, ne jouer qu'un coup valide
        pas nécessairement un bon coup)

        :Argument: color

        :modifie: l'état de partie
        """

    def state(self):
        """
        Méthode permet de retourne l'état de partie actuelle

        :returns: l'état de partie (qui sera utilisé pour __str__, donc sans les coups valides)

        Note: l'état de partie est un rassemblement des état de jeu
        de chaque type de pion. Il faudra aller piger les bons éléments
        dans le dictionnaire retourné par les méthodes dans la class Piece
        des pions.
        """
        self.__pion()
        self.__tour()
        self.__roi()
        self.__reine()
        self.__cheval()
        self.__fou()

        return self.etat

    def checkmate(self, color):
        """
        Méthode vérifiant si le roi adverse est en position
        d'échec et mat

        :Argument: color (le roi adverse est le roi de inverse à 'color')

        Si True,
        :returns: le nom du gagnant

        Autrement,
        :returns: False
        """

    def check(self, color):
        """
        Vérifie si le roi adverse est en position d'échec

        :Argument: color (le roi adverse est le roi de inverse à 'color')

        :returns: booleen
        """

    def eat(self, color, piece, pos1, pos2):
        """
        Méthode permettant de manger un pion adverse placé
        à la position pos2

        :Argument: piece, position de 'piece' (pos1), nouvelle position (pos2)

        :raise ChessError: s'il n'y a aucun pion à la position pos2
        :raise ChessError: si le pion à la position pos2 n'est pas un pion adverse

        Pour déplacer le pion, faire appel à la méthode move avec action='move'
        Pour supprimer le pion, faire appel à la méthode du pion à supprimer avec action='del'.
        Ce pion est celui placé à la position 'pos2'
        """
        positions_pions = [[position for position in positions.keys()] for positions in self.state().values()]
        positions_pions = positions_pions[0] + positions_pions[1]
        couleur_adverse = {'black':'white', 'white':'black'}

        # Traitement d'erreurs
        if pos2 not in positions_pions:
            raise ChessError("Il n'y a aucun pion à bouffer à cette position")
        elif pos2 not in self.state()[couleur_adverse[color]].keys():
            raise ChessError("Ce pion n'est pas ennemi.")

        # Déplacement
        self.move(color, piece, pos1, pos2)

        # Suppression du pion à manger
        oppo_color = couleur_adverse[color]
        pion_adverse = self.state()[oppo_color][pos2][0]

        if pion_adverse == 'P':
            self.__pion(color=oppo_color, pos2=pos2, action='del')
        elif pion_adverse == 'K':
            self.__roi(color=oppo_color, pos2=pos2, action='del')
        elif pion_adverse == 'F':
            self.__fou(color=oppo_color, pos2=pos2, action='del')
        elif pion_adverse == 'Q':
            self.__reine(color=oppo_color, pos2=pos2, action='del')
        elif pion_adverse == 'C':
            self.__cheval(color=oppo_color, pos2=pos2, action='del')
        elif pion_adverse == 'T':
            self.__tour(color=oppo_color, pos2=pos2, action='del')

    def __pion(self, color=None, pos1=None, pos2=None, action=None):

        # Déplacement du pion
        if color and pos1 and pos2 is not None and action == 'move':
            del self.etat[color][pos1]
            self.etat[color][pos2] = ['P', []]

        # Suppression du pion
        elif color and pos2 is not None and action == 'del':
            del self.etat[color][pos2]

        # Mise à jour des coups valides pour chaque pion
        for color, positions in self.etat.items():
            for position, liste in positions.items():
                if liste[0] == 'P':
                    coup_valide = []
                    x, y = position
                    # Revoir pour lorsqu'un pion peut manger un pion adverse!
                    # ATTENTION! Si un pion est directement devant un pion, le pion ne
                    # peut pas avancer.
                    if color == 'black':
                        if y == 7:
                            coup_valide.append((x, y-2))
                        coup_valide.append((x, y-1))
                    else:
                        if y == 2:
                            coup_valide.append((x, y+2))
                        coup_valide.append((x, y+1))

                    self.etat[color][position][1] += coup_valide

    def __fou(self, color=None, pos1=None, pos2=None, action=None):

        # Déplacement d'un fou
        if color and pos1 and pos2 is not None and action == 'move':
            del self.etat[color][pos1]
            self.etat[color][pos2] = ['F', []]

        # Suppression d'un fou
        elif color and pos2 is not None and action == 'del':
            del self.etat[color][pos2]

        # Mise à jour des coups valides pour chaque fou
        coord = [[position for position in positions.keys()] for positions in self.etat.values()]
        positions_restantes = {(x, y) for x in range(1, 9) for y in range(1, 9)} - set(coord[0]+ coord[1])

        for color, positions in self.etat.items():
            for position, liste in positions.items():
                if liste[0] == 'F':
                    x, y = position
                    coup_valide = [
                                    [(x+i, y+i) for i in range(1, 9)], [(x+i, y-i) for i in range(1, 9)],
                                    [(x-i, y+i) for i in range(1, 9)], [(x-i, y-i) for i in range(1, 9)]
                                    ]
                    for i, direction in enumerate(coup_valide):
                        for n, coord in enumerate(direction):
                            if coord not in positions_restantes:
                                del coup_valide[i][n:]
                                break
                    for direction in coup_valide:
                        self.etat[color][position][1] += direction

    def __roi(self, color=None, pos1=None, pos2=None, action=None):

        # Déplacement d'un roi
        if color and pos1 and pos2 is not None and action == 'move':
            del self.etat[color][pos1]
            self.etat[color][pos2] = ['K', []]

        # Suppression d'un roi
        elif color and pos2 is not None and action == 'del':
            del self.etat[color][pos2]

        # Mise à jour des coups valides pour chaque roi
        coord = [[position for position in positions.keys()] for positions in self.etat.values()]
        positions_restantes = {(x, y) for x in range(1, 9) for y in range(1, 9)} - set(coord[0]+ coord[1])

        for color, positions in self.etat.items():
            for position, liste in positions.items():
                if liste[0] == 'K':
                    x, y = position
                    coup_valide = [(x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y-1), (x-1, y-1), (x-1, y)]
                    for coord in coup_valide:
                        if coord in positions_restantes:
                            self.etat[color][position][1].append(coord)

    def __reine(self, color=None, pos1=None, pos2=None, action=None):

        # Déplacement d'une reine
        if color and pos1 and pos2 is not None and action == 'move':
            del self.etat[color][pos1]
            self.etat[color][pos2] = ['Q', []]

        # Suppression d'une reine
        elif color and pos2 is not None and action == 'del':
            del self.etat[color][pos2]

        # Mise à jour des coups valides pour chaque reine
        coord = [[position for position in positions.keys()] for positions in self.etat.values()]
        positions_restantes = {(x, y) for x in range(1, 9) for y in range(1, 9)} - set(coord[0]+ coord[1])

        for color, positions in self.etat.items():
            for position, liste in positions.items():
                if liste[0] == 'Q':
                    x, y = position
                    coup_valide = [
                                    [(x+i, y+i) for i in range(1, 9)], [(x+i, y-i) for i in range(1, 9)],
                                    [(x-i, y+i) for i in range(1, 9)], [(x-i, y-i) for i in range(1, 9)],
                                    [(x, y+i) for i in range(1, 9)], [(x+i, y) for i in range(1, 9)],
                                    [(x, y-i) for i in range(1, 9)], [(x-i, y) for i in range(1, 9)]
                                    ]
                    for i, direction in enumerate(coup_valide):
                        for n, coord in enumerate(direction):
                            if coord not in positions_restantes:
                                del coup_valide[i][n:]
                                break
                    for direction in coup_valide:
                        self.etat[color][position][1] += direction

    def __tour(self, color=None, pos1=None, pos2=None, action=None):

        # Déplacement d'une tour
        if color and pos1 and pos2 is not None and action == 'move':
            del self.etat[color][pos1]
            self.etat[color][pos2] = ['T', []]

        # Suppression d'une tour
        elif color and pos2 is not None and action == 'del':
            del self.etat[color][pos2]

        # Mise à jour des coups valides pour chaque tour
        coord = [[position for position in positions.keys()] for positions in self.etat.values()]
        positions_restantes = {(x, y) for x in range(1, 9) for y in range(1, 9)} - set(coord[0]+ coord[1])

        for color, positions in self.etat.items():
            for position, liste in positions.items():
                if liste[0] == 'T':
                    x, y = position
                    coup_valide = [
                                    [(x, y+i) for i in range(1, 9)], [(x+i, y) for i in range(1, 9)],
                                    [(x, y-i) for i in range(1, 9)], [(x-i, y) for i in range(1, 9)]
                                    ]
                    for i, direction in enumerate(coup_valide):
                        for n, coord in enumerate(direction):
                            if coord not in positions_restantes:
                                del coup_valide[i][n:]
                                break
                    for direction in coup_valide:
                        self.etat[color][position][1] += direction

    def __cheval(self, color=None, pos1=None, pos2=None, action=None):

        # Déplacement d'un cheval
        if color and pos1 and pos2 is not None and action == 'move':
            del self.etat[color][pos1]
            self.etat[color][pos2] = ['C', []]

        # Suppression d'un cheval
        elif color and pos2 is not None and action == 'del':
            del self.etat[color][pos2]

        # Mise à jour des positions pour chaque cheval
        coord = [[position for position in positions.keys()] for positions in self.etat.values()]
        positions_restantes = {(x, y) for x in range(1, 9) for y in range(1, 9)} - set(coord[0]+ coord[1])

        for color, positions in self.etat.items():
            for position, liste in positions.items():
                if liste[0] == 'C':
                    x, y = position
                    coup_valide = [(x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1),
                                (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2)]
                    for coord in coup_valide:
                        if coord in positions_restantes:
                            self.etat[color][position][1].append(coord)

        """
        Permet de supprimer un pion de l'état actuelle de jeu

        :Argument: pos (à supprimer)

        :modifie: l'état de partie
        """


game = Chess('Jacob', 'Pascal')
print(game.state())
print(game)
game.move('white', 'P', (1, 2), (1, 4))
print(game)
game.move('white', 'P', (1, 4), (1, 5))
game.move('white', 'P', (1, 5), (1, 6))
game.eat('black', 'C', (2, 8), (1, 6))
game.move('black', 'C', (1, 6), (2, 4))
print(game)
