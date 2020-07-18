import random
import string


def random_num_gen(string_length):
    """
    Generates random numbers with the given length.

    Parameters:
        string_length(int): Length of the generated number.

    Returns:
        string: random string of the given length.
    """
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(string_length))


def decorate_heading(heading):
    """
    Decorates the heading for each page.

    Parameters:
        heading(string): The heading for a page
    """
    print(("."*30) + heading + ("."*30))


