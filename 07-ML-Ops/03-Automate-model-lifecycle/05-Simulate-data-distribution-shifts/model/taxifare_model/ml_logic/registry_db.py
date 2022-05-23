
# YOUR CODE HERE

from colorama import Fore, Style


def get_latest_trained_row(experiment):

    print(Fore.BLUE + "\nRetrieve last trained row from mlflow db..." + Style.RESET_ALL)

    # get latest trained row
    # YOUR CODE HERE

    print(f"\n✅ last trained rows: row {next_row}")

    return next_row
