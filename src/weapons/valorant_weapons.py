"""
VALORANT Weapon Profiles
Comprehensive weapon configurations for VALORANT
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from src.weapons.bo6_weapons import WeaponProfile


# VALORANT Rifles
VALORANT_RIFLES = {
    "vandal": WeaponProfile(
        name="vandal",
        display_name="Vandal",
        weapon_class="Rifle",
        damage=100,
        fire_rate=75,
        accuracy=80,
        range=85,
        mobility=70,
        control=65,
        vertical_pattern=[
            -3.8, -4.9, -5.7, -6.3, -6.8, -7.1, -7.3, -7.4, -7.4, -7.3,
            -7.1, -6.8, -6.4, -5.9, -5.3, -4.6, -3.8, -3.0, -2.1, -1.2,
            -0.3, 0.6, 1.4, 2.2, 2.9, 3.5, 4.0, 4.4, 4.7, 4.9
        ],
        horizontal_pattern=[
            0.0, -0.7, 1.3, -1.8, 2.2, -2.5, 2.7, -2.8, 2.8, -2.7,
            2.5, -2.2, 1.8, -1.3, 0.7, -0.1, -0.5, 1.0, -1.5, 1.9,
            -2.2, 2.4, -2.5, 2.5, -2.4, 2.2, -1.9, 1.5, -1.0, 0.5
        ],
        timing_pattern=[0.100] * 30,  # ~600 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.75
    ),
    
    "phantom": WeaponProfile(
        name="phantom",
        display_name="Phantom",
        weapon_class="Rifle",
        damage=95,
        fire_rate=80,
        accuracy=85,
        range=80,
        mobility=75,
        control=75,
        vertical_pattern=[
            -3.2, -4.1, -4.8, -5.3, -5.7, -5.9, -6.0, -6.0, -5.9, -5.7,
            -5.4, -5.0, -4.5, -3.9, -3.2, -2.4, -1.6, -0.7, 0.2, 1.0,
            1.7, 2.3, 2.8, 3.2, 3.5, 3.7, 3.8, 3.8, 3.7, 3.5
        ],
        horizontal_pattern=[
            0.0, -0.5, 0.9, -1.3, 1.6, -1.8, 1.9, -2.0, 2.0, -1.9,
            1.7, -1.4, 1.1, -0.7, 0.3, 0.1, -0.4, 0.7, -1.0, 1.2,
            -1.4, 1.5, -1.5, 1.4, -1.3, 1.1, -0.9, 0.6, -0.3, 0.0
        ],
        timing_pattern=[0.091] * 30,  # ~660 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.8
    ),
    
    "guardian": WeaponProfile(
        name="guardian",
        display_name="Guardian",
        weapon_class="Rifle",
        damage=110,
        fire_rate=55,
        accuracy=90,
        range=90,
        mobility=60,
        control=70,
        vertical_pattern=[
            -2.5, -3.2, -3.7, -4.1, -4.4, -4.6, -4.7, -4.7, -4.6, -4.4,
            -4.1, -3.7, -3.2, -2.6, -1.9, -1.2, -0.4, 0.4, 1.1, 1.8,
            2.4, 2.9, 3.3, 3.6, 3.8, 3.9, 3.9, 3.8, 3.6, 3.3
        ],
        horizontal_pattern=[
            0.0, -0.3, 0.6, -0.8, 1.0, -1.1, 1.2, -1.2, 1.1, -1.0,
            0.8, -0.6, 0.3, 0.0, -0.3, 0.5, -0.7, 0.9, -1.0, 1.1,
            -1.1, 1.0, -0.9, 0.7, -0.5, 0.3, -0.1, -0.2, 0.4, -0.5
        ],
        timing_pattern=[0.133] * 30,  # ~450 RPM
        base_sensitivity=0.9,
        ads_sensitivity=0.7
    )
}


# VALORANT SMGs
VALORANT_SMGS = {
    "spectre": WeaponProfile(
        name="spectre",
        display_name="Spectre",
        weapon_class="SMG",
        damage=70,
        fire_rate=85,
        accuracy=70,
        range=55,
        mobility=85,
        control=75,
        vertical_pattern=[
            -2.0, -2.6, -3.1, -3.5, -3.8, -4.0, -4.1, -4.1, -4.0, -3.8,
            -3.5, -3.1, -2.6, -2.0, -1.3, -0.6, 0.1, 0.8, 1.4, 2.0,
            2.5, 2.9, 3.2, 3.4, 3.5, 3.5, 3.4, 3.2, 2.9, 2.5
        ],
        horizontal_pattern=[
            0.0, -0.2, 0.4, -0.6, 0.7, -0.8, 0.9, -0.9, 0.8, -0.7,
            0.6, -0.4, 0.2, 0.0, -0.2, 0.3, -0.5, 0.6, -0.7, 0.8,
            -0.8, 0.7, -0.6, 0.5, -0.3, 0.1, 0.1, -0.3, 0.4, -0.5
        ],
        timing_pattern=[0.075] * 30,  # ~800 RPM
        base_sensitivity=1.1,
        ads_sensitivity=0.85
    ),
    
    "stinger": WeaponProfile(
        name="stinger",
        display_name="Stinger",
        weapon_class="SMG",
        damage=65,
        fire_rate=95,
        accuracy=60,
        range=45,
        mobility=95,
        control=65,
        vertical_pattern=[
            -2.2, -2.9, -3.4, -3.8, -4.1, -4.3, -4.4, -4.4, -4.3, -4.1,
            -3.8, -3.4, -2.9, -2.3, -1.6, -0.8, 0.0, 0.8, 1.5, 2.1,
            2.6, 3.0, 3.3, 3.5, 3.6, 3.6, 3.5, 3.3, 3.0, 2.6
        ],
        horizontal_pattern=[
            0.0, -0.4, 0.7, -1.0, 1.2, -1.4, 1.5, -1.5, 1.4, -1.2,
            1.0, -0.7, 0.4, -0.1, -0.3, 0.6, -0.8, 1.0, -1.1, 1.2,
            -1.2, 1.1, -1.0, 0.8, -0.6, 0.3, -0.1, -0.2, 0.4, -0.6
        ],
        timing_pattern=[0.066] * 30,  # ~900 RPM
        base_sensitivity=1.2,
        ads_sensitivity=0.9
    )
}


# VALORANT Sniper Rifles
VALORANT_SNIPERS = {
    "operator": WeaponProfile(
        name="operator",
        display_name="Operator",
        weapon_class="Sniper Rifle",
        damage=150,
        fire_rate=20,
        accuracy=100,
        range=100,
        mobility=30,
        control=30,
        vertical_pattern=[
            -12.0, -15.0, -17.0, -18.5, -19.5, -20.0, -20.2, -20.1, -19.8, -19.3,
            -18.6, -17.7, -16.6, -15.3, -13.8, -12.1, -10.2, -8.1, -5.8, -3.3,
            -0.6, 2.2, 5.1, 8.1, 11.2, 14.4, 17.7, 21.1, 24.6, 28.2
        ],
        horizontal_pattern=[
            0.0, -3.0, 5.5, -7.5, 9.0, -10.0, 10.5, -10.8, 10.9, -10.7,
            10.2, -9.5, 8.6, -7.5, 6.2, -4.7, 3.1, -1.3, -0.5, 2.3,
            -4.1, 5.8, -7.4, 8.9, -10.2, 11.3, -12.2, 12.9, -13.4, 13.7
        ],
        timing_pattern=[0.750] * 30,  # ~80 RPM (bolt-action)
        base_sensitivity=0.5,
        ads_sensitivity=0.25
    ),
    
    "marshal": WeaponProfile(
        name="marshal",
        display_name="Marshal",
        weapon_class="Sniper Rifle",
        damage=110,
        fire_rate=35,
        accuracy=95,
        range=90,
        mobility=45,
        control=50,
        vertical_pattern=[
            -8.0, -10.0, -11.5, -12.5, -13.0, -13.2, -13.3, -13.2, -13.0, -12.6,
            -12.0, -11.2, -10.2, -9.0, -7.6, -6.0, -4.2, -2.2, 0.0, 2.4,
            4.9, 7.5, 10.2, 13.0, 15.9, 18.9, 22.0, 25.2, 28.5, 31.9
        ],
        horizontal_pattern=[
            0.0, -2.0, 3.5, -4.8, 5.8, -6.5, 7.0, -7.2, 7.3, -7.1,
            6.7, -6.1, 5.3, -4.4, 3.4, -2.3, 1.1, 0.2, -1.3, 2.7,
            -4.0, 5.2, -6.3, 7.3, -8.1, 8.7, -9.1, 9.3, -9.3, 9.1
        ],
        timing_pattern=[0.500] * 30,  # ~120 RPM (bolt-action)
        base_sensitivity=0.7,
        ads_sensitivity=0.4
    )
}


# VALORANT Sidearms
VALORANT_SIDEARMS = {
    "sheriff": WeaponProfile(
        name="sheriff",
        display_name="Sheriff",
        weapon_class="Sidearm",
        damage=95,
        fire_rate=60,
        accuracy=80,
        range=70,
        mobility=80,
        control=55,
        vertical_pattern=[
            -4.5, -5.8, -6.8, -7.5, -8.0, -8.3, -8.4, -8.4, -8.2, -7.9,
            -7.4, -6.8, -6.0, -5.1, -4.0, -2.8, -1.5, -0.1, 1.3, 2.7,
            4.1, 5.5, 6.9, 8.2, 9.5, 10.7, 11.8, 12.8, 13.7, 14.5
        ],
        horizontal_pattern=[
            0.0, -1.0, 1.8, -2.5, 3.1, -3.5, 3.8, -3.9, 3.9, -3.7,
            3.4, -3.0, 2.5, -1.9, 1.2, -0.5, -0.2, 0.9, -1.5, 2.0,
            -2.4, 2.7, -2.9, 3.0, -3.0, 2.9, -2.7, 2.4, -2.0, 1.5
        ],
        timing_pattern=[0.167] * 30,  # ~360 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.75
    ),
    
    "ghost": WeaponProfile(
        name="ghost",
        display_name="Ghost",
        weapon_class="Sidearm",
        damage=75,
        fire_rate=85,
        accuracy=75,
        range=60,
        mobility=85,
        control=70,
        vertical_pattern=[
            -2.5, -3.2, -3.7, -4.1, -4.4, -4.6, -4.7, -4.7, -4.6, -4.4,
            -4.1, -3.7, -3.2, -2.6, -1.9, -1.1, -0.3, 0.5, 1.3, 2.0,
            2.7, 3.3, 3.8, 4.2, 4.5, 4.7, 4.8, 4.8, 4.7, 4.5
        ],
        horizontal_pattern=[
            0.0, -0.3, 0.6, -0.8, 1.0, -1.1, 1.2, -1.2, 1.1, -1.0,
            0.8, -0.6, 0.3, 0.0, -0.3, 0.5, -0.7, 0.9, -1.0, 1.1,
            -1.1, 1.0, -0.9, 0.7, -0.5, 0.3, -0.1, -0.2, 0.4, -0.5
        ],
        timing_pattern=[0.100] * 30,  # ~600 RPM
        base_sensitivity=1.1,
        ads_sensitivity=0.8
    )
}


def get_all_valorant_weapons() -> Dict[str, WeaponProfile]:
    """Get all VALORANT weapon profiles."""
    all_weapons = {}
    all_weapons.update(VALORANT_RIFLES)
    all_weapons.update(VALORANT_SMGS)
    all_weapons.update(VALORANT_SNIPERS)
    all_weapons.update(VALORANT_SIDEARMS)
    return all_weapons


def get_weapon_by_name(weapon_name: str) -> WeaponProfile:
    """Get a specific VALORANT weapon profile by name."""
    all_weapons = get_all_valorant_weapons()
    return all_weapons.get(weapon_name.lower())


def get_weapons_by_class(weapon_class: str) -> Dict[str, WeaponProfile]:
    """Get VALORANT weapons by class."""
    class_mapping = {
        "rifle": VALORANT_RIFLES,
        "smg": VALORANT_SMGS,
        "sniper_rifle": VALORANT_SNIPERS,
        "sidearm": VALORANT_SIDEARMS
    }
    return class_mapping.get(weapon_class.lower(), {})


def get_recommended_settings(weapon_name: str) -> Dict[str, float]:
    """Get recommended sensitivity settings for a VALORANT weapon."""
    weapon = get_weapon_by_name(weapon_name)
    if weapon:
        return {
            "base_sensitivity": weapon.base_sensitivity,
            "ads_sensitivity": weapon.ads_sensitivity,
            "randomization": 0.05 if weapon.accuracy > 85 else 0.1,  # VALORANT has strict anti-cheat
            "security_level": "maximum"  # Always use maximum security for VALORANT
        }
    return {"base_sensitivity": 1.0, "ads_sensitivity": 0.8, "randomization": 0.05}