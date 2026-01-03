"""Apply these patches if the target mozApp is Komodo for Firefox 140 ESR."""

def applicable(config):
    return config.patch_target == "komodoapp" and \
           config.mozVer == 140.0


def add(config):
    return [
        # Copy the "komodo/..." tree to the top-level mozilla dir.
        ("komodo", "komodo"),
    ]