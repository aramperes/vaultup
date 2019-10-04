import argparse
import sys

import hvac
from colorama import Fore, Style

from vaultup.cli import Action
from vaultup.manifests import RootManifest, SecretsEngineManifest


class CloneAction(Action):
    """
    The "clone" action. Creates manifests locally
    by scanning the configuration of a remote Vault instance.

    Examples: * vaultup clone vault.myserver.com
                Prints the YAML config for vault.myserver.com.

              * vaultup clone vault.myserver.com -o vault.yml
                Saves the YAML manifest for vault.myserver.com
                to a local vault.yml file.
    """

    def create_parser(self, parser: argparse._SubParsersAction) -> None:
        action = parser.add_parser("clone",
                                   help="Create manifests locally by scanning the configuration of a remote "
                                        "Vault instance. Requires a root token of the remote instance.")
        action.add_argument("url",
                            action="store",
                            help="The URL of the remote Vault instance.")
        action.add_argument("-o", "--output",
                            action="store",
                            help="Saves the YAML file (remote manifest) to the OUTPUT path.")

    def exec(self, ns: argparse.Namespace) -> None:
        client = hvac.Client(url=ns.url)
        client.token = input(
            f"{Fore.BLUE}{Style.BRIGHT}Root token for "
            f"{Fore.YELLOW}{ns.url}"
            f"{Fore.BLUE}: "
            f"{Style.RESET_ALL}")
        if not client.is_authenticated():
            print(f"{Fore.RED}{Style.BRIGHT}Invalid root token."
                  f"{Style.RESET_ALL}", file=sys.stderr)
            exit(1)
            return

        manifest = RootManifest(path=ns.output, load=False)

        print(f"Token valid, cloning {ns.url}...")

        secret_backends = client.sys.list_mounted_secrets_engines()["data"]

        # Deleted secrets engines
        for name in manifest.list_secrets_backend_names():
            if name not in SecretsEngineManifest.IGNORED_SECRET_TYPES \
                    and name not in map(lambda name: name.strip("/"), secret_backends.keys()):
                manifest.delete_secrets_backend(name)

        # Modified and added secrets engines
        for name, backend in secret_backends.items():
            manifest.add_secrets_backend(name, SecretsEngineManifest(backend))

        if manifest.path:
            manifest.save()
            print(f"{Fore.GREEN}{Style.BRIGHT}Clone successful. "
                  f"Manifest for {Fore.YELLOW}{ns.url}{Fore.GREEN} was saved to {Fore.YELLOW}{manifest.path}{Fore.GREEN}."
                  f"{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}{Style.BRIGHT}Clone successful. Manifest for {Fore.YELLOW}{ns.url}{Fore.GREEN}:"
                  f"{Style.RESET_ALL}\n")
            print(f"{Fore.GREEN}{manifest.yaml()}{Style.RESET_ALL}")
