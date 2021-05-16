import re

PIECES = {
    'K': 1,
    'Q': 1,
    'R': 1,
    'N': 1,
    'B': 1
}

RANKS = {
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7
}

FILES = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}

SQUARES = {
    'a1': [0, 0],
    'a2': [0, 1],
    'a3': [0, 2],
    'a4': [0, 3],
    'a5': [0, 4],
    'a6': [0, 5],
    'a7': [0, 6],
    'a8': [0, 7],
    'b1': [1, 0],
    'b2': [1, 1],
    'b3': [1, 2],
    'b4': [1, 3],
    'b5': [1, 4],
    'b6': [1, 5],
    'b7': [1, 6],
    'b8': [1, 7],
    'c1': [1, 8],
    'c2': [2, 0],
    'c3': [2, 1],
    'c4': [2, 2],
    'c5': [2, 3],
    'c6': [2, 4],
    'c7': [2, 5],
    'c8': [2, 6],
    'd1': [3, 0],
    'd2': [3, 1],
    'd3': [3, 2],
    'd4': [3, 3],
    'd5': [3, 4],
    'd6': [3, 5],
    'd7': [3, 6],
    'd8': [3, 7],
    'e1': [4, 0],
    'e2': [4, 1],
    'e3': [4, 2],
    'e4': [4, 3],
    'e5': [4, 4],
    'e6': [4, 5],
    'e7': [4, 6],
    'e8': [4, 7],
    'f1': [5, 0],
    'f2': [5, 1],
    'f3': [5, 2],
    'f4': [5, 3],
    'f5': [5, 4],
    'f6': [5, 5],
    'f7': [5, 6],
    'f8': [5, 7],
    'g1': [6, 0],
    'g2': [6, 1],
    'g3': [6, 2],
    'g4': [6, 3],
    'g5': [6, 4],
    'g6': [6, 5],
    'g7': [6, 6],
    'g8': [6, 7],
    'h1': [7, 0],
    'h2': [7, 1],
    'h3': [7, 2],
    'h4': [7, 3],
    'h5': [7, 4],
    'h6': [7, 5],
    'h7': [7, 6],
    'h8': [7, 7],
}

# other terminators?
RESULTS = {
    '0-1': 'black wins',
    '1-0': 'white wins',
    '1/2-1/2': 'draw'
}

S = list(SQUARES.keys())
P = list(PIECES.keys())
R = list(RESULTS.keys())


def rook_moves(coord: list):
    cx, cy = coord[0], coord[1]
    n = 7
    moves = []

    sum = cx
    while sum < n:
        sum += 1
        moves.append([sum, cy])

    sum = cx
    while sum > 0:
        sum -= 1
        moves.append([sum, cy])

    sum = cy
    while sum < n:
        sum += 1
        moves.append([cy, sum])

    sum = cy
    while sum > 0:
        sum -= 1
        moves.append([cy, sum])

    return moves


def bishop_moves(coord: list):
    cx, cy = coord[0], coord[1]
    n = 7
    moves = []

    sum_cx = cx
    sum_cy = cy
    while sum_cx < n and sum_cy < n:
        sum_cx += 1
        sum_cy += 1
        moves.append([sum_cx, sum_cy])

    sum_cx = cx
    sum_cy = cy
    while sum_cx > 0 and sum_cy > 0:
        sum_cx -= 1
        sum_cy -= 1
        moves.append([sum_cx, sum_cy])

    return moves


def knight_moves(coord: list):
    pass


def queen_moves(coord: list):
    pass


def king_moves(coord: list):
    pass


def pawn_moves(coord: list):
    pass


def search_for(regex, s):
    try:
        re.search(regex, s).group(0)
    except AttributeError:
        return None

    return re.search(regex, s).group(0)


class Move:
    """
        For seq 1. Nf3 Nf6, 'Nf3' and 'Nf6' are white and black's respective moves.
    """

    def __init__(self, move: str, player: str):
        self.move = move
        self.player = player
        self.disambiguation = self.move.replace(str(self.piece), '').replace(str(self.destination), '')
        # TODO: comments

    @property
    def short_castle(self):
        if search_for('O-O', self.move):
            return True
        else:
            return False

    @property
    def long_castle(self):
        if search_for('O-O-O', self.move):
            return True
        else:
            return False

    @property
    def check(self):
        if self.move[-1] == '+':
            return True
        else:
            return False

    @property
    def mate(self):
        if self.move[-1] == '#':
            return True
        else:
            return False

    @property
    def promotion(self):
        if search_for('.=', self.move):
            return True
        else:
            return False

    @property
    def piece(self):
        return search_for('|'.join(P), self.move[0])

    @property
    def destination(self):
        # should be last two chars unless
        # check +, castles O-O O-O-O,
        # FIXME: this is return None inappropriately
        if self.long_castle or self.short_castle:
            # FIXME: these should return the castling king sqs
            # TODO: add these char sets to enum
            return None

        # FIXME: these should return the castling king sqs
        if self.check or self.mate:
            return search_for('|'.join(S), self.move.rstrip(self.move[-1])[-2:])
        # still not accounting yet for disambiguation
        return search_for('|'.join(S), self.move[-2:])

    @property
    def takes(self):
        if search_for('x', self.move):
            return True
        else:
            return False

    @property
    def rank_of_departure(self):
        return search_for('[1-8]', self.disambiguation)

    @property
    def file_of_departure(self):
        return search_for('[a-h]', self.disambiguation)

        # 1) ...Rdf8, 2) R1a3, 3) Qh4e1
        # <piece>...<rank> or <file> or <rank><file>...<destination>

    def __eq__(self, other):
        return self.move == other.move and self.player == other.player


