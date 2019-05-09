import items as i
import math
import random

class TreasureHelper:

    def _find_key(self, dictionary, roll):
        """
        Item dictionary keys are tuples of the range and this returns the key that equates to a roll.

        type dictionary:    dict()
        type roll:          int(dice roll)

        rtype:              dict[key]
        """
        for k, v in dictionary.items():
            if k[0] <= roll <= k[1]:
                return k

    def _roll_dice_total(self, num, sides):
        """
        Rolls a given amount of dice.

        type num:   int(number of dice)
        type sides: int(number of sides)

        rtype:      int(total roll)
        """
        total = 0
        for roll in range(num):
            die = random.randint(1, sides)
            total += die
        return total




class Treasure(TreasureHelper):
    def __init__(self):
        self.coins = random.randint(1, 100)
        self.goods = random.randint(1, 100)
        self.items = random.randint(1, 100)
        self.total = 0
        self.sell = 0

    def _goods_and_values(self, good, num):
        """
        Finds gems and the amount they are worth for all gems.
    
        type good:  str(type of good)
        type num:   int(number of goods to create)

        rtype:      list[int, str...]
        """
        goods = []
        if good == 'gems':
            good_value = i.GEM_VALUE
            good_item = i.GEMS
        else:
            good_value = i.ART_VALUE
            good_item = i.ART
        for each in range(num):
            roll = random.randint(1, 100)
            key = self._find_key(good_value, roll)
            value = good_value[key]
            price = self._roll_dice_total(value[0], value[1]) * value[2]
            self.total += price
            self.sell += price
            item = random.choice(good_item[value[3]])
            goods.append('{} ({})'.format(item, price))
        return goods

    def _item_types(self, num, level):
        """
        Determines types of items.

        type num:   int(number of items)
        type level: str(item stregnth)

        rtype:      list[str]
        """
        items = {}
        for each in range(num):
            roll = random.randint(1, 100)
            key = self._find_key(i.ITEM_TYPE[level], roll)
            value = i.ITEM_TYPE[level][key]
            if value in items:
                items[value] += 1
            else:
                items[value] = 1
        return items


    def get_coins(self, cr, modifier=1):
        if cr > 20:
            cr = 20
        key = self._find_key(i.INITIAL_TREASURE[cr]['coins'], self.coins)
        value = i.INITIAL_TREASURE[cr]['coins'][key]
        if value:
            total = self._roll_dice_total(value[0], value[1]) * (modifier*value[2])
            if value[3] == 'copper':
                self.total += total/100
                self.sell += total/100
            elif value[3] == 'silver':
                self.total += total/10
                self.sell += total/10
            elif value[3] == 'gold':
                self.total += total
                self.sell += total
            else:
                self.total += total*10
                self.sell += total*10 
            return '{} {}'.format(total, value[3])
        else:
            return None


    def get_goods(self, cr, modifier=1):
        if cr > 20:
            cr = 20
        key = self._find_key(i.INITIAL_TREASURE[cr]['goods'], self.goods)
        value = i.INITIAL_TREASURE[cr]['goods'][key]
        if value:
            total = math.floor(self._roll_dice_total(value[0], value[1])*modifier)
            goods =  self._goods_and_values(value[2], total)
            return goods
        else:
            return None

    def get_items(self, cr, modifier=1):
        if cr > 20:
            cr = 20
            extras = True
        key = self._find_key(i.INITIAL_TREASURE[cr]['items'], self.items)
        value = i.INITIAL_TREASURE[cr]['items'][key]
        if value:
            total = self._roll_dice_total(value[0], value[1])
            total = math.floor(total*modifier)
            types = self._item_types(total, value[2])

            all_items = []

            if 'Armor and Shield' in types:
                all_items += self.get_armor(value[2], types['Armor and Shield'])

            if 'Weapon' in types:
                all_items += self.get_weapon(value[2], types['Weapon'])

            if 'Potion' in types:
                all_items += self.get_potion(value[2], types['Potion'])

            if 'Ring' in types:
                all_items += self.get_ring(value[2], types['Ring'])

            if 'Rod' in types:
                all_items += self.get_rod(value[2], types['Rod'])

            if 'Scroll' in types:
                all_items += self.get_scroll(value[2], types['Scroll'])

            if 'Staff' in types:
                all_items += self.get_staff(value[2], types['Staff'])

            if 'Wand' in types:
                all_items += self.get_wand(value[2], types['Wand'])

            if 'Wondrous' in types:
                all_items += self.get_wondrous(value[2], types['Wondrous'])

            return all_items
        else:
            return None

    def get_treasure(self, cr, *args):
        all_treasure = []
        if not args:
            coins = self.get_coins(cr)
            goods = self.get_goods(cr)
            items = self.get_items(cr)
            return [self.total, self.sell, coins, goods, items]

        if 'x2' in args:
            coins = self.get_coins(cr, 2)
            goods = self.get_goods(cr, 2)
            items = self.get_items(cr, 2)
            return [self.total, self.sell, coins, goods, items]
        elif 'x3' in args:
            coins = self.get_coins(cr, 3)
            goods = self.get_goods(cr, 3)
            items = self.get_items(cr, 3)
            return [self.total, self.sell, coins, goods, items]


        if '-c' not in args:
            if 'c-' in args:
                coins = self.get_coins(cr, 0.5)
            elif 'c--' in args:
                coins = self.get_coins(cr, 0.1)
            elif 'c+' in args:
                coins = self.get_coins(cr, 2)
            else:
                coins = self.get_coins(cr)
        else:
            coins = None

        if '-g' not in args:
            if 'g-' in args:
                goods = self.get_goods(cr, 0.5)
            elif 'g+' in args:
                goods = self.get_goods(cr, 2)
            else:
                goods = self.get_goods(cr)

        else:
            goods = None

        if '-i' not in args:
            if 'i-' in args:
                items = self.get_items(cr, 0.5)
            elif 'i+' in args:
                items = self.get_items(cr, 2)
            else:
                items = self.get_items(cr)

        else:
            items = None

        logging.info('Rolled a treasure')
        return [self.total, self.sell, coins, goods, items]




    def get_armor(self, strength, n=1):
        all_armors = []
        armor = Armor(strength)
        for _ in range(n):
            all_armors.append(armor.get_armor())
        self.total += armor.price
        self.sell += armor.sell
        return all_armors

    def get_weapon(self, strength, n=1):
        all_weapons = []
        weapon = Weapon(strength)
        for _ in range(n):
            all_weapons.append(weapon.get_weapon())
        self.total += weapon.price
        self.sell += weapon.sell
        return all_weapons

    def get_potion(self, strength, n=1):
        all_potions = []
        potion = Potion(strength)
        for _ in range(n):
            all_potions.append(potion.get_potion())
        self.total += potion.price
        self.sell += potion.sell
        return all_potions

    def get_ring(self, strength, n=1):
        all_rings = []
        ring = Ring(strength)
        for _ in range(n):
            all_rings.append(ring.get_ring())
        self.total += ring.price
        self.sell += ring.sell
        return all_rings

    def get_rod(self, strength, n=1):
        all_rods = []
        rod = Rod(strength)
        for _ in range(n):
            all_rods.append(rod.get_rod())
        self.total += rod.price
        self.sell += rod.sell
        return all_rods

    def get_scroll(self, strength, n=1):
        all_scrolls = []
        scroll = Scroll(strength)
        for _ in range(n):
            all_scrolls.append(scroll.get_scroll())
        self.total += scroll.price
        self.sell += scroll.sell
        return all_scrolls

    def get_staff(self, strength, n=1):
        all_staff = []
        staff = Staff(strength)
        for _ in range(n):
            all_staff.append(staff.get_staff())
        self.total += staff.price
        self.sell += staff.sell
        return all_staff

    def get_wand(self, strength, n=1):
        all_wands = []
        wand = Wand(strength)
        for _ in range(n):
            all_wands.append(wand.get_wand())
        self.total += wand.price
        self.sell += wand.sell
        return all_wands

    def get_wondrous(self, strength, n=1):
        all_wondrous = []
        wondrous = Wondrous(strength)
        for _ in range(n):
            all_wondrous.append(wondrous.get_wondrous())
        self.total += wondrous.price
        self.sell += wondrous.sell
        return all_wondrous



