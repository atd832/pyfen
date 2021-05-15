from pyfen.pyfen import (
    Move,
    Turn,
    rook_moves, bishop_moves
)


def test_rook_moves():
    moves = [[2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [0, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 0]]

    assert rook_moves([1, 1]) == moves


def test_bishop_moves():
    moves = [[2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [0, 0]]

    assert bishop_moves([1, 1]) == moves


class TestMove:

    m = Move('Nf6', 'w')
    t = Move('axb3', 'w')
    d = Move('Qh4e1', 'b')
    p = Move('e8=Q', 'w')

    def test_piece(self):
        e = 'N'
        assert self.m.piece == e

    def test_destination(self):
        e = 'f6'
        assert self.m.destination == e

    def test_takes(self):
        assert self.t.takes is True

    def test_disambiguation(self):
        assert self.d.rank_of_departure == '4'
        assert self.d.file_of_departure == 'h'

    def test_promotion(self):
        assert self.p.promotion is True


class TestTurn:
    t = Turn('1. d4 d5')

    def test_turn(self):
        w = Move('d4', 'w')
        b = Move('d5', 'b')
        assert self.t.white_move == w
        assert self.t.black_move == b
