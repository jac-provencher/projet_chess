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
        if not isinstance(player1, str) or not isinstance(player2, str):
            raise ChessError("Les deux joueurs doivent être des chaines de caractères.")

        self.player1 = player1
        self.player2 = player2

        self.etat = {
                'black': {
                    (1, 7): ['P', [], []], (2, 7): ['P', [], []], (3, 7): ['P', [], []], (4, 7): ['P', [], []],
                    (5, 7): ['P', [], []], (6, 7): ['P', [], []], (7, 7): ['P', [], []], (8, 7): ['P', [], []],
                    (1, 8): ['T', [], []], (8, 8): ['T', [], []], (2, 8): ['C', [], []], (7, 8): ['C', [], []],
                    (3, 8): ['F', [], []], (6, 8): ['F', [], []], (5, 8): ['K', [], []], (4, 8): ['Q', [], []]
                        },
                'white': {
                    (1, 2): ['P', [], []], (2, 2): ['P', [], []], (3, 2): ['P', [], []], (4, 2): ['P', [], []],
                    (5, 2): ['P', [], []], (6, 2): ['P', [], []], (7, 2): ['P', [], []], (8, 2): ['P', [], []],
                    (1, 1): ['T', [], []], (8, 1): ['T', [], []], (2, 1): ['C', [], []], (7, 1): ['C', [], []],
                    (3, 1): ['F', [], []], (6, 1): ['F', [], []], (4, 1): ['K', [], []], (5, 1): ['Q', [], []]
                        }
                    }

        self.pieces = {
                    'black': {'P': '♙', 'C': '♘', 'F': '♗', 'Q': '♕', 'K': '♔', 'T': '♖'},
                    'white': {'P': '♟', 'C': '♞', 'F': '♝', 'Q': '♛', 'K': '♚', 'T': '♜'}
                    }

        self.oppo = {'black':'white', 'white':'black'}

    def __str__(self):

        # Construction de l'équiquier
        d1 = [[' ' for _ in range(35)] for _ in range(15)]
        for i, ligne in enumerate(d1[::2]):
            ligne[0] = str(8 - i)
            for n in range(4, 35, 4):
                ligne[n] = '.'
        d2 = []
        for ligne in d1:
            ligne[2] = ligne[34] = '┃'
            d2 += ligne + ['\n']

        # Position des joueurs
        for color, dico in self.state().items():
            for position, info in dico.items():
                x, y = position
                d2[36*(16-2*y)+4*x] = self.pieces[color][info[0]]

        # Affiche de l'échiquier
        title = "Chessgame"
        debut = ['   ', '━'*31, '\n']
        end = ['━━┃', '━'*31, '\n', '  ┃ ', '   '.join(str(n) for n in range(1, 9))]

        return f"{title:^37}" + '\n' + ''.join(debut + d2 + end) + '\n' + \
        f"White: {self.player1}" + '\n' + f"Black: {self.player2}"

    def move(self, color, pos1, pos2):
        """
        Méthode permettant de déplacer le pion 'piece' situé à
        la position pos1 vers la position pos2.
        :raise ChessError: si aucun pion ne se trouve à la position pos1
        :raise ChessError: si pos2 n'est pas un coup valide pour le pion 'piece'
        """
        # Traitement d'erreurs
        for x, y in [pos1, pos2]:
            if not isinstance(x, int) or not isinstance(y, int):
                raise ChessError("Veuillez entrer que des nombres entiers.")

        # pos1 n'est liée à aucun pion sur l'échiquier
        if pos1 not in self.__positions()['pions'][color]:
            raise ChessError("Aucun pion ne peut être déplacer.")

        # Déplacement invalide
        elif pos2 not in self.state()[color][pos1][1]:
            raise ChessError("Ce coup est invalide pour ce pion.")

        # Déplacement du pion 'piece'
        piece = self.etat[color][pos1][0]
        del self.etat[color][pos1]
        self.etat[color][pos2] = [piece, [], []]

    def autoplay(self, color):
        """
        Méthode permettant de jouer un coup valide pour
        l'état actuelle de jeu (pour le moment, ne jouer qu'un coup valide
        pas nécessairement un bon coup)
        :raise ChessError: si la couleur est ni 'black' ni 'white'
        """
        # Traitement d'erreur
        if color not in ['black', 'white']:
            raise ChessError("Cette couleur n'existe pas aux échecs.")

        # Choix random parmi l'état de jeu actuelle
        pos, coups = [], []
        for position, info in self.state()[color].items():
            if len(info[1]):
                coups.append(info[1])
                pos.append(position)

        # Déplacement du pion choisi
        coup = random.choice(list(zip(pos, coups)))
        self.move(color, coup[0], random.choice(coup[1]))

    def state(self):
        """
        Méthode permet de retourne l'état de partie actuelle
        :returns: l'état de partie (qui sera utilisé pour __str__, donc sans les coups valides)
        """
        self.__pieces(self.etat)

        return self.etat

    def isCheckmate(self, color):
        """
        Méthode vérifiant si le roi adverse est en position
        d'échec et mat
        Si True,
        :returns: le nom du gagnant
        Autrement,
        :returns: False
        """
        player = {'black':self.player1, 'white':self.player2}
        king_pos = self.__positions()['roi'][color]
        deplacement = self.state()[color][king_pos][1]
        capture = self.state()[color][king_pos][2]

        # Situation d'échec
        if not self.isCheck(color):
            return False

        # Déplacement impossible
        elif deplacement:
            for coup in deplacement:
                if coup not in self.__coup()['capture'][self.oppo[color]]:
                    return False

        # Capture impossible
        elif capture:
            for attack in capture:
                if attack not in self.__coup()['capture'][self.oppo[color]]:
                    return False

        # Sacrifice impossible
        sacrifice = {}
        for color, dico in self.state().items():
            sacrifice[color] = {position:[info[0], info[1]] for position, info in dico.items() if info[1]}
        for pos, info in sacrifice[color].items():
            del self.etat[color][pos]
            for move in info[1]:
                self.etat[color][move] = [info[0], [], []]
                if not self.isCheck(color):
                    return False
                del self.etat[color][move]

        return f"Le gagnant est {player[self.oppo[color]]}!"

    def isCheck(self, color):
        """
        Vérifie si le roi adverse est en position d'échec
        :returns: booleen
        """
        echec = False
        if self.__positions()['roi'][color] in self.__coup()['capture'][self.oppo[color]]:
            echec = True

        return echec

    def eat(self, color, pos1, pos2):
        """
        Méthode permettant de manger un pion adverse placé
        à la position pos2
        :raise ChessError: s'il n'y a aucun pion à la position pos2
        :raise ChessError: si le pion à la position pos2 n'est pas un pion adverse
        """

        # Traitement d'erreurs
        for x, y in [pos1, pos2]:

            # Une des deux coordonnées n'est pas un entier
            if not isinstance(x, int) or not isinstance(y, int):
                raise ChessError("Veuillez entrer que des nombres entiers.")

            # Une des deux coordonnées n'est pas sur l'échiquier
            elif not 1 <= x <= 8 or not 1 <= y <= 8:
                raise ChessError("Une position est hors de l'échiquier.")

        # pos1 n'est pas liée à un pion sur l'échiquier
        if pos1 not in self.__positions()['pions'][color]:
            raise ChessError("Aucun pion ne peut être déplacer.")

        # pos2 n'est pas liée à un pion sur l'échiquier
        elif pos2 not in self.__positions()['pions'][self.oppo[color]]:
            raise ChessError("Aucun pion ne se trouve à la position d'attaque.")

        # pos2 n'est pas un coup_for_eat valide
        elif pos2 not in self.state()[color][pos1][2]:
            raise ChessError("Coup d'attaque invalide.")

        # Suppression du pion à manger
        del self.etat[self.oppo[color]][pos2]

        # Déplacement du pion
        piece = self.etat[color][pos1][0]
        del self.etat[color][pos1]
        self.etat[color][pos2] = [piece, [], []]

    def __positions(self):
        """
        :returns: dico de la position des pions de chaque couleur
        et les positions libres/vides
        """

        # Positions des rois et des autres pions
        coord, king = {}, {}
        for team, positions in self.etat.items():
            coord[team] = {position for position in positions.keys()}
            for position, info in positions.items():
                if info[0] == 'K':
                    king[team] = position

        # Cases libres/vides
        positions_restantes = {(x, y) for x in range(1, 9) for y in range(1, 9)} - (coord['black']|coord['white'])

        return {'pions':coord, 'libres':positions_restantes, 'roi':king}

    def __coup(self):
        """
        :returns: dico des deplacements et des captures possibles
        pour chaque couleur
        """
        move, eat = {}, {}
        for color, dico in self.state().items():
            move[color], eat[color] = set(), set()
            for info in dico.values():
                # Positions de déplacement
                for coup in info[1]:
                    move[color].add(coup)
                # Positions de capture
                for pos in info[2]:
                    eat[color].add(pos)

        return {'deplacement':move, 'capture':eat}

    def __pieces(self, etat):

        # Mise à jour des coups valides
        pos_free = self.__positions()['libres']
        pos_pions = self.__positions()['pions']

        for color, positions in etat.items():
            for position, liste in positions.items():
                x, y = position

                if liste[0] == 'P':

                    if color == 'black':
                        # Pion noir est sur la ligne de départ
                        if y == 7:
                            coup_valide = [(x, y-i) for i in range(1, 3)]
                            for i, coord in enumerate(coup_valide):
                                if coord not in pos_free:
                                    del coup_valide[i:]
                                    break
                            etat['black'][position][1] = coup_valide

                        # Pion noir n'est pas sur la ligne de départ et peut avancer
                        elif (x, y-1) in pos_free:
                            etat['black'][position][1] = [(x, y-1)]

                        # Pion noir ne peut pas avancer
                        else:
                            etat['black'][position][1] = []

                        # Positions que le pion noir peut aller pour bouffer
                        coup_for_eat = []
                        for pos in [(x+1, y-1), (x-1, y-1)]:
                            if pos in pos_pions[self.oppo[color]]:
                                coup_for_eat.append(pos)
                        etat['black'][position][2] = coup_for_eat

                    elif color == 'white':
                        # Pion blanc est sur la ligne de départ
                        if y == 2:
                            coup_valide = [(x, y+i) for i in range(1, 3)]
                            for i, coord in enumerate(coup_valide):
                                if coord not in pos_free:
                                    del coup_valide[i:]
                                    break
                            etat['white'][position][1] = coup_valide

                        # Pion blanc n'est pas sur la ligne de départ et peut avancer
                        elif (x, y+1) in pos_free:
                            etat['white'][position][1] = [(x, y+1)]

                        # Pion blanc ne peut pas avancer
                        else:
                            etat['white'][position][1] = []

                        # Positions que le pion blanc peut aller pour bouffer
                        coup_for_eat = []
                        for pos in [(x-1, y+1), (x+1, y+1)]:
                            if pos in pos_pions[self.oppo[color]]:
                                coup_for_eat.append(pos)
                        etat['white'][position][2] = coup_for_eat

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

                        # Coups valides de déplacement
                        etat[color][position][1] = list(set(coup_valide[liste[0]]) & pos_free)
                        # Coups valides pour bouffer
                        etat[color][position][2] = list(set(coup_valide[liste[0]]) & pos_pions[self.oppo[color]])

                    # Positions longues portées
                    else:
                        coup_for_eat = []

                        for i, direction in enumerate(coup_valide[liste[0]]):
                            for n, coord in enumerate(direction):
                                if coord not in pos_free:
                                    del coup_valide[liste[0]][i][n:]
                                    x, y = coord
                                    if coord in pos_pions[self.oppo[color]]:
                                        coup_for_eat.append(coord)
                                    break

                        moves = []
                        for direction in coup_valide[liste[0]]:
                            moves += direction

                        # Coups valides pour déplacement
                        etat[color][position][1] = moves
                        # Coups valides pour bouffer
                        etat[color][position][2] = coup_for_eat

