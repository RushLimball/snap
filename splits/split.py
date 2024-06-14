# from snap.classes import card_db
import numpy as np
import ipdb


def split_card(split_number=1):
    # generate a random split based on the number of splits so far
    if split_number == 1:
        background = np.random.choice(['Foil', 'Prism'], p=[0.5, 0.5])
        effect = 'None'
    elif split_number < 4:
        background = np.random.choice(['Foil', 'Prism'], p=[0.5, 0.5])
        effect = np.random.choice(['Glimmer', 'Tone'], p=[0.5, 0.5])
    elif split_number == 4:
        background = np.random.choice(['Foil', 'Prism', 'Ink'],
                                      p=[0.45, 0.45, 0.1])
        effect = np.random.choice(['Glimmer', 'Tone', 'Stardust'],
                                  p=[1/3, 1/3, 1/3])
    elif split_number == 5:
        background = np.random.choice(['Foil', 'Prism', 'Ink', 'Gold'],
                                      p=[0.40, 0.40, 0.1, 0.1])
        effect = np.random.choice(['Glimmer', 'Tone', 'Stardust'],
                                  p=[1/3, 1/3, 1/3])
    else:
        background = np.random.choice(['Foil', 'Prism', 'Ink', 'Gold'],
                                      p=[0.40, 0.40, 0.1, 0.1])
        effect = np.random.choice(['Glimmer', 'Tone', 'Stardust', 'Krackle'],
                                  p=[0.3, 0.3, 0.3, 0.1])

    # ensure there is an effect ot give the color
    if effect != 'None':
        # made up probabilities, sort of doesn't matter
        # as we account for disallowing duplicates
        prob_array = np.array([1, 2, 2, 5, 5, 5, 5, 5])
        color = np.random.choice(['Black', 'Gold', 'Rainbow', 'Red',
                                  'Purple', 'Blue', 'Green',
                                  'White'], p=prob_array/np.sum(prob_array))
    else:
        color = 'None'

    return background, effect, color


if __name__ == '__main__':
    # get cards
    split_dict = {}
    # need to make this better
    cards = card_db.cardDB(path='./snap/data/')

    for ind, card in cards.cards.iterrows():
        # ipdb.set_trace()
        # print(card['cname'])
        # intialize dict entry for card
        split_number = 0
        split_dict[card['cname']] = {}
        split_dict[card['cname']]['split_count'] = 0
        split_dict[card['cname']]['split_list'] = []
        split_dict[card['cname']]['gold_split_num'] = 0
        split_dict[card['cname']]['ink_split_num'] = 0

        # card is unsplit, so has no background and doesn't have ink or gold
        last_background = 'None'
        has_ink = False
        has_gold = False

        # begin splitting
        while not (has_ink):  # and has_gold):
            # increase number of splits
            split_number += 1
            # split the card
            last_background, effect, color = split_card(
                split_number=split_number)
            # check to see if the split exists for the card already
            # as duplicate splits are not allowed
            if ([last_background, effect, color] in
                    split_dict[card['cname']]['split_list']):
                # if the card has the split, we re-roll

                # remove this split from the split count
                split_number -= 1
                # continue to next split
                continue

            # add split to the list of splits
            split_dict[card['cname']]['split_list'].append([last_background,
                                                            effect,
                                                            color])
            # if the most recent split is ink, flag it and
            # mark the split number
            if last_background == 'Ink' and not has_ink:
                has_ink = True
                split_dict[card['cname']]['ink_split_num'] = split_number
            # if the most recent split is gold, flag it and
            # mark the split number
            if last_background == 'Gold' and not has_gold:
                has_gold = True
                split_dict[card['cname']]['gold_split_num'] = split_number
        # record the number of splits the card has had
        split_dict[card['cname']]['split_count'] = split_number

    ipdb.set_trace()

    gold_split_nums = []
    ink_split_nums = []
    total_splits = 0
    for ind, card in cards.cards.iterrows():
        ink_split_nums.append(split_dict[card['cname']]['ink_split_num'])
        gold_split_nums.append(split_dict[card['cname']]['gold_split_num'])
        total_splits += split_dict[card['cname']]['split_count']

    min_bin = 4
    max_bin = np.max([np.max(ink_split_nums), np.max(gold_split_nums)])
    bins = np.linspace(min_bin-0.5, max_bin+0.5, (2+max_bin-min_bin))

    ipdb.set_trace()
