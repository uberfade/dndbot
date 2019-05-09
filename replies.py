class RedditReply:

    def stats(self, stats):
        reply = 'Choose a column  \n  \n1 | 2\n--|--\n'
        for stat in stats:
            reply += '{} | {}\n'.format(stat[0], stat[1])
        return reply

    def treasure(self, treasure):
        reply = '#Treasure  \n  \n'
        for hoard in treasure:
            reply += '**Total**: {}  \n'.format(hoard[0])
            reply += '**Sell**: {}  \n  \n'.format(hoard[1])
            reply += '**Coins**: {}  \n  \n'.format(hoard[2])
            if hoard[3]:
                if len(hoard[3]) == 1:
                    reply += '**Goods**: {}  \n'.format(hoard[3][0])
                else:
                    reply += '**Goods**:  \n  \n'
                    for good in hoard[3]:
                        reply += '* {}  \n'.format(good)
            else:
                reply += '**Goods**: None  \n'.format(hoard[3])

            reply += '  \n'

            if hoard[4]:
                if len(hoard[4]) == 1:
                    reply += '**Items**: {}  \n'.format(hoard[4][0])
                else:
                    reply += '**Items**:  \n  \n'
                    for item in hoard[4]:
                        reply += '* {}  \n'.format(item)
            else:
                reply += '**Items**: None  \n'

            reply += '  \n'

        reply += '^^1. ^^The ^^number ^^enclosed ^^in ^^parenthesis ^^next ^^to ^^an ^^item ^^is ^^its ^^full ^^value.  \n'
        reply += '^^2. ^^All ^^items ^^and ^^goods ^^valued ^^are ^^in ^^gold.  \n'
        reply += '^^3. ^^Sell ^^value ^^is ^^the ^^full ^^value ^^of ^^coins, ^^goods, ^^and ^^potions ^^and ^^half ^^for ^^everything ^^else.  \n  \n'

        return reply

    def dice(self, rolls):
        reply = 'You made {} roll(s).  \n'.format(len(rolls))
        for roll in rolls:
            reply += '  \nRoll: {}  \nRolls: {}  \nTotal: {}  \n  \n'.format(*roll)
        return reply

    def items(self, items):
        if len(items) < 2:
            reply = 'Item: {}'.format(items[0])
        else:
            reply = 'Items:  \n  \n'
            for item in items:
                reply += '* {}\n'.format(item)
        return reply

    def coins(self, coins):
        reply = 'Coins: {}'.format(coins)
        return reply

    def goods(self, goods):
        if len(goods) < 2:
            reply = 'Goods: {}'.format(goods[0])
        else:
            reply = 'Goods:  \n  \n'
            for good in goods:
                reply += '* {}\n'.format(good)
        return reply

    def inv(self, inv):
        reply = '#Your Inventory  \n  \n'
        reply += '**Coins**:  \n  \n'
        reply += 'Coin|Amount  \n--|--\n'
        for val in inv[0]:
            reply += '{}|{}\n'.format(val[0], val[1])
        reply += '  \n'
        reply += 'Total: {}  \n  \n'.format(inv[1])
        reply += '**Inventory**:    \n'
        if inv[2]:
            for item in inv[2]:
                reply += '* {}  \n'.format(item)
        else:
            reply += '* None  \n'
        reply += '  \n'
        reply += 'Weight: {}'.format(inv[3])
        return reply
