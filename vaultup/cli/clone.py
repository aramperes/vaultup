import argparse
import sys
from pprint import pprint

import hvac
from colorama import Fore, Style

from vaultup.cli import Action
from vaultup.manifests import RootManifest, SecretsEngineManifest, AuthMethodManifest


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

        try:
            client.token = input(
                f"{Fore.BLUE}{Style.BRIGHT}Root token for "
                f"{Fore.YELLOW}{ns.url}"
                f"{Fore.BLUE}: "
                f"{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print()
            exit(1)
            return

        if not client.is_authenticated():
            print(f"{Fore.RED}{Style.BRIGHT}Invalid root token."
                  f"{Style.RESET_ALL}", file=sys.stderr)
            exit(1)
            return

        manifest = RootManifest(path=ns.output, load=False)

        print(f"{Fore.BLUE}Cloning {ns.url}...{Fore.RESET}", end="\r")

        secret_backends = client.sys.list_mounted_secrets_engines()["data"]
        auth_methods = client.sys.list_auth_methods()["data"]
        pprint(client.auth.ldap)

        # Secrets engines (mounts)
        manifest.create_secrets_backend_section()
        for name, backend in secret_backends.items():
            manifest.add_secrets_backend(name, SecretsEngineManifest(client, name, backend))

        # Auth methods
        manifest.create_auth_method_section()
        for name, method in auth_methods.items():
            manifest.add_auth_method(name, AuthMethodManifest(client, name, method))

        manifest.set_header(f"vaultup manifest for {ns.url}\n"
                            f"Generated using the 'clone' action.")

        if manifest.path:
            manifest.save()
            print(f"{Fore.GREEN}{Style.BRIGHT}Clone successful. "
                  f"Manifest for {Fore.YELLOW}{ns.url}{Fore.GREEN} was saved to {Fore.YELLOW}{manifest.path}{Fore.GREEN}."
                  f"{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}{Style.BRIGHT}Clone successful. Manifest for {Fore.YELLOW}{ns.url}{Fore.GREEN}:"
                  f"{Style.RESET_ALL}\n")
            print(f"{Fore.GREEN}{manifest.yaml()}{Style.RESET_ALL}")
