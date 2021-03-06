import random
import string

RIGHT = (1, 0)
DOWN = (0, 1)
RIGHT_DOWN = (1, 1)
RIGHT_UP = (1, -1)
DIRECTIONS = (RIGHT, DOWN, RIGHT_DOWN, RIGHT_UP)


def get_size(grid):
    """returns the width and height of a grid of letters that was passed to it"""
    height = len(grid)
    width = len(grid[0])

    return (width, height)

def print_word_grid(grid):
    """outputs the word grid that was passed to it"""
    number = 0

    for rows in grid:
        for letter in grid[number]:
            print(letter, end='')

        print()
        number += 1

def copy_word_grid(grid):
    """creates a copy of the word grid called new_grid, and returns new_grid"""
    row_list = []
    new_grid = []

    for num_rows in range(len(grid)):
        for letter in grid[num_rows]:
            row_list.append(letter)
        new_grid.append(row_list)
        row_list = []

    return new_grid

def extract(grid, position, direction, max_len):
    """extracts a series of letters from the word grid using the starting position of the word,
        the direction of the word, and the size of the word. returns the extracted letters"""
    word = ''

    for number in range(max_len):
        if direction == RIGHT:
            word = word + grid[position[1]][position[0] + number]
            if (position[0] + number) == len(grid[0]) - 1:
                break
        elif direction == DOWN:
            word = word + grid[position[1] + number][position[0]]
            if (position[1] + number) == len(grid) - 1:
                break
        elif direction == RIGHT_DOWN:
            word = word + grid[position[1] + number][position[0] + number]
            if (position[0] + number) == len(grid[0]) or (position[1] + number) == len(grid) - 1:
                break
        elif direction == RIGHT_UP:
            word = word + grid[position[1] - number][position[0] + number]
            if (position[0] + number) == len(grid[0]) or (position[1] - number) == 0:
                break

    return word

def show_solution(grid, word, solution):
    """searches the grid for a string word, at the given solution spot in the grid (False if no solution).
        prints a prompt depending on if the solution is found, or is not found"""
    if not solution:
        print(word, "is not found in this word search")
    else:
        print(word.upper(), "can be found as below")
        new_grid = copy_word_grid(grid)

        for number in range(len(word)):
            if solution[1] == (1, 0):
                new_grid[solution[0][1]][solution[0][0] + number] = new_grid[solution[0][1]][
                    solution[0][0] + number].upper()
            elif solution[1] == (0, 1):
                new_grid[solution[0][1] + number][solution[0][0]] = new_grid[solution[0][1] + number][
                    solution[0][0]].upper()
            elif solution[1] == (1, 1):
                new_grid[solution[0][1] + number][solution[0][0] + number] = new_grid[solution[0][1] + number][
                    solution[0][0] + number].upper()
            elif solution[1] == (1, -1):
                new_grid[solution[0][1] - number][solution[0][0] + number] = new_grid[solution[0][1] - number][
                    solution[0][0] + number].upper()

        print_word_grid(new_grid)

def find(grid, word):
    """searches the word grid for a string word, and returns its starting postion, and the direction
        the word is going in as a tuple. returns False of word was not found"""
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] == word[0]:
                temp_word = ''
                start_location = (column, row)
                for number in range(len(word)):
                    temp_word = temp_word + grid[row][column + number]
                    if column + number == len(grid[0]) - 1:
                        break

                if temp_word == word:
                    return (start_location, RIGHT)
                else:
                    temp_word = ''

                for number in range(len(word)):
                    temp_word = temp_word + grid[row + number][column]
                    if grid[row + number] == grid[-1]:
                        break

                if temp_word == word:
                    return (start_location, DOWN)
                else:
                    temp_word = ''

                for number in range(len(word)):
                    temp_word = temp_word + grid[row + number][column + number]

                    if grid[row + number] == grid[-1] or column + number == len(grid[0]) - 1:
                        break

                if temp_word == word:
                    return (start_location, RIGHT_DOWN)
                else:
                    temp_word = ''

                for number in range(len(word)):
                    temp_word = temp_word + grid[row - number][column + number]

                    if grid[row - number] == grid[0] or column + number == len(grid[0]) - 1:
                        break

                if temp_word == word:
                    return (start_location, RIGHT_UP)
                else:
                    temp_word = ''

    return False

def find_all(grid, word):
    """searches the grid for a list of words, the adds those words as keys, and the starting point and position as
        values for that key. the value is False if the word was not found."""
    found_words = {}

    for string in word:
        found_words[string] = find(grid, string)

    return found_words

def randomize_word_direction():
    """helper function for generate that randomly generates, and returns, a direction for a word"""
    return random.choice(DIRECTIONS)

def randomize_word_placement(grid):
    """helper function for generate that randomly generates, and returns, an x and a y starting position for
       a word to be put into grid"""
    return (random.randint(0, len(grid[0]) - 1), random.randint(0, len(grid) - 1))

def place_words_in_grid(grid, completed_words, word_placement, word_direction):
    """helper functioon for generate that places each word in to a grid given their direction and
       starting position. returns the grid"""
    for word in completed_words:
        for number in range(len(word)):
            if word_direction[word] == RIGHT:
                grid[word_placement[word][1]][word_placement[word][0] + number] = word[number]
            elif word_direction[word] == DOWN:
                grid[word_placement[word][1] + number][word_placement[word][0]] = word[number]
            elif word_direction[word] == RIGHT_DOWN:
                grid[word_placement[word][1] + number][word_placement[word][0] + number] = word[number]
            else:
                grid[word_placement[word][1] - number][word_placement[word][0] + number] = word[number]

    return grid