class Armor(TreasureHelper):
    def __init__(self, level):
        self.level = level
        self.price = 0
        self.sell = 0

    def _armor_material(self, armor):
        """
        Rolls for special Material and checks to see if it works for the
        armor and gets the cost.

        type armor: tup(str(armor), int(size))  

        rtype:      tup(str(material), int(value))
        """

        while True:
            roll = random.randint(1, 100)
            roll_key = self._find_key(i.SPECIAL_ARMOR_MATERIAL, roll)
            roll_value = i.SPECIAL_ARMOR_MATERIAL[roll_key]

            if roll_value:

                if type(armor) == list:
                    if roll_value[armor[1]+2]:
                        if roll_value[0] == 'dragonscale':
                            dragonscale_roll = random.randint(1, 100)
                            dragonscale_key = self._find_key(i.DRAGONSCALE_TYPE, dragonscale_roll)
                            dragonscale_value = i.DRAGONSCALE_TYPE[dragonscale_key]
                            return ('{} {}'.format(dragonscale_value, roll_value[0]), roll_value[armor[1]+2])
                        return (roll_value[0], roll_value[armor[1]+2])

                else:
                    if roll_value[1]:
                        if roll_value[0] == 'dragonscale':
                            dragonscale_roll = random.randint(1, 100)
                            dragonscale_key = self._find_key(i.DRAGONSCALE_TYPE, dragonscale_roll)
                            dragonscale_value = i.DRAGONSCALE_TYPE[dragonscale_key]
                            return ('{} {}'.format(dragonscale_value, roll_value[0]), roll_value[2])
                        return (roll_value[0], roll_value[2])

            else:
                return None



    def _value_check(self, enhancement, abilities):
        """
        This makes sure the item does is not either over +10 enhancement nor over 200k gold.

        type enhancement:   int(base item enhancement)
        type abilities:     list[str(ability name), int(value)]
        *args               weapon, shield, armor

        rtype:              list[str(ability name, int(value)] 
        """

        total_enhancement = enhancement
        total_gold = 0

        for ability in abilities:
            if ability[1] <= 10:
                total_enhancement += ability[1]
            else:
                total_gold += ability[1]

        total = (total_enhancement**2*1000)+total_gold
        if total > 200000:
            fixed = self._fix_cost(enhancement, abilities)
            
            bonuses = enhancement
            for ability in fixed:
                if ability[1] <= 10:
                    bonuses += ability[1]
            if bonuses > 10:
                fixed = self._fix_bonus(enhancement, fixed)
                return fixed
            else:
                return fixed

        return abilities


    def _fix_cost(self, enhancement, abilities):
        """
        Picks the highest value abilities to fit for the armor. Orders the abilities
        by value and selects the most valuable abilities to add first.

        type base:      int(base enchancement bonus)
        type abilities: list[str(ability name), int(value)]
        args:           cost

        rtype:          list[str(ability name), int(value)]
        """
        ordered_abilities = abilities
        ordered_abilities.sort(key=lambda x: x[1], reverse=True)
        gold_abilities = []
        adjusted_abilities = []
        total_enhancement = enhancement

        for ability in ordered_abilities:
            if ability[1] > 10:
                gold_abilities.append((ability))
            else:
                adjusted_abilities.append(ability)
                total_enhancement += ability[1]

        total = total_enhancement**2*1000

        for ability in gold_abilities:
            if ability[1] + total <= 200000:
                adjusted_abilities.append(ability)
                total += ability[1]

        return adjusted_abilities


    def _fix_bonus(self, enhancement, abilities):
        """
        Picks the highest value abilities to fit for the armor. Orders the abilities
        by value and selects the highest bonuses abilities to add first.

        type base:      int(base enchancement bonus)
        type abilities: list[str(ability name), int(value)]
        args:           cost

        rtype:          list[str(ability name), int(value)]
        """
        ordered_abilities = abilities
        ordered_abilities.sort(key=lambda x: x[1], reverse=True)
        adjusted_abilities = []
        bonus_abilities = []
        total_enhancement = enhancement



        for ability in ordered_abilities:
            if ability[1] <= 10:
                bonus_abilities.append(ability)
            else:
                adjusted_abilities.append(ability)

        for ability in bonus_abilities:
            if ability[1] + total_enhancement <= 10:
                adjusted_abilities.append(ability)
                total_enhancement += ability[1]


        return adjusted_abilities


    def _upgrade_ability(self, abilities, current):
        """
        Checks current ability rolled vs abilities you already have
        and upgrades where appropriate.

        type abilities: list[list[str(ability name), int(value)]]
        type current:   list[str(ability name), int(value)]

        rtype:          list[list[str(ability name), int(value)]]
        """
        values = {
            'light': 1,
            'moderate': 2,
            'heavy': 3,
            'improved': 1,
            'greater': 2,
            '(13)': 1,
            '(15)': 2,
            '(17)': 3,
            '(19)': 4
        }

        if 'resistance' in current[0]:
            for num, ability in enumerate(abilities):
                if 'resistance' in ability[0]:
                    if 'spell' in ability[0] and 'spell' in current[0]:
                        new = current[0].split()
                        old = ability[0].split()
                        if values[new[2]] > values[old[2]]:
                            return (True, num)
                    elif 'acid' in ability[0] and 'acid' in current[0]:
                        new = current[0].split()
                        old = ability[0].split()
                        if len(new) > len(old):
                            return (True, num)
                        elif len(new) == len(old):
                            if values[new[0]] > values[old[0]]:
                                return (True, num)
                    elif 'cold' in ability[0] and 'cold' in current[0]:
                        new = current[0].split()
                        old = ability[0].split()
                        if len(new) > len(old):
                            return (True, num)
                        elif len(new) == len(old):
                            if values[new[0]] > values[old[0]]:
                                return (True, num)
                    elif 'fire' in ability[0] and 'fire' in current[0]:
                        new = current[0].split()
                        old = ability[0].split()
                        if len(new) > len(old):
                            return (True, num)
                        elif len(new) == len(old):
                            if values[new[0]] > values[old[0]]:
                                return (True, num)
                    elif 'electricity' in ability[0] and 'electricity' in current[0]:
                        new = current[0].split()
                        old = ability[0].split()
                        if len(new) > len(old):
                            return (True, num)
                        elif len(new) == len(old):
                            if values[new[0]] > values[old[0]]:
                                return (True, num)
                    elif 'sonic' in ability[0] and 'sonic' in current[0]:
                        new = current[0].split()
                        old = ability[0].split()
                        if len(new) > len(old):
                            return (True, num)
                        elif len(new) == len(old):
                            if values[new[0]] > values[old[0]]:
                                return (True, num)
                else:
                    return (False, True)

        elif 'fortification' in current[0]:
            for num, ability in enumerate(abilities):
                if 'fortification' in ability[0]:
                    new = current[0].split()
                    old = ability[0].split()
                    if values[new[0]] > values[old[0]]:
                        return (True, num)
                else:
                    return (False, True)

        return False



    def _finish_armor(self, material, abilities, armor, enhancement):
        """
        turns the material, armor, abilities, and enhancement into a readable string
        with the value of the item in parenthese.

        type material:      str()
        type abilities:     list[str(ability name), int(value)]
        type armor:         str()
        type enhancement:   int()

        rtype:              str()
        """

        total_enhancements = enhancement
        total_gold = 0
        if material:
            material_type = material[0]
            material_cost = material[1]
        else:
            material_cost = 0

        abilities_string = ''
        for ability in abilities:
            if abilities_string:
                abilities_string += ', ' + ability[0]
            else:
                abilities_string = ability[0]

            if ability[1] <= 10:
                total_enhancements += ability[1]
            else:
                total_gold += ability[1]

        total = (total_enhancements**2*1000)+total_gold+material_cost

        self.price += total
        self.sell += total/2


        if material:
            return '{} {} {} +{} ({})'.format(abilities_string, material_type, armor, enhancement, str(total))
        else:
            return '{} {} +{} ({})'.format(abilities_string, armor, enhancement, str(total))


    def get_armor(self):
        """
        Gets the armor type and enchancements.

        type leve:  str(item strength)
        """
        material = ''
        material_cost = 0
        armor_type = ''
        enhancement_bonus = 0

        special_rolls = ('specific armor', 'specific shield', 'special')

        enchant_roll = random.randint(1, 100)
        enchant_key = self._find_key(i.ARMOR_BONUS[self.level], enchant_roll)
        enchant_value = i.ARMOR_BONUS[self.level][enchant_key]

        if enchant_value in special_rolls:
            if enchant_value == 'specific armor':
                specific_armor_roll = random.randint(1, 100)
                specific_armor_key = self._find_key(i.SPECIFIC_ARMOR[self.level], specific_armor_roll)
                specific_armor_value = i.SPECIFIC_ARMOR[self.level][specific_armor_key]
                armor_type = specific_armor_value[0]
                self.price += specific_armor_value[1]
                self.sell += specific_armor_value[1]/2
                return '{} ({})'.format(armor_type, specific_armor_value[1])

            elif enchant_value == 'specific shield':
                specific_shield_roll = random.randint(1, 100)
                specific_shield_key = self._find_key(i.SPECIFIC_SHIELD[self.level], specific_shield_roll)
                specific_shield_value = i.SPECIFIC_SHIELD[self.level][specific_shield_key]
                armor_type = specific_shield_value[0]
                self.price += specific_shield_value[1]
                self.sell += specific_shield_value[1]/2
                return '{} ({})'.format(armor_type, specific_shield_value[1])

            else:
                total_special_rolls = 1
                all_abilities = []
                result = True
                while result:
                    armor_bonus_roll = random.randint(1, 100)
                    armor_bonus_key = self._find_key(i.ARMOR_BONUS[self.level], armor_bonus_roll)
                    armor_bonus_value = i.ARMOR_BONUS[self.level][armor_bonus_key]
                    if armor_bonus_value == 'special':
                        total_special_rolls += 1
                    elif type(armor_bonus_value) is list:
                        armor_type = armor_bonus_value[1]
                        enhancement_bonus = armor_bonus_value[0]
                        result = False

                special_armor_roll = random.randint(1, 100)
                if armor_bonus_value[1] == 'shield':
                    shield_key = self._find_key(i.SHIELD, special_armor_roll)
                    shield_value = i.SHIELD[shield_key]
                    armor_type = '{} {}'.format(shield_value, 'shield')
                    material_info = self._armor_material(shield_value)
                    if material_info:
                        material = material_info[0]
                        material_cost = material_info[1]


                else:
                    armor_key = self._find_key(i.ARMOR, special_armor_roll)
                    armor_value = i.ARMOR[armor_key]
                    armor_type = armor_value[0]
                    material_info = self._armor_material(armor_value)
                    if material_info:
                        material = material_info[0]
                        material_cost = material_info[1]

                dupes = set()
                while total_special_rolls:
                    special_roll = random.randint(1, 100)
                    if armor_bonus_value[1] == 'armor':
                        special_key = self._find_key(i.ARMOR_ABILITIES[self.level], special_roll)
                        special_value = i.ARMOR_ABILITIES[self.level][special_key]
                    else:
                        special_key = self._find_key(i.SHIELD_ABILITIES[self.level], special_roll)
                        special_value = i.SHIELD_ABILITIES[self.level][special_key]

                    if special_value == 'roll':
                        total_special_rolls += 2
                    elif special_value[0] in dupes:
                        total_special_rolls += 1
                    else:
                        upgrade = self._upgrade_ability(all_abilities, special_value)
                        if upgrade:
                            if upgrade[0]:
                                all_abilities[upgrade[1]] = special_value
                            else:
                                total_special_rolls += 1
                        else:
                            all_abilities.append(special_value)
                            dupes.add(special_value[0])
                    total_special_rolls -= 1

                final_abilities = self._value_check(enhancement_bonus, all_abilities)
                final_armor = self._finish_armor(material_info, final_abilities, armor_type, enhancement_bonus)


                return final_armor

        else:
            if enchant_value[1] == 'armor':
                armor_roll = random.randint(1, 100)
                armor_key = self._find_key(i.ARMOR, armor_roll)
                armor_value = i.ARMOR[armor_key]
                armor_type = armor_value[0]
                enhancement_bonus = enchant_value[0]
                material_info = self._armor_material(armor_value)
                if material_info:
                    material = material_info[0]
                    material_cost = material_info[1]
                armor_cost = (enhancement_bonus**2*1000)+material_cost
                self.price += armor_cost
                self.sell += armor_cost/2

                if material:

                    final_armor = '{} {} +{} ({})'.format(material, armor_type, enhancement_bonus, armor_cost)
                    return final_armor
                else:
                    final_armor = '{} +{} ({})'.format(armor_type, enhancement_bonus, armor_cost)
                    return final_armor

            else:
                shield_roll = random.randint(1, 100)
                shield_key = self._find_key(i.SHIELD, shield_roll)
                shield_value = i.SHIELD[shield_key]
                armor_type = '{} {}'.format(shield_value, 'shield')
                enhancement_bonus = enchant_value[0]
                material_info = self._armor_material(shield_value)
                if material_info:
                    material = material_info[0]
                    material_cost = material_info[1]
                armor_cost = (enhancement_bonus**2*1000)+material_cost
                self.price += armor_cost
                self.sell += armor_cost/2

                if material:
                    final_armor = '{} {} +{} ({})'.format(material, armor_type, enhancement_bonus, armor_cost)
                    return final_armor
                else:
                    final_armor = '{} +{} ({})'.format(armor_type, enhancement_bonus, armor_cost)
                    return final_armor

