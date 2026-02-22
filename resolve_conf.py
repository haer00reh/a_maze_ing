from dotenv import dotenv_values
from Parsing import Parsing
from Errors import BaseConfFileErrors, FileEmptyError
from pydantic import ValidationError


def parse_errors(errors: list) -> None:
    i = 1
    for e in errors:
        if e['type'] == 'value_error':
            print(f"Error ({i}):", e['msg'])
        else:
            print(f"Error ({e['loc'][0]}):", e['msg'])
        i += 1


def resolve_conf() -> dict:
    env: dict = {**dotenv_values()}
    result: dict = {}
    try:
        conf_file: str | None = env.get('conf_file')
        re: str = open(conf_file or "config.txt", 'r').read()
        if len(re) <= 0:
            raise FileEmptyError("the configuratoin file can't be empty")
    except (BaseConfFileErrors):
        print("Error: configuration file is empty")
        return result
    except FileNotFoundError:
        print("Error: configuration file not found")
        return result

    try:
        content: dict = Parsing.get_conf(re)
    except ValueError as e:
        print("Error:", e)
        return result
    try:
        conf: Parsing = Parsing(**content)
    except ValidationError as e:
        parse_errors(e.errors())
        return result
    else:
        result = (conf.__dict__)
    return result
