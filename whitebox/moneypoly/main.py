""" Takes player names as input, Running the game
and and handle errors """

from moneypoly.game import Game


def get_player_names():
    """ Takes the input of player names and returs list of names. """
    print("Enter player names separated by commas (minimum 2 players):")
    raw = input("> ").strip()
    names = [n.strip() for n in raw.split(",") if n.strip()]
    return names


def main():
    """ This is the main function.
    it calls get_player_names function
    and handle errors which can occur during game setup. """
    names = get_player_names()
    try:
        game = Game(names)
        game.run()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!")
    except ValueError as exc:
        print(f"Setup error: {exc}")


if __name__ == "__main__":
    main()
