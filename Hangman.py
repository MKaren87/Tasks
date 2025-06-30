import random
import os

HANGMAN_PICS = [
    '''
    ╔═══════╗
    ║       ║
            ║
            ║
            ║
            ║
    ═════════════''',
    '''
    ╔═══════╗
    ║       ║
    😐      ║
            ║
            ║
            ║
    ═════════════''',
    '''
    ╔═══════╗
    ║       ║
    😕      ║
    │       ║
            ║
            ║
    ═════════════''',
    '''
    ╔═══════╗
    ║       ║
    😟      ║
   /│       ║
            ║
            ║
    ═════════════''',
    '''
    ╔═══════╗
    ║       ║
    😧      ║
   /│\\     ║
            ║
            ║
    ═════════════''',
    '''
    ╔═══════╗
    ║       ║
    😵      ║
   /│\\     ║
   /        ║
            ║
    ═════════════''',
    '''
    ╔═══════╗
    ║       ║
    ☠️      ║
   /│\\     ║
   / \\     ║
            ║
    ═════════════'''
]

def load_words(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        print(f"⚠️ Error: The file '{filename}' was not found.")
        return []
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def hangman():
    words = load_words('words.txt')
    word = random.choice(words)
    guessed = set()
    incorrect = 0
    max_incorrect = len(HANGMAN_PICS) - 1
    display = ['_'] * len(word)

    while incorrect < max_incorrect and '_' in display:
        clear_screen()
        print(HANGMAN_PICS[incorrect])
        print(f"\nWord: {' '.join(display)}")
        print(f"Guessed letters: {' '.join(sorted(guessed))}")
        print(f"Mistakes left: {max_incorrect - incorrect}\n")

        guess = input("Your guess: ").lower()

        if not guess.isalpha() or len(guess) != 1:
            print("⚠️ Please enter a single letter.")
            input("Press Enter to continue...")
            continue
        if guess in guessed:
            print("❗ You already guessed that.")
            input("Press Enter to continue...")
            continue

        guessed.add(guess)

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    display[i] = guess
        else:
            incorrect += 1

    clear_screen()
    print(HANGMAN_PICS[incorrect])
    if '_' not in display:
        print(f"\n🎉 You won! The word was: {word}")
    else:
        print(f"\n💀 Game over. The word was: {word}")

if __name__ == "__main__":
    hangman()