import random
import copy

class ChessError(Exception):
    """
    Crée un nouveau type d'erreur, soit ChessError.
    """

class Gamestate:
    """
    Classe qui donne accès aux informations nécessaires
    aux bons fonctionnement d'une partie d'échecs:
    positions, coups valides et etat de jeu
    """
    def __init__(self):

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
        self.value = {'K':0, 'P':1, 'F':3, 'C':3, 'T':5, 'Q':9}
        self.ate = {'black':[], 'white':[]}
        self.pieces = {
                    'black': {'P': '♙', 'C': '♘', 'F': '♗', 'Q': '♕', 'K': '♔', 'T': '♖'},
                    'white': {'P': '♟', 'C': '♞', 'F': '♝', 'Q': '♛', 'K': '♚', 'T': '♜'}
                    }
        self.oppo = {'black':'white', 'white':'black'}

    def state(self):
        """
        Méthode permet de retourne l'état de partie actuelle
        :returns: l'état de partie (qui sera utilisé pour __str__, donc sans les coups valides)
        """
        return self.valid_generator(self.etat)

    def positions(self):
        """
        :returns: dico de la position des pions de chaque couleur,
        les positions libres/vides, la position des rois et les positions
        de pions 'pion' pour chaque couleur.
        """

        # Positions des rois et des autres pions
        coord, king, pions = {}, {}, {'black':[], 'white':[]}
        for team, positions in self.etat.items():
            coord[team] = {position for position in positions.keys()}
            for position, info in positions.items():
                if info[0] == 'K':
                    king[team] = position
                if info[0] == 'P':
                    pions[team].append(position)

        # Cases libres/vides
        positions_restantes = {(x, y) for x in range(1, 9) for y in range(1, 9)} - (coord['black']|coord['white'])

        return {'pions':coord, 'libres':positions_restantes, 'roi':king, 'pion':pions}

    def coups(self):
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

        return {'deplacement':move, 'all_capture':eat}

    def valid_generator(self, etat):

        # Mise à jour des coups valides
        pos_free = self.positions()['libres']
        pos_pions = self.positions()['pions']

        for color, positions in etat.items():
            for position, liste in positions.items():
                x, y = position

                if liste[0] == 'P':

                    dico_pion = {
                                    'black':[[(x, y-i) for i in range(1, 3)], (x, y-1), [(x+1, y-1), (x-1, y-1)]],
                                    'white':[[(x, y+i) for i in range(1, 3)], (x, y+1), [(x-1, y+1), (x+1, y+1)]]
                                }

                    # Pion est sur la ligne de départ
                    if (color, y) == ('black', 7) or (color, y) == ('white', 2):
                        for i, coord in enumerate(dico_pion[color][0]):
                            if coord not in pos_free:
                                del dico_pion[color][0][i:]
                                break
                        etat[color][position][1] = dico_pion[color][0]

                    # Pion n'est pas sur la ligne de départ et peut avancer
                    elif dico_pion[color][1] in pos_free:
                        etat[color][position][1] = [dico_pion[color][1]]

                    # Pion ne peut pas avancer
                    else:
                        etat[color][position][1] = []

                    # Positions que le pion peut aller pour bouffer
                    coup_for_eat = []
                    for pos in dico_pion[color][2]:
                        if pos in pos_pions[self.oppo[color]]:
                            coup_for_eat.append(pos)
                    etat[color][position][2] = coup_for_eat

                else:
                    # Revoir pour simplifier les 'for i in range(1, 9)'
                    dico_piece = {
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
                        etat[color][position][1] = list(set(dico_piece[liste[0]]) & pos_free)
                        # Coups valides pour bouffer
                        etat[color][position][2] = list(set(dico_piece[liste[0]]) & pos_pions[self.oppo[color]])

                    # Positions longues portées
                    else:

                        coup_for_eat = []
                        for i, direction in enumerate(dico_piece[liste[0]]):
                            for n, coord in enumerate(direction):
                                if coord not in pos_free:
                                    del dico_piece[liste[0]][i][n:]
                                    if coord in pos_pions[self.oppo[color]]:
                                        coup_for_eat.append(coord)
                                    break

                        # Coups valides pour déplacement
                        etat[color][position][1] = [move for direction in dico_piece[liste[0]] for move in direction]
                        # Coups valides pour bouffer
                        etat[color][position][2] = coup_for_eat

        return etat

    def isCheckmate(self, color):
        """
        Méthode vérifiant si le roi adverse est en position
        d'échec et mat
        Si True,
        :returns: le nom du gagnant
        Autrement,
        :returns: False
        """
        player = {'black':'joueur noir', 'white':'joueur blanc'}
        king_pos = self.positions()['roi'][color]
        deplacement, capture = self.state()[color][king_pos][1], self.state()[color][king_pos][2]

        # Situation d'échec
        if not self.isCheck(color):
            return False

        # Déplacement impossible
        elif deplacement:
            for coup in deplacement:
                if coup not in self.coups()['all_capture'][self.oppo[color]]:
                    return False

        # Capture impossible
        # elif capture:
        #     for attack in capture:
        #         if attack not in self.coups()['all_capture'][self.oppo[color]]:
        #             return False

        # Sacrifice impossible
        sacrifice = {}
        for color, dico in self.state().items():
            sacrifice[color] = {position:[info[0], info[1]] for position, info in dico.items() if info[1]}

        for pos, info in sacrifice[color].items():
            del self.etat[color][pos]

            # Essaie pour chaque déplacement et vérif si le roi est en échec
            for move in info[1]:
                self.etat[color][move] = [info[0], [], []]
                if not self.isCheck(color):
                    return False
                del self.etat[color][move]

            self.etat[color][pos] = [info[0], [], []]

        return f"Le gagnant est {player[self.oppo[color]]}!"

    def isCheck(self, color):
        """
        Vérifie si le roi adverse est en position d'échec
        :returns: booleen
        """
        echec = False
        if self.positions()['roi'][color] in self.coups()['all_capture'][self.oppo[color]]:
            echec = True

        return echec

    def exchange_pion(self):
        """
        Méthode qui permet d'échanger le pion par
        le meilleur pion déjà manger
        """
        endline = {'black':1, 'white':8}

        for color, positions in self.positions()['pion'].items():

            # l'équipe 'color' s'est fait mangé au moins un pion
            if self.ate[color]:
                for position in positions:

                    # Si un pion est sur endline
                    if position[1] == endline[color]:
                        piece = self.state()[color][position][0]
                        del self.state()[color][position]

                        # Ajout du pion échangé à la liste des bouffés
                        self.ate[color][self.ate[color].index(max(self.ate[color]))] = (self.value[piece], piece)
                        # Ajout de la pièce échangé sur l'échiquier
                        self.etat[color][position] = [max(self.ate[color])[1], [], []]

class Optimize(Gamestate):
    """
    Classe qui permet de faire l'optimisation du meilleur coup
    en fonction de l'état de jeu courant
    """
    def __init__(self):
        super().__init__()

    def team_value(self, color):
        """
        Retourne la valeur de la couleur demandée.
        Note: prend les valeurs prédéfinies dans self.value
        :returns: int
        """
        return sum(self.value[info[0]] for info in self.etat[color].values())

    def try_kill(self):
        """
        Permet d'avoir le meilleur pion à capturer pour
        chaque pion (si le pion peut manger)
        :returns: dict {cle:valeur} = {pos1:[(pion_value, pos2)]}
        """
        dico_capture = {'black':{}, 'white':{}}

        for color, dico in self.state().items():

            # On va chercher les coup_capture de chaque pion
            for pos1, coups in dico.items():
                if coups[2]:
                    dico_capture[color][pos1] = [coup for coup in coups[2]]

            # On va chercher la valeur de pieces mangées
            for pos1, attacks in dico_capture[color].items():
                for i, attack in enumerate(attacks):
                    piece = self.state()[self.oppo[color]][attack][0]
                    dico_capture[color][pos1][i] = (self.value[piece], attack)

        return dico_capture

    def future_state(self, color, pos1, pos2):
        """
        Méthode qui permet de déplacer conditionnellement
        des pions afin de pouvoir évaluer différentes situations
        :returns: un etat de partie modifié
        """
        gamestate = copy.deepcopy(self.etat)
        piece = gamestate[color][pos1][0]

        # un pion se trouve à 'pos2' et en est un adverse
        if gamestate[self.oppo[color]].get(pos2):
            del gamestate[self.oppo[color]][pos2]

        del gamestate[color][pos1]
        gamestate[color][pos2] = [piece, [], []]

        return gamestate

class Chess(Optimize):
    """
    Classe gère une partie d'échecs
    """
    def __init__(self, player1, player2='robot'):
        """
        Initialiser un nouvel état de partie
        :raise ChessError: si un des deux joueurs n'est pas une str
        """

        if not isinstance(player1, str) or not isinstance(player2, str):
            raise ChessError("Les deux joueurs doivent être des chaines de caractères.")

        super().__init__()

        self.player1 = player1
        self.player2 = player2

    def __str__(self):

        # Construction de l'équiquier
        d1 = [['━' if y % 2 != 0 else ' ' for x in range(35)] for y in range(15)]
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
        title = "♔  Chessgame ♚"
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
        pion = self.state()[color][pos1]

        # Traitement d'erreurs
        for x, y in [pos1, pos2]:
            if not isinstance(x, int) or not isinstance(y, int):
                raise ChessError("Veuillez entrer que des nombres entiers.")

        # pos1 n'est liée à aucun pion sur l'échiquier
        if pos1 not in self.positions()['pions'][color]:
            raise ChessError("Aucun pion ne peut être déplacer.")

        # Déplacement invalide pour un pion
        elif pion[0] == 'P' and pos2 not in pion[1] + pion[2]:
            raise ChessError("Ce coup est invalide pour un pion.")

        # Déplacement invalide pour les autres pions
        elif pion[0] in ['K', 'Q', 'F', 'C', 'T'] and pos2 not in pion[1]:
            raise ChessError("Ce coup est invalide pour ce pion.")

        # Déplacement du pion 'piece'
        piece = self.etat[color][pos1][0]
        del self.etat[color][pos1]
        self.etat[color][pos2] = [piece, [], []]

    def autoplay(self, color):
        """
        Méthode permettant de jouer un coup valide pour
        l'état actuelle de jeu
        :raise ChessError: si la couleur est ni 'black' ni 'white'
        """
        # Traitement d'erreur
        if color not in ['black', 'white']:
            raise ChessError("Cette couleur n'existe pas aux échecs.")

        elif self.isCheckmate(color):
            raise ChessError("La partie est terminée.")

        self.exchange_pion()

        # Tentative de coincer le roi adverse
        for pos1, info in self.state()[color].items():
            if info[1]:
                for pos2 in info[1]:
                    state_future = self.valid_generator(self.future_state(color, pos1, pos2))
                    if state_future[color][pos2][1]:
                        for coord in state_future[color][pos2][1]:
                            if coord in state_future[self.oppo[color]][self.positions()['roi'][self.oppo[color]]][1]:
                                self.etat = self.future_state(color, pos1, coord)
                                break
                            else:
                                continue
                        break
            else:
                continue

        else:
            color_pos = [position for position, info in self.state()[color].items() if info[1] or info[2]]
            coord1 = random.choice(color_pos)
            pion = self.state()[color][coord1]

            # Si possible de manger
            if pion[2]:
                best = 0
                coord2 = False
                for pos in pion[2]:
                    if self.state()[self.oppo[color]][pos][0] == 'K':
                        continue
                    elif self.value[self.state()[self.oppo[color]][pos][0]] > best:
                        best = self.value[self.state()[self.oppo[color]][pos][0]]
                        coord2 = pos
                    else:
                        break
                if coord2:
                    self.eat(color, coord1, coord2)

            # Autrement, se déplacer
            elif pion[1]:
                move = random.choice(pion[1])
                self.move(color, coord1, move)

    def formatted_state(self):
        """
        Permet d'afficher l'état de partie de façon plus clair
        """
        total, message = set(), 'All on board'

        for color, info in self.state().items():
            print(f"{color}: value = {self.team_value(color)}")
            for position, liste in info.items():
                liste1 = ', '.join(map(str, (coord for coord in sorted(liste[1]))))
                liste2 = ', '.join(map(str, (coord for coord in sorted(liste[2]))))
                print(f"{liste[0]}:{position} ⇒  moves = {liste1 if liste[1] else 'cannot move'}, food = {liste2 if liste[2] else 'None'}")
                total.add(position)

        print(f"{len(total)} pions sur l'échiquier")

        for color, pions in self.ate.items():
            if pions:
                print(f"Pions bouffés pour team {color} (total = {len(pions)}): {', '.join([pion[1] for pion in pions])} ")
            else:
                print(f"Pions bouffés pour team {color} (total = {len(pions)}) : {message}")

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
        if pos1 not in self.positions()['pions'][color]:
            raise ChessError("Aucun pion ne peut être déplacer.")

        # pos2 n'est pas liée à un pion sur l'échiquier
        elif pos2 not in self.positions()['pions'][self.oppo[color]]:
            raise ChessError("Aucun pion ne se trouve à la position d'attaque.")

        # pos2 n'est pas un coup_for_eat valide
        elif pos2 not in self.state()[color][pos1][2]:
            raise ChessError("Coup d'attaque invalide.")

        # Déplacement et suppression des pions
        piece = self.etat[self.oppo[color]][pos2][0]

        if self.etat[color][pos1][0] == 'P':
            self.move(color, pos1, pos2)
            self.ate[self.oppo[color]].append((self.value[piece], piece))
            del self.etat[self.oppo[color]][pos2]
        else:
            self.ate[self.oppo[color]].append((self.value[piece], piece))
            del self.etat[self.oppo[color]][pos2]
            self.move(color, pos1, pos2)

class Game:
    """
    Classe qui run les games pour Chess
    """
    def __init__(self, player1, player2='Robot'):

        self.player1 = player1
        self.player2 = player2

    def autogame(self, n=0):

        jeu = Chess(self.player1, self.player2)
        jeu.formatted_state()
        print(jeu)

        if n > 0:
            count = 0
            while count < n:
                jeu.autoplay('white')
                jeu.formatted_state()
                print(jeu)
                if jeu.isCheckmate('black'):
                    print(jeu.isCheckmate('black'))
                    break

                jeu.autoplay('black')
                jeu.formatted_state()
                print(jeu)
                if jeu.isCheckmate('white'):
                    print(jeu.isCheckmate('white'))
                    break

                count += 1

        else:
            while True:
                jeu.autoplay('white')
                jeu.formatted_state()
                print(jeu)
                if jeu.isCheckmate('black'):
                    print(jeu.isCheckmate('black'))
                    break

                jeu.autoplay('black')
                jeu.formatted_state()
                print(jeu)
                if jeu.isCheckmate('white'):
                    print(jeu.isCheckmate('white'))
                    break

    def handgame(self):

        jeu = Chess(self.player1, self.player2)
        print(jeu)

        while True:
            action = input("Type de coup (m, e): ")
            pos1 = input("Position du pion xy: ")
            pos2 = input("Position de déplacement xy: ")
            try:
                if action == 'm':
                    jeu.move('white', (int(pos1[0]), int(pos1[1])), (int(pos2[0]), int(pos2[1])))
                elif action == 'e':
                    jeu.eat('white', (int(pos1[0]), int(pos1[1])), (int(pos2[0]), int(pos2[1])))
                if jeu.isCheckmate('black'):
                    print(jeu.isCheckmate('black'))
                print(jeu)

                jeu.autoplay('black')
                print(jeu)
                if jeu.isCheckmate('white'):
                    print(jeu.isCheckmate('white'))

            except ChessError as err:
                print(err)
                print(jeu)
            except Exception:
                print(jeu)
                print("Coup invalide, réessayer.")

Game('joueur1').autogame(n=30)
