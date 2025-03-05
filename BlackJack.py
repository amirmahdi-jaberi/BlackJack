import random
import time

# Initialize total scores for User and Device
total_score = {'User': 0, 'Device': 0}

# Function to choose a random card from the deck
def choice_card():
    Options = list(card_list.keys())
    while True:
        card = random.choice(Options)
        if card_list[card] == 4:  # Skip if all 4 cards of this type have been used
            continue
        card_list[card] += 1  # Increment usage count
        if card in image:  # Replace face cards with their respective values
            card = image[card]
        return int(card)

# Function to determine the winner based on scores
def choosing_winner(user_rate, device_rate):
    if device_rate > 21:  # Device loses if its score exceeds 21
        print('You Won <>-<>\n')
        total_score['User'] += 1
    elif device_rate >= user_rate and device_rate <= 21:  # Device wins if its score is higher and <= 21
        print('You lost "|"\n')
        total_score['Device'] += 1
    else:  # Otherwise, user wins
        print('You Won <>-<>\n')
        total_score['User'] += 1

# Function to handle the device's turn
def device_turn(user_rate, device_rate):
    global turn
    if turn == 'd1':  # First turn for the device
        turn = 'u'  # Switch turn to user
        device.append(choice_card())  # Add the chosen card to the device's hand
    else:
        if device_rate <= 16:  # Device draws a card if its score is <= 16
            time.sleep(2)  # Simulate thinking time
            card = choice_card()
            print(f'<> Device Card : {card}\n')
            device.append(card)  # Add the chosen card to the device's hand
        elif device_rate >= 17 and device_rate <= 21:  # Device stops if its score is between 17 and 21
            print("Device decides to stop.\n")
            choosing_winner(user_rate, device_rate)
            return True
        else:  # Device loses if its score exceeds 21
            print("Device went over 21 and lost.\n")
            total_score['User'] += 1
            return True

# Function to display current scores
def display_scores():
    print(f"Round {round_counter}:")
    print(f"User Total Score: {total_score['User']}, Device Total Score: {total_score['Device']}\n")

# Function to suggest a move to the user
def suggest_move(user_rate):
    if user_rate < 15:
        print("Suggestion: You should take another card.\n")
    elif user_rate >= 15 and user_rate <= 19:
        print("Suggestion: It's risky, but you can try another card.\n")
    else:
        print("Suggestion: Stop taking cards.\n")

# Main game loop
max_rounds = 5  # Maximum number of rounds
for round_counter in range(1, max_rounds + 1):
    print(f"Starting Round {round_counter}...\n")

    # Reset game variables for each round
    card_list = {'5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, 'j': 0, 'q': 0, 'k': 0}
    image = {'j': 2, 'q': 3, 'k': 4}
    device = []
    user = []
    turn = 'd1'

    while True:
        card = choice_card()
        if turn in ['d1', 'd2']:  # If it's the device's turn
            if device_turn(sum(user), sum(device)):
                break  # Break if the game round ends
        elif turn == 'u':  # If it's the user's turn
            user.append(card)
            print(f'>< User Card : {card}\n')

            # Check if user loses or wins
            if sum(user) > 21:  # User loses if their score exceeds 21
                print(f'You lost, The total of your cards reached {sum(user)} and is higher than 21 \n')
                total_score['Device'] += 1
                break
            elif sum(user) == 21:  # User wins if their score is exactly 21
                print(f'You won great <>-<>\n')
                total_score['User'] += 3
                break

            # Suggest move to the user
            suggest_move(sum(user))

            # Ask user if they want another card
            q = input('Do you want a card? y|n : ')
            if q == 'y':
                continue
            elif q == 'n':
                turn = 'd2'
                print(f'Device first Card : {device[0]}\n')


# Display final scores
print("Game Over! Final Scores:")
display_scores()

# Save results to a file
try:
    with open("results.txt", "a") as file:
        file.write(f"Final Scores: User-{total_score['User']}, Device-{total_score['Device']}\n")
except Exception as e:
    print(f"Error saving results to file: {e}")