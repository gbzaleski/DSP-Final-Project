from analysis import *
import difflib


if __name__ == "__main__":
    # Read data
    emissions = pd.read_csv('co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv')
    emissions['Country'] = emissions['Country'].map(lambda n: n.lower())
    print(emissions.shape)

    # Deletes extra unnamed columns with NaNs
    population = pd.read_csv('API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv').dropna(how='all', axis='columns')
    print(population.shape)
    population['Country Name'] = population['Country Name'].map(lambda n: n.lower())

    gdps = pd.read_csv('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv').dropna(how='all', axis='columns')
    gdps['Country Name'] = gdps['Country Name'].map(lambda n: n.lower())
    print(gdps.shape)



    countries_emissions = np.sort(emissions['Country'].unique())
    countries_list = np.sort(population['Country Name'].unique())
    # countries_gdps = countries_population

    decapitalise = np.vectorize(lambda x : x.lower())
    countries_emissions = decapitalise(countries_emissions)
    countries_list = decapitalise(countries_list)

    matches = {} # name -> (correct_name, similarity)

    #difflib.get_close_matches("Hallo", words, len(words), 0)
    for name in countries_emissions:
        res = difflib.get_close_matches(name, countries_list, len(countries_list), 0)[0]
        matches[name] = res

    # Manual updates
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

    print(matches)

