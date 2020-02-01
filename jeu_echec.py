from copy import deepcopy
from sys import getsizeof
from itertools import chain, takewhile
from more_itertools import first_true
from random import choice

"""
TODO LIST:
(1) OK les méthodes isValidPosition, takeWhile et pawnPositions doivent pouvoir prendre en argument un etat de jeu
(2) OK Faire les méthodes movePiece et killPiece
(3) Trouver un moyen de simplifier moveBank
(4) OK Faire isCheckmate
(5) OK Faire isCheck
(6) Apprendre à travailler avec les files (pour avoir un historique des coups joués)
(7) Voir si possible d'implanter la sous-promotion
(8) OK Faire un affichage avec pygame
(9) Faire algorithme minimax
"""

class ChessError(Exception):
    """Classe pour les erreurs soulevées par chess."""

class chess:

    def __init__(self, state=None):
        if state is None:
            self.etat = {'white': {(1, 8): 'T', (8, 8): 'T', (2, 8): 'C', (7, 8): 'C', (3, 8): 'F', (6, 8): 'F', (5, 8): 'Q', (4, 8): 'K', (1, 7): 'P', (2, 7): 'P', (3, 7): 'P', (4, 7): 'P', (5, 7): 'P', (6, 7): 'P', (7, 7): 'P', (8, 7): 'P'}, 'black': {(1, 1): 'T', (8, 1): 'T', (2, 1): 'C', (7, 1): 'C', (3, 1): 'F', (6, 1): 'F', (5, 1): 'Q', (4, 1): 'K', (1, 2): 'P', (2, 2): 'P', (3, 2): 'P', (4, 2): 'P', (5, 2): 'P', (6, 2): 'P', (7, 2): 'P', (8, 2): 'P'}}
        else:
            self.etat = state
        self.uniCode = {
        'black': {'P': '♙', 'C': '♘', 'F': '♗', 'Q': '♕', 'K': '♔', 'T': '♖'},
        'white': {'P': '♟', 'C': '♞', 'F': '♝', 'Q': '♛', 'K': '♚', 'T': '♜'}
        }
        self.pawnValue = {'P':10, 'C':30, 'F':30, 'T':50, 'Q':90, 'K':1000}
        self.oppo = {'black':'white', 'white':'black'}
        self.pawnKilled = {'black':[], 'white':[]}
        self.startingLine = {'black': 2, 'white': 7}
        self.endingLine = {'black': 8, 'white': 1}
        self.boardPositions = lambda: ((x, y) for x in range(1, 9) for y in range(1, 9))
        self.onBoard = lambda position: 1 <= position[0] <= 8 and 1 <= position[1] <= 8
        self.pawnPositions = lambda state: chain(state['black'], state['white'])
        self.infinity = 999_999_999

    def __str__(self):
        """Retourne une représentation en ASCII du board"""
        board = [['.' for x in range(8)] for y in range(8)]
        for color, positions in self.etat.items():
            for position, piece in positions.items():
                x, y = position
                board[8-y][x-1] = self.uniCode[color][piece]

        return '='*16 + '\n' + '\n'.join(' '.join(spot for spot in row) for row in board) + '\n' + '='*16

    def moveBank(self, position, piece):
        """
        Méthode qui retourne un tuple des coups légals
        pour la piece à la position en argument
        :returns: tuple
        """
        x, y = position
        if piece == 'K':
            return (
            (x, y+1), (x, y-1), (x+1, y), (x-1, y),
            (x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1)
            )
        elif piece == 'C':
            return (
            (x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1),
            (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2)
            )
        elif piece == 'T':
            return (
            ((x+i, y) for i in range(1, 9)), ((x-i, y) for i in range(1, 9)),
            ((x, y+i) for i in range(1, 9)), ((x, y-i) for i in range(1, 9))
            )
        elif piece == 'Q':
            return (
            ((x, y+i) for i in range(1, 9)), ((x, y-i) for i in range(1, 9)),
            ((x+i, y) for i in range(1, 9)), ((x-i, y) for i in range(1, 9)),
            ((x+i, y+i) for i in range(1, 9)), ((x-i, y+i) for i in range(1, 9)),
            ((x+i, y-i) for i in range(1, 9)), ((x-i, y-i) for i in range(1, 9))
            )
        elif piece == 'F':
            return (
            ((x+i, y+i) for i in range(1, 9)), ((x+i, y-i) for i in range(1, 9)),
            ((x-i, y+i) for i in range(1, 9)), ((x-i, y-i) for i in range(1, 9))
            )

    def moveGenerator(self, state, color, position):
        """
        Méthode qui génère les déplacement légals pour la position demandée
        """
        isValidPosition = lambda position: position not in self.pawnPositions(state) and self.onBoard(position)
        piece = state[color][position]

        # Pions portés fixes
        if piece in ('K', 'C'):
            freeSpots = set(self.boardPositions()) - set(self.pawnPositions(state))
            legalMoves = freeSpots & set(self.moveBank(position, piece))
            for move in legalMoves:
                yield move
        # Pions
        elif piece == 'P':
            x, y = position
            deplacements = ((x, y-1), (x, y-2)) if color == 'white' else ((x, y+1), (x, y+2))
            if y == self.startingLine[color]:
                legalMoves = takewhile(isValidPosition, deplacements)
                for move in legalMoves:
                    yield move
            elif isValidPosition(move := deplacements[0]):
                    yield move
        # Pions longues portées
        else:
            legalMoves = map(lambda direction: takewhile(isValidPosition, direction), self.moveBank(position, piece))
            for moves in legalMoves:
                for move in moves:
                    yield move

    def killGenerator(self, state, color, position):
        """
        Méthode qui génère les attaques possibles pour la
        position demandée selon le state donné
        """
        piece = state[color][position]
        oppoPawnPositions = state[self.oppo[color]].keys()

        # Pions portés fixes
        if piece in ('K', 'C'):
            if attacks := set(oppoPawnPositions) & set(self.moveBank(position, piece)):
                for attack in attacks:
                    yield attack
        # Pions
        elif piece == 'P':
            x, y = position
            legalAttacks = ((x+1, y+1), (x-1, y+1)) if color == 'white' else ((x+1, y-1), (x-1, y-1))
            for attack in legalAttacks:
                if attack in oppoPawnPositions:
                    yield attack
        # Pions longues portées
        else:
            isPawn = lambda position: position in self.pawnPositions(state)
            for direction in self.moveBank(position, piece):
                if attack := first_true(direction, default=False, pred=isPawn):
                    if attack in oppoPawnPositions:
                        yield attack

    def movePiece(self, color, pos1, pos2):
        """
        Méthode qui permet de déplacer le pion
        à pos1 vers pos2.
        """
        # Déplacement du pion (pos1 --> pos2)
        piece = self.etat[color][pos1]
        self.etat[color].update({pos2:piece})
        del self.etat[color][pos1]

        # Check si promotion possible
        if position := self.pawnPromotion(self.etat, color):
            self.etat[color].update({position:'Q'})

        # Check si echec et mat
        elif winner := self.isCheckmate(self.etat, self.oppo[color]):
            raise ChessError(winner)

    def killPiece(self, color, pos1, pos2):
        """
        Méthode qui permet d'attaquer le pion
        à pos2 avec le pion à pos1
        """
        # Check l'input
        if pos2 not in self.etat[self.oppo[color]]:
            raise ChessError("Aucun pion adverse ne peut être mangé à cette position.")

        # Déplacement du pion (pos1 --> pos2)
        self.movePiece(color, pos1, pos2)

        # Suppression du pion à pos2
        target = self.etat[self.oppo[color]][pos2]
        self.pawnKilled[self.oppo[color]].append(target)
        del self.etat[self.oppo[color]][pos2]

    def getMove(self, color, pos1=None, pos2=None):
        """
        Méthode qui prend le input de l'utilisateur
        Appel la méthode approprié selon le coup.
        """
        # Check l'input
        self.isValidInput(color, pos1, pos2)

        # Appel de la bonne méthode
        if pos2 in self.etat[self.oppo[color]]:
            self.killPiece(color, pos1, pos2)
        else:
            self.movePiece(color, pos1, pos2)

    def isValidInput(self, color, pos1, pos2):
        """
        Méthode qui valide si le input rentrer
        par l'utilisateur est valide. Raise une
        ChessError
        """
        if not isinstance(color, str):
            raise ChessError("La couleur doit être une chaine de caractère.")
        if color not in ('black', 'white'):
            raise ChessError("Couleur invalide.")
        if not isinstance(pos1, tuple) or not isinstance(pos2, tuple):
            raise ChessError("Au moins une des positions n'a pas le bon format, soit (x, y).")
        if len(pos1) != 2 or len(pos2) != 2:
            raise ChessError("Au moins une des positions n'a pas le bon nombre d'éléments.")
        if not self.onBoard(pos1) or not self.onBoard(pos2):
            raise ChessError("Au moins une des positions n'est pas sur l'échiquier")
        if pos1 not in self.etat[color]:
            raise ChessError(f"La case sélectionné n'est pas occupé par un pion {color}")
        if pos2 not in chain(self.moveGenerator(self.etat, color, pos1), self.killGenerator(self.etat, color, pos1)):
            raise ChessError("Ce coup ne respecte pas les règles du jeu.")

    def isCheckmate(self, state, color):
        """
        Méthode qui verifie si le roi 'color'
        est en situation d'échec et mat.
        Retourne le gagnant si oui,
        False autrement.
        """
        if not self.isCheck(state, color):
            return False

        for position in state[color]:
            for move in chain(self.moveGenerator(state, color, position), self.killGenerator(state, color, position)):
                temporaryState = self.simulateState(state, color, position, move)
                if not self.isCheck(temporaryState, color):
                    return False

        return f"Le gagnant est le joueur {self.oppo[color]}!"

    def isCheck(self, state, color):
        """
        Vérifie si un des roi est en échec.
        Retourne un bool
        """
        oppoTargets = (move for position in state[self.oppo[color]] for move in self.killGenerator(state, self.oppo[color], position))
        for position, piece in state[color].items():
            if piece == 'K':
                if position in oppoTargets:
                    return True
                break
        return False

    def pawnPromotion(self, state, color):
        """
        Méthode qui vérifie si la promotion d'un pion 'color'
        est possible. Si oui, retourne sa position,
        autrement, retourne False
        """
        linePositions = ((x, self.endingLine[color]) for x in range(1, 9))
        for position in linePositions:
            if position in state[color] and state[color][position] == 'P':
                return position
        return False

    def simulateState(self, etatCourant, color, pos1, pos2):
        """
        Méthode qui permet de déplacer conditionnellement un pion
        Retourne un état de partie
        """
        piece = etatCourant[color][pos1]
        futureState = deepcopy(etatCourant)
        if pos2 in futureState[self.oppo[color]]:
            del futureState[self.oppo[color]][pos2]
        futureState[color].update({pos2:piece})
        del futureState[color][pos1]

        return futureState

    def autoplay(self, color):
        """
        Méthode qui joue un coup automatiquement
        pour les pions 'color'
        """
        pos1, pos2 = self.minimax(3, self.etat, color, -self.infinity, self.infinity, True)[1]

        # Appel de la bonne méthode
        if pos2 in self.etat[self.oppo[color]]:
            self.killPiece(color, pos1, pos2)
        else:
            self.movePiece(color, pos1, pos2)

    def minimax(self, depth, state, color, alpha, beta,  isMaximizing):
        """
        Méthode permettant de chercher, dans l'arbre de récursion,
        le coup le plus avantageux pour le joueur 'color'.
        :returns: (value, position)
        """
        if depth == 0 or self.isCheckmate(state, color):
            return -self.staticEvaluation(state, color), None

        elif isMaximizing:
            maxEval = -self.infinity
            bestMove = None
            for position in state[color]:
                possibleMoves = chain(self.moveGenerator(state, color, position), self.killGenerator(state, color, position))
                for move in possibleMoves:
                    temportaryState = self.simulateState(state, color, position, move)
                    bestReply = self.minimax(depth-1, temportaryState, self.oppo[color], alpha, beta, not isMaximizing)[0]
                    if bestReply > maxEval:
                        maxEval, bestMove = bestReply, (position, move)
                    alpha = max(alpha, maxEval)
                    if beta <= alpha:
                        return maxEval, bestMove

            return maxEval, bestMove

        else:
            minEval = self.infinity
            bestMove = None
            for position in state[color]:
                possibleMoves = chain(self.moveGenerator(state, color, position), self.killGenerator(state, color, position))
                for move in possibleMoves:
                    temportaryState = self.simulateState(state, color, position, move)
                    bestReply = self.minimax(depth-1, temportaryState, self.oppo[color], alpha, beta, not isMaximizing)[0]
                    if bestReply < minEval:
                        minEval, bestMove = bestReply, (position, move)
                    beta = min(beta, minEval)
                    if beta <= alpha:
                        return minEval, bestMove

            return minEval, bestMove

    def staticEvaluation(self, state, color):
        """
        Méthode permettant d'obtenir la valeur utilitaire de
        l'état de jeu 'state' en fonction des paramètres désirés.
        :returns: int
        """
        return self.getMaterialValue(state, color)

    def getMaterialValue(self, state, color):
        """
        Méthode qui retourne la valeur matériel pour le joueur
        'color'.
        :returns: int
        """
        return sum(self.pawnValue[piece] for piece in state[color].values())

    def displayLegalMoves(self, state):
        for color, positions in state.items():
            print(f"{color}:")
            for position, piece in positions.items():
                legalMoves = ', '.join(str(move) for move in self.moveGenerator(state, color, position))
                legalKills = ', '.join(str(attack) for attack in self.killGenerator(state, color, position))
                print(f"{piece}: {position} → Moves: {legalMoves} Attacks: {legalKills}")
