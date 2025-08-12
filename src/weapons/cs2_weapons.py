"""
Counter-Strike 2 Weapon Profiles
Comprehensive weapon configurations for Counter-Strike 2
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from src.weapons.bo6_weapons import WeaponProfile


# CS2 Rifles
CS2_RIFLES = {
    "ak47": WeaponProfile(
        name="ak47",
        display_name="AK-47",
        weapon_class="Rifle",
        damage=115,
        fire_rate=60,
        accuracy=70,
        range=85,
        mobility=60,
        control=50,
        vertical_pattern=[
            -5.2, -6.8, -8.1, -9.2, -10.1, -10.8, -11.3, -11.6, -11.7, -11.6,
            -11.3, -10.8, -10.1, -9.2, -8.1, -6.8, -5.3, -3.6, -1.7, 0.3,
            2.4, 4.6, 6.9, 9.3, 11.8, 14.4, 17.1, 19.9, 22.8, 25.8
        ],
        horizontal_pattern=[
            0.0, -1.5, 2.7, -3.6, 4.3, -4.8, 5.1, -5.3, 5.4, -5.3,
            5.0, -4.6, 4.0, -3.3, 2.5, -1.6, 0.6, 0.4, -1.4, 2.3,
            -3.1, 3.8, -4.4, 4.9, -5.3, 5.6, -5.8, 5.9, -5.9, 5.8
        ],
        timing_pattern=[0.100] * 30,  # ~600 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.65
    ),
    
    "m4a4": WeaponProfile(
        name="m4a4",
        display_name="M4A4",
        weapon_class="Rifle",
        damage=95,
        fire_rate=75,
        accuracy=80,
        range=80,
        mobility=70,
        control=70,
        vertical_pattern=[
            -3.8, -4.9, -5.7, -6.3, -6.8, -7.1, -7.3, -7.4, -7.4, -7.3,
            -7.1, -6.8, -6.4, -5.9, -5.3, -4.6, -3.8, -3.0, -2.1, -1.2,
            -0.3, 0.6, 1.4, 2.2, 2.9, 3.5, 4.0, 4.4, 4.7, 4.9
        ],
        horizontal_pattern=[
            0.0, -0.8, 1.4, -1.9, 2.3, -2.6, 2.8, -2.9, 2.9, -2.8,
            2.6, -2.3, 1.9, -1.4, 0.8, -0.2, -0.4, 0.9, -1.4, 1.8,
            -2.1, 2.3, -2.4, 2.4, -2.3, 2.1, -1.8, 1.4, -0.9, 0.4
        ],
        timing_pattern=[0.091] * 30,  # ~660 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.75
    ),
    
    "m4a1s": WeaponProfile(
        name="m4a1s",
        display_name="M4A1-S",
        weapon_class="Rifle",
        damage=100,
        fire_rate=70,
        accuracy=85,
        range=85,
        mobility=65,
        control=80,
        vertical_pattern=[
            -3.2, -4.1, -4.8, -5.3, -5.7, -5.9, -6.0, -6.0, -5.9, -5.7,
            -5.4, -5.0, -4.5, -3.9, -3.2, -2.4, -1.6, -0.7, 0.2, 1.0,
            1.7, 2.3, 2.8, 3.2, 3.5, 3.7, 3.8, 3.8, 3.7, 3.5
        ],
        horizontal_pattern=[
            0.0, -0.6, 1.1, -1.5, 1.8, -2.0, 2.1, -2.2, 2.2, -2.1,
            1.9, -1.6, 1.3, -0.9, 0.5, -0.1, -0.3, 0.6, -1.0, 1.3,
            -1.5, 1.6, -1.6, 1.5, -1.4, 1.2, -0.9, 0.6, -0.3, 0.0
        ],
        timing_pattern=[0.100] * 30,  # ~600 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.8
    ),
    
    "aug": WeaponProfile(
        name="aug",
        display_name="AUG",
        weapon_class="Rifle",
        damage=90,
        fire_rate=80,
        accuracy=85,
        range=75,
        mobility=65,
        control=75,
        vertical_pattern=[
            -3.0, -3.8, -4.4, -4.9, -5.2, -5.4, -5.5, -5.5, -5.4, -5.2,
            -4.9, -4.5, -4.0, -3.4, -2.7, -1.9, -1.1, -0.2, 0.6, 1.4,
            2.1, 2.7, 3.2, 3.6, 3.9, 4.1, 4.2, 4.2, 4.1, 3.9
        ],
        horizontal_pattern=[
            0.0, -0.4, 0.7, -1.0, 1.2, -1.4, 1.5, -1.5, 1.4, -1.3,
            1.1, -0.9, 0.6, -0.3, 0.0, 0.2, -0.5, 0.7, -0.9, 1.0,
            -1.1, 1.1, -1.0, 0.9, -0.7, 0.5, -0.3, 0.1, 0.1, -0.3
        ],
        timing_pattern=[0.091] * 30,  # ~660 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.85
    )
}


# CS2 SMGs
CS2_SMGS = {
    "mp9": WeaponProfile(
        name="mp9",
        display_name="MP9",
        weapon_class="SMG",
        damage=60,
        fire_rate=95,
        accuracy=60,
        range=45,
        mobility=90,
        control=65,
        vertical_pattern=[
            -2.0, -2.6, -3.1, -3.5, -3.8, -4.0, -4.1, -4.1, -4.0, -3.8,
            -3.5, -3.1, -2.6, -2.0, -1.3, -0.6, 0.1, 0.8, 1.4, 2.0,
            2.5, 2.9, 3.2, 3.4, 3.5, 3.5, 3.4, 3.2, 2.9, 2.5
        ],
        horizontal_pattern=[
            0.0, -0.5, 0.9, -1.2, 1.4, -1.5, 1.6, -1.6, 1.5, -1.4,
            1.2, -0.9, 0.6, -0.2, -0.2, 0.5, -0.8, 1.0, -1.2, 1.3,
            -1.3, 1.2, -1.1, 0.9, -0.7, 0.4, -0.1, -0.2, 0.5, -0.7
        ],
        timing_pattern=[0.057] * 30,  # ~1050 RPM
        base_sensitivity=1.2,
        ads_sensitivity=0.9
    ),
    
    "ump45": WeaponProfile(
        name="ump45",
        display_name="UMP-45",
        weapon_class="SMG",
        damage=75,
        fire_rate=75,
        accuracy=70,
        range=55,
        mobility=80,
        control=75,
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
        timing_pattern=[0.092] * 30,  # ~650 RPM
        base_sensitivity=1.1,
        ads_sensitivity=0.85
    )
}


# CS2 Snipers
CS2_SNIPERS = {
    "awp": WeaponProfile(
        name="awp",
        display_name="AWP",
        weapon_class="Sniper Rifle",
        damage=150,
        fire_rate=20,
        accuracy=100,
        range=100,
        mobility=25,
        control=20,
        vertical_pattern=[
            -15.0, -18.5, -21.0, -22.8, -24.0, -24.8, -25.2, -25.3, -25.1, -24.6,
            -23.8, -22.7, -21.3, -19.6, -17.6, -15.3, -12.7, -9.8, -6.6, -3.1,
            0.6, 4.5, 8.6, 12.9, 17.4, 22.1, 27.0, 32.1, 37.4, 42.9
        ],
        horizontal_pattern=[
            0.0, -4.0, 7.2, -9.8, 11.8, -13.2, 14.2, -14.8, 15.1, -14.9,
            14.4, -13.6, 12.5, -11.1, 9.5, -7.7, 5.7, -3.5, 1.1, 1.3,
            -3.8, 6.4, -8.9, 11.3, -13.6, 15.8, -17.8, 19.6, -21.3, 22.8
        ],
        timing_pattern=[1.200] * 30,  # ~50 RPM (bolt-action)
        base_sensitivity=0.4,
        ads_sensitivity=0.2
    ),
    
    "ssg08": WeaponProfile(
        name="ssg08",
        display_name="SSG 08",
        weapon_class="Sniper Rifle",
        damage=105,
        fire_rate=40,
        accuracy=95,
        range=90,
        mobility=50,
        control=40,
        vertical_pattern=[
            -8.5, -10.8, -12.5, -13.7, -14.5, -15.0, -15.2, -15.1, -14.8, -14.2,
            -13.4, -12.3, -11.0, -9.4, -7.6, -5.5, -3.2, -0.7, 2.0, 4.9,
            8.0, 11.3, 14.8, 18.5, 22.4, 26.5, 30.8, 35.3, 40.0, 44.9
        ],
        horizontal_pattern=[
            0.0, -2.5, 4.5, -6.0, 7.2, -8.0, 8.5, -8.7, 8.8, -8.6,
            8.1, -7.4, 6.5, -5.4, 4.1, -2.7, 1.1, 0.5, -2.1, 3.6,
            -5.1, 6.5, -7.8, 8.9, -9.9, 10.7, -11.3, 11.7, -11.9, 12.0
        ],
        timing_pattern=[0.800] * 30,  # ~75 RPM (bolt-action)
        base_sensitivity=0.6,
        ads_sensitivity=0.35
    )
}


# CS2 Pistols
CS2_PISTOLS = {
    "deagle": WeaponProfile(
        name="deagle",
        display_name="Desert Eagle",
        weapon_class="Pistol",
        damage=120,
        fire_rate=35,
        accuracy=75,
        range=75,
        mobility=75,
        control=30,
        vertical_pattern=[
            -6.5, -8.5, -10.0, -11.0, -11.8, -12.3, -12.6, -12.7, -12.6, -12.3,
            -11.8, -11.1, -10.2, -9.1, -7.8, -6.3, -4.6, -2.7, -0.6, 1.6,
            4.0, 6.5, 9.2, 12.1, 15.2, 18.5, 22.0, 25.7, 29.6, 33.7
        ],
        horizontal_pattern=[
            0.0, -1.8, 3.2, -4.3, 5.2, -5.8, 6.2, -6.4, 6.5, -6.4,
            6.1, -5.6, 4.9, -4.1, 3.1, -2.0, 0.8, 0.4, -1.6, 2.7,
            -3.7, 4.6, -5.4, 6.1, -6.7, 7.2, -7.6, 7.9, -8.1, 8.2
        ],
        timing_pattern=[0.267] * 30,  # ~225 RPM
        base_sensitivity=0.9,
        ads_sensitivity=0.6
    ),
    
    "glock": WeaponProfile(
        name="glock",
        display_name="Glock-18",
        weapon_class="Pistol",
        damage=65,
        fire_rate=85,
        accuracy=70,
        range=50,
        mobility=85,
        control=75,
        vertical_pattern=[
            -2.2, -2.8, -3.3, -3.7, -4.0, -4.2, -4.3, -4.3, -4.2, -4.0,
            -3.7, -3.3, -2.8, -2.2, -1.5, -0.7, 0.1, 0.9, 1.6, 2.3,
            2.9, 3.4, 3.8, 4.1, 4.3, 4.4, 4.4, 4.3, 4.1, 3.8
        ],
        horizontal_pattern=[
            0.0, -0.4, 0.7, -1.0, 1.2, -1.4, 1.5, -1.5, 1.4, -1.2,
            1.0, -0.7, 0.4, -0.1, -0.3, 0.5, -0.8, 1.0, -1.1, 1.2,
            -1.2, 1.1, -1.0, 0.8, -0.6, 0.3, -0.1, -0.2, 0.4, -0.6
        ],
        timing_pattern=[0.150] * 30,  # ~400 RPM
        base_sensitivity=1.1,
        ads_sensitivity=0.8
    ),
    
    "usp": WeaponProfile(
        name="usp",
        display_name="USP-S",
        weapon_class="Pistol",
        damage=85,
        fire_rate=70,
        accuracy=85,
        range=65,
        mobility=80,
        control=80,
        vertical_pattern=[
            -2.0, -2.5, -2.9, -3.2, -3.4, -3.5, -3.5, -3.4, -3.2, -2.9,
            -2.5, -2.0, -1.4, -0.7, 0.0, 0.7, 1.4, 2.0, 2.5, 2.9,
            3.2, 3.4, 3.5, 3.5, 3.4, 3.2, 2.9, 2.5, 2.0, 1.4
        ],
        horizontal_pattern=[
            0.0, -0.2, 0.4, -0.6, 0.7, -0.8, 0.8, -0.8, 0.7, -0.6,
            0.4, -0.2, 0.0, 0.2, -0.4, 0.5, -0.6, 0.7, -0.7, 0.6,
            -0.5, 0.4, -0.2, 0.0, 0.2, -0.4, 0.5, -0.6, 0.6, -0.5
        ],
        timing_pattern=[0.171] * 30,  # ~350 RPM
        base_sensitivity=1.0,
        ads_sensitivity=0.75
    )
}


def get_all_cs2_weapons() -> Dict[str, WeaponProfile]:
    """Get all CS2 weapon profiles."""
    all_weapons = {}
    all_weapons.update(CS2_RIFLES)
    all_weapons.update(CS2_SMGS)
    all_weapons.update(CS2_SNIPERS)
    all_weapons.update(CS2_PISTOLS)
    return all_weapons


def get_weapon_by_name(weapon_name: str) -> WeaponProfile:
    """Get a specific CS2 weapon profile by name."""
    all_weapons = get_all_cs2_weapons()
    return all_weapons.get(weapon_name.lower())


def get_weapons_by_class(weapon_class: str) -> Dict[str, WeaponProfile]:
    """Get CS2 weapons by class."""
    class_mapping = {
        "rifle": CS2_RIFLES,
        "smg": CS2_SMGS,
        "sniper_rifle": CS2_SNIPERS,
        "pistol": CS2_PISTOLS
    }
    return class_mapping.get(weapon_class.lower(), {})


def get_recommended_settings(weapon_name: str) -> Dict[str, float]:
    """Get recommended sensitivity settings for a CS2 weapon."""
    weapon = get_weapon_by_name(weapon_name)
    if weapon:
        return {
            "base_sensitivity": weapon.base_sensitivity,
            "ads_sensitivity": weapon.ads_sensitivity,
            "randomization": 0.08 if weapon.control > 70 else 0.12,  # CS2 has VAC
            "security_level": "high"
        }
    return {"base_sensitivity": 1.0, "ads_sensitivity": 0.8, "randomization": 0.10}