import argparse

from vaultup.cli import Action


class CloneAction(Action):
    """
    The "clone" action. Creates manifests locally
    by scanning the configuration of a remote Vault instance.

    Examples: * vaultup clone vault.myserver.com
                Clones the config for vault.myserver.com.
                If the local directory is not bare (there is
                already a vault.yml file), a diff will be created
                to merge the configs, taking the remote server as
                priority.

              * vaultup clone vault.myserver.com --preview
                Clones the config, but does not apply any
                changes locally.

              * vaultup clone vault.myserver.com --clean
                Clones the config, overwriting the local
                vault.yml file (if exists) with all the
                remote configuration.
    """

    def __init__(self):
        self.url = ""
        self.clean = False
        self.preview = False

    def create_parser(self, parser: argparse._SubParsersAction) -> None:
        action = parser.add_parser("clone",
                                   help="Create manifests locally by scanning the configuration of a remote "
                                        "Vault instance. Requires a root token of the remote instance.")
        action.add_argument("url",
                            action="store",
                            help="The URL of the remote Vault instance.")
        action.add_argument("--clean",
                            action="store_true",
                            help="Discards any local manifests to be at the same "
                                 "configuration as the remote instance.")
        action.add_argument("--preview",
                            action="store_true",
                            help="Shows a preview of the local manifest changes, "
                                 "without applying them.")

    def parse(self, ns: argparse.Namespace) -> None:
        self.url = ns.url
        self.clean = ns.clean
        self.preview = ns.preview
