def check_winner(board):
    for row in board:  
        if row[0] == row[1] == row[2] and row[0] in ('X', '0'):
            return row[0]

    for col in range(3):  
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] in ('X', '0'):
            return board[0][col]

    return "Draw"  

def save_result(winner, game_num):
    file = open("X_0_results.txt", "a")  
    file.write(f"Game {game_num}: Winner - {winner}\n")
    file.close()  

game_num = 1
while True:
    print(f"Game {game_num}. Enter the game board:")
    board = [list(input().strip()) for _ in range(3)]
    winner = check_winner(board)
    print(f"Winner: {winner}")

    save_result(winner, game_num)
    
    next_game = input("Do you want to play another game? (yes/no): ").strip().lower()
    if next_game != "yes":
        break

    game_num += 1

print("Game over! Results saved in X_0_results.txt.")



