from typing import Optional, List
from pydantic import BaseModel, Field, model_validator


def is_empty(s: str) -> bool:
    return s == ""


class Parsing(BaseModel):
    width: int = Field(
        ge=6, description="width conf should be greater than 6"
        )
    height: int = Field(
        ge=7, description="height conf should be greater than 6"
    )
    entry: tuple = Field(
        description="enty should be valid cordinates x,y"
    )
    exit: tuple = Field(
        description="exit should be valid cordinates x,y"
    )
    output_file: str = Field(
        max_length=10,
        min_length=3,
        description="output file should be of type string with max length 10"
    )
    perfect: bool = Field(
        description="perfect argument should be valid boolian (True or False)"
    )
    seed: Optional[int] = Field(
        description="seed field should be valid number"
    )
    seeded: bool = False

    @staticmethod
    def get_conf(data: str) -> dict:
        conf: dict = {}
        filtered: list = data.split('\n')
        filtered = [
            ele.strip() for ele in filtered if not ele.strip().startswith('#')
            and not is_empty(ele.strip())
            ]
        for ele in filtered:
            if "#" in ele:
                raise ValueError(
                    "invalid configuration syntax, line contains '#'"
                    )
            elif ele.startswith('='):
                raise ValueError(
                    "invalid configuration syntax, line starts with '='")
            elif "=" not in ele:
                raise ValueError(
                    "invalid configuration syntax, line without '='")
        req_conf: List[str] = [
            'width', 'height', 'entry', 'exit', 'seed', 'perfect',
            'output_file'
            ]
        for ele in filtered:
            key: str = ele.strip().split('=')[0].lower().strip()
            if key not in req_conf:
                raise ValueError(f"invalid configuration param '{key}'")
            val: str = ele.strip().split('=')[1].strip()
            conf[key] = val
        return conf

    @staticmethod
    def valid_numbers(n: str) -> int:
        for el in n:
            if el not in '0123456789':
                return False
        return True

    @staticmethod
    def to_int(data: tuple) -> tuple:
        return (int(data[0]), int(data[1]))

    @model_validator(mode='after')
    def finishing(s) -> 'Parsing':
        s.entry = s.to_int(s.entry)
        s.exit = s.to_int(s.exit)
        if (s.seed is not None):
            s.seeded = True
        if s.entry[0] >= s.width or s.entry[1] >= s.height:
            raise ValueError(
                f"entry({s.entry[0]},{s.entry[1]}) cordinates out of "
                f"maze dimentions w={s.width}, h={s.height}"
                )
        if s.exit[0] >= s.width or s.exit[1] >= s.height:
            raise ValueError(
                f"exit({s.exit[0]},{s.exit[1]}) cordinates out of "
                f"maze dimentions w={s.width}, h={s.height}"
                )
        return s

    @model_validator(mode='before')
    @staticmethod
    def preparation(data: dict) -> dict:
        if 'width' not in data:
            raise ValueError("there is no width on configuration file")
        elif 'height' not in data:
            raise ValueError("there is no height on configuration file")
        if not Parsing.valid_numbers(data['width']):
            raise ValueError("width value not a valid positive number")
        elif not Parsing.valid_numbers(data['height']):
            raise ValueError("height value not a valid positive number")
        if 'entry' not in data:
            raise ValueError("no entry provided on configuration file")
        elif 'exit' not in data:
            raise ValueError("no exit provided on configuration file")

        data['width'] = int(data['width'])
        data['height'] = int(data['height'])
        data['entry'] = tuple(data['entry'].strip().split(','))
        data['exit'] = tuple(data['exit'].strip().split(','))
        if len(data['entry']) != 2:
            raise ValueError("the provided enty not valid")
        for ele in data['entry']:
            if not Parsing.valid_numbers(ele):
                raise ValueError("the provided entry not valid")
        for ele in data['exit']:
            if not Parsing.valid_numbers(ele):
                raise ValueError("the provided exit not valid")
        if len(data['exit']) != 2:
            raise ValueError("the provided exit not valid")
        if 'perfect' not in data:
            raise ValueError("perfect filed is required")
        if 'seed' not in data:
            data['seed'] = None
        return data
