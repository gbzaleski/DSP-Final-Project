from analysis import *
import argparse
import difflib
import sys

# clear && python3 main.py API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv -start 1950
if __name__ == "__main__":

    # Reads paths and limits
    parser = argparse.ArgumentParser(description='Conducts data science analisys on emission, GDP and population')
    parser.add_argument('GDP_path', type=str, help='path for csv file on GDP')
    parser.add_argument('population_path', type=str, help='path for csv file on population')
    parser.add_argument('emission_path', type=str, help='path for csv file on emission')
    
    parser.add_argument('-start', type=int, help='lower year threshold for analisys')
    parser.add_argument('-koniec', type=int, help='upper year threshold for analisys')

    # Infinity range
    year_range_start = int(-1e9)
    year_range_end = int(1e9)

    args = parser.parse_args()

    if args.start != None:
        year_range_start = args.start

    if args.koniec != None:
        year_range_end = args.koniec

    print(args.GDP_path, args.population_path, args.emission_path)
    print(year_range_start, year_range_end)

    # Read data
    emissions = get_emission_data(args.emission_path)
    if emissions is None:
        print("File with emission data not found!", file=sys.stderr)
        exit(1)
    print(emissions.shape)

    population = get_population_data(args.population_path)
    print(population.shape)
    
    gdps = get_GDP_data(args.GDP_path)
    print(gdps.shape)

    exit(1)


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

