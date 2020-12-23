import re
from typing import List, Union


def sanitize(
    input: Union[int, float, str, List[str]]
) -> Union[int, float, str, List[str]]:
    """Sanitizes input to contain only unicode words, hyphens, or spaces

    Args:
        input: Input to sanitize

    Returns:
        Sanitized input
    """
    if type(input) == int:
        return input
    if type(input) == float:
        return input
    if type(input) == str:
        inputs = [input]
    elif type(input) == list:
        inputs = input
    else:
        raise NotImplementError

    for e, i in enumerate(inputs):
        if type(i) == str:
            inputs[e] = re.sub("[^\w\-\+\.\>\)\(\ \:]+", "", i, re.UNICODE)
        elif type(i) == int:
            inputs[e] = i
        elif type(i) == float:
            inputs[e] = i
        else:
            raise NotImplementError

    if type(input) == str:
        assert len(inputs) == 1
        return inputs[0]
    else:
        return inputs
