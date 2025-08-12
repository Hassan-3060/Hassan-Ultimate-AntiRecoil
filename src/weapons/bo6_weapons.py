"""
Black Ops 6 Weapon Profiles
Comprehensive weapon configurations for Call of Duty: Black Ops 6
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class WeaponProfile:
    """Black Ops 6 weapon profile."""
    name: str
    display_name: str
    weapon_class: str
    damage: int
    fire_rate: int
    accuracy: int
    range: int
    mobility: int
    control: int
    
    # Recoil pattern data
    vertical_pattern: List[float]
    horizontal_pattern: List[float]
    timing_pattern: List[float]
    
    # Sensitivity settings
    base_sensitivity: float = 1.0
    ads_sensitivity: float = 0.8
    
    # Attachments effects
    attachment_modifiers: Dict[str, Dict[str, float]] = None


# Black Ops 6 Assault Rifles
BO6_ASSAULT_RIFLES = {
    "xm4": WeaponProfile(
        name="xm4",
        display_name="XM4",
        weapon_class="Assault Rifle",
        damage=85,
        fire_rate=75,
        accuracy=80,
        range=85,
        mobility=65,
        control=70,
        vertical_pattern=[
            -3.2, -4.1, -4.8, -5.2, -5.8, -6.1, -6.5, -6.8, -7.0, -7.2,
            -7.1, -6.9, -6.6, -6.2, -5.8, -5.3, -4.8, -4.2, -3.6, -3.0,
            -2.4, -1.8, -1.2, -0.8, -0.4, -0.2, 0.0, 0.1, 0.2, 0.3
        ],
        horizontal_pattern=[
            0.0, -0.5, 0.8, -1.2, 1.6, -1.8, 2.1, -2.3, 2.5, -2.6,
            2.4, -2.1, 1.8, -1.4, 1.0, -0.6, 0.3, 0.1, -0.2, 0.4,
            -0.6, 0.8, -0.9, 1.0, -1.1, 1.2, -1.0, 0.8, -0.5, 0.2
        ],
        timing_pattern=[0.092] * 30,  # ~650 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.75
    ),
    
    "ames_85": WeaponProfile(
        name="ames_85",
        display_name="AMES 85",
        weapon_class="Assault Rifle",
        damage=90,
        fire_rate=70,
        accuracy=85,
        range=90,
        mobility=60,
        control=75,
        vertical_pattern=[
            -2.8, -3.6, -4.2, -4.8, -5.3, -5.7, -6.0, -6.2, -6.4, -6.5,
            -6.4, -6.2, -5.9, -5.5, -5.0, -4.4, -3.8, -3.1, -2.4, -1.7,
            -1.0, -0.4, 0.2, 0.7, 1.1, 1.4, 1.6, 1.7, 1.8, 1.8
        ],
        horizontal_pattern=[
            0.0, 0.3, -0.6, 1.0, -1.4, 1.7, -2.0, 2.2, -2.3, 2.4,
            -2.3, 2.1, -1.8, 1.4, -1.0, 0.5, -0.1, -0.4, 0.7, -1.0,
            1.2, -1.4, 1.5, -1.6, 1.6, -1.5, 1.3, -1.0, 0.6, -0.2
        ],
        timing_pattern=[0.100] * 30,  # ~600 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.7
    ),
    
    "ictv": WeaponProfile(
        name="ictv",
        display_name="ICTV",
        weapon_class="Assault Rifle",
        damage=80,
        fire_rate=80,
        accuracy=75,
        range=80,
        mobility=70,
        control=65,
        vertical_pattern=[
            -3.5, -4.5, -5.2, -5.8, -6.3, -6.7, -7.0, -7.2, -7.4, -7.5,
            -7.4, -7.2, -6.9, -6.5, -6.0, -5.4, -4.7, -4.0, -3.2, -2.4,
            -1.6, -0.8, 0.0, 0.7, 1.3, 1.8, 2.2, 2.5, 2.7, 2.8
        ],
        horizontal_pattern=[
            0.0, -0.8, 1.4, -2.0, 2.5, -2.8, 3.0, -3.1, 3.1, -3.0,
            2.8, -2.5, 2.1, -1.6, 1.0, -0.4, -0.2, 0.6, -1.1, 1.5,
            -1.8, 2.0, -2.1, 2.1, -2.0, 1.8, -1.5, 1.1, -0.6, 0.1
        ],
        timing_pattern=[0.075] * 30,  # ~800 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.8
    ),
    
    "ak74": WeaponProfile(
        name="ak74",
        display_name="AK-74",
        weapon_class="Assault Rifle",
        damage=95,
        fire_rate=65,
        accuracy=70,
        range=85,
        mobility=55,
        control=60,
        vertical_pattern=[
            -4.0, -5.2, -6.1, -6.8, -7.4, -7.8, -8.1, -8.3, -8.4, -8.4,
            -8.3, -8.0, -7.6, -7.1, -6.5, -5.8, -5.0, -4.1, -3.2, -2.2,
            -1.2, -0.2, 0.8, 1.7, 2.5, 3.2, 3.8, 4.3, 4.7, 5.0
        ],
        horizontal_pattern=[
            0.0, -1.0, 1.8, -2.5, 3.1, -3.5, 3.8, -3.9, 3.9, -3.8,
            3.6, -3.2, 2.7, -2.1, 1.4, -0.7, 0.0, 0.7, -1.4, 2.0,
            -2.5, 2.9, -3.2, 3.4, -3.5, 3.5, -3.3, 3.0, -2.6, 2.1
        ],
        timing_pattern=[0.109] * 30,  # ~550 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.65
    )
}


# Black Ops 6 SMGs
BO6_SMGS = {
    "jackal_pdw": WeaponProfile(
        name="jackal_pdw",
        display_name="Jackal PDW",
        weapon_class="SMG",
        damage=70,
        fire_rate=90,
        accuracy=65,
        range=50,
        mobility=95,
        control=70,
        vertical_pattern=[
            -2.1, -2.8, -3.3, -3.7, -4.0, -4.2, -4.3, -4.4, -4.4, -4.3,
            -4.1, -3.8, -3.4, -3.0, -2.5, -1.9, -1.3, -0.7, -0.1, 0.5,
            1.0, 1.4, 1.7, 2.0, 2.2, 2.3, 2.4, 2.4, 2.3, 2.2
        ],
        horizontal_pattern=[
            0.0, -0.3, 0.6, -0.9, 1.2, -1.4, 1.5, -1.6, 1.6, -1.5,
            1.4, -1.2, 0.9, -0.6, 0.3, 0.0, -0.3, 0.5, -0.8, 1.0,
            -1.1, 1.2, -1.2, 1.1, -1.0, 0.8, -0.6, 0.4, -0.2, 0.0
        ],
        timing_pattern=[0.063] * 30,  # ~950 RPM
        base_sensitivity=1.2,
        ads_sensitivity=0.9
    ),
    
    "kompakt_92": WeaponProfile(
        name="kompakt_92",
        display_name="Kompakt 92",
        weapon_class="SMG",
        damage=75,
        fire_rate=85,
        accuracy=70,
        range=55,
        mobility=90,
        control=75,
        vertical_pattern=[
            -2.3, -3.1, -3.7, -4.1, -4.4, -4.6, -4.7, -4.7, -4.6, -4.4,
            -4.1, -3.7, -3.2, -2.6, -2.0, -1.3, -0.6, 0.1, 0.7, 1.3,
            1.8, 2.2, 2.5, 2.7, 2.8, 2.8, 2.7, 2.5, 2.2, 1.8
        ],
        horizontal_pattern=[
            0.0, 0.2, -0.5, 0.8, -1.0, 1.2, -1.3, 1.4, -1.4, 1.3,
            -1.1, 0.9, -0.6, 0.3, 0.0, -0.3, 0.6, -0.8, 1.0, -1.1,
            1.2, -1.2, 1.1, -1.0, 0.8, -0.6, 0.4, -0.2, 0.0, 0.2
        ],
        timing_pattern=[0.071] * 30,  # ~850 RPM
        base_sensitivity=1.1,
        ads_sensitivity=0.85
    )
}


# Black Ops 6 LMGs
BO6_LMGS = {
    "xm4_lmg": WeaponProfile(
        name="xm4_lmg",
        display_name="XMG",
        weapon_class="LMG",
        damage=100,
        fire_rate=60,
        accuracy=85,
        range=95,
        mobility=40,
        control=55,
        vertical_pattern=[
            -5.0, -6.5, -7.8, -8.8, -9.6, -10.2, -10.6, -10.8, -10.9, -10.8,
            -10.6, -10.2, -9.7, -9.1, -8.4, -7.6, -6.7, -5.7, -4.6, -3.5,
            -2.3, -1.1, 0.1, 1.3, 2.4, 3.5, 4.5, 5.4, 6.2, 6.9
        ],
        horizontal_pattern=[
            0.0, -1.2, 2.2, -3.0, 3.6, -4.0, 4.2, -4.3, 4.3, -4.1,
            3.8, -3.4, 2.9, -2.3, 1.6, -0.9, 0.2, 0.5, -1.2, 1.8,
            -2.3, 2.7, -3.0, 3.2, -3.3, 3.3, -3.1, 2.8, -2.4, 1.9
        ],
        timing_pattern=[0.120] * 30,  # ~500 RPM
        base_sensitivity=0.8,
        ads_sensitivity=0.5
    )
}


# Black Ops 6 Snipers
BO6_SNIPERS = {
    "lr_762": WeaponProfile(
        name="lr_762",
        display_name="LR 7.62 Sniper",
        weapon_class="Sniper Rifle",
        damage=120,
        fire_rate=30,
        accuracy=95,
        range=100,
        mobility=35,
        control=40,
        vertical_pattern=[
            -8.0, -10.5, -12.0, -13.0, -13.5, -13.8, -14.0, -14.0, -13.8, -13.5,
            -13.0, -12.3, -11.5, -10.5, -9.4, -8.2, -6.9, -5.5, -4.0, -2.4,
            -0.8, 0.8, 2.4, 3.9, 5.3, 6.6, 7.8, 8.9, 9.8, 10.6
        ],
        horizontal_pattern=[
            0.0, -2.0, 3.5, -4.8, 5.8, -6.5, 7.0, -7.2, 7.3, -7.2,
            6.9, -6.4, 5.7, -4.9, 4.0, -3.0, 1.9, -0.8, -0.3, 1.4,
            -2.5, 3.5, -4.4, 5.2, -5.8, 6.3, -6.6, 6.7, -6.6, 6.3
        ],
        timing_pattern=[0.400] * 30,  # ~150 RPM (semi-auto)
        base_sensitivity=0.6,
        ads_sensitivity=0.3
    )
}


def get_all_bo6_weapons() -> Dict[str, WeaponProfile]:
    """Get all Black Ops 6 weapon profiles."""
    all_weapons = {}
    all_weapons.update(BO6_ASSAULT_RIFLES)
    all_weapons.update(BO6_SMGS)
    all_weapons.update(BO6_LMGS)
    all_weapons.update(BO6_SNIPERS)
    return all_weapons


def get_weapon_by_name(weapon_name: str) -> WeaponProfile:
    """Get a specific weapon profile by name."""
    all_weapons = get_all_bo6_weapons()
    return all_weapons.get(weapon_name.lower())


def get_weapons_by_class(weapon_class: str) -> Dict[str, WeaponProfile]:
    """Get weapons by class."""
    class_mapping = {
        "assault_rifle": BO6_ASSAULT_RIFLES,
        "smg": BO6_SMGS,
        "lmg": BO6_LMGS,
        "sniper_rifle": BO6_SNIPERS
    }
    return class_mapping.get(weapon_class.lower(), {})


def get_recommended_settings(weapon_name: str) -> Dict[str, float]:
    """Get recommended sensitivity settings for a weapon."""
    weapon = get_weapon_by_name(weapon_name)
    if weapon:
        return {
            "base_sensitivity": weapon.base_sensitivity,
            "ads_sensitivity": weapon.ads_sensitivity,
            "randomization": 0.1 if weapon.control > 70 else 0.15,
            "security_level": "high" if weapon.damage > 90 else "medium"
        }
    return {"base_sensitivity": 1.0, "ads_sensitivity": 0.8, "randomization": 0.15}