class Weapon(TreasureHelper):
    def __init__(self, level):
        self.level = level
        self.price = 0
        self.sell = 0


    def _is_compatible(self, weapon, ability):
        """
        Checks to see if the ability rolled is valid on the weapon

        type weapon:    str(letters)
        type ability:   str(letters)

        rtype:          bool

        """
        w = set(weapon)
        a = set(ability)

        return w.issubset(a)
        


    def _bane_foe(self, abilities):
        """
        Checks if bane is an abilitity and rolls a foe for it.
        
        type abilities:     list[str(ability name), int(value)]

        rtype abilities:    list[str(ability name), int(value)]
        """
        for ability in abilities:
            if ability[0] == 'bane':
                roll = random.randint(1, 100)
                roll_key = self._find_key(i.BANE_TYPES, roll)
                roll_value = i.BANE_TYPES[roll_key]
                ability[0] = '{} {}'.format(roll_value, 'bane')

        return abilities



    def _check_abilities(self, bonus, abilities):
        """
        This makes sure the item does is not either over +10 enhancement nor over 200k gold.

        type enhancement:   int(base item enhancement)
        type abilities:     list[str(ability name), int(value)]
        *args               weapon, shield, armor

        rtype:              list[str(ability name, int(value)] 
        """
        total_enhancement = bonus
        total_gold = 0

        for ability in abilities:
            if ability[1] <= 10:
                total_enhancement += ability[1]
            else:
                total_gold += ability[1]

        total = (total_enhancement**2*2000)+total_gold
        if total > 200000:
            fixed = self._fix_cost(bonus, abilities)
            bonuses = bonus
            for ability in fixed:
                if ability[1] <= 10:
                    bonuses += ability[1]
            if bonuses > 10:
                fixed = self._fix_bonus(bonus, fixed)
                return fixed
            else:
                return fixed

        return abilities


    def _fix_cost(self, enhancement, abilities):
        """
        Picks the highest value abilities to fit for the weapon. Orders the abilities
        by value and selects the most valuable abilities to add first.

        type base:      int(base enchancement bonus)
        type abilities: list[str(ability name), int(value)]
        args:           cost

        rtype:          list[str(ability name), int(value)]
        """
        ordered_abilities = abilities
        ordered_abilities.sort(key=lambda x: x[1], reverse=True)
        gold_abilities = []
        adjusted_abilities = []
        total_enhancement = enhancement

        for ability in ordered_abilities:
            if ability[1] > 10:
                gold_abilities.append((ability))
            else:
                adjusted_abilities.append(ability)
                total_enhancement += ability[1]

        total = total_enhancement**2*2000

        for ability in gold_abilities:
            if ability[1] + total <= 200000:
                adjusted_abilities.append(ability)
                total += ability[1]

        return adjusted_abilities


    def _fix_bonus(self, enhancement, abilities):
        """
        Picks the highest value abilities to fit for the armor. Orders the abilities
        by value and selects the highest bonuses abilities to add first.

        type base:      int(base enchancement bonus)
        type abilities: list[str(ability name), int(value)]
        args:           cost

        rtype:          list[str(ability name), int(value)]
        """
        ordered_abilities = abilities
        ordered_abilities.sort(key=lambda x: x[1], reverse=True)
        adjusted_abilities = []
        bonus_abilities = []
        total_enhancement = enhancement

        for ability in ordered_abilities:
            if ability[1] <= 10:
                bonus_abilities.append(ability)
            else:
                adjusted_abilities.append(ability)

        for ability in bonus_abilities:
            if ability[1] + total_enhancement <= 10:
                adjusted_abilities.append(ability)
                total_enhancement += ability[1]


        return adjusted_abilities


    def _finish_weapon(self, material, bonus, weapon, abilities):
        """
        Puts the weapon together with abilities, material, and bonus 
        and gives the total price.

        type material:  list[]
        type bonus:     int()
        type weapon:    str()
        type abilities: list[]

        rtype:          str()
        """

        abilities_string = ''
        total_enhancement = bonus
        total_gold = 0
        if material:
            material_cost = material[1]
        else:
            material_cost = 0

        for ability in abilities:
            if abilities_string:
                abilities_string += ', ' + ability[0]
            else:
                abilities_string = ability[0]
            if ability[1] > 10:
                total_gold += ability[1]
            else:
                total_enhancement += ability[1]

        total = (total_enhancement**2*2000)+total_gold+material_cost

        self.price += total
        self.sell += total/2

        if material:
            return '{} {} {} +{} ({})'.format(abilities_string, material[0], weapon, bonus, str(total))
        else:
            return '{} {} +{} ({})'.format(abilities_string, weapon, bonus, str(total))


    def get_weapon(self):
        """
        Gets a random weapon.
        """
        
        weapon_roll = random.randint(1, 100)
        weapon_key = self._find_key(i.WEAPONS, weapon_roll)
        weapon_value = i.WEAPONS[weapon_key]
        weapon = weapon_value[0]
        weapon_properties = weapon_value[1]


        weapon_bonus_roll = random.randint(1, 100)
        weapon_bonus_key = self._find_key(i.WEAPON_BONUS[self.level], weapon_bonus_roll)
        weapon_bonus_value = i.WEAPON_BONUS[self.level][weapon_bonus_key]

        if weapon_bonus_value == 'specific':

            specific_weapon_roll = random.randint(1, 100)
            specific_weapon_key = self._find_key(i.SPECIFIC_WEAPONS[self.level], specific_weapon_roll)
            specific_weapon_value = i.SPECIFIC_WEAPONS[self.level][specific_weapon_key]
            self.price += specific_weapon_value[1]
            self.sell += specific_weapon_value[1]/2

            return '{} ({})'.format(specific_weapon_value[0], specific_weapon_value[1])

        elif weapon_bonus_value != 'special':

            weapon_bonus = weapon_bonus_value
            weapon_material_roll = random.randint(1, 100)
            weapon_material_key = self._find_key(i.WEAPON_MATERIALS, weapon_material_roll)
            weapon_material_value = i.WEAPON_MATERIALS[weapon_material_key]
            if weapon_material_value:
                weapon_cost = weapon_bonus**2*2000+weapon_material_value[1]
            else:
                weapon_cost = weapon_bonus**2*2000
            self.price += weapon_cost
            self.sell += weapon_cost/2

            if weapon_material_value:
                return '{} {} +{} ({})'.format(weapon_material_value[0], weapon, weapon_bonus, weapon_cost)
            else:
                return '{} +{} ({})'.format(weapon, weapon_bonus, weapon_cost)

        else:

            special_rolls = 1
            result = True
            while result:
                weapon_bonus_roll = random.randint(1, 100)
                weapon_bonus_key = self._find_key(i.WEAPON_BONUS[self.level], weapon_bonus_roll)
                weapon_bonus_value = i.WEAPON_BONUS[self.level][weapon_bonus_key]

                if weapon_bonus_value == 'special':
                    special_rolls += 1
                elif weapon_bonus_value is not 'specific':
                    weapon_bonus = weapon_bonus_value
                    weapon_material_roll = random.randint(1, 100)
                    weapon_material_key = self._find_key(i.WEAPON_MATERIALS, weapon_material_roll)
                    weapon_material_value = i.WEAPON_MATERIALS[weapon_material_key]
                    result = False

            all_abilities = []
            dupes = set()
            while special_rolls:
                weapon_ability_roll = random.randint(1, 100)
                weapon_ability_key = self._find_key(i.WEAPON_ABILITIES[self.level], weapon_ability_roll)
                weapon_ability_value = i.WEAPON_ABILITIES[self.level][weapon_ability_key]


                if weapon_ability_value == 'roll':
                    special_rolls += 2
                else:
                    if self._is_compatible(weapon_properties, weapon_ability_value[2]):
                        if weapon_ability_value[0] in dupes:
                            special_rolls += 1
                        else:
                            dupes.add(weapon_ability_value[0])
                            all_abilities.append(weapon_ability_value)
                    else:
                        special_rolls += 1

                special_rolls -= 1

            final_abilities = self._check_abilities(weapon_bonus, all_abilities)
            final_abilities = self._bane_foe(final_abilities)
            final_weapon = self._finish_weapon(weapon_material_value, weapon_bonus, weapon, final_abilities)

            return final_weapon


