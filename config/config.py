from dataclasses import dataclass

from dotenv import load_dotenv

import os


class ImproperlyConfigured(Exception):
    def __init__(self, variable_name: str, *args, **kwargs):
        self.variable_name = variable_name
        self.message = f"Set the {variable_name} environment variable."
        super().__init__(self.message, *args, **kwargs)


def getenv(var_name: str, cast_to=str) -> str:
    try:
        value = os.environ[var_name]
        return cast_to(value)
    except KeyError:
        raise ImproperlyConfigured(var_name)
    except ValueError:
        raise ValueError(f"The value {value} can't be cast to {cast_to}.")


@dataclass
class Config:
    bot_token: str
    available_parsers: list[str]
    available_checkers: list[str]


load_dotenv()


def get_config() -> Config:
    return Config(
        bot_token=getenv("BOT_TOKEN"),
        available_parsers=[
            "DeWork",
            "Aspecta",
        ],
        available_checkers=[
            "DeBank",
            "Solscan (Soon)",
        ]
    )
