# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Tuple,List
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re
import unidecode

from .constants import NEIGHBOURHOODS_CAPITAL_FEDERAL, PRICE_BANNED_WORDS, ROOMS
from .constants import LOCATION_BANNED_WORDS,ADDRESS_BANNED_WORDS,SPACE_WORDS

#dict_keys(['images', 'price', 'url', 'expenses', 'location', 'address', 'extras'])


class RetoScrapingPipeline:

    def _clean_price(self,price:str)->float:
        if not price:
            return None
        price = price.lower()
        if not any(p in price for p in PRICE_BANNED_WORDS):
            price =  float(re.sub("[^0-9]", "", price))
            return price 
        return None

    def _clean_expenses(self,expense:str)->float:
        if not expense:
            return 0.00
        return float(re.sub("[^0-9]", "", expense))

    def _clean_extras(self,extras:List[str])->Tuple[float,int,List[str]]:
        other = []
        m2,ambients = None,None
        for extra in extras:
            if 'm²' in extra:
                space=re.sub("[^0-9]", " ", extra)
                number_m2 = float(max(space.split()))
                m2 = number_m2 if number_m2>20.00 else None 
            elif any(word in extra.lower() for word in SPACE_WORDS):
                number_amb = re.sub("[^0-9]", " ", extra).strip()
                number_amb = 1 if not number_amb else number_amb
                number_amb = int(number_amb)
                ambients = number_amb+1 if any(word in extra.lower() for word in ROOMS) else number_amb
            else:
                other.append(extra)
        return (m2,ambients,other)

    def _clean_location(self,location:str)->str:
        if not location:
            return None
        location = location.lower()
        for word in LOCATION_BANNED_WORDS:
            location= location.replace(word,'')
        location = location.replace(',','').strip()
        for neihborhood in NEIGHBOURHOODS_CAPITAL_FEDERAL:
            if unidecode.unidecode(neihborhood.lower()) in unidecode.unidecode(location):
                return neihborhood
        return 'Otro'

    def _clean_address(self,address:str)->str:
        address=address.lower()
        for word in ADDRESS_BANNED_WORDS:
            address=address.replace(word,'')
        return address.strip().capitalize()


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        images = adapter.get('images')
        if not images:
            raise DropItem(f'No images in {item}')
        
        price = self._clean_price(adapter.get('price'))
        location = self._clean_location(adapter.get('location')) 
        m2,rooms,other = self._clean_extras(adapter.get('extras'))

        if price and location and m2 and rooms:
            expenses = self._clean_expenses(adapter.get('expenses'))
            address = self._clean_address(adapter.get('address'))
            adapter['price']=price
            adapter['location']=location
            adapter['m2']=m2
            adapter['rooms']=rooms
            adapter['extras']=other
            adapter['expenses']=expenses
            adapter['address']=address

            return item

        raise DropItem(f'Incomplete info in {item}')
    