class Potion(TreasureHelper):
    def __init__(self, level):
        self.level = level
        self.price = 0
        self.sell = 0

    def get_potion(self):
        potion_type = [
            'potion of',
            'oil of'
        ]
        potion_roll = random.randint(1, 100)
        potion_key = self._find_key(i.POTIONS[self.level], potion_roll)
        potion_value = i.POTIONS[self.level][potion_key]

        self.price += potion_value[1]
        self.sell  += potion_value[1]

        potion_list = potion_value[0].split()
        potion_name = ' '.join(potion_list[:-1])
        if potion_list[-1] == '(potion)':
            potion = 'potion of {} ({})'.format(potion_name, potion_value[1])
        elif potion_list[-1] == '(oil)':
            potion = 'oil of {} ({})'.format(potion_name, potion_value[1])
        else:
            potion = '{} {} ({})'.format(random.choice(potion_type), potion_name, potion_value[1])

        return potion

class Ring(TreasureHelper):
    def __init__(self, level):
        self.level = level
        self.price = 0
        self.sell = 0

    def get_ring(self):
        ring_roll = random.randint(1, 100)
        ring_key = self._find_key(i.RINGS[self.level], ring_roll)
        ring_value = i.RINGS[self.level][ring_key]

        self.price += ring_value[1]
        self.sell += ring_value[1]/2

        ring = 'ring of {} ({})'.format(ring_value[0], ring_value[1])
        return ring

