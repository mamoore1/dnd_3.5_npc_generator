# Dictionaries for weapons and armour

# Dictionary for melee weapons. If the list has a 3rd item, this indicates that
# the weapon uses two hands
melee_weapon_dict = {'simple': {
                                'dagger': ['1d4', '19-20/x2'],
                                'punch dagger': ['1d4', 'x3'],
                                'light mace': ['1d6', 'x2'],
                                'sickle': ['1d6', 'x2'],
                                'club': ['1d6', 'x2'],
                                'heavy mace': ['1d8', 'x2'],
                                'morningstar': ['1d8', 'x2'],
                                'shortspear': ['1d6', 'x2'],
                                'longspear': ['1d8', 'x3', 2],
                                'quarterstaff': ['1d6/1d6', 'x2', 2],
                                'spear': ['1d8', 'x3', 2]
                                },
                     'martial': {
                         'light hammer': ['1d4', 'x2'],
                         'handaxe': ['1d6', 'x3'],
                         'kukri': ['1d4', '18-20/x2'],
                         'light pick': ['1d4', 'x4'],
                         'sap': ['(Non-lethal) 1d6', 'x2'],
                         'shortsword': ['1d6', '19-20/x2'],
                         'battleaxe': ['1d8', 'x3'],
                         'flail': ['1d8', 'x2'],
                         'longsword': ['1d8', '19-20/x2'],
                         'heavy pick': ['1d6', 'x4'],
                         'rapier': ['1d6', '18-20/x2'],
                         'scimitar': ['1d6', '18-20/x2'],
                         'trident': ['1d8', 'x2'],
                         'warhammer': ['1d8', 'x3'],
                         'falchion': ['2d4', '18-20/x2', 2],
                         'glaive': ['1d10', 'x3', 2],
                         'heavy flail': ['1d20', '19-20/x2', 2],
                         'greatsword': ['2d6', '19-20/x2', 2],
                         'guisarme': ['2d4', 'x3', 2],
                         'halberd': ['1d10', 'x3', 2],
                         'lance': ['1d8', 'x3', 2],
                         'ranseur': ['2d4', 'x3', 2],
                         'scythe': ['2d4', 'x4', 2]
                      },
                      'exotic': {
                          'kama': ['1d6', 'x2'],
                          'nunchaku': ['1d6', 'x2'],
                          'sai': ['1d4', 'x2'],
                          'siangham': ['1d6', 'x2'],
                          'whip': ['(Non-lethal) 1d3', 'x2']
                      }
                     }
# Damage, crit ratio, range in feet
ranged_weapon_dict = {
    'simple': {
        'heavy crossbow': ['1d10', '19-20/x2', '120'],
        'light crossbow': ['1d8', '19-20/x2', '80'],
        'dart': ['1d4', 'x2', '20'],
        'javelin': ['1d6', 'x2', '30'],
        'sling': ['1d4', 'x2', '50']
    },
    'martial': {
        'longbow': ['1d8', 'x3', '100'],
        'shortbow': ['1d6', 'x3', '60']
    },
    'exotic': {
        'hand crossbow': ['1d4', '19-20/x2', '30'],
        'shuriken': ['1d2', 'x2', '10']
    }
}

# Putting all weapons and stats into dictionary
melee_weapon_list = {**melee_weapon_dict['simple'], **melee_weapon_dict['martial'], **melee_weapon_dict['exotic']}
ranged_weapon_list = {**ranged_weapon_dict['simple'], **ranged_weapon_dict['martial'], **ranged_weapon_dict['exotic']}

# Dictionary for armour. List contains: [AC Bonus, Max DEX Bonus]
armour_dict = {
    'light': {
        'padded': [1, 8],
        'leather': [2, 6],
        'studded leather': [3, 5],
        'chain shirt': [4, 4]
    },
    'medium': {
        'hide': [3, 4],
        'scale mail': [4, 3],
        'chainmail': [5, 2],
        'breastplate': [5, 3]
    },
    'heavy': {'splint mail': [6, 0],
              'banded mail': [6, 1],
              'half-plate': [7, 0],
              'full plate': [8, 1]
    }
}

armour_list = {**armour_dict['light'], **armour_dict['medium'], **armour_dict['heavy']}