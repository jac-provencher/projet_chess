import random


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
        :raise ChessError: si aucun pion ne se trouve à la position pos1
        :raise ChessError: si pos2 n'est pas un coup valide pour le pion 'piece'
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

        # Déplacement du pion 'piece'
        del self.etat[color][pos1]
        self.etat[color][pos2] = [piece, []]

    def autoplay(self, color):
        """
        Méthode permettant de jouer un coup valide pour
        l'état actuelle de jeu (pour le moment, ne jouer qu'un coup valide
        pas nécessairement un bon coup)
        :raise ChessError: si la couleur est ni 'black' ni 'white'
        """
        if color not in ['black', 'white']:
            raise ChessError("Cette couleur n'existe pas aux échecs.")

        # Choix random parmi l'état de jeu actuelle
        piece, pos, coups = [], [], []
        for position, info in self.state()[color].items():
            if len(info[1]):
                piece.append(info[0])
                coups.append(info[1])
                pos.append(position)

        # Déplacement du pion choisi
        coup = random.choice(list(zip(piece, pos, coups)))
        self.move(color, coup[0], coup[1], random.choice(coup[2]))

    def state(self):
        """
        Méthode permet de retourne l'état de partie actuelle
        :returns: l'état de partie (qui sera utilisé pour __str__, donc sans les coups valides)
        """
        self.__pieces()

        return self.etat

    def checkmate(self):
        """
        Méthode vérifiant si le roi adverse est en position
        d'échec et mat
        Si True,
        :returns: le nom du gagnant
        Autrement,
        :returns: False
        """
        player = {'black':self.player1, 'white':self.player2}

        # Coups valides pour chaque couleur
        coup_valide = {'white':set(), 'black':set()}
        oppo = {'black':'white', 'white':'black'}

        for color in self.state().keys():
            for coups in [coord[1] for coord in self.state()[color].values() if coord[1]]:
                for coup in coups:
                    coup_valide[color].add(coup)

        for color, info in self.state().items():
            for piece, coups in info.values():
                if piece == 'K':
                    for coord in set(coups):
                        if coord not in coup_valide[oppo[color]]:
                            return False
                        else:
                            return f"Le gagnant est {player[color]}!"

        return False

    def check(self):
        """
        Vérifie si le roi adverse est en position d'échec
        :returns: booleen
        """

    def eat(self, color, piece, pos1, pos2):
        """
        Méthode permettant de manger un pion adverse placé
        à la position pos2
        :raise ChessError: s'il n'y a aucun pion à la position pos2
        :raise ChessError: si le pion à la position pos2 n'est pas un pion adverse
        """
        positions_pions = [[position for position in positions.keys()] for positions in self.state().values()]
        positions_pions = positions_pions[0] + positions_pions[1]
        couleur_adverse = {'black':'white', 'white':'black'}

        # Traitement d'erreurs
        if pos2 not in positions_pions:
            raise ChessError("Il n'y a aucun pion à bouffer à cette position")
        elif pos2 not in self.state()[couleur_adverse[color]].keys():
            raise ChessError("Ce pion n'est pas ennemi.")

        # Suppression du pion à manger
        oppo_color = couleur_adverse[color]
        del self.etat[oppo_color][pos2]

        # Déplacement
        self.move(color, piece, pos1, pos2)

    def __pieces(self):

        # Mise à jour des coups valides
        coord = [[position for position in positions.keys()] for positions in self.etat.values()]
        positions_restantes = {(x, y) for x in range(1, 9) for y in range(1, 9)} - set(coord[0] + coord[1])

        for color, positions in self.etat.items():
            for position, liste in positions.items():
                x, y = position

                if liste[0] == 'P':

                    if color == 'black':
                        if y == 7:
                            coup_valide = [(x, y-i) for i in range(1, 3)]
                            for i, coord in enumerate(coup_valide):
                                if coord not in positions_restantes:
                                    del coup_valide[i:]
                                    break
                            self.etat['black'][position][1] = coup_valide

                        elif (x, y-1) in positions_restantes:
                            self.etat['black'][position][1] = [(x, y-1)]

                        else:
                            self.etat['black'][position][1] = []

                    elif color == 'white':
                        if y == 2:
                            coup_valide = [(x, y+i) for i in range(1, 3)]
                            for i, coord in enumerate(coup_valide):
                                if coord not in positions_restantes:
                                    del coup_valide[i:]
                                    break
                            self.etat['white'][position][1] = coup_valide

                        elif (x, y+1) in positions_restantes:
                            self.etat['white'][position][1] = [(x, y+1)]

                        else:
                            self.etat['white'][position][1] = []

                else:
                    # Revoir pour simplifier les 'for i in range(1, 9)'
                    coup_valide = {
                                    'K':[
                                            (x, y+1), (x, y-1), (x+1, y), (x-1, y),
                                            (x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1)
                                        ],
                                    'Q':[
                                            [(x, y+i) for i in range(1, 9)], [(x, y-i) for i in range(1, 9)],
                                            [(x+i, y) for i in range(1, 9)], [(x-i, y) for i in range(1, 9)],
                                            [(x+i, y+i) for i in range(1, 9)], [(x-i, y+i) for i in range(1, 9)],
                                            [(x+i, y-i) for i in range(1, 9)], [(x-i, y-i) for i in range(1, 9)]
                                        ],
                                    'F':[
                                            [(x+i, y+i) for i in range(1, 9)], [(x+i, y-i) for i in range(1, 9)],
                                            [(x-i, y+i) for i in range(1, 9)], [(x-i, y-i) for i in range(1, 9)]
                                        ],
                                    'T':[
                                            [(x+i, y) for i in range(1, 9)], [(x-i, y) for i in range(1, 9)],
                                            [(x, y+i) for i in range(1, 9)], [(x, y-i) for i in range(1, 9)]
                                        ],
                                    'C':[
                                            (x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1),
                                            (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2)
                                        ]
                                    }

                    # Positions fixes
                    if liste[0] in ['K', 'C']:
                        self.etat[color][position][1] = list(set(coup_valide[liste[0]]) & positions_restantes)

                    # Positions longues portées
                    else:
                        for i, direction in enumerate(coup_valide[liste[0]]):
                            for n, coord in enumerate(direction):
                                if coord not in positions_restantes:
                                    del coup_valide[liste[0]][i][n:]
                                    break
                        coup = []
                        for direction in coup_valide[liste[0]]:
                            coup += direction

                        self.etat[color][position][1] = coup

