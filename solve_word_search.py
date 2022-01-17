import word_search

height = int(input("Enter the number of rows in the grid: "))
grid = [list(input("Enter the word grid (new line for each row):\n"))]
number = 0

while number < height - 1:
    newline = list(input())
    if len(newline) != len(grid[0]):
        print("wrong line length")
        continue
    grid.append(newline)
    number += 1

words = input("Enter a list of the words that are in the grid seperated by a comma: ").split(',')

for number in range(len(words)):
    words[number] = words[number].strip()

found_words = word_search.find_all(grid, words)

for keys in found_words:
    word_search.show_solution(grid, keys, found_words[keys])
    print()
