 
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

    # Uses difflib function to find the matching name
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

    # Removing corrupted inputs (safe-checking if element will cease to exist in the future)
    matches.pop('zanzibar', None)
    matches.pop('antarctic fisheries', None)
    matches.pop('christmas island', None)
    matches.pop('ussr', None)
    matches.pop('united korea', None)
    matches.pop('former panama canal zone', None)
    matches.pop('occupied palestinian territory', None)
    matches.pop('saint helena', None)
    matches.pop('republic of south vietnam', None)
    matches.pop('taiwan', None)
    matches.pop('yugoslavia (former socialist federal republic)', None)
    matches.pop('bonaire, saint eustatius, and saba', None)
    matches.pop('niue', None)
    matches.pop('st. pierre & miquelon', None)

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
            return np.float64(gdps.loc[(gdps['Country Name'] == country_name)][str(year)])
        except:
            return np.nan 
        
    def parsePopulation(row):
        row['Population'] = getPopulation(row['Country'], row['Year'])
        row['GDP'] = getGDP(row['Country'], row['Year'])
        return row

    data = data.apply(parsePopulation, axis=1)

    return data

# Kt??re kraje w poszczeg??lnych latach z danymi, emituj?? najwi??cej CO2 w
# przeliczeniu na mieszka??ca. To znaczy generuje posortowan?? po latach
# tabelk?? pi??cioma krajami o najwi??kszej emisji na osob?? (z podan?? nazw??
# kraju, emisj?? na osob?? i ca??kowit?? emisj??
def task1(data, year_range_start, year_range_end):

    return data[['Year', 'Country', 'Per Capita', 'Total']]\
        [(data['Year'] >= year_range_start) & (data['Year'] <= year_range_end)]\
        .sort_values('Per Capita').groupby(['Year']).tail(5)\
        .sort_values(['Year', 'Per Capita'], ascending=False)

# Kt??re kraje w poszczeg??lnych latach z danymi maj?? najwi??kszy przych??d
# mieszka??ca. To znaczy generuje posortowan?? po latach tabelk?? pi??cioma
# krajami o najwi??kszym dochodzie na mieszka??ca (z podan?? nazw?? kraju,
# dochodem na mieszka??ca i ca??kowitym dochodem)
def task2(data, year_range_start, year_range_end):

    data['GDP per capita'] = data['GDP'] / data['Population']
    return data[['Year', 'Country', 'GDP per capita', 'GDP']]\
        [(data['Year'] >= year_range_start) & (data['Year'] <= year_range_end)]\
        .dropna().sort_values('GDP per capita').groupby(['Year'])\
        .tail(5).sort_values(['Year', 'GDP per capita'], ascending=False)

# Kt??re kraje (w przeliczeniu na mieszka??ca) najbardziej zmniejszy??y przez ost. 10 lat (z danych) emisj?? CO2
def task3_best(data):
    year = data.dropna()['Year'].max()
    year_back = year - 10
    data_ch = data[data['Year'] == year][['Country', 'Per Capita']]\
        .merge(data[data['Year'] == year_back][['Country', 'Per Capita']], left_on='Country', right_on='Country')
    data_ch['Change (10 yrs)'] = data_ch['Per Capita_x'] - data_ch['Per Capita_y']
    return data_ch.sort_values('Change (10 yrs)', ascending=False).tail(5)\
        [['Country', 'Change (10 yrs)']].iloc[::-1]

# Kt??re kraje (w przeliczeniu na mieszka??ca) najbardziej zwi??kszy??y przez ost. 10 lat (z danych) emisj?? CO2
def task3_worst(data):
    year = data.dropna()['Year'].max()
    year_back = year - 10
    data_ch = data[data['Year'] == year][['Country', 'Per Capita']]\
        .merge(data[data['Year'] == year_back][['Country', 'Per Capita']], left_on='Country', right_on='Country')
    data_ch['Change (10 yrs)'] = data_ch['Per Capita_x'] - data_ch['Per Capita_y']
    return data_ch.sort_values('Change (10 yrs)').tail(5)[['Country', 'Change (10 yrs)']].iloc[::-1]
    
    
