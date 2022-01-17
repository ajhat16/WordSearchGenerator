import word_search

width = int(input("Enter width: "))
height = int(input("Enter height: "))
words = input("Enter words separated by a comma: ").split(',')

for number in range(len(words)):
    words[number] = words[number].strip()

go_again = 'y'

while go_again == 'y':
    ws = word_search.generate(width, height, words)
    word_search.print_word_grid(ws[0])
    print(ws[1])

    go_again = input("Would you like another word search? (y/n): ")