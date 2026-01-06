from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld



class MAWebWorld(WebWorld):
    game = "Magic Archery"

    theme = "jungle"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Magic Archery for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["PlatanoBailando"],
    )

    tutorials = [setup_en, ]

    # option_groups = option_groups
    # options_presets = option_presets
