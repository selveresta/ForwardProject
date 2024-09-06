import random
from .consts import comments


def generate_random_comment():
    n = random.randint(0, len(comments) - 1)

    return comments[n]
