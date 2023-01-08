 
import pandas as pd
import numpy as np


def get_emission_data(path):
    try:
        emissions = pd.read_csv(path)
        emissions['Country'] = emissions['Country'].map(lambda n: n.lower())
        return emissions
    except:
        return None

def get_population_data(path):
    try:
        # Deletes extra unnamed columns with NaNs
        population = pd.read_csv(path).dropna(how='all', axis='columns')
        population['Country Name'] = population['Country Name'].map(lambda n: n.lower())
        return population
    except:
        return None

def get_GDP_data(path):
    try:
        # Deletes extra unnamed columns with NaNs
        gdps = pd.read_csv(path).dropna(how='all', axis='columns')
        gdps['Country Name'] = gdps['Country Name'].map(lambda n: n.lower())
        return gdps
    except:
        return None
