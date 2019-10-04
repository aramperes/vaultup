import argparse
import sys

import hvac

from vaultup.cli import Action
from vaultup.manifests import RootManifest, SecretsEngineManifest


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

    def exec(self, ns: argparse.Namespace) -> None:
        client = hvac.Client(url=ns.url)
        client.token = input(f"Root token for {ns.url}: ")
        if not client.is_authenticated():
            print("Invalid root token.", file=sys.stderr)
            exit(1)
            return

        manifest = RootManifest(load=(not ns.clean))

        secret_backends = client.sys.list_mounted_secrets_engines()["data"]

        # Deleted secrets engines
        for name in manifest.list_secrets_backend_names():
            if name not in SecretsEngineManifest.IGNORED_SECRET_TYPES \
                    and name not in map(lambda name: name.strip("/"), secret_backends.keys()):
                manifest.delete_secrets_backend(name)

        # Modified and added secrets engines
        for name, backend in secret_backends.items():
            manifest.add_secrets_backend(name, SecretsEngineManifest(backend))

        # TODO: Pretty print difference
