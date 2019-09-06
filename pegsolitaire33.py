#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


PEG_NUMS = 32
CENTER = 16
MAX_JUMP = PEG_NUMS - 1
# 各ペグのジャンプ表
# (ジャンプ先, 除去するペグ)のタプル
JUMPS = [((2, 1), (8, 3), ),                           # 0
         ((9, 4), ),                                   # 1
         ((0, 1), (10, 5), ),                          # 2
         ((5, 4), (15, 8), ),                          # 3
         ((16, 9), ),                                  # 4
         ((3, 4), (17, 10), ),                         # 5
         ((8, 7), (20, 13), ),                         # 6
         ((9, 8), (21, 14), ),                         # 7
         ((0, 3), (6, 7), (10, 9), (22, 15), ),        # 8
         ((1, 4), (7, 8), (11, 10), (23, 16), ),       # 9
         ((2, 5), (8, 9), (12, 11), (24, 17), ),       # 10
         ((9, 10), ),                                  # 11
         ((10, 11), (26, 19), ),                       # 12
         ((15, 14), ),                                 # 13
         ((16, 15), ),                                 # 14
         ((3, 8), (13, 14), (17, 16), (27, 22), ),     # 15
         ((4, 9), (14, 15), (18, 17), (28, 23), ),     # 16
         ((5, 10), (15, 16), (19, 18), (29, 24), ),    # 17
         ((16, 17), ),                                 # 18
         ((17, 18), ),                                 # 19
         ((6, 13), (22, 21), ),                        # 20
         ((7, 14), (23, 22), ),                        # 21
         ((8, 15), (20, 21), (24, 23), (30, 27), ),    # 22
         ((9, 16), (21, 22), (25, 24), (31, 28), ),    # 23
         ((10, 17), (22, 23), (26, 25), (32, 29), ),   # 24
         ((11, 18), (23, 24), ),                       # 25
         ((12, 19), (24, 25), ),                       # 26
         ((15, 22), (29, 28), ),                       # 27
         ((16, 23), ),                                 # 28
         ((17, 24), (27, 28), ),                       # 29
         ((22, 27), (32, 31), ),                       # 30
         ((23, 28), ),                                 # 31
         ((24, 29), (30, 31), ),                       # 32
         ]


class Peg:
    def __init__(self, position):
        self.exists = True
        if position == CENTER:
            self.exists = False
        self.position = position

    def __str__(self):
        if self.exists:
            return "*"
        return "-"

    def __repr__(self):
        return "position:{}, value:{}".format(self.position, self.str())


class Board:
    def __init__(self):
        self.pegs = []
        self.opereation_log = []
        self._jump_count = 0
        for i in range(33):
            self.pegs.append(Peg(i))

    def move_peg(self, ope):
        self.pegs[ope.src].exists = False
        self.pegs[ope.rmv].exists = False
        self.pegs[ope.dst].exists = True
        self._jump_count += 1
        self.opereation_log.append(ope)

    def back_peg(self):
        back_op = self.opereation_log.pop()
        self.pegs[back_op.src].exists = True
        self.pegs[back_op.rmv].exists = True
        self.pegs[back_op.dst].exists = False
        self._jump_count -= 1

    def search_move(self):
        candidates = []
        if self.is_winner():
            self.print_operations()
            return True
        if self.is_loser():
            return False
        for peg in self.pegs:
            if not peg.exists:
                continue
            for move in JUMPS[peg.position]:
                dst = move[0]
                rmv = move[1]
                if self.pegs[dst].exists:
                    continue
                if not self.pegs[rmv].exists:
                    continue
                candidates.append(Operation(peg.position, dst, rmv))
        if candidates:
            for ope in sorted(candidates, key=lambda ope: ope.priority):
                self.move_peg(ope)
                if self.search_move():
                    return True
                self.back_peg()

    def is_winner(self):
        return self._jump_count == MAX_JUMP and self.pegs[CENTER].exists

    def is_loser(self):
        result = True
        for i in (4, 14, 16, 18, 28):
            result = result or self.pegs[i].exists
        return not result

    def print_board(self):
        print("  {}{}{}  ".format(self.pegs[0], self.pegs[1], self.pegs[2]))
        print("  {}{}{}  ".format(self.pegs[3], self.pegs[4], self.pegs[5]))
        print("{}{}{}{}{}{}{}".format(self.pegs[6], self.pegs[7],
                                      self.pegs[8], self.pegs[9],
                                      self.pegs[10], self.pegs[11],
                                      self.pegs[12]))
        print("{}{}{}{}{}{}{}".format(self.pegs[13], self.pegs[14],
                                      self.pegs[15], self.pegs[16],
                                      self.pegs[17], self.pegs[18],
                                      self.pegs[19]))
        print("{}{}{}{}{}{}{}".format(self.pegs[20], self.pegs[21],
                                      self.pegs[22], self.pegs[23],
                                      self.pegs[24], self.pegs[25],
                                      self.pegs[26]))
        print("  {}{}{}  ".format(self.pegs[27], self.pegs[28], self.pegs[29]))
        print("  {}{}{}  ".format(self.pegs[30], self.pegs[31], self.pegs[32]))

    def print_operations(self):
        for op in self.opereation_log:
            print(op)


class Operation():
    groups = ((4, 14, 18, 28),
              (7, 9, 11, 15, 17, 21, 23, 25, 31),
              (3, 5, 13, 19, 27, 29),
              (0, 2, 6, 8, 10, 12, 20, 22, 24, 26, 30, 32),
              )

    def __init__(self, src, dst, rmv):
        self.src = src
        self.dst = dst
        self.rmv = rmv
        if rmv in self.groups[0]:
            self.priority = 3
        elif rmv in self.groups[1]:
            self.priority = 2
        elif rmv in self.groups[2]:
            self.priority = 1
        else:
            self.priority = 0

    def __str__(self):
        return "{}->{}:del {}".format(self.src, self.dst, self.rmv)


def main():
    start = time.time()
    board = Board()
    board.search_move()
    end = time.time()
    execution_time = end - start
    hour = execution_time // (60*60)
    minute = (execution_time - hour*60*60) // 60
    second = execution_time - (hour*60*60) - (minute*60)
    print("{}:{}:{}".format(hour, minute, second))


if __name__ == '__main__':
    main()
