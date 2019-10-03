import argparse

from vaultup.cli import Action


class PushAction(Action):
    """
    The "push" action. Creates manifests locally
    by scanning the configuration of a remote Vault instance.

    Examples: * vaultup push vault.myserver.com
                Scans the remote Vault instance, compares
                with the local manifests, and applies all the
                differences.

              * vaultup push vault.myserver.com --preview
                Shows a preview of the changes when
                applying the local manifests to the remote
                instance.

              * vaultup push vault.myserver.com --clean
                Clears all configurations of the remote server,
                then re-creates the manifests. Note that this will
                delete ALL secrets and other data, resetting the
                remote instance to its bare state.
    """

    def __init__(self):
        self.url = ""
        self.clean = False
        self.preview = False

    def create_parser(self, parser: argparse._SubParsersAction) -> None:
        action = parser.add_parser("push",
                                   help="Applies the differences between the local manifests "
                                        "to the remote Vault instance.")
        action.add_argument("url",
                            action="store",
                            help="The URL of the remote Vault instance.")
        action.add_argument("--clean",
                            action="store_true",
                            help="Clears all configurations of the remote server, "
                                 "then applies all local manifests. This effectively "
                                 "deletes all secrets and other data before applying "
                                 "manifests.")
        action.add_argument("--preview",
                            action="store_true",
                            help="Shows a preview of the remote changes, "
                                 "without applying them.")

    def parse(self, ns: argparse.Namespace) -> None:
        self.url = ns.url
        self.clean = ns.clean
        self.preview = ns.preview
