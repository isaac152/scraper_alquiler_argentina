from typing import Dict


#dict_keys(['images', 'price', 'url', 'expenses', 'location', 'address', 'extras'])


class Apartament:
    
    def __init__(self,item_json:Dict[str,str]):
        if item_json is not None:
            for k,v in item_json.items():
                setattr(self,k,v)
    
    def get_total_price(self)->float:
        try:
            return self.price+self.expenses
        except:
            return 0.00
    def get_relation_m_price(self)->float:
        return self.get_total_price()//self.m2
