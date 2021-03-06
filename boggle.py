"""
Usage:
    python3 boggle.py <boggle-board> <--word-length>
Examples:
    python3 boggle.py ESUSIMBEREDRBECA
    python3 boggle.py ESUSIMBEREDRBECA --word-length=5
    python3 boggle.py ESUSIMBEREDRBECA --word-length=5 --moar
"""
import argparse
import enchant

class BBictionary(object):

    def __init__(self, moar=False):
        self.moar = moar
        if self.moar:
            with open('words_alpha.txt') as word_file:
                self.english_words = set(word_file.read().split())
        self.us_dict, self.gb_dict = enchant.Dict("en_US"), enchant.Dict("en_GB")

    def is_word(self, w):
        w = w.lower()
        if self.moar:
            return w in self.english_words \
                    and not self.us_dict.check(w) and not self.gb_dict.check(w)
        else:
            return self.us_dict.check(w) or self.gb_dict.check(w)

class BBoggleBoard(object):
    BOARD_SIZE = 4
    WORD_LENGTHS = list(range(3, 8))

    def __init__(self, board, moar=False):
        """board : str length  BOARD_SIZE x BOARD_SIZE"""
        self.board = [board[i:i+BBoggleBoard.BOARD_SIZE]
                for i in range(0, len(board), BBoggleBoard.BOARD_SIZE)]
        self.dict = BBictionary(moar=moar)

    def neighbors(self, x, y):
        neighbors_coords = []
        for nx in range(max(x-1, 0), min(x+2, BBoggleBoard.BOARD_SIZE)):
            for ny in range(max(y-1, 0), min(y+2, BBoggleBoard.BOARD_SIZE)):
                if (nx != x) or (ny != y):
                    neighbors_coords.append((nx, ny))
        return neighbors_coords

    def find_words_rec(self, x, y, length, path_so_far):
        if length == 0:
            return []
        word = self.board[x][y]
        if length == 1:
            return [word]
        else:
            words = []
            path_so_far.append((x, y))
            for n in self.neighbors(x, y):
                if n not in path_so_far:
                    for w in self.find_words_rec(n[0], n[1], length - 1, path_so_far):
                        words.append(word + w)
            path_so_far.remove((x, y))
            return words

    def find_words(self, x, y, length):
        words = self.find_words_rec(x, y, length, [])
        return [w.lower() for w in words if self.dict.is_word(w)]

    def solve_for_length(self, word_length):
        print('Finding words of length {}'.format(word_length))
        words = set()
        for i in range(BBoggleBoard.BOARD_SIZE):
            for j in range(BBoggleBoard.BOARD_SIZE):
                words.update(self.find_words(i, j, word_length))
        return sorted(list(words))

    def solve_all(self):
        print('Solving entire board')
        words = []
        num_words = 0
        for word_length in BBoggleBoard.WORD_LENGTHS:
            words.append(self.solve_for_length(word_length))
            num_words += len(words[-1])
        print('Found {} unique words'.format(num_words))
        return words

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('board', help='A 16-character input board')
    parser.add_argument('--word-length', choices=BBoggleBoard.WORD_LENGTHS,
            type=int, help='The length of words you want to find')
    parser.add_argument('--moar', action='store_true',
            help='U want moar werdz?')
    args = parser.parse_args()

    board = BBoggleBoard(args.board, moar=args.moar)
    if args.word_length:
        print(board.solve_for_length(args.word_length))
    else:
        print(board.solve_all())