class Turn:
    """
        For seq 1. d4 d5 2. Nf3 Nf6,
        '1. d4 d5' and '2. Nf3 Nf6' would be Turns comprised of Moves
    """

    def __init__(self, turn: str):
        self._t = turn
        self.turn = self._t.split(' ')
        # the sequence would be index in turns...
        # self.seq_no = self.turn[0]
        self.white_move = Move(self.turn[0], 'w')
        self.black_move = Move(self.turn[1], 'b') if self.turn[1] else None
        # self.end_of_game

    def __str__(self):
        return self._t


class PGN:
    def __init__(self, pgn: str):
        # TODO: strip comments...
        # bracket format:
        # 1. e4 {Best by test!} e5
        # semicolon format:
        # 1. e4; Best by test!
        # 1... e5
        # TODO: game termination
        self.pgn = pgn
        self.termination = search_for('|'.join(R), self.pgn)
        self.turns = [Turn(t.strip()) for t in re.split(r'\d+[\.]', self.pgn) if t]


class Board:
    def __init__(self):
        self.white_king = [[0, 0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
        self.black_king = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 0, 0, 0]]
        self.white_rook = [[1, 0, 0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
        self.black_rook = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0, 1]]
        self.white_knight = [[0, 1, 0, 0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]]
        self.black_knight = [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 1, 0]]
        self.white_bishop = [[0, 0, 1, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]]
        self.black_bishop = [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 1, 0, 0]]
        self.white_queen = [[0, 0, 0, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
        self.black_queen = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0, 0]]
        self.white_pawn = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
        self.black_pawn = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 0, 0, 0, 0, 0, 0, 0]]

    # def _update(self):
    #     """  """
    #     # remove 1 from current position
    #     # move 1 to new position
    #     pass

    # TODO: one func for all pieces
    # def rook_viable_squares(self, bitmap):
    #     """ return bitmap coords of viable squares """
    #     current_pos = []
    #     for i in range(0, 8):
    #         for j in range(0, 8):
    #             if bitmap[i][j] == 1:
    #                 current_pos.append([i, j])
    #
    #     viable = set()
    #     for c in current_pos:
    #         viable.append(rook_moves(c))
    #
    #     return list(viable)

    def _bitmap(self, piece: "pieces", player: str):
        w = {
            'R': self.white_rook,
            'N': self.white_knight,
            'B': self.white_bishop,
            'K': self.white_king,
            'Q': self.white_queen
        }

        b = {
            'R': self.black_rook,
            'N': self.black_knight,
            'B': self.black_bishop,
            'K': self.black_king,
            'Q': self.black_queen
        }

        if player == 'w':
            return w.get(piece) if w.get(piece) else self.white_pawn

        if player == 'b':
            return b.get(piece) if b.get(piece) else self.black_pawn

    # return list of viable squares
    def _viable_moves(self, pos: list, piece: str):
        pass

    def move(self, move: Move):
        """ takes Move and assigns it to the board """
        piece = move.piece
        player = move.player
        # get the bitmap
        bitmap = self._bitmap(piece, player)

        # find the current board pos of piece(s) on bitmap
        pos = {}       # need pos to be a dict for each pos
        for i in range(0, 8):
            for j in range(0, 8):
                if bitmap[i][j] == i:
                    pos[SQUARES[[i, j]]] = {'coord': [i, j], 'viable': []}

        # find viable moves for piece
        for p in pos.keys():
            pos['viable'] = self._viable_moves(p['coord'], piece)

        # figure out of square is in viable moves
        starting = []
        for p in pos.keys():
            if move in p['viable']:
                starting.append(p)

        if len(starting) > 1:
            # disambiguation needed
            pass

        pass


# '1. d4 d5 2. Nf3 Nf6' => FENs
# seq no. w move b move
# move formats:
#   piece | square   [pieces][squares]  Bb3
#   pawn | square    [squares]  d6
#   piece | takes | square  [pieces]['x'][squares]  Nxf7
#   pawn | takes | square   [^pieces]['x'][squares]  cxb5
#   castles short   O-O     ['O-O']
#   castles long    O-O-O   ['O-O-O']
#   check   Ra6+    any above with '+'  +$ ends with
# disambiguating
#   piece | original file | square

# mapping a move sequence to a board state


class PGNConverter:
    """
    takes pgn
    outputs fen
    """
    pass
