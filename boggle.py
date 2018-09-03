board = [
    'AEFA',
    'VSPY',
    'OTRH',
    'MELA',
]
WORD_LENGTH = 4
BOARD_SIZE = 4


def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

english_words = load_words()


def is_word(w):
    return w.lower() in english_words


def neighbors(x, y, board_size):
    neighbors_coords = []
    for nx in range(max(x-1, 0), min(x+2, board_size)):
        for ny in range(max(y-1, 0), min(y+2, board_size)):
            if (nx != x) or (ny != y):
                neighbors_coords.append((nx, ny))
    return neighbors_coords


def find_words_rec(x, y, length, path_so_far):
    if length == 0:
        return []
    word = board[x][y]
    if length == 1:
        return [word]
    else:
        words = []
        path_so_far.append((x, y))
        for n in neighbors(x, y, BOARD_SIZE):
            if n not in path_so_far:
                for w in find_words_rec(n[0], n[1], length - 1, path_so_far):
                    words.append(word + w)
        path_so_far.remove((x, y))
        return words


def find_words(x, y, length):
    words = find_words_rec(x, y, length, [])
    # print words
    real_words = [w for w in words if is_word(w)]
    if real_words:
        print real_words


for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        # print "node:", board[i][j]
        # print "neighbors:", [board[n["x"]][n["y"]] for n in neighbors(i, j, BOARD_SIZE)]
        find_words(i, j, WORD_LENGTH)