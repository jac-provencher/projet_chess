# # def afficher(etat):
# #         """
# #         Produire la représentation en art ascii correspondant à l'état actuel de la partie.
# #         Cette représentation est la même que celle du TP précédent.
# #         :returns: la chaîne de caractères de la représentation.
# #         """
# #         # Construction du damier
# #         d1 = [[' ' for _ in range(35)] for _ in range(15)]
# #         for i, ligne in enumerate(d1[::2]):
# #             ligne[0] = str(8 - i)
# #             for n in range(4, 35, 4):
# #                 ligne[n] = '.'
# #         d2 = []
# #         for ligne in d1:
# #             ligne[2] = ligne[34] = '|'
# #             d2 += ligne + ['\n']

# #         # Position des joueurs
# #         for positions in etat.values():
# #             for pos, pion in positions.items():
# #                 x, y = pos
# #                 d2[36*(16-2*y)+4*x] = pion

# #         # Affiche du damier
# #         title = "Chessgame"
# #         debut = ['   ', '-'*31, '\n']
# #         end = ['--|', '-'*31, '\n', '  | ', '   '.join(str(n) for n in range(1, 9))]

# #         return f"{title:^37}" + '\n' + ''.join(debut + d2 + end)

# # pions = {
# #         'black': {(1, 2): 'P', (2, 2): 'P', (3, 2): 'P', (4, 2): 'P', (5, 2): 'P', (6, 2): 'P', (7, 2): 'P', (8, 2): 'P'},
# #         'white': {(1, 7): 'P', (2, 7): 'P', (3, 7): 'P', (4, 7): 'P', (5, 7): 'P', (6, 7): 'P', (7, 7): 'P', (8, 7): 'P'}
# #         }
# # tours = {
# #         'black': {(1, 8): 'T', (8, 8): 'T'},
# #         'white': {(1, 1): 'T', (8, 1): 'T'}
# #         }
# # chevals = {
# #         'black': {(2, 8): 'C', (7, 8): 'C'},
# #         'white': {(2, 1): 'C', (7, 1): 'C'}
# #         }
# # fous = {
# #         'black': {(3, 8): 'F', (6, 8): 'F'},
# #         'white': {(3, 1): 'F', (3, 4): 'F'}
# #         }
# # rois = {
# #         'black':{(5, 8):'K'},
# #         'white': {(4, 1): 'K'}
# #         }
# # reines = {
# #         'black': {(4, 8): 'Q'},
# #         'white': {(5, 1): 'Q'}
# #         }

# # # pieces = [pions, tours, chevals, fous, rois, reines]
# # # dico = {'black':{}, 'white':{}}
# # # for piece in pieces:
# # #     for color, pos in piece.items():
# # #         dico[color].update(pos)

# # # print(afficher(dico))
# # # print(dico)


# # dico = {'black': {(1, 2): ['P'], (2, 2): ['P'], (3, 2): ['P'], (4, 2): ['P'],
# #                   (5, 2): ['P'], (6, 2): ['P'], (7, 2): ['P'], (8, 2): ['P'],
# #                   (1, 8): ['T'], (8, 8): ['T'], (2, 8): ['C'], (7, 8): ['C'],
# #                   (3, 8): ['F'], (6, 8): ['F'], (5, 8): ['K'], (4, 8): ['Q']},
# #         'white': {(1, 7): ['P'], (2, 7): ['P'], (3, 7): ['P'], (4, 7): ['P'],
# #                   (5, 7): ['P'], (6, 7): ['P'], (7, 7): ['P'], (8, 7): ['P'],
# #                   (1, 1): ['T'], (8, 1): ['T'], (2, 1): ['C'], (7, 1): ['C'],
# #                   (3, 1): ['F'], (6, 1): ['F'], (4, 1): ['K'], (5, 1): ['Q']}
# #        }

# # fous = {
# #         'black': {(3, 8): ['F'], (6, 8): ['F']},
# #         'white': {(3, 1): ['F'], (6, 1): ['F']}
# #         }

# # coord = []
# # for color, positions in dico.items():
# #     for position in positions.keys():
# #         coord.append(position)

# # for color, positions in fous.items():
# #     for position in positions.keys():
# #         coup_valide = []
# #         x, y = position
# #         # Sur une piste... peut-être faire 4 boucles différentes pour les 4 directions possibles.
# #         # ...certainement une possibilité de simplifier
# #         all_pos = [(x, y) for x in range(1, 9) for y in range(1, 9)]
# #         for i in range(1, 9):
# #                 if (x+i, y+i) in coord or (x+i, y+i) not in all_pos:
# #                         break
# #                 else:
# #                         coup_valide.append((x+i, y+i))
# #         for i in range(1, 9):
# #                 if (x+i, y-i) in coord or (x+i, y-i) not in all_pos:
# #                         break
# #                 else:
# #                         coup_valide.append((x+i, y-i))
# #         for i in range(1, 9):
# #                 if (x-i, y+i) in coord or (x-i, y+i) not in all_pos:
# #                         break
# #                 else:
# #                         coup_valide.append((x-i, y+i))
# #         for i in range(1, 9):
# #                 if (x-i, y-i) in coord or (x-i, y-i) not in all_pos:
# #                         break
# #                 else:
# #                         coup_valide.append((x-i, y-i))

# #         fous[color][position].append(coup_valide)

# # print(coord)
# # print(fous)

# dico = {
#         'K': [
#                 (x, y+1), (x, y-1), (x+1, y), (x-1, y),
#                 (x+1, y+1), (x-1, y+1), (x+1, y-1,), (x-1, y-1)
#                 ],
#         'Q': [
#                 [(x, y+i) for i in range(1, 9)], [(x, y-i) for i in range(1, 9)],
#                 [(x+i, y) for i in range(1, 9)], [(x-i, y) for i in range(1, 9)],
#                 [(x+i, y+i) for i in range(1, 9)], [(x-i, y+i) for i in range(1, 9)],
#                 [(x+i, y-i) for i in range(1, 9)], [(x-i, y-i)] for i in range(1, 9)
#                 ],
#         'F': [
#                 [(x+i, y+i) for i in range(1, 9)], [(x+i, y-i) for i in range(1, 9)],
#                 [(x-i, y+i) for i in range(1, 9)], [(x-i, y-i) for i in range(1, 9)]
#                 ],
#         'T': [
#                 [(x+i, y) for i in range(1, 9)], [(x-i, y) for i in range(1, 9)],
#                 [(x, y+i) for i in range(1, 9)], [(x, y-i) for i in range(1, 9)]
#                 ],
#         'C': [
#                 (x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1),
#                 (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2)
#                 ]
#         }

# """
# Cas spécial : positions valides des pions

# (1) Si le pion est encore sur sa ligne de départ,
# faire un dico = {'black':[(x, y-1), (x, y-2)], 'white':[(x, y+1), (x, y+2)]}
# for color, coup in dico.items():
#         for i, coord in enumerate(coup):
#                 if coord in self.etat:
#                         del coup_valide[color][i]

# (2) Autrement,
# si (x, y+1) n'est pas dans self.etat:
# ajouter (x, y+1) dans ses coups valides.



# (x-1, y+1) ou (x+1, y+1) pour bouffer (**garder pour plus tard**)
# *Cas du prise en passant...

# Donc,
# BLACK:
# (x, y-1)
# (x, y-2)
# (x+1, y-1) ou (x-1, y-1)

# WHITE:
# (x, y+1)
# (x, y+2)
# (x-1, y+1) ou (x+1, y+1)
# """
