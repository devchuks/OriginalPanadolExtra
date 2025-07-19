import random
import time

def get_valid_guess_range(player_count):
    return 0, player_count * 5

def get_unique_guesses(player_names, existing_guesses=None):
    guesses = existing_guesses if existing_guesses else {}
    valid_min, valid_max = get_valid_guess_range(len(player_names))
    already_chosen = set(guesses.values())

    print(f"\nEach player must choose a unique number between {valid_min} and {valid_max}\n")
    
    for name in player_names:
        if name in guesses:
            continue  # already has a valid guess
        while True:
            try:
                guess = int(input(f"{name}, enter your guess: "))
                if guess < valid_min or guess > valid_max:
                    print(f"Guess must be between {valid_min} and {valid_max}")
                elif guess in already_chosen:
                    print("This number has already been taken by another player")
                else:
                    guesses[name] = guess
                    already_chosen.add(guess)
                    break
            except ValueError:
                print("Enter a valid number abeg")
    return guesses

def chant_intro():
    chant_lines = [
        "\n🎵 After round one...",
        "🎵 original Panadol extra...",
        "🎵 otun gbede...",
        "🎵 Babangida YASO!'"
    ]
    for line in chant_lines:
        print(line)
        time.sleep(1)

def say_yaso():
    print("\n🗣️ YASO!\n")
    time.sleep(1)

def check_and_update_invalid_guesses(active_players, guesses):
    valid_min, valid_max = get_valid_guess_range(len(active_players))
    current_guesses = set(guesses[player] for player in active_players)
    updated = False

    for player in active_players:
        guess = guesses[player]
        if guess > valid_max:
            print(f"\n⚠️ {player}'s number {guess} is no longer possible (maximum fingers is now {valid_max})")
            # remove temporarily from guesses so they can pick a new unique one
            del guesses[player]
            new_guess = None
            while True:
                try:
                    new_guess = int(input(f"{player}, pick a new number (0 to {valid_max}): "))
                    if new_guess < 0 or new_guess > valid_max:
                        print("Invalid range")
                    elif new_guess in guesses.values():
                        print("That number has already been picked, bossman")
                    else:
                        guesses[player] = new_guess
                        updated = True
                        break
                except ValueError:
                    print("Enter a valid number abeg")
    return updated

def play_game(player_names, guesses):
    active_players = player_names[:]
    round_num = 1

    # First round: full chant, no pause after
    chant_intro()
    finger_shows = {player: random.randint(0, 5) for player in active_players}
    total = sum(finger_shows.values())

    print("🖐️ Fingers shown:")
    for player, fingers in finger_shows.items():
        print(f"  {player}: {fingers}")
    print(f"➕ Total fingers: {total}")

    eliminated = None
    for player in active_players:
        if guesses[player] == total:
            eliminated = player
            break

    if eliminated:
        print(f"\n🎉 {eliminated}'s number ({guesses[eliminated]}) was matched! E don go")
        active_players.remove(eliminated)
        check_and_update_invalid_guesses(active_players, guesses)
    else:
        print("\nNo match this round. Game continues")

    round_num += 1

    # Remaining rounds
    while len(active_players) > 2:
        input(f"\n🔁 Press Enter to start ROUND {round_num}...")
        say_yaso()

        finger_shows = {player: random.randint(0, 5) for player in active_players}
        total = sum(finger_shows.values())

        print("🖐️ Fingers shown:")
        for player, fingers in finger_shows.items():
            print(f"  {player}: {fingers}")
        print(f"➕ Total fingers: {total}")

        eliminated = None
        for player in active_players:
            if guesses[player] == total:
                eliminated = player
                break

        if eliminated:
            print(f"\n🎉 {eliminated}'s number ({guesses[eliminated]}) was matched! E don go")
            active_players.remove(eliminated)
            check_and_update_invalid_guesses(active_players, guesses)
        else:
            print("\nNo match this round. Game continues")

        round_num += 1

    # Final round
    print(f"\n🏁 FINAL ROUND between {active_players[0]} and {active_players[1]}!")

    while True:
        input("\n🔁 Press Enter for final YASO...")
        say_yaso()

        finger_shows = {player: random.randint(0, 5) for player in active_players}
        total = sum(finger_shows.values())

        print("🖐️ Fingers shown:")
        for player, fingers in finger_shows.items():
            print(f"  {player}: {fingers}")
        print(f"➕ Total fingers: {total}")

        for player in active_players:
            if guesses[player] == total:
                winner = player
                loser = [p for p in active_players if p != winner][0]
                print(f"\n🏆 {winner} WINS! 🎉")
                print(f"😬 baba {loser} never got guessed... slap their hand joor")
                return

        print("No match yet. Trying again...\n")

# Entry point
def main():
    print("👋 AFTER ROUND ONE JARE")
    while True:
        try:
            player_count = int(input("Enter number of players (2 or more): "))
            if player_count < 2:
                print("You need at least 2 players")
            else:
                break
        except ValueError:
            print("Enter a valid number")
    
    player_names = [input(f"Enter name for player {i+1}: ") for i in range(player_count)]
    guesses = get_unique_guesses(player_names)
    play_game(player_names, guesses)

# Uncomment to run
main()
