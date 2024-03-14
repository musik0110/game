import random

def print_board(player_board, computer_board, hide_computer_ships=True):
    print("Ваша доска:")
    for row in player_board:
        print(" ".join(row))
    
    print("Доска компьютера:")
    for row in computer_board:
        if hide_computer_ships:
            row = ['O' if cell == 'X' else cell for cell in row]
        print(" ".join(row))

def create_board():
    return [["O" for _ in range(5)] for _ in range(5)]

def is_ship_nearby(board, row, col):
    neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1),
                 (row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)]
    for r, c in neighbors:
        if 0 <= r < 5 and 0 <= c < 5 and board[r][c] == "X":
            return True
    return False

def is_ship_nearby_single(board, row, col):
    neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in neighbors:
        if 0 <= r < 5 and 0 <= c < 5 and board[r][c] == "X":
            return True
    return False

def is_ship_sunk(board, row, col):
    return board[row][col] == "W"

def manual_place_ship(board, ship_length):
    try:
        row = int(input("Введите номер строки для размещения корабля (0-4): "))
        col = int(input("Введите номер столбца для размещения корабля (0-4): "))

        if is_ship_nearby(board, row, col):
            print("Невозможно разместить корабль рядом с другим кораблем. Попробуйте еще раз.")
            manual_place_ship(board, ship_length)
        elif ship_length == 1:
            if board[row][col] == "X" or is_ship_nearby(board, row, col):
                print("Невозможно разместить корабль здесь. Попробуйте еще раз.")
                manual_place_ship(board, ship_length)
            else:
                board[row][col] = "X"
                print("Корабль успешно размещен!")
        elif ship_length == 2:
            orientation = input("Выберите ориентацию (v - вертикальная, h - горизонтальная): ")
            if orientation == "v":
                if row < 4 and board[row][col] == "O" and board[row + 1][col] == "O" and not is_ship_nearby_single(board, row + 1, col):
                    board[row][col] = "X"
                    board[row + 1][col] = "X"
                    print("Корабль успешно размещен!")
                else:
                    print("Невозможно разместить корабль здесь. Попробуйте еще раз.")
                    manual_place_ship(board, ship_length)
            elif orientation == "h":
                if col < 4 and board[row][col] == "O" and board[row][col + 1] == "O" and not is_ship_nearby_single(board, row, col + 1):
                    board[row][col] = "X"
                    board[row][col + 1] = "X"
                    print("Корабль успешно размещен!")
                else:
                    print("Невозможно разместить корабль здесь. Попробуйте еще раз.")
                    manual_place_ship(board, ship_length)
            else:
                print("Некорректная ориентация. Попробуйте еще раз.")
                manual_place_ship(board, ship_length)
        else:
            print("Некорректная длина корабля. Попробуйте еще раз.")
            manual_place_ship(board, ship_length)

    except (ValueError, IndexError):
        print("Некорректные значения. Повторите ввод.")
        manual_place_ship(board, ship_length)

def place_ship(board):
    ship_row = random.randint(0, 4)
    ship_col = random.randint(0, 4)
    board[ship_row][ship_col] = "X"

def random_place_ship(board, ship_length):
    while True:
        ship_row = random.randint(0, 4)
        ship_col = random.randint(0, 4)

        if ship_length == 1 and not is_ship_nearby(board, ship_row, ship_col):
            board[ship_row][ship_col] = "X"
            break
        elif ship_length == 2:
            orientation = random.choice(["v", "h"])

            if orientation == "v" and ship_row < 4 and board[ship_row][ship_col] == "O" and board[ship_row + 1][ship_col] == "O" and not is_ship_nearby_single(board, ship_row + 1, ship_col):
                board[ship_row][ship_col] = "X"
                board[ship_row + 1][ship_col] = "X"
                break
            elif orientation == "h" and ship_col < 4 and board[ship_row][ship_col] == "O" and board[ship_row][ship_col + 1] == "O" and not is_ship_nearby_single(board, ship_row, ship_col + 1):
                board[ship_row][ship_col] = "X"
                board[ship_row][ship_col + 1] = "X"
                break

def get_player_move():
    try:
        row = int(input("Введите номер строки (0-4): "))
        col = int(input("Введите номер столбца (0-4): "))
        return row, col
    except ValueError:
        print("Введите корректные значения.")
        return get_player_move()

def get_computer_move():
    row = random.randint(0, 4)
    col = random.randint(0, 4)
    return row, col

def is_all_ships_sunk(board):
    for row in board:
        for cell in row:
            if cell == "X":
                return False
    return True

def main():
    player_board = create_board()
    computer_board = create_board()

    print_board(player_board, computer_board)
    print("Разместите свои корабли:")
    
    print("Разместите одноклеточный корабль:")
    manual_place_ship(player_board, 1)
    
    print("Разместите двухклеточный корабль:")
    manual_place_ship(player_board, 2)

    print("Компьютер размещает корабли:")
    random_place_ship(computer_board, 1)
    random_place_ship(computer_board, 2)
    
    while True:
        print_board(player_board, computer_board, hide_computer_ships=True)

        print("Ваш ход:")
        player_row, player_col = get_player_move()

        if computer_board[player_row][player_col] == "X" and not is_ship_sunk(computer_board, player_row, player_col):
            print("Поздравляем! Вы попали в корабль компьютера!")

            # Check if the ship is sunk
            if is_ship_nearby_single(computer_board, player_row, player_col):
                print("Вы потопили корабль компьютера!")
                computer_board[player_row][player_col] = "W"
                if is_all_ships_sunk(computer_board):
                    print("Вы потопили все корабли компьютера! Победа!")
                    break
            else:
                computer_board[player_row][player_col] = "H"  # Mark as hit

        else:
            print("Промах! Ход компьютера.")
            computer_board[player_row][player_col] = "M"

        computer_row, computer_col = get_computer_move()

        if player_board[computer_row][computer_col] == "X" and not is_ship_sunk(player_board, computer_row, computer_col):
            print("Компьютер попал по вашему кораблю!")

            # Check if the player's ship is sunk
            if is_ship_nearby_single(player_board, computer_row, computer_col):
                print("Компьютер потопил ваш корабль!")
                player_board[computer_row][computer_col] = "W"
                if is_all_ships_sunk(player_board):
                    print("Все ваши корабли потоплены! Вы проиграли.")
                    break
            else:
                player_board[computer_row][computer_col] = "H"  # Mark as hit

        else:
            print("Компьютер промахнулся.")
            player_board[computer_row][computer_col] = "M"

if __name__ == "__main__":
    main()