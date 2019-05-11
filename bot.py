import gspread
import inventory
import logging
import keys
import praw
import random
import re
import replies
import rolls
import sqlite3
import treasure

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s","%Y-%m-%d %H:%M:%S")
fh = logging.FileHandler('redditbot.log')
fh.setFormatter(fmt)
logger.addHandler(fh)


class RedditBot:
    def __init__(self):
        self.reddit = praw.Reddit('bot1', user_agent='dice roll bot by /u/uberfade')

    def _roll_dice(self, re_dice):
        r = rolls.Rolls()
        reply = replies.RedditReply()
        rolled = r.dice(re_dice)
        logger.info('made {} dice roll(s)'.format(len(re_dice)))
        return reply.dice(rolled)

    def _roll_hps(self, re_hps):
        r = rolls.Rolls()
        reply = replies.RedditReply()
        rolled = r.hp(re_hps)
        logger.info('rolled for hps')
        return reply.dice(rolled)

    def _roll_treasure(self, re_treasure):
        r = rolls.Rolls()
        reply = replies.RedditReply()
        rolled = r.treasure(re_treasure)
        logger.info('rolled up {} treasure(s)'.format(len(re_treasure)))
        return reply.treasure(rolled)

    def _roll_items(self, re_items):
        r = rolls.Rolls()
        reply = replies.RedditReply()
        rolled = r.items(re_items)
        logger.info('rolled for items')
        return reply.items(rolled)

    def _roll_stats(self, re_stats):
        r = rolls.Rolls()
        reply = replies.RedditReply()
        rolled = r.stats(re_stats)
        logger.info('rolled stats')
        return reply.stats(rolled)

    def _inventory(self, player):
        i = inventory.Inv()
        reply = replies.RedditReply()
        get_inv = i.get_inv(player)
        logger.info('retrieved inventory for {}'.format(player))
        return reply.inv(get_inv)


    def search_comments(self):
        conn = sqlite3.connect('dicebot.db')
        c = conn.cursor()
        try:
            c.execute('CREATE TABLE comments (id text primary key)')
            conn.commit()
        except sqlite3.OperationalError:
            pass
        subs = self.reddit.subreddit('uberfadednd')
        # subs = self.reddit.subreddit('AntarsaCampaign+AntarsaK+AntarsaM+AntarsaS+uberfadednd')
        comments = subs.comments(limit=30)

        for comment in comments:
            text = comment.body
            redditor = comment.author
            author = redditor.name
            re_dice = re.findall(r'!roll\s(\d{1,3})d(\d{1,3})\s?(\+|-|\*)?\s?(\d+)?', text)
            re_hps = re.findall(r'!hp\s(\d+)d(\d+)', text)
            re_treasure = re.findall(r'!treasure\((\d{1,2})\)', text)
            re_mod_treasure = re.findall(r'!treasure\((\d{1,2})\s([\scgi\+\-]{2,9})\)', text)
            re_items = re.findall(r'!items\(([a-z]{3,8})\s(minor|medium|major)(\s\d{1,3})?\)', text)
            re_stats = re.findall(r'!stats', text)
            re_add = re.findall(r'\+inv\s(art|kannab|zlatan|uberfade)\s(.*),\s(-?\d{1,4})\s(\d{1,9})\s\+inv', text)
            re_sub = re.findall(r'\-inv\s(art|kannab|zlatan|uberfade)\s(.+)\s\-inv', text)
            re_coins = re.findall(r'!coins\s(art|kannab|zlatan|uberfade)\s(-?\d+)\s(-?\d+)\s(-?\d+)\s(-?\d+)', text)
            re_inv = re.findall(r'(!inv)', text)


            all_replies = ''
            adjust_inv = False
            c.execute('SELECT id FROM comments WHERE id=:id', {'id': comment.id})
            if not c.fetchone():

                if re_dice:
                    reply = self._roll_dice(re_dice)
                    if all_replies:
                        all_replies += '  \n  \n{}'.format(reply)
                    else:
                        all_replies = reply

                if re_hps:
                    reply = self._roll_hps(re_hps)
                    if all_replies:
                        all_replies += '  \n  \n{}'.format(reply)
                    else:
                        all_replies = reply

                if re_treasure:
                    reply = self._roll_treasure(re_treasure)
                    if all_replies:
                        all_replies += '  \n  \n{}'.format(reply)
                    else:
                        all_replies = reply

                if re_mod_treasure:
                    reply = self._roll_treasure(re_mod_treasure)
                    if all_replies:
                        all_replies += '  \n  \n{}'.format(reply)
                    else:
                        all_replies = reply

                if re_items:
                    reply = self._roll_items(re_items)
                    if all_replies:
                        all_replies += '  \n  \n{}'.format(reply)
                    else:
                        all_replies = reply


                if re_stats:
                    reply = self._roll_stats(re_stats)
                    if all_replies:
                        all_replies += '  \n  \n{}'.format(reply)
                    else:
                        all_replies = reply

                if re_add and author == 'uberfade':
                    i = inventory.Inv()
                    for inv in re_add:
                        i.add_inv(inv[0], inv[1], int(inv[2]), int(inv[3]))
                    logger.info('added to inventory')
                    adjust_inv = True

                if re_sub and author == 'uberfade':
                    i = inventory.Inv()
                    for inv in re_sub:
                        reply = i.sub_inv(inv[0], inv[1])
                    if reply:
                        if all_replies:
                            all_replies += '  \n  \n{}'.format(reply)
                        else:
                            all_replies = reply
                    if reply:
                        logger.info('failed to remove item')
                    else:
                        logger.info('removed from inventory')
                    adjust_inv = True

                if re_coins and author == 'uberfade':
                    i = inventory.Inv()
                    for inv in re_coins:
                        i.adjust_coins(inv[0], int(inv[1]), int(inv[2]), int(inv[3]), int(inv[4]))
                    logger.info('adjusted wealth')
                    adjust_inv = True

                if re_inv:
                    char = keys.REDDIT_KEYS[author]

                    reply = self._inventory(char)
                    if all_replies:
                        all_replies += '  \n  \n{}'.format(reply)
                    else:
                        all_replies = reply
                    adjust_inv = True


            if all_replies or adjust_inv:
                c.execute('INSERT INTO comments VALUES (:id)', {'id': comment.id})
                conn.commit()
                if all_replies:
                    comment.reply(all_replies)

        conn.close()

def main():
    bot = RedditBot()
    bot.search_comments()

if __name__ == '__main__':
    main()