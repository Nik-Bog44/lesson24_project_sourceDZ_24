import os
from typing import Union, Optional, Callable, Iterator

from flask import Flask, render_template, request, Response

from constants import BASE_DIR
from utils import dict_of_utils, log_generator

app = Flask(__name__)


@app.get('/')
def index() -> str:
    return render_template('index.html')


@app.post("/perform_query")
def perform_query() -> Union[str, Response]:
    file_name: str = request.form.get('file_name')
    cmd1: str = request.form.get('cmd1')
    value1: str = request.form.get('value1')
    cmd2: str = request.form.get('cmd2')
    value2: str = request.form.get('value2')

    if any(arg is None for arg in [file_name, cmd1, value1, cmd2, value2]):
        return Response("Не все поля заполнены", 400)

    file_path = os.path.join(BASE_DIR, '/data/', file_name)

    if not os.path.exists(file_path):
        return Response("Файл не найден", 400)

    default_generator = log_generator()

    first_func: Optional[Callable] = dict_of_utils.get(cmd1)
    second_func: Optional[Callable] = dict_of_utils.get(cmd2)

    result: Optional[Iterator[str]] = None
    if first_func is not None:
        result = first_func(param=value1, generator=default_generator)
    if second_func is not None:
        result = second_func(param=value2, generator=result)

    return render_template('block.html', items=result)


if __name__ == '__main__':
    app.run(port=25000)
