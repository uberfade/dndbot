import gspread
import keys
from oauth2client.service_account import ServiceAccountCredentials

class Inv:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'] 
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('dndbot-7aa0f8cc155a.json', self.scope)


    def _empty_inv_row(self, worksheet):
        row = worksheet.col_values(1)
        for num, entry in enumerate(row):
            if entry == '':
                return num+1
        return len(row)+1

    def _empty_goods_row(self, worksheet):
        row = worksheet.col_values(4)
        for num, entry in enumerate(row):
            if entry == '':
                return num+1
        return len(row)+1

    def sub_inv(self, person, items):
        gs = gspread.authorize(self.credentials)
        key = keys.PLAYER_KEYS[person]

        all_items = items.split(', ')
        wb = gs.open_by_key(key).sheet1


        for item in all_items:
            if item[0] != '$':

                first = wb.find(item)
                row = int(first.row)
                col = int(first.col)
                
                for n in range(1, 4):
                    wb.update_cell(row, n, '')
            else:

                item = item[1:]
                first = wb.find(item)
                row = int(first.row)
                col = int(first.col)

                wb.update_cell(row, col, '')
                wb.update_cell(row, col+1, '')


    def add_inv(self, person, item, weight, value):
        gs = gspread.authorize(self.credentials)
        key = keys.PLAYER_KEYS[person]
        wb = gs.open_by_key(key).sheet1


        if weight < 0:
            row = self._empty_goods_row(wb)
            wb.update_cell(row, 4, item)
            wb.update_cell(row, 5, value)
        else:
            row = self._empty_inv_row(wb)
            for col in range(1, 4):
                if col == 1:
                    wb.update_cell(row, col, item)
                elif col == 2:
                    wb.update_cell(row, col, weight)
                else:
                    wb.update_cell(row, col, value)

    def adjust_coins(self, person, plat, gold, silver, copper):
        gs = gspread.authorize(self.credentials)
        key = keys.PLAYER_KEYS[person]
        wb = gs.open_by_key(key).sheet1

        cells = [
            ('G1', copper),
            ('G2', silver),
            ('G3', gold),
            ('G4', plat)
        ]

        for tup in cells:
            current = wb.acell(tup[0]).value
            new = int(current)+tup[1]
            wb.update_acell(tup[0], new)

    def get_inv(self, person):
        gs = gspread.authorize(self.credentials)
        key = keys.PLAYER_KEYS[person]
        wb = gs.open_by_key(key).sheet1

        inv = []
        coins = []
        for i in range(1, 7):
            coin = wb.cell(i, 6).value
            amount = wb.cell(i, 7).value
            coins.append((coin, amount))

        inv.append(coins)
        inv.append(wb.cell(6, 7).value)

        items = []
        all_items = wb.col_values(1)
        valuables = wb.col_values(4)

        for item in all_items:
            if item:
                if item != 'Inventory':
                    items.append(item)

        for valuable in valuables:
            if valuable:
                if valuable != 'Gems/Goods':
                    items.append(valuable)

        inv.append(items)
        inv.append(wb.cell(8, 7).value)

        return inv
