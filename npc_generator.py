from math import floor
import char_class as cc
# Class list = adept, aristocrat, barbarian, bard, cleric, commoner, druid, expert, fighter, monk, paladin, ranger, rogue, sorcerer, warrior, wizard
from armour_weapons_dicts import melee_weapon_dict, ranged_weapon_dict, melee_weapon_list, ranged_weapon_list, armour_dict, armour_list
import numpy as np
import random

class Character:
    def __init__(self, char_class, level):
        self.char_class = char_class.name
        self.hit_dice = char_class.hit_dice
        self.level = level
        self.str = 10
        self.dex = 10
        self.con = 10
        self.int = 10
        self.wis = 10
        self.cha = 10
        self.base_attack = char_class.base_attack
        self.melee_attack = 0
        self.ranged_attack = 0
        self.fort_save = char_class.fort_save_ratio
        self.reflex_save = char_class.reflex_save_ratio
        self.will_save = char_class.will_save_ratio
        self.hp = self.hit_dice 
        
    def __repr__(self):
        return f'''
        level: {self.level}, class: {self.char_class}
        
        Stats:
        HP: {self.hp}   AC: {self.ac} (touch: {self.touch_ac}, flat-footed: {self.flat_ac})\tArmour: {self.armour.title()}
        STR: {self.str}, DEX: {self.dex}, CON: {self.con}, INT: {self.int}, WIS: {self.wis}, CHA: {self.cha}
        Initiative: +{self.initiative}
        
        Attacks:
        Base attack: +{self.base_attack}{self.extra_atks}
        Melee attack: +{self.melee_attack}{self.extra_melee_atks}, {self.melee_weapon.title()}: {self.melee_damage}, {self.mel_crit},\
        Ranged attack: +{self.ranged_attack}{self.extra_ranged_atks}, {self.ranged_weapon.title()}: {self.ranged_damage}, {self.ranged_crit}, Range: {self.range}ft 
        
        Saves:
        F/R/W: +{self.fort_save}/+{self.reflex_save}/+{self.will_save}
        '''
    
    # Called after distributing ability scores, updates base attack, melee attack and ranged attack
    # based on char_class's base attack value, and Character's level, str and con
    def update_attacks(self):
        base = self.base_attack
        level = self.level
        str_mod = floor((self.str-10)/2)
        dex_mod = floor((self.dex-10)/2)
        self.base_attack = floor(base * level)
        self.melee_attack = floor((base * level) + str_mod)
        self.ranged_attack = floor((base * level) + dex_mod)
    
    # Called after distributing ability scores, updates fortitude, will and reflex saves based on char_class's
    # fortitude, will and reflex save values, and Characters' level, con, wis and dex scores
    def update_saves(self):
        level = self.level
        fort_save_ratio = self.fort_save
        will_save_ratio = self.will_save
        reflex_save_ratio = self.reflex_save
        con_mod = mod_calculator(self.con)
        wis_mod = mod_calculator(self.wis)
        dex_mod = mod_calculator(self.dex)
        self.fort_save = floor(2 + con_mod + (level * .5)) if (fort_save_ratio == 'good') else floor(con_mod + (level * 1/3))
        self.will_save = floor(2 + wis_mod + (level * .5)) if (will_save_ratio == 'good') else floor(wis_mod + (level * 1/3))
        self.reflex_save = floor(2 + dex_mod + (level * .5)) if (reflex_save_ratio == 'good') else floor(dex_mod + (level * 1/3))
        self.initiative = dex_mod
    
    # Called after distributing ability scores, sets hp based on level, con mod and hit dice
    def update_hp(self):
        con_mod = mod_calculator(self.con)
        hit_dice = self.hit_dice
        level = self.level
        self.hp = sum(dice_roller(level, con_mod, hit_dice))
        
    # Function which uses the weapon proficiences of a specific character class to choose a weapon for the character
    def select_weapons(self, char_class):
        weapon_profs = char_class.weapon_proficiencies
        gen_weapon_profs = weapon_profs[0] # General weapon proficiences, i.e., 'simple' or 'martial'
        spec_mel_profs = weapon_profs[1] # Specific melee weapon profs, e.g., 'shortsword', 'club'
        spec_ran_profs = weapon_profs[2] # Specific ranged weapon profs, e.g., 'light crossbow'
        try:
            melee_weapons = list(melee_weapon_dict[gen_weapon_profs[0]].keys())
        except IndexError:
            melee_weapons = []
        if spec_mel_profs:
            melee_weapons.extend(spec_mel_profs)
        self.melee_weapon = random.choice(melee_weapons)
        melee_weapon_stats = melee_weapon_list[self.melee_weapon] # Getting weapon stats from list
        str_bonus = mod_calculator(self.str)
        if len(melee_weapon_stats) == 3:
            str_bonus *= 2
        self.melee_damage = '{0}{1:+d}'.format(melee_weapon_stats[0], str_bonus) # Defining melee damage
        self.mel_crit = melee_weapon_stats[1] # Defining crit chance
        try:
            ranged_weapons = list(ranged_weapon_dict[gen_weapon_profs[0]].keys())
        except IndexError:
            ranged_weapons = []
        if spec_ran_profs:
            ranged_weapons.extend(spec_ran_profs)
        self.ranged_weapon = random.choice(ranged_weapons)
        ranged_stats = ranged_weapon_list[self.ranged_weapon]
        self.ranged_damage, self.ranged_crit, self.range = ranged_stats # Defining damage, crit chance and range
        
      
    # Function which calculates the value of bonus attacks based on character base attack                                               
    def update_extra_attacks(self):
        base = self.base_attack
        melee = self.melee_attack
        ranged = self.ranged_attack
        num_bonus_atks = floor((base-1)/5) # Should be first bonus at +6, next at +11, etc.
        self.extra_atks = ''
        self.extra_melee_atks = ''
        self.extra_ranged_atks = ''
        for i in range(num_bonus_atks): # Adding extra attacks using base attack, melee attack and ranged attack
            self.extra_atks += f'/+{base-(i+1)*5}'
            self.extra_melee_atks += f'/+{melee-(i+1)*5}' # Using "melee" because melee could be updated based on magic weapons
            self.extra_ranged_atks += f'/+{ranged-(i+1)*5}'
    
    # Function which selects armour based on character armour proficiences
    def select_armour(self, char_class):
        try:
            armour_profs = char_class.armour_proficiencies[0]
        except IndexError:
            self.armour = ''
            self.armour_vals = [0, 10]
            return
        try:
            armours = list(armour_dict[armour_profs].keys())
        except IndexError:
            armours = ['']
        self.armour = random.choice(armours)
        if self.armour in armour_list:
            self.armour_vals = armour_list[self.armour]
        else:
            self.armour_vals = [0, 10]

    # Function which determines the AC for character    
    def update_ac(self):
        dex_mod = mod_calculator(self.dex)
        self.touch_ac = 10 + dex_mod # Calculating touch AC
        max_dex_mod = self.armour_vals[1]
        if max_dex_mod < dex_mod:
            dex_mod = max_dex_mod
        self.ac = 10 + self.armour_vals[0] + dex_mod
        self.flat_ac = self.ac - dex_mod
        
