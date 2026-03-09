from mazegen.Parsing import Parsing
from mazegen.Errors import BaseConfFileErrors, FileEmptyError
from pydantic import ValidationError


def parse_errors(errors: list) -> None:
    """
    parse given errors from errors list

    :param errors: list of errors objects
    :type errors: list
    """
    i = 1
    for e in errors:
        if e['type'] == 'value_error':
            print(f"Error ({i}):", e['msg'])
        else:
            print(f"Error ({e['loc'][0]}):", e['msg'])
        i += 1


def resolve_conf(conf_file: str) -> dict:
    """
    unpack configurations from conf_file to parse them

    :param conf_file: conf file name
    :type conf_file: str
    :return: dict of validated parsed configurations
    :rtype: dict
    """
    result: dict = {}
    try:
        re: str = open(conf_file, 'r').read()
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
