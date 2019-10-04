import argparse


class Action:
    """
    Defines a vaultup CLI action.
    """

    def create_parser(self, parser: argparse._SubParsersAction) -> None:
        raise NotImplementedError()

    def exec(self, ns: argparse.Namespace) -> None:
        raise NotImplementedError()


from .clone import CloneAction
from .start import StartAction
from .push import PushAction
from .parser import actions, parser

__all__ = ["actions", "parser",
           "Action", "CloneAction", "StartAction", "PushAction"]
