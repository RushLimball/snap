import time
import numpy as np
import json
import ipdb


class Collection:
    def __init__(self, path='../data/', filename='CollectionState.jjerot.json'):

        # Load JSON data from CollectionState.JSON
        try:
            with open(path+filename, 'r', encoding='utf-8-sig') as f:
                self.collection_state = json.load(f)
        except FileNotFoundError:
            print("Error: FileNotFoundError - CollectionState.JSON"
                  " file not found.")
            exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: JSONDecodeError - {e}")
            exit(1)
        self.collection = {}
        self.collection['AllCards'] = []
        self.collection['FavoriteCards'] = []
        self.collection['SplitCards'] = []
        cards_info = []

        # make an attribute for all splits (excluding custom cards)
        # this will be a list of dicts
        for card in self.collection_state['ServerState']['Cards']:
            
            if "Custom" in card and card["Custom"] is True:
                continue  # Skip entries where Custom is true

            card_def_id = card.get('CardDefId', '')
            surface_effect_def_id = card.get('SurfaceEffectDefId', '')
            reveal_effect_def_id = card.get('CardRevealEffectDefId', '')
            time_created = card.get('TimeCreated', '')

            if card_def_id and surface_effect_def_id:
                if reveal_effect_def_id:
                    # Check if the reveal effect is one of the known colors
                    if any(color in reveal_effect_def_id for color in ["Black", "Gold", "Green", "Blue", "Red", "White", "Purple"]):
                        #cards_info.append(f"{card_def_id} {surface_effect_def_id} {reveal_effect_def_id} {}")
                        cards_info.append(f"{card_def_id} {surface_effect_def_id} {reveal_effect_def_id} {time_created}")
                    else:
                        # Append "Rainbow" to specific card types
                        if reveal_effect_def_id in ["Comic", "Glimmer", "Kirby", "Sparkle"]:
                            #cards_info.append(f"{card_def_id} {surface_effect_def_id} {reveal_effect_def_id}Rainbow")
                            cards_info.append(f"{card_def_id} {surface_effect_def_id} {reveal_effect_def_id}Rainbow {time_created}")
                        else:
                            #cards_info.append(f"{card_def_id} {surface_effect_def_id} Rainbow")
                            cards_info.append(f"{card_def_id} {surface_effect_def_id} Rainbow {time_created}")
                else:
                    #cards_info.append(f"{card_def_id} {surface_effect_def_id}")
                    cards_info.append(f"{card_def_id} {surface_effect_def_id} None {time_created}")
        ipdb.set_trace()
        self.split_info = cards_info

        with open('../data/newSplitData.txt', 'w', encoding='utf-8') as outfile:
            for card_info in cards_info:
                outfile.write(f"{card_info}\n")

if __name__ == '__main__':
    #ipdb.set_trace()
    x = Collection()

