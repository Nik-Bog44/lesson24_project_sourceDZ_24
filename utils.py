import re
from typing import Iterator, Any, Optional, Dict, Callable

from constants import DATA_DIR


def log_generator() -> Iterator[str]:
    with open(DATA_DIR) as file:
        log_string: list(str) = file.readlines()
        for log in log_string:
            yield log


def user_filter(param: str, generator: Iterator[str]) -> Iterator[str]:
    return filter(lambda x: param in x, generator)


def user_map(param: int, generator: Iterator[str]) -> Iterator[str]:
    return map(lambda string: string.split()[int(param)], generator)


def user_unique(generator: Iterator[str], *args: Any, **kwargs: Any) -> Iterator[str]:
    list_t: list(str) = []
    for string in generator:
        if string not in list_t:
            list_t.append(string)
            yield string


def user_sort(param: str, generator: Iterator[str]) -> Iterator[str]:
    return iter(sorted(generator, reverse='desc' == param))


def user_limit(param: str, generator: Iterator[str]) -> Iterator[str]:
    counter = 1
    for string in generator:
        if counter > int(param):
            break

        counter += 1
        yield string


def regex_query(param: str, generator: Iterator[str]) -> Iterator[str]:
    pattern: re.Pattern = re.compile(param)
    return filter(lambda x: re.search(pattern, x), generator)


dict_of_utils: Dict[str, Callable[..., Iterator[str]]] = {
    'filter': user_filter,
    'map': user_map,
    'unique': user_unique,
    'sort': user_sort,
    'limit': user_limit,
    'regex': regex_query
}

