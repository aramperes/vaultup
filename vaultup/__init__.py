def is_remote_compatible(remote_version: str):
    major, minor, patch = remote_version.split(".")

    # 0.11.x supported
    if major == "0" and minor == "11":
        return True

    # 1.0.x and 1.1.x supported
    if major == "1" and minor in ("0", "1"):
        return True

    return False
