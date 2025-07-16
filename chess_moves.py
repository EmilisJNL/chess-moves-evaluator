import re
import random
import time

white_pieces = {
    "Rook": '\u2656',
    "Pawn": '\u2659'
    }
black_pieces = {
    "King": '\u265A',
    "Queen": '\u265B',
    "Rook": '\u265C',
    "Bishop": '\u265D',
    "Knight": '\u265E',
    "Pawn": '\u265F'
    } 
remaining_black_pieces = {
    "Pawn": 8,
    "Rook": 2,
    "King": 1,
    "Queen": 1,
    "Bishop": 2,
    "Knight": 2
    }
empty_cell = '-'

def main():
    board = initiate_new_board()
    good_input = False
    print("Welcome to the game!")
    print("Type 'r' to populate the board randomly, or 'm' to assign all pieces manually: ")
    while good_input == False:
        user_input = input("")
        if user_input.lower() == 'r':
            board = add_pieces_randomly(board)
            good_input = True
        elif user_input.lower() == 'm':
            board = prompt_for_white_piece(board)
            board = prompt_for_black_pieces(board)
            good_input = True
        else:
            print("Invalid input, only 'r' or 'm' accepted. Try again: ")
    determine_possible_moves(board)

def initiate_new_board():
    columns = "ABCDEFGH"
    rows = list(range(1,9))[::-1]
    empty_board = {}

    for number in rows:
        empty_board[number] = {}
        for letter in columns:
            empty_board[number][letter] = empty_cell
    return empty_board

def print_current_board(board):
    print("")
    col_names = "   "

    for row in board:
        for key in board[row]:
            col_names += f" {key}  "
        break
    print(col_names)
    print("  "+"_" * 33)
    temp = ""
    for key1, value1 in board.items():
        temp += f"{key1} |"
        for key2, value2 in board[key1].items():
            if (int(key1) % 2 == 1 and key2 in 'ACEG') or (int(key1) % 2 == 0 and key2 in 'BDFH'):
                if value2 == empty_cell:
                    temp += f"···|"
                else:
                    temp += f"·{value2}·|"
            else:
                    temp += f" {value2} |"
        temp += f" {key1}"
        print(temp)
        temp = ""
    print("  "+"‾" * 33)
    print(col_names)
    print("")

def prompt_for_white_piece(board):
    good_input = False

    while good_input == False:
        user_input = input('Enter the name of a white chest piece (Rook or Pawn only) and it\'s position seperated by space (e.g. "Rook D9"): ')
        user_input = re.sub(r'\s+', ' ', user_input).strip()
        spaces_in_input = user_input.count(" ")

        if spaces_in_input != 1:
            print("Exactly two values separated by a space are required.")
            continue
        
        user_input = user_input.split()
        piece = user_input[0].title()
        position = user_input[1].upper()
        current_board = board
        y = position[1]
        x = position[0]

        if piece not in white_pieces:
            print(f"Bad piece name. Available options: {', '.join(white_pieces)}")
        elif len(position) != 2:
            print("Invalid position length - it must be exactly 2 characters.")
        elif x.isalpha() == False or str(y).isdigit() == False:
            print("Invalid position format - it must be 1 letter followed by 1 integer.")
        elif x > "H" or int(y) < 1 or int(y) > 8:
            print("Invalid position - out of range")
        else:
            print(f"A white {piece} has been added to {position}: ")
            good_input = True
            current_board[int(y)][x] = white_pieces[piece]
            print_current_board(current_board)
            return current_board  

def prompt_for_black_pieces(board):
    done = False
    pieces_added = 0
    current_board = board
    
    while done == False:
        user_input = input('Enter the name of a black chest piece and it\'s position seperated by space (e.g. "Queen c3"): ')
        user_input = re.sub(r'\s+', ' ', user_input).strip()
        spaces_in_input = user_input.count(" ")

        if user_input.lower() == "done":
            if pieces_added > 0:
                done = True
                print(f"A total of {pieces_added} black pieces have been added.")
                print("")
                return current_board
            else:
                print("At least 1 black chess piece must be added.")
                continue
        elif spaces_in_input != 1:
            print("Exactly two values separated by a space are required.")
            continue

        user_input = user_input.split()
        piece = user_input[0].title()
        position = user_input[1].upper()
        y = position[1]
        x = position[0]
        
        if piece not in black_pieces:
            print(f"Invalid piece name. Available choices: {', '.join(black_pieces)}")
        elif len(position) != 2:
            print("Invalid position length - it must be exactly 2 characters long.")
        elif x.isalpha() == False or str(y).isdigit() == False:
            print('Invalid position format - it must be one letter + one integer (e.g. "d7").')
        elif x > "H" or int(y) < 1 or int(y) > 8:
            print("Invalid position - only letters A-H and numbers 1-8 are accepted.")
        elif piece in black_pieces and remaining_black_pieces[piece] == 0:
            print(f"Invalid: there are no more {piece} pieces left.")
        elif current_board[int(y)][x] != empty_cell:
            print(f"Position {x}{y} is already taken.")
        else:
            print(f"A black {piece} has been added to {position}.")
            current_board[int(y)][x] = black_pieces[piece]
            pieces_added += 1
            remaining_black_pieces[piece] -= 1
            print_current_board(current_board)

            if pieces_added == 16:
                print("All 16 black pieces have been added: ")
                done = True
                return current_board

