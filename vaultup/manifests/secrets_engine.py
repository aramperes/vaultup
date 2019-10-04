from typing import Dict, Optional

from vaultup.manifests import ManifestItem


class SecretsEngineManifest(ManifestItem):
    """
    Manifest entry for a secrets engine.
    """

    # Secrets engine types that are not tracked by vaultup.
    IGNORED_SECRET_TYPES = ("cubbyhole", "identity", "system")

    def __init__(self, data: Dict):
        super().__init__(data)

    def convert(self) -> Optional[Dict]:
        engine_type = self.data["type"]

        if engine_type in self.IGNORED_SECRET_TYPES:
            return None

        return {
            "description": self.data.get("description"),
            "type": self.data["type"]
        }
