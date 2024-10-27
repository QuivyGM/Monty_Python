#type random string given as quick as possible

import random
import time



def generate_random_string(mode='number'):
    """create random string"""
    if mode == 'number':
        return str(random.randint(10000, 99999))
    else:
        return ''.join(random.choices('ACBDEFGHIJKLMNOPQRSTUVWXYZ', k=5))

def reaction_time_game(mode='number'):
    """Start reflex game"""
    random_string = generate_random_string(mode)
    print(f"\nrandom { 'Number' if mode == 'number' else 'letter'}: {random_string}")

    start_time = time.time()
    user_input = input("Enter: ")
    reaction_time = time.time() - start_time

    if user_input == random_string:
        accuracy = sum(a==b for a,b in zip(user_input, random_string))/len(random_string)*100
        print(f"Success! {reaction_time:.2f} seconds. Accuracy is {accuracy:.2f}%.")
    else:
        print("Try again.")

    return reaction_time, user_input == random_string

def main():
    """Start main loop of the game"""
    print("===Reaction Game===")
    print("1: Number Mode")
    print("2: Letter Mode")
    print("3: Terminate")

    scores = []

    while True:
        choice = input("\nSelect an option (1/2/3):")

        if choice == '3':
            break
        elif choice in ['1', '2']:
            mode = 'number' if choice == '1' else 'letter'
            reaction_time, success = reaction_time_game(mode)
            scores.append((mode, reaction_time,success))
        else:
            print("Try again.")

    print("\n===Game Result ===")
    for i, (mode, time, success) in enumerate(scores, 1):
        print(f"{i}. Mode: {'Number'if mode == 'number' else 'Letter'}, Time: {time:.2f}s, {'Successful' if success else 'Failed'}")

if __name__ == '__main__':
    main()
