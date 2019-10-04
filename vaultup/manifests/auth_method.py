from typing import Dict, Optional

from vaultup.manifests import ManifestItem


class AuthMethodManifest(ManifestItem):
    """
    Manifest entry for an auth method.
    """

    def __init__(self, data: Dict):
        super().__init__(data)

    def convert(self) -> Optional[Dict]:
        return {
            "type": self.data["type"],
            "description": self.data.get("description"),
            "config": self.data.get("config"),
            "local": self.data.get("local"),
            "options": self.data.get("options"),
            "seal_wrap": self.data.get("seal_wrap"),
        }
