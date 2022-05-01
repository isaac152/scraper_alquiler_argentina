from typing import List,Dict
from models.apartament import Apartament

def get_neighborhoods(apartaments:List[Apartament])->Dict[str,int]:
    regions = {}
    for apartament in apartaments:
        location = apartament.location
        regions[location] = 1 if not location in regions else regions[location]+1
    return regions

def get_apartaments_by_neighborhood(apartaments:List[Apartament],neighborhood:str)->List[Apartament]:
    return [apartament for apartament in apartaments if apartament.location==neighborhood]

def get_best_apartaments_m2_price(apartaments:List[Apartament])->List[Apartament]:
    return sorted(apartaments, key = lambda apartament:apartament.get_relation_m_price())[:3]

def get_cheaper_apartaments_per_m2(apartaments:List[Apartament])->List[Apartament]:
    return sorted(apartaments,key = lambda apartament:(apartament.get_total_price(),-apartament.m2))[:3]