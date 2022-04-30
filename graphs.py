#Python imports
from typing import List,Dict,Tuple
from statistics import mean
import json
from glob import glob

#External imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Local imports
from models.apartament import Apartament

#Constants
JSON_PATH = './data/*.json'
GRAPH_PATH = './graphs'

def get_data()->List[Apartament]:
    """Extract the data from folder with the json files"""
    data= []
    for filename in glob(JSON_PATH):
        with open(filename) as p:
            data_j = json.load(p)
        data.extend(data_j)
    return [Apartament(d) for d in data]     

def most_rents_per_region_plot_bar(apartaments:List[Apartament])->None:
    """Create a bar graph amount rents / neighborhood """
    regions_dict={}
    for apartament in apartaments:
        region = apartament.location
        regions_dict[region]=regions_dict[region]+1 if region in regions_dict else 1
    
    df = pd.DataFrame.from_dict(regions_dict,orient='index').sort_values(by=0)
    ax = df.plot.bar(
        title='Apartamentos en alquiler por Barrios en Capital Federal. Argentina',
        xlabel = 'Barrios',
        ylabel = 'Cantidad',
        legend = False,
        figsize = (10,20),
        grid = True
    )
    ax.bar_label(ax.containers[0],label_type='edge')

    fig = ax.get_figure()
    fig.savefig(f'{GRAPH_PATH}/rents_per_region.png')


def create_histogram_figure(data:List[Apartament],range_bars:List[Tuple[int,int]]):
    """Logic to convert list of apartaments into a bar """
    data_dict= {}
    for bar in range_bars:
        min_bar,max_bar=bar
        for price in data:
            if price>=min_bar and price<=max_bar:
                data_dict[max_bar]= 1 if max_bar not in data_dict else data_dict[max_bar]+1
    
    df = pd.DataFrame.from_dict(data_dict,orient='index')
    ax = df.plot.bar(
        title='Frecuencia de precio de alquileres',
        xlabel = 'Precio ARS (Renta+Expensas) ',
        ylabel = 'Cantidad',
        legend = False,
        figsize = (10,14),
        grid= True
    )
    return ax.get_figure()


def price_distribution_histogram(apartaments:List[Apartament])->Tuple:
    """Generate two histograms. One with all the data and other with a normalize version"""
    data = [apartament.get_total_price() for apartament in apartaments]
    range_bars_full = [(i,i+10_000) for i in range(0,1_000_000,10_000)]
    range_bars_normalize = [(i,i+10_000) for i in range(0,310_000,10_000)]
    f1 =create_histogram_figure(data,range_bars_full)
    f2 =create_histogram_figure(data,range_bars_normalize)

    f1.savefig(f'{GRAPH_PATH}/full_histogram_distribution.png')
    f2.savefig(f'{GRAPH_PATH}/normalize_histogram_distrubtion.png')

def create_line_chart(dict_a:Dict[str,float],meta:List[str]):
    """Logic to convert the info into a line chart"""
    dict_graph = {
        'Min value':[],
        'Max value':[],
        'Average value':[]
    }
    list_filtred = [k for k in dict_a.keys() if len(dict_a[k])>5]
    for location in list_filtred:
        value = dict_a[location]
        dict_graph['Min value'].append(min(value))
        dict_graph['Max value'].append(max(value))
        dict_graph['Average value'].append(mean(value))
    df = pd.DataFrame(dict_graph, index=list_filtred).sort_index()
    lines = df.plot.line(
        style='.-',
        xlabel = meta[1],
        ylabel = meta[2],
        title = meta[0],
        grid=True,
        figsize=(10,16)
    ).get_figure()
    return lines,list_filtred

def m2_distribution_line_chart(apartaments:List[Apartament]):
    """Generate a line chart with the distribution of m2 per neighborhood"""
    dict_a = {}
    for apartament in apartaments:
        location = apartament.location
        if location not in dict_a:
            dict_a[location]=[]
        dict_a[location].append(apartament.m2)
    
    meta = [ "Distribución de M2 en los Barrios de Capital Federal Argentina",'Barrios','Superficie (m2)']
    lines,list_filtred = create_line_chart(dict_a,meta)
    plt.xticks(range(0,len(list_filtred)), labels=list_filtred,rotation=90)
    plt.yticks(np.arange(0, 900, 50))
    
    lines.savefig(f'{GRAPH_PATH}/m2_distribution_line_chart.png')

def m2_relation_neighborhood_line_chart(apartaments:List[Apartament])->None:
    """"""
    dict_a = {}
    for apartament in apartaments:
        rooms = apartament.rooms
        if rooms not in dict_a:
            dict_a[rooms]=[]
        dict_a[rooms].append(apartament.m2)
    meta = [ "Relación de Superficie con respecto a los ambientes en alquiler en Capital Federal.",'Ambientes','Superficie (m2)']
    lines,list_filtred = create_line_chart(dict_a,meta)
    plt.yticks(np.arange(0, 900, 50))
    lines.savefig(f'{GRAPH_PATH}/m2_neighborhood.png')
    
def relation_m2_price_boxplot(apartaments:List[Apartament])->None:
    """Generate a boxplot to watch the range of prices per m2 in the neighborhoods"""
    location_d = {}
    for apartament in apartaments:
        location = apartament.location
        if location not in location_d:
            location_d[location]= []
        #borrar
        value = apartament.get_relation_m_price()
        if value>0:
            location_d[location].append(value)
    

    fig,ax = plt.subplots(figsize=(16,16))

    ax.boxplot(location_d.values(),showfliers=False)
    ax.set_xticklabels(location_d.keys())
    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, 4200, 300))
    plt.grid()
    plt.title('Relación Superficie (m2)/ Precio (ARS) en alquileres de Capital Federal. Argentina ',fontsize=20)
    plt.xlabel('Barrios',fontsize=16)
    plt.ylabel('Precio ARS (Alquiler+Expensas)/m2',fontsize=16)
    
    fig.savefig(f'{GRAPH_PATH}/m2_price_box_plot.png')


def generate_graphs(data:List[Apartament])->None:
    """Wrapper to generate the graphs"""
    most_rents_per_region_plot_bar(data)
    price_distribution_histogram(data)
    m2_distribution_line_chart(data)
    m2_relation_neighborhood_line_chart(data)
    relation_m2_price_boxplot(data)

if __name__=='__main__':
    data = get_data()
    generate_graphs(data)
