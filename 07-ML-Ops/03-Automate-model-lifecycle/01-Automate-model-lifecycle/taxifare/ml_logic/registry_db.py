
# YOUR CODE HERE

from colorama import Fore, Style


def get_next_first_row(experiment: str) -> int:
    """
    Get the rank of the next first row to be trained in the Mlflow experiment database
    parameters:
    - experiment: experiment name (str)
    returns:
    - next_row: rank of the next first row to be trained (int)
    """

    print(Fore.BLUE + "\nRetrieve last trained row from mlflow db..." + Style.RESET_ALL)

    # get latest trained row
    # YOUR CODE HERE

    print(f"\n✅ Rank of the next first row to train: row {next_row}")

    return next_row
