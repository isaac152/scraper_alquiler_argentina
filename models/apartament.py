from typing import Dict


class Apartament:
    
    def __init__(self,item_json:Dict[str,str]):

        self.address=item_json.get('address')
        self.expenses=item_json.get('expenses')
        self.extras=item_json.get('extras')
        self.images=item_json.get('images')
        self.location=item_json.get('location')
        self.m2=item_json.get('m2')
        self.rooms=item_json.get('rooms')
        self.url=item_json.get('url')
        self.price=item_json.get('price')

    def get_total_price(self)->float:
        try:
            return self.price+self.expenses
        except:
            return 0.00
    def get_relation_m_price(self)->float:
        return round((self.get_total_price())/self.m2,2)
    
    def __repr__(self) -> str:
        return f'PRICE: {self.price} ROOMS: {self.rooms} M2: {self.m2}'
        