def add_pieces_randomly(board):

    done = False
    current_board = board
    added_black_pieces = 0
    random_white_item = random.choice(list(white_pieces.items()))
    x1 = random.choice('ABCDEFGH')
    y1 = random.randint(1, 8)

    print("All pieces are being placed randomly: ")
    current_board[y1][x1] = random_white_item[1]
    print(f"- White {random_white_item[0]}: {x1}{y1}")

    while done == False:
        random_black_item = random.choice(list(black_pieces.items()))
        x2 = random.choice('ABCDEFGH')
        y2 = random.randint(1, 8)
     
        if remaining_black_pieces[random_black_item[0]] != 0 and current_board[y2][x2] == empty_cell:
            current_board[y2][x2] = random_black_item[1]
            added_black_pieces += 1
            remaining_black_pieces[random_black_item[0]] -= 1
            time.sleep(0.05)
            print(f"- Black {random_black_item[0]}: {x2}{y2}")
            if added_black_pieces == 16:
                done = True
                print("All 16 black pieces have been added.")
                print("")
                return current_board
        else:
            continue

def determine_possible_moves(board):
    current_board = board

    white_piece_position = ""
    x = ""
    y = ""

    white_piece_symbol = ""
    white_piece_name = ""

    hittable_positions = []
    hittable_names = []

    for row in current_board:
        for col in current_board[row]:
            if current_board[row][col] in white_pieces.values():
                white_piece_position = col + str(row)
                x = int(white_piece_position[1])
                y = white_piece_position[0]
                white_piece_symbol = current_board[row][col]
                current_board[row][col] = f"\033[32m{current_board[row][col]}\033[0m"
                for key, value in white_pieces.items():
                    if value == white_piece_symbol:
                        white_piece_name = key                        
                        print(f"\033[32mWhite {key}\033[0m is at {col}{row}.")

    if white_piece_symbol == '\u2659': #pawn
        if x == 8:
            pass
        elif y == 'A':
            row = x + 1
            col = chr(ord(y) + 1)
            if current_board[row][col] == empty_cell:
                pass
            else:           
                for key, value in black_pieces.items():
                    if value == current_board[row][col]:
                        hittable_positions.append(col + str(row))
                        hittable_names.append(key)
                        current_board[row][col] = f"\033[31m{value}\033[0m"
        elif y == 'H':
            row = x + 1
            col = chr(ord(y) - 1)
            if current_board[row][col] == empty_cell:
                pass
            else:           
                for key, value in black_pieces.items():
                    if value == current_board[row][col]:
                        hittable_positions.append(col + str(row))
                        hittable_names.append(key)
                        current_board[row][col] = f"\033[31m{value}\033[0m"
        else:
            row = x + 1
            cols = [
                chr(ord(y) + 1),
                chr(ord(y) - 1)
                ]
            if current_board[row][cols[0]] == empty_cell and current_board[row][cols[1]] == empty_cell:
                pass
            else:   
                for c in cols:        
                    for key, value in black_pieces.items():
                        if value == current_board[row][c]:
                            hittable_positions.append(c + str(row))
                            hittable_names.append(key)
                            current_board[row][c] = f"\033[31m{value}\033[0m"

    elif white_piece_symbol == '\u2656': #rook
        dist_to_top = 8 - x
        dist_to_bottom = x - 1
        dist_to_right = ord('H') - ord(y)
        dist_to_left = ord(y) - ord('A')

        x1 = x
        y1 = y
        stop_outer = False

        for i in range(dist_to_top):
            x1 += 1
            if current_board[x1][y1] == empty_cell:
                continue
            else:
                for key, value in black_pieces.items():
                    if current_board[x1][y1] == value:
                        hittable_positions.append(y1 + str(x1))
                        hittable_names.append(key)
                        current_board[x1][y1] = f"\033[31m{value}\033[0m"
                        stop_outer = True
            if stop_outer == True:
                break
        x1 = x
        stop_outer == False
        
        for i in range(dist_to_bottom):
            x1 -= 1
            if current_board[x1][y1] == empty_cell:
                continue
            else:
                for key, value in black_pieces.items():
                    if current_board[x1][y1] == value:
                        hittable_positions.append(y1 + str(x1))
                        hittable_names.append(key)
                        current_board[x1][y1] = f"\033[31m{value}\033[0m"
                        stop_outer = True
            if stop_outer == True:
                break
        x1 = x
        stop_outer == False

        for i in range(dist_to_right):
            y1 = chr(ord(y1) + 1)
            if current_board[x1][y1] == empty_cell:
                continue
            else:
                for key, value in black_pieces.items():
                    if current_board[x1][y1] == value:
                        hittable_positions.append(y1 + str(x1))
                        hittable_names.append(key)
                        current_board[x1][y1] = f"\033[31m{value}\033[0m"
                        stop_outer = True
            if stop_outer == True:
                break
        y1 = y
        stop_outer == False

        for i in range(dist_to_left):
            y1 = chr(ord(y1) - 1)
            if current_board[x1][y1] == empty_cell:
                continue
            else:
                for key, value in black_pieces.items():
                    if current_board[x1][y1] == value:
                        hittable_positions.append(y1 + str(x1))
                        hittable_names.append(key)
                        current_board[x1][y1] = f"\033[31m{value}\033[0m"
                        stop_outer = True
            if stop_outer == True:
                break
        y1 = y
        stop_outer == False

    if len(hittable_positions) == 0:
        print(f"There is nothing for \033[32mWhite {white_piece_name}\033[0m to hit.")
    else:
        message = f"\033[32mWhite {white_piece_name}\033[0m can hit: "
        for key, value in enumerate(hittable_positions):
            message += f"\n\033[31m- Black {hittable_names[key]}\033[0m at {hittable_positions[key]}"
        print(message)

    print_current_board(current_board)

if __name__ == "__main__":
    main()