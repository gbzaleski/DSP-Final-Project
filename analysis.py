 
import pandas as pd
import numpy as np
import difflib

# Reads emission data
def get_emission_data(path):
    try:
        emissions = pd.read_csv(path)
        emissions['Country'] = emissions['Country'].map(lambda n: n.lower())
        return emissions
    except:
        return None

# Reads population data
def get_population_data(path):
    try:
        # Deletes extra unnamed columns with NaNs
        population = pd.read_csv(path).dropna(how='all', axis='columns')
        population['Country Name'] = population['Country Name'].map(lambda n: n.lower())
        return population
    except:
        return None

# Reads GDP data
def get_GDP_data(path):
    try:
        # Deletes extra unnamed columns with NaNs
        gdps = pd.read_csv(path).dropna(how='all', axis='columns')
        gdps['Country Name'] = gdps['Country Name'].map(lambda n: n.lower())
        return gdps
    except:
        return None

# Preprocesses data for future merging of both sources
def constuct_name_matches(emissions, population):
    countries_emissions = np.sort(emissions['Country'].unique())
    countries_list = np.sort(population['Country Name'].unique())
    # GDP and Population data uses the same encoding for countries

    decapitalise = np.vectorize(lambda x : x.lower())
    countries_emissions = decapitalise(countries_emissions)
    countries_list = decapitalise(countries_list)

    matches = {} # name -> corresponding name in the second dataframe

    for name in countries_emissions:
        res = difflib.get_close_matches(name, countries_list, len(countries_list), 0)[0]
        matches[name] = res

    # Manual updates for selected countries
    matches['czech republic'] = 'czechia'
    matches['china (mainland)'] = 'china'
    matches['democratic republic of the congo (formerly zaire)'] = 'congo, dem. rep.'
    matches['congo'] = 'congo, rep.'
    matches['democratic republic of vietnam'] = 'vietnam'
    matches['federated states of micronesia'] = 'micronesia, fed. sts.'
    matches['gambia'] = 'gambia, the'
    matches['france (including monaco)'] = 'france'
    matches['kyrgyzstan'] = 'kyrgyz republic'
    matches['federal republic of germany'] = 'germany'
    matches['japan (excluding the ruyuku islands)'] = 'japan'
    matches['lao people s democratic republic'] = 'lao pdr'
    matches['italy (including san marino)'] = 'italy'
    matches['islamic republic of iran'] = 'iran, islamic rep.'
    matches['plurinational state of bolivia'] = 'bolivia'
    matches['slovakia'] = 'slovak republic'
    matches['myanmar (formerly burma)'] = 'myanmar'
    matches['republic of korea'] = 'korea, rep.'
    matches['libyan arab jamahiriyah'] = 'libya'

    # Removing corrupted inputs
    del matches['zanzibar']
    del matches['antarctic fisheries']
    del matches['christmas island']
    del matches['ussr']
    del matches['united korea']
    del matches['former panama canal zone']
    del matches['occupied palestinian territory']
    del matches['saint helena']
    del matches['republic of south vietnam']
    del matches['taiwan']
    del matches['yugoslavia (former socialist federal republic)']
    del matches['bonaire, saint eustatius, and saba']
    del matches['niue']
    del matches['st. pierre & miquelon']

    return matches

# Combines data
def combine_datasources(emissions, population, gdps):
    # Combine emssions with gdp and population data
    data = emissions
    data['Population'] = np.nan
    data['GDP'] = np.nan

    def getPopulation(country_name, year):
        try:
            return np.float64(population.loc[(population['Country Name'] == country_name)][str(year)])
        except:
            return np.nan

    def getGDP(country_name, year):
        try:
            return np.float64(gdps.loc[(population['Country Name'] == country_name)][str(year)])
        except:
            return np.nan 
        
    def parsePopulation(row):
        row['Population'] = getPopulation(row['Country'], row['Year'])
        row['GDP'] = getGDP(row['Country'], row['Year'])
        return row

    data = data.apply(parsePopulation, axis=1)

    return data

# Które kraje w poszczególnych latach z danymi, emitują najwięcej CO2 w
# przeliczeniu na mieszkańca. To znaczy generuje posortowaną po latach
# tabelkę pięcioma krajami o największej emisji na osobę (z podaną nazwą
# kraju, emisją na osobę i całkowitą emisją
def task1(data, year_range_start, year_range_end):

    return data[['Year', 'Country', 'Per Capita', 'Total']]\
        [(data['Year'] >= year_range_start) & (data['Year'] <= year_range_end)]\
        .sort_values('Per Capita').groupby(['Year']).tail(5)\
        .sort_values(['Year', 'Per Capita'], ascending=False)

# Które kraje w poszczególnych latach z danymi mają największy przychód
# mieszkańca. To znaczy generuje posortowaną po latach tabelkę pięcioma
# krajami o największym dochodzie na mieszkańca (z podaną nazwą kraju,
# dochodem na mieszkańca i całkowitym dochodem)
def task2(data, year_range_start, year_range_end):

    data['GDP per capita'] = data['GDP'] / data['Population']
    return data[['Year', 'Country', 'GDP per capita', 'GDP']]\
        [(data['Year'] >= year_range_start) & (data['Year'] <= year_range_end)]\
        .dropna().sort_values('GDP per capita').groupby(['Year'])\
        .tail(5).sort_values(['Year', 'GDP per capita'], ascending=False)

# Które kraje (w przeliczeniu na mieszkańca) najbardziej zmniejszyły przez ost. 10 lat (z danych) emisję CO2
def task3_best(data):
    year = data.dropna()['Year'].max()
    year_back = year - 10
    data_ch = data[data['Year'] == year][['Country', 'Per Capita']]\
        .merge(data[data['Year'] == year_back][['Country', 'Per Capita']], left_on='Country', right_on='Country')
    data_ch['Change (10 yrs)'] = data_ch['Per Capita_x'] - data_ch['Per Capita_y']
    return data_ch.sort_values('Change (10 yrs)', ascending=False).tail(5)\
        [['Country', 'Change (10 yrs)']].iloc[::-1]

# Które kraje (w przeliczeniu na mieszkańca) najbardziej zwiększyły przez ost. 10 lat (z danych) emisję CO2
def task3_worst(data):
    year = data.dropna()['Year'].max()
    year_back = year - 10
    data_ch = data[data['Year'] == year][['Country', 'Per Capita']]\
        .merge(data[data['Year'] == year_back][['Country', 'Per Capita']], left_on='Country', right_on='Country')
    data_ch['Change (10 yrs)'] = data_ch['Per Capita_x'] - data_ch['Per Capita_y']
    return data_ch.sort_values('Change (10 yrs)').tail(5)[['Country', 'Change (10 yrs)']].iloc[::-1]
    
    
