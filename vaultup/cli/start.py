import argparse

from vaultup.cli import Action


class StartAction(Action):
    """
    The "start" action. Launches a local Vault instance,
    applying all local manifests. Using the "--edit"
    flag will create an audit engine to monitor the instance
    for changes, and allow the user to save their changes
    to the local manifests.

    Examples: * vaultup start
                Starts a local instance on the default port,
                applies all local manifests.

              * vaultup start --edit
                Starts a local instance on the default port,
                applies all local manifests, and monitors
                changes from the instance to apply locally
                at the end.

              * vaultup start --port 3000
                Starts the local instance on port 3000.
    """

    def __init__(self):
        self.edit = False
        self.port = -1

    def create_parser(self, parser: argparse._SubParsersAction) -> None:
        action = parser.add_parser("start",
                                   help="Launches a local Vault instance, "
                                        "applying all local manifests. Using the \"--edit\" "
                                        "flag will create an audit engine to monitor the instance "
                                        "for changes, and allow the user to save their changes "
                                        "to the local manifests.")
        action.add_argument("--port",
                            type=int,
                            default=8200,
                            action="store",
                            help="Launches the Vault instance on the given port.")
        action.add_argument("--edit",
                            action="store_true",
                            help="Turns on edit-mode. An audit engine will be "
                                 "created to monitor all changes, and a prompt "
                                 "to compare/apply the changes will be shown at the end.")

    def parse(self, ns: argparse.Namespace) -> None:
        self.edit = ns.edit
        self.port = ns.port