def randomize_remaining_letters(grid):
    """helper function for generate that randomizes any remaining positions (spaces) in
       grid that were not filled in by a word. returns grid"""
    for row in grid:
        for column in range(len(grid[0])):
            if row[column] == ' ':
                row[column] = random.choice(string.ascii_lowercase)

    return grid

def is_word_correct_len(word, grid, word_direction, word_placement):
    """helper function for generate. checks if a given word fits in a grid given the word's
       direction and starting position. return True or False if word fits or does not fit"""
    if word_direction[word] == RIGHT:
        if abs(len(grid[0]) - word_placement[word][0]) < len(word):
            return False
        else:
            return True
    elif word_direction[word] == DOWN:
        if abs(len(grid) - word_placement[word][1]) < len(word):
            return False
        else:
            return True
    elif word_direction[word] == RIGHT_DOWN:
        if (abs(len(grid) - word_placement[word][1]) < len(word)) or \
                (abs(len(grid[0]) - word_placement[word][0]) < len(word)):
            return False
        else:
            return True
    else:
        if (word_placement[word][1] - len(word) < 0) or \
                (abs(len(grid[0]) - word_placement[word][0] < len(word))):
            return False
        else:
            return True

def overlaps_previous_word(word, grid, word_direction, word_placement):
    """helper function for generate. the function checks to see if the next letter of word is going to
       overlap the previous word in the grid. if it overlaps, return False. otherwise, adds the current
       letter in word to the grid. if every letter gets added, returns True"""
    backup = copy_word_grid(grid)

    for number in range(len(word)):
        if word_direction[word] == RIGHT:
            if word_placement[word][0] + number == len(grid[0]):
                break
            if grid[word_placement[word][1]][word_placement[word][0] + number] != ' ' and\
                    grid[word_placement[word][1]][word_placement[word][0] + number] != word[number]:
                grid = backup
                return False
            else:
                grid[word_placement[word][1]][word_placement[word][0] + number] = word[number]
        elif word_direction[word] == DOWN:
            if word_placement[word][1] + number == len(grid):
                break
            if grid[word_placement[word][1] + number][word_placement[word][0]] != ' ' and\
                    grid[word_placement[word][1] + number][word_placement[word][0]] != word[number]:
                grid = backup
                return False
            else:
                grid[word_placement[word][1] + number][word_placement[word][0]] = word[number]
        elif word_direction[word] == RIGHT_DOWN:
            if word_placement[word][1] + number == len(grid) or word_placement[word][0] + number == len(grid[0]):
                break
            if grid[word_placement[word][1] + number][word_placement[word][0] + number] != ' ' and\
                    grid[word_placement[word][1] + number][word_placement[word][0] + number] != word[number]:
                grid = backup
                return False
            else:
                grid[word_placement[word][1] + number][word_placement[word][0] + number] = word[number]
        else:
            if word_placement[word][0] + number == len(grid[0]) or word_placement[word][1] - number == -1:
                break
            if grid[word_placement[word][1] - number][word_placement[word][0] + number] != ' ' and\
                    grid[word_placement[word][1] - number][word_placement[word][0] + number] != word[number]:
                grid = backup
                return False
            else:
                grid[word_placement[word][1] - number][word_placement[word][0] + number] = word[number]

    return True

def generate(width, height, words):
    """generates a grid from a given width and height, then randomly puts the words into the grid.
       the function will attempt to successfully put each word in the grid 100 times. after it goes
       through this process for every word, the remaining empty spaces in the grid will be filled
       with random letters. the function returns a tuple of the completed grid, and the words that were
       successfully added to the grid."""
    grid = []

    for rows in range(height):
        grid.append([])

    for list in grid:
        for number in range(width):
            list.append(" ")

    word_direction = {}
    word_placement = {}
    is_good = {}
    completed_words = []
    completed_grid = copy_word_grid(grid)

    for word in words:
        word_direction[word] = randomize_word_direction()
        word_placement[word] = randomize_word_placement(grid)
        is_good[word] = False

    for word in words:
        other_number = 0
        while other_number != 100 and is_good[word] == False:
            is_good[word] = is_word_correct_len(word, grid, word_direction, word_placement)

            if is_good[word] == True:
                completed_words.append(word)
                if not overlaps_previous_word(word, grid, word_direction, word_placement):
                    is_good[word] = False
                    completed_words.remove(word)

            if word not in completed_words:
                word_placement[word] = randomize_word_placement(grid)
                is_good[word] = False
                word_direction[word] = randomize_word_direction()

            other_number += 1

    completed_grid = place_words_in_grid(completed_grid, completed_words, word_placement, word_direction)
    completed_grid = randomize_remaining_letters(completed_grid)

    return (completed_grid, completed_words)


if __name__ == "__main__":
    grid = generate(5, 5, ['cat', 'dog', 'art', 'town', 'den', 'wolf', 'part', 'mansion'])
    print(grid)
    print()
    print_word_grid(grid[0])
    print(grid[1])
    found_words = find_all(grid[0], grid[1])
    print()



