# import numpy as np
import pandas as pd
import ipdb
import re


class cardDB:
    """
    The card database class.
    """
    def __init__(self, path='../data/', filename='cards.csv'):
        self.path = path
        self.filename = filename
        date_cols = [9]
        # load in the cards csv
        self.all_cards = pd.read_csv(path+filename,
                                     parse_dates=date_cols,
                                     date_format='%Y-%m-%d')
        self.cards = self.all_cards[self.all_cards['type'] == 'Character']
        self.cards = self.cards[self.cards['release_date'] <
                                pd.Timestamp.today()]
        return

    def add_card(self, attr_dict, sort=False):
        self.all_cards.append(attr_dict, ignore_index=True)
        return

    def add_card_prompt(self):
        attr_dict = {}
        attr_dict['cname'] = input('cardname:\n')
        attr_dict['type'] = input('type (0:Character, 1:Summon, else:str):')
        if attr_dict['type'] == '0':
            attr_dict['type'] = 'Character'
        elif attr_dict['type'] == '1':
            attr_dict['type'] = 'Summon'
        attr_dict['ability'] = input('abililty:\n')
        attr_dict['cost'] = int(input('cost:\n'))
        attr_dict['power'] = int(input('power:\n'))
        regex = re.compile('[^a-zA-Z]')
        attr_dict['carddefid'] = regex.sub('', attr_dict['cname'])
        source_input = input('source code/series:')
        attr_dict['source'] = self.source_map(source_input)
        attr_dict['release_series'] = float(input('release_series:\n'))
        attr_dict['current_series'] = float(input('current_series:\n'))
        # attr_dict['release_date'] = pd.Timestamp.strftime(
        # input('release_date (YYYY-MM-DD)'),'%Y-%m-%d')
        # add more if needed
        self.add_card(attr_dict)
        return

    def source_map(self, source_input):
        if source_input == '1':
            return 'Collection Level 1-214 (Pool 1)'
        elif source_input == '2':
            return 'Collection Level 222-474 (Pool 2)'
        elif source_input == '3':
            return 'Collection Level 486+ (Pool 3)'
        elif source_input == '4':
            return 'Series 4 Rare - Collection Level 486+ (Pool 4)'
        elif source_input == '5':
            return 'Series 5 Ultra Rare - Collection Level 486+ (Pool 5)'
        else:
            return ''

    def manual_update_all(self):
        """
        A wrapper to check every card and update it if necessary.
        """
        # convert each row to a dict and iterate over them
        for card in self.all_cards.to_dict(orient='records'):
            print(card)
            attr_dict = card
            ipdb.set_trace()
            self.update_card(attr_dict)

    def update_card(self, attr_dict):
        # see if we have enough information to find the card.
        # This will be expanded to a more comprehensive search.
        # Currently requires exact card name.
        if 'cname' not in attr_dict.keys():
            print("Please provide a the EXACT cname "
                  "for the card to be updated.")
            return

        if attr_dict['cname'] not in self.all_cards['cname'].values:
            print("No matching card name.")
            return

        # save current state for card
        original_card = self.all_cards[self.all_cards['cname']
                                       == attr_dict['cname']]

        # now loop over attr_dict keys to update values in self.all_cards
        for key, value in attr_dict.items():
            self.all_cards.loc[self.all_cards['cname'] == attr_dict['cname'],
                               key] = value

        # get updated values
        print('Original Card values: ')
        print(original_card[attr_dict.keys()])
        print('Updated Card values: ')
        print(self.all_cards[self.all_cards['cname'] ==
                             attr_dict['cname']][attr_dict.keys()])
        return None

    def save_db(self, overwrite=True, path='../data/', filename='cards.csv'):
        if overwrite:
            self.all_cards.to_csv(self.path + self.filename, index=False)
        else:
            self.all_cards.to_csv(path + filename, index=False)


if __name__ == '__main__':
    cards = cardDB()
    # update_dict = {'cname': 'Silver Surfer', 'power': 2}
    ipdb.set_trace()
    cards.manual_update_all()
    # cards.update_card(update_dict)
