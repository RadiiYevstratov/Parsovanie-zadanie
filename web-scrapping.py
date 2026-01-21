import requests, json
from bs4 import BeautifulSoup
from datetime import datetime




class CurrentBrochures:
    def __init__(self):
        self.url = 'https://www.prospektmaschine.de/hypermarkte/'
        self.res = requests.get(url = self.url)
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
        self.cards = self.soup.select('div.brochure-thumb')   
        self.cards_info = []
        

    def card_info(self):
        for card in self.cards:
            self.parse_card(card)

        
        self.save_json(self.cards_info)


    def parse_card(self, card):
        card_dict = {}
        valid_from, valid_to = self.get_expiration_date(card)
        card_dict["title"] = self.title_finder(card)
        card_dict["thumbnail"] = self.thumbnail_finder(card)
        card_dict["shop_name"] = self.shop_name_finder(card)
        card_dict["valid_from"] = valid_from
        card_dict["valid_to"] = valid_to
        card_dict["parsed_time"] = self.get_parsed_time()
        self.cards_info.append(card_dict) 





    def title_finder(self, card):
        try:
            card_title = card.select_one('.grid-item-content strong')
            return card_title.get_text(strip=True) if card_title else None

        except Exception:
                return None




    def thumbnail_finder(self, card):

        try:
            img = card.select_one(".img-container img")
            if img:
                src = (
                    img.get("src")
                    or img.get("data-src")
                    or img.get("data-original")
                    or img.get("data-lazy-src")
                )

                return src
            else: 
                return None
        except Exception:
            return None


    def shop_name_finder(self, card):

        try:
            card_shop_name = card.select_one('.lazyloadLogo')
            return card_shop_name["alt"][4::].strip() if card_shop_name else None
        except Exception:
            return None

    def  get_expiration_date(self, card):

        try:
            date = card.select_one('.hidden-sm')

            if not date:
                return None, None

            date = date.get_text(strip=True).split(' - ')
            valid_from = datetime.strptime(date[0], "%d.%m.%Y").strftime("%Y-%m-%d")
            valid_to = datetime.strptime(date[1], "%d.%m.%Y").strftime("%Y-%m-%d")

            return valid_from, valid_to
        except Exception:
            return None, None

    def get_parsed_time(self):
        parsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return parsed_time

    def save_json(self, cards_info):
        with open('cards_info.json', 'w') as f:
            json.dump(cards_info, f, indent=4)

# scrapper = AktuelleProspekte()
# scrapper.card_info()