class Rod(TreasureHelper):
    def __init__(self, level):
        self.level = level
        self.price = 0
        self.sell = 0

    def get_rod(self):
        rod_roll = random.randint(1, 100)
        rod_key = self._find_key(i.RODS[self.level], rod_roll)
        rod_value = i.RODS[self.level][rod_key]

        self.price += rod_value[1]
        self.sell += rod_value[1]/2

        rod = 'rod of {} ({})'.format(rod_value[0], rod_value[1])
        return rod

class Scroll(TreasureHelper):
    def __init__(self, level):
        self.level = level
        self.price = 0
        self.sell = 0


    def get_scroll(self):
        scroll_type_roll = random.randint(1, 100)
        scroll = ''
        if scroll_type_roll < 70:
            spells_roll = random.randint(1, 100)
            spells_value = i.NUMBER_OF_SPELLS[self.level]

            level_roll = random.randint(1, 100)
            level_key = self._find_key(i.LEVEL_OF_SPELL[self.level], level_roll)
            level_value = i.LEVEL_OF_SPELL[self.level][level_key]

            num = self._roll_dice_total(spells_value[0], spells_value[1])

            for _ in range(num):
                scroll_roll = random.randint(1, 100)
                scroll_key = self._find_key(i.ARCANE_SPELLS[level_value], scroll_roll)
                scroll_value = i.ARCANE_SPELLS[level_value][scroll_key]

                self.price += scroll_value[1]
                self.sell += scroll_value[1]/2

                spell = '{} ({})'.format(scroll_value[0], scroll_value[1])
                if scroll:
                    scroll += ', {}'.format(spell)
                else:
                    scroll = 'scroll of {}'.format(spell)

            return scroll 


        else:
            spells_roll = random.randint(1, 100)
            spells_value = i.NUMBER_OF_SPELLS[self.level]

            level_roll = random.randint(1, 100)
            level_key = self._find_key(i.LEVEL_OF_SPELL[self.level], level_roll)
            level_value = i.LEVEL_OF_SPELL[self.level][level_key]

            num = self._roll_dice_total(spells_value[0], spells_value[1])

            for _ in range(num):
                scroll_roll = random.randint(1, 100)
                scroll_key = self._find_key(i.DIVINE_SPELLS[level_value], scroll_roll)
                scroll_value = i.DIVINE_SPELLS[level_value][scroll_key]

                self.price += scroll_value[1]
                self.sell += scroll_value[1]/2

                spell = '{} ({})'.format(scroll_value[0], scroll_value[1])
                if scroll:
                    scroll += ', {}'.format(spell)
                else:
                    scroll = 'scroll of {}'.format(spell)
                    
            return scroll 


