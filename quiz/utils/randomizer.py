import random
from copy import deepcopy


def shuffle_questions(questions):
    """
    Shuffle questions and return new list + order map.
    """
    shuffled = deepcopy(questions)
    random.shuffle(shuffled)

    order = [str(q.id) for q in shuffled]
    return shuffled, order


def shuffle_options(question):
    """
    Shuffle options of a question and return:
    - shuffled options
    - option order mapping
    """
    options = deepcopy(question.options)
    random.shuffle(options)

    order_map = [str(opt.id) for opt in options]
    return options, order_map


def build_option_order_map(questions):
    """
    Build option order map for all questions.
    """
    option_order_map = {}

    for q in questions:
        _, order = shuffle_options(q)
        option_order_map[str(q.id)] = order

    return option_order_map
