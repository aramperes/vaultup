import os
from collections import OrderedDict
from copy import deepcopy
from typing import Dict, Optional, List

from ruamel import yaml
from ruamel.yaml.comments import CommentedMap


class ManifestItem:
    def __init__(self, data: Dict):
        self.data = data

    def convert(self) -> Optional[Dict]:
        raise NotImplementedError()


class RootManifest:
    """
    Manifest: defaults to the "vault.yml" file in
    the current directory.
    """

    def __init__(self, path: str = None, load: bool = True):
        self.path = os.path.abspath(path) if path else None
        self._backing = OrderedDict()

        if load:
            self._load()

        self._changes = deepcopy(self._backing)

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, mode="r") as f:
                self._backing.update(yaml.safe_load(f))

    def add_secrets_backend(self, name: str, manifest: ManifestItem) -> None:
        converted = manifest.convert()
        if not converted:
            return

        if "secrets_backends" not in self._changes:
            self._changes["secrets_backends"] = {}

        name = name.strip("/")
        new_dict = self._changes["secrets_backends"].get(name, {})
        new_dict.update(converted)
        self._changes["secrets_backends"][name] = new_dict

    def delete_secrets_backend(self, name: str) -> None:
        name = name.strip("/")

        if "secrets_backends" in self._changes and name in self._changes["secrets_backends"]:
            del self._changes["secrets_backends"][name]

    def list_secrets_backend_names(self) -> List[str]:
        return [name.strip("/") for name in self._backing.get("secrets_backends", {})]

    def yaml(self) -> str:
        cs = CommentedMap()
        cs.update(self._changes)
        return yaml.round_trip_dump(cs)

    def save(self) -> None:
        with open(self.path, "w") as f:
            f.write(self.yaml())
