from typing import Dict, Optional

import hvac

from vaultup.manifests import ManifestItem


class AuthMethodManifest(ManifestItem):
    """
    Manifest entry for an auth method.
    """

    def __init__(self, client: hvac.Client, name: str, data: Dict):
        super().__init__(data)
        auth_type = data["type"]
        if auth_type in client.auth.implemented_class_names:
            client.auth.__getattr__(auth_type)
            self._auth_config = client.auth.__getattr__(auth_type).read_configuration(mount_point=name)["data"]
        else:
            self._auth_config = None

    def convert(self) -> Optional[Dict]:
        config = self.data.get("config", {})
        if self._auth_config:
            config[self.data["type"]] = self._auth_config
        return {
            "type": self.data["type"],
            "description": self.data.get("description"),
            "config": self.data.get("config"),
            "local": self.data.get("local"),
            "options": self.data.get("options"),
            "seal_wrap": self.data.get("seal_wrap"),
        }