def mod_calculator(ability):
    return floor((ability-10)/2)
        
                                                      
# Function for rolling d6s with modifiers
def dice_roller(dice=1, modifier=0, sides=6):
    result = np.array(random.choices(range(1,sides+1), k=dice))
    result += modifier
    return result
    
# Function for rolling 4 d6 and dropping the lowest
def fourd6drop1():
    result = dice_roller(4)
    result.sort()
    result = result[1:4]
    return sum(result)
    
# Function for generating a sorted list of ability scores    
def ability_generator():
    ability_list = []
    for i in range(6):
        ability_list.append(fourd6drop1())
    ability_list.sort(reverse=True)
    return ability_list

#Function to hold character generation
def character_generator(char_class, level):
    character = Character(char_class, level)
    ability_scores = ability_generator()
    assign_ability_score(character, char_class, ability_scores)
    character.update_attacks()
    character.update_saves()
    character.update_hp()
    character.select_weapons(char_class)
    character.update_extra_attacks()
    character.select_armour(char_class)
    character.update_ac()
    print(character)
    
# Function assigning ability scores based on character class  
def assign_ability_score(character, char_class, ability_scores):
    # Barbarian: Str, Dex, Con
    if char_class.name == 'barbarian':
        character.str = ability_scores[0]
        character.dex = ability_scores[1]
        character.con = ability_scores[2]
        character.int, character.wis, character.cha = random.sample(ability_scores[3:], k=3)
    # Bard: Cha, Int, Dex
    elif char_class.name == 'bard':
        character.cha = ability_scores[0]
        character.int = ability_scores[1]
        character.dex = ability_scores[2]
        character.str, character.con, character.wis = random.sample(ability_scores[3:], k=3)
    # Cleric: Wis, Con, Str
    elif char_class.name == 'cleric':
        character.wis = ability_scores[0]
        character.con = ability_scores[1]
        character.str = ability_scores[2]
        character.dex, character.int, character.cha = random.sample(ability_scores[3:], k=3)
    # Druid and Adept: Wis, Dex, Con
    elif char_class.name == 'druid' or char_class.name == 'adept':
        character.wis = ability_scores[0]
        character.dex = ability_scores[1]
        character.con = ability_scores[2]
        character.str, character.int, character.cha = random.sample(ability_scores[3:], k=3)
    # Fighter, Commoner or Warrior: Str, Con, Dex
    elif char_class.name == 'fighter' or char_class.name == 'commoner' or char_class.name == 'warrior':
        character.str = ability_scores[0]
        character.con = ability_scores[1]
        character.dex = ability_scores[2]
        character.int, character.wis, character.cha = random.sample(ability_scores[3:], k=3)
    # Monk: Wis, Str, Dex
    elif char_class.name == 'monk':
        character.wis = ability_scores[0]
        character.str = ability_scores[1]
        character.dex = ability_scores[2]
        character.con, character.int, character.cha = random.sample(ability_scores[3:], k=3)
    # Paladin: Cha, Str, Wis
    elif char_class.name == 'paladin':
        character.cha = ability_scores[0]
        character.str = ability_scores[1]
        character.wis = ability_scores[2]
        character.dex, character.con, character.int = random.sample(ability_scores[3:], k=3)
    # Ranger: Dex, Str, Con
    elif char_class.name == 'ranger':
        character.dex = ability_scores[0]
        character.str = ability_scores[1]
        character.con = ability_scores[2]
        character.int, character.wis, character.cha = random.sample(ability_scores[3:], k=3)
    # Rogue, Aristocrat and Expert: Dex, Int, Con
    elif char_class.name == 'rogue' or char_class.name == 'aristocrat' or char_class.name == 'expert':
        character.dex = ability_scores[0]
        character.int = ability_scores[1]
        character.con = ability_scores[2]
        character.str, character.wis, character.cha = random.sample(ability_scores[3:], k=3)
    # Sorcerer: Cha, Dex, Con
    elif char_class.name == 'sorcerer':
        character.cha = ability_scores[0]
        character.dex = ability_scores[1]
        character.con = ability_scores[2]
        character.str, character.int, character.cha = random.sample(ability_scores[3:], k=3)
    # Wizard: Int, Dex, Con
    elif char_class.name == 'wizard':
        character.int = ability_scores[0]
        character.dex = ability_scores[1]
        character.con = ability_scores[2]
        character.str, character.wis, character.cha = random.sample(ability_scores[3:], k=3)


