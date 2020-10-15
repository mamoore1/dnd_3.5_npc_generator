from math import floor

# TO DO:
# Separate file with weapons and armour, (possibly?) classes for each. Might be easier just to determine the AC, etc.,
# as don't actually need the other stats

# TO DO:
# Class for character races, holding racial abilities and feats (it also might be better to have race be a function)

# Class for character classes, holding hit dice, saving throws, etc.
class CharClass:
    def __init__(self, name, hit_dice, base_attack, fort_save_ratio, reflex_save_ratio, will_save_ratio,\
                 armour_proficiencies = None, weapon_proficiencies = ['simple']):
        self.name = name
        self.hit_dice = hit_dice
        self.base_attack = base_attack # To get a character's base attack, multiply level by base attack value, round down
        self.fort_save_ratio = fort_save_ratio # These ratios come in good and poor forms: good = 2 + level/2, poor = (1/3)*level
        self.reflex_save_ratio = reflex_save_ratio
        self.will_save_ratio = will_save_ratio
        self.weapon_proficiencies = weapon_proficiencies # aw[1:4]
        self.armour_proficiencies = armour_proficiencies # aw[0]
        # self.class_feats = {1: None} # Choose from list
        # self.extra_class_feats = [0, []] # Multiply by character level
        # TO DO:
        # self.spell_caster - type? (divine/arcane?)
        # some way of determining how many spells they should have (known and per day)
        # AC, touch AC and flat-footed AC
        # num of feats
        # class feats
        # class skills, skill points and assigned skill points (maybe randomly?)
        # add 1 to max ability score every 4 levels
        
    def __repr__(self):
        return self.name
    
    def get_class_feats(self):
        return self._class_feats
    
    def set_class_feats(self, val):
        self._class_feats = determine_class_feats(self.name)


def determine_class_feats(class_name):
    if class_name == 'fighter':
        feat_mod = 0
        feat_list = []
    #elif class_name == 'rogue':
        
# Class armour proficiences [0], general weapon proficiences [1] and specific melee [2] and ranged [3] weapon proficiences:
# For weapons, if the character is proficient with martial only this is listed, and if heavier armour proficiences are available,
# light is not shown
adept_aw = [[], ['simple'], [], []]
aristocrat_aw = [['medium', 'heavy'], ['martial'], [], []]
barbarian_aw = [['medium'], ['martial'], [], []]
bard_aw = [['light'], ['simple'], ['longsword', 'rapier', 'shortsword', 'sap', 'whip'], ['shortbow']]
cleric_aw = [['medium', 'heavy'], ['simple'], [], []]
commoner_aw = [[], ['simple'], [], []]
druid_aw = [['medium'], [], ['club', 'dagger', 'quarterstaff', 'scimitar', 'sickle', 'shortspear', 'spear'], ['dart', 'sling']]
expert_aw = [['light'], ['simple'], [], []]
fighter_aw = [['medium', 'heavy'], ['martial'], [], []]
monk_aw = [[], [], ['club', 'dagger', 'handaxe',  'kama', 'nunchaku', 'quarterstaff', 'sai', 'siangham'], ['light crossbow', 'heavy crossbow', 'javelin', 'shuriken', 'sling']]
paladin_aw = [['medium', 'heavy'], ['martial'], [], []]
ranger_aw = [['light'], ['martial'], [], []]
rogue_aw = [['light'], ['simple'], ['rapier', 'sap', 'shortsword'], ['hand crossbow', 'shortbow']]
sorcerer_aw = [[], ['simple'], [], []]
warrior_aw = [['medium', 'heavy'], ['martial'], [], []]
wizard_aw = [[], [], ['club', 'dagger', 'quarterstaff'], ['light crossbow', 'heavy crossbow']]

adept = CharClass('adept', 6, 1/2, 'poor', 'poor', 'good', adept_aw[0], adept_aw[1:])
aristocrat = CharClass('aristocrat', 8, 2/3, 'poor', 'poor', 'good', aristocrat_aw[0], aristocrat_aw[1:])
barbarian = CharClass('barbarian', hit_dice=12, base_attack=1, fort_save_ratio='good', will_save_ratio='poor', reflex_save_ratio='poor', armour_proficiencies=barbarian_aw[0], weapon_proficiencies=barbarian_aw[1:])
bard = CharClass('bard', 6, 2/3, 'poor', 'good', 'good', bard_aw[0], bard_aw[1:])
cleric = CharClass('cleric', 8, 2/3, 'good', 'poor', 'good', cleric_aw[0], bard_aw[1:])
commoner = CharClass('commoner', 4, 1/2, 'poor', 'poor', 'poor', commoner_aw[0], commoner_aw[1:])
druid = CharClass('druid', 8, 2/3, 'good', 'poor', 'good', druid_aw[0], druid_aw[1:])
expert = CharClass('expert', 6, 2/3, 'poor', 'poor', 'good', expert_aw[0], expert_aw[1:])
fighter = CharClass('fighter', 10, 1, 'good', 'poor', 'poor', fighter_aw[0], fighter_aw[1:])
monk = CharClass('monk', 8, 2/3, 'good', 'good', 'good', monk_aw[0], monk_aw[1:])
paladin = CharClass('paladin', 10, 1, 'good', 'poor', 'poor', paladin_aw[0], paladin_aw[1:])
ranger = CharClass('ranger', 8, 1, 'good', 'good', 'poor', ranger_aw[0], ranger_aw[1:])
rogue = CharClass('rogue', 6, 2/3, 'poor', 'good', 'poor', rogue_aw[0], rogue_aw[1:])
sorcerer = CharClass('sorcerer', 4, 1/2, 'poor', 'poor', 'good', sorcerer_aw[0], sorcerer_aw[1:])
warrior = CharClass('warrior', 8, 1, 'good', 'poor', 'poor', warrior_aw[0], warrior_aw[1:])
wizard = CharClass('wizard', 4, 1/2, 'poor', 'poor', 'good', wizard_aw[0], wizard_aw[1:])


class_list = [adept, aristocrat, barbarian, bard, cleric, commoner, druid, expert, fighter, monk, paladin, ranger, rogue, sorcerer, warrior, wizard]
