from typing import Dict, Optional

import hvac

from vaultup.manifests import ManifestItem


class LdapAuthConfigManifest(ManifestItem):

    def __init__(self, client: hvac.Client, name: str, data: Dict):
        super().__init__(data)

    def convert(self) -> Optional[Dict]:
        return self.data


AUTH_TYPES = {
    "ldap": LdapAuthConfigManifest
}


class AuthMethodManifest(ManifestItem):
    """
    Manifest entry for an auth method.
    """

    def __init__(self, client: hvac.Client, name: str, data: Dict):
        super().__init__(data)
        auth_type = data["type"]
        if auth_type in client.auth.implemented_class_names and auth_type in AUTH_TYPES:
            auth_conf = client.auth.__getattr__(auth_type).read_configuration(mount_point=name)["data"]
            self._auth_config = AUTH_TYPES[auth_type](client, name, auth_conf).convert()
        else:
            self._auth_config = None

    def convert(self) -> Optional[Dict]:
        config = self.data.get("config", {})

        # add type-specific entries to config
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
