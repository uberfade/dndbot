import random
import treasure

class Rolls:

    def dice(self, rolls):
        """
        """
        all_rolls = []
        for roll in rolls:
            each = []
            for _ in range(int(roll[0])):
                value = random.randint(1, int(roll[1]))
                each.append(value)
            if roll[2]:
                if roll[2] == '+':
                    dice_roll = '{}d{} + {}'.format(roll[0], roll[1], roll[3])
                    total = sum(each) + int(roll[3])
                    all_rolls.append((dice_roll, each, total))
                elif roll[2] == '-':
                    dice_roll = '{}d{} - {}'.format(roll[0], roll[1], roll[3])
                    total = sum(each) - int(roll[3])
                    all_rolls.append((dice_roll, each, total))
                else:
                    dice_roll = '{}d{} * {}'.format(roll[0], roll[1], roll[3])
                    total = sum(each) * int(roll[3])
                    all_rolls.append((dice_roll, each, total))
            else:
                dice_roll = '{}d{}'.format(roll[0], roll[1])
                total = sum(each)
                all_rolls.append((dice_roll, each, total))
        return all_rolls


    def hp(self, rolls):
        """
        """
        all_rolls = []
        for roll in rolls:
            each = []
            for _ in range(int(roll[0])):
                value = random.randint(2, int(roll[1]))
                each.append(value)
            hp = '{}d{}'.format(roll[0], roll[1])
            total = sum(each)
            all_rolls.append((hp, each, total))
        return all_rolls

    def _drop_lowest(self, values):
        """
        """
        values.sort(reverse=True)
        return values[:-1]      

    def stats(self, rolls):
        """
        """
        stats1 = []
        stats2 = []
        for _ in range(6):
            roll1 = []
            roll2 = []
            for _ in range(4):
                roll1.append(random.randint(2, 6))
                roll2.append(random.randint(2, 6))
            stats1.append(sum(self._drop_lowest(roll1)))
            stats2.append(sum(self._drop_lowest(roll2)))

        return list(zip(stats1, stats2))


    def treasure(self, hoard):
        all_treasures = []
        if type(hoard[0]) == str:
            t = treasure.Treasure()
            all_treasures.append(t.get_treasure(int(hoard[0])))
        else:
            for thing in hoard:
                t = treasure.Treasure()
                all_treasures.append(t.get_treasure(int(thing[0]), *thing[1:]))
        return all_treasures

    def items(self, items):
        all_items = []
        for item in items:
            t = treasure.Treasure()
            if not item[2]:
                if item[0] == 'armor':
                    all_items += (t.get_armor(item[1]))
                elif item[0] == 'weapon':
                    all_items += (t.get_weapon(item[1]))
                elif item[0] == 'potion':
                    all_items += (t.get_potion(item[1]))
                elif item[0] == 'ring':
                    all_items += (t.get_ring(item[1]))
                elif item[0] == 'rod':
                    all_items += (t.get_rod(item[1]))
                elif item[0] == 'scroll':
                    all_items += (t.get_scroll(item[1]))
                elif item[0] == 'staff':
                    all_items += (t.get_staff(item[1]))
                elif item[0] == 'wand':
                    all_items += (t.get_wand(item[1]))
                else:
                    all_items += (t.get_wondrous(item[1]))
            else:
                if item[0] == 'armor':
                    all_items += (t.get_armor(item[1], int(item[2])))
                elif item[0] == 'weapon':
                    all_items += (t.get_weapon(item[1], int(item[2])))
                elif item[0] == 'potion':
                    all_items += (t.get_potion(item[1], int(item[2])))
                elif item[0] == 'ring':
                    all_items += (t.get_ring(item[1], int(item[2])))
                elif item[0] == 'rod':
                    all_items += (t.get_rod(item[1], int(item[2])))
                elif item[0] == 'scroll':
                    all_items += (t.get_scroll(item[1], int(item[2])))
                elif item[0] == 'staff':
                    all_items += (t.get_staff(item[1], int(item[2])))
                elif item[0] == 'wand':
                    all_items += (t.get_wand(item[1], int(item[2])))
                else:
                    all_items += (t.get_wondrous(item[1], int(item[2])))
        return all_items

