"""
CLI actions (program startup).
"""
import argparse

from vaultup.cli import CloneAction, StartAction, PushAction

parser = argparse.ArgumentParser(
    prog="vaultup", description="Vault file-based management tool"
)
parser.add_argument("--version", action="version", version="vaultup 0.0.1")

action_arg = parser.add_subparsers(title="action", dest='action')
action_arg.required = True

actions = {
    "clone": CloneAction(),
    "start": StartAction(),
    "push": PushAction(),
}

for name, action in actions.items():
    action.create_parser(action_arg)