class Staff(TreasureHelper):
    def __init__(self, level):
        self.level = level
        self.price = 0
        self.sell = 0


    def get_staff(self):
        staff_roll = random.randint(1, 100)
        staff_key = self._find_key(i.STAFFS[self.level], staff_roll)
        staff_value = i.STAFFS[self.level][staff_key]

        self.price += staff_value[1]
        self.sell += staff_value[1]/2

        staff = '{} ({})'.format(staff_value[0], staff_value[1])
        return staff



class Wand(TreasureHelper):
    def __init__(self, level):
        self.level = level
        self.price = 0
        self.sell = 0


    def get_wand(self):
        wand_roll = random.randint(1, 100)
        wand_key = self._find_key(i.WANDS[self.level], wand_roll)
        wand_value = i.WANDS[self.level][wand_key]

        self.price += wand_value[1]
        self.sell += wand_value[1]/2

        wand = 'wand of {} ({})'.format(wand_value[0], wand_value[1])
        return wand

class Wondrous(TreasureHelper):
    def __init__(self, level):
        self.level = level
        self.price = 0
        self.sell = 0

    def get_wondrous(self):
        wondrous_value = random.choice(i.WONDROUS[self.level])

        self.price += wondrous_value[1]
        self.sell += wondrous_value[1]/2

        wondrous = '{} ({})'.format(wondrous_value[0], wondrous_value[1])
        return wondrous
