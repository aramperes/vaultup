from typing import Dict, Optional

import hvac

from vaultup.manifests import ManifestItem


class SecretsEngineManifest(ManifestItem):
    """
    Manifest entry for a secrets engine.
    """

    # Secrets engine types that are not tracked by vaultup.
    IGNORED_SECRET_TYPES = ("cubbyhole", "identity", "system")

    def __init__(self, client: hvac.Client, name: str, data: Dict):
        super().__init__(data)
        self._load_extras(client, name)

    def convert(self) -> Optional[Dict]:
        engine_type = self.data["type"]

        if engine_type in self.IGNORED_SECRET_TYPES:
            return None

        result = {
            "type": self.data["type"],
            "description": self.data.get("description"),
            "config": self.data.get("config"),
            "local": self.data.get("local"),
            "options": self.data.get("options"),
            "seal_wrap": self.data.get("seal_wrap"),
        }
        result.update(self._extras)
        return result

    def _load_extras(self, client: hvac.Client, name: str):
        self._extras = {}
        if self.data["type"] == "pki":
            role_keys = client.secrets.pki.list_roles(mount_point=name)["data"]["keys"]
            self._extras["roles"] = {}
            for key in role_keys:
                self._extras["roles"][key] = client.secrets.pki.read_role(key, mount_point=name)["data"]