def etat(state):
    total = set()
    for color, info in state.items():
        print(f"{color}:")
        for position, liste in info.items():
            print(f"{liste[0]}:{position}, coups valides = {liste[1]}")
            total.add(position)
    print(f"{len(total)} pions sur l'échiquier")

def autogame(name1, name2, nb_coup=0):
    game = Chess(name1, name2)
    etat(game.state())
    print(game)

    while not game.checkmate():

        game.autoplay('black')
        etat(game.state())
        print(game)
        if game.checkmate():
            print(game.checkmate())
            break

        game.autoplay('white')
        etat(game.state())
        print(game)
        if game.checkmate():
            print(game.checkmate())
            break

def handgame(name1, name2='Robot'):
    game = Chess(name1, name2)
    print(game)
    # while not game.checkmate():
    count = 0
    while count < 10:
        piece = input("Pion à déplacer (P, F, C, T, K, Q): ")
        pos1 = input("Position du pion xy: ")
        pos2 = input("Position de déplacement xy: ")
        try:
            game.move('white', piece, (int(pos1[0]), int(pos1[1])), (int(pos2[0]), int(pos2[1])))
            print(game)
            game.autoplay('black')
            print(game)
        except ChessError as err:
            print(err)
            print(game)

        count += 1

# handgame('Jacob')
autogame('Jacob', 'Pascal')
