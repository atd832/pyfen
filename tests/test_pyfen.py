from pyfen.pyfen import (
    Move,
    Turn,
    PGN,
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
    t = Turn('d4 d5')

    def test_turn(self):
        w = Move('d4', 'w')
        b = Move('d5', 'b')
        assert self.t.white_move == w
        assert self.t.black_move == b


class TestPGN:
    _ = '1.e4 e6 2.d4 d5 3.Nd2 Nf6 4.e5 Nfd7 5.f4 c5 6.c3 Nc6 7.Ndf3 cxd4 8.cxd4 f6' \
        '9.Bd3 Bb4+ 10.Bd2 Qb6 11.Ne2 fxe5 12.fxe5 O-O 13.a3 Be7 14.Qc2 Rxf3 15.gxf3 Nxd4' \
        '16.Nxd4 Qxd4 17.O-O-O Nxe5 18.Bxh7+ Kh8 19.Kb1 Qh4 20.Bc3 Bf6 21.f4 Nc4 22.Bxf6 Qxf6' \
        '23.Bd3 b5 24.Qe2 Bd7 25.Rhg1 Be8 26.Rde1 Bf7 27.Rg3 Rc8 28.Reg1 Nd6 29.Rxg7 Nf5' \
        '30.R7g5 Rc7 31.Bxf5 exf5 32.Rh5+  1-0'
    pgn = PGN(_)

    def test_pgn(self):
        expected_turn_25 = Turn('Rhg1 Be8')

        assert self.pgn.termination == '1-0'
        assert self.pgn.turns[24] == expected_turn_25