def etat(state):
    total = set()
    for color, info in state.items():
        print(f"{color}:")
        for position, liste in info.items():
            print(f"{liste[0]}:{position}  moves = {liste[1]}, to eat = {liste[2]}")
            total.add(position)
    print(f"{len(total)} pions sur l'échiquier")

def autogame(name1, name2, nb_coup=0):
    game = Chess(name1, name2)
    etat(game.state())
    print(game)

    if nb_coup > 0:
        count = 0
        while count < nb_coup:
            game.autoplay('white')
            etat(game.state())
            # print(game.state())
            print(game)
            game.autoplay('black')
            etat(game.state())
            # print(game.state())
            print(game)
            count += 1

    else:
        while True:
            game.autoplay('white')
            # etat(game.state())
            print(game)
            if game.isCheckmate('black'):
                print(game.isCheckmate('black'))
                break
            game.autoplay('black')
            # etat(game.state())
            print(game)
            if game.isCheckmate('white'):
                print(game.isCheckmate('white'))
                break

def handgame(name1, name2='Robot'):
    game = Chess(name1, name2)
    print(game)
    # while not game.isCheckmate():
    while True:
        action = input("Type de coup (m, e): ")
        pos1 = input("Position du pion xy: ")
        pos2 = input("Position de déplacement xy: ")
        try:
            if action == 'm':
                game.move('white', (int(pos1[0]), int(pos1[1])), (int(pos2[0]), int(pos2[1])))
            elif action == 'e':
                game.eat('white', (int(pos1[0]), int(pos1[1])), (int(pos2[0]), int(pos2[1])))
            if game.isCheckmate('black'):
                print(game.isCheckmate('black'))
            print(game)

            game.autoplay('black')
            print(game)
            if game.isCheckmate('white'):
                print(game.isCheckmate('white'))

        except ChessError as err:
            print(err)
            print(game)
        except Exception:
            print(game)
            print("Coup invalide, réessayer.")

handgame('Jacob')
# autogame('Jacob', 'Pascal', nb_coup=50)