# cc.class_list = ['barbarian', 'bard', 'cleric', 'druid', 'fighter', 'monk', 'paladin', 'ranger', 'rogue', 'sorcerer', 'wizard']

#character_generator(cc.fighter, 20)
#character_generator(cc.druid, 20)
#character_generator(cc.wizard, 10)

# Function providing a crude UI for useability
def app_handler():
    character_class_lvl = []
    enum_list = enumerate(cc.class_list)
    enum_list = [[item1, item2] for item1, item2 in enum_list]
    characters = {key: value for key, value in enum_list}
    for i in range(len(enum_list)):
        print(f'{enum_list[i][0]}) {enum_list[i][1]}')
    while True:
        response = input('Please type the number of the class you want to select:\n> ')
        try:
            print(characters[int(response)])
            character_class_lvl.append(characters[int(response)])
            break
        except:
            print('Please enter a number:\n> ')
    while True:
        response = input('Please type the character level:\n> ')
        try:
            response = int(response)
            character_class_lvl.append(response)
            break
        except:
            print('Please enter a number:\n> ')
    while True:
        response = input('How many would you like to generate?\n> ')
        try:
            response = int(response)
            character_class_lvl.append(response)
            break
        except:
            print('Please enter a number:\n> ')
    for i in range(character_class_lvl[2]):
        character_generator(character_class_lvl[0], character_class_lvl[1])
    
app_handler()