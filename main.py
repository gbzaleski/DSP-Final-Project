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

    # Infinity range if not provided otherwise
    year_range_start = int(-1e9)
    year_range_end = int(1e9)

    args = parser.parse_args()

    if args.start != None:
        year_range_start = args.start

    if args.koniec != None:
        year_range_end = args.koniec

    # Read data
    emissions = get_emission_data(args.emission_path)
    if emissions is None:
        print("File with emission data not found!", file=sys.stderr)
        exit(1)

    print(emissions.shape)

    population = get_population_data(args.population_path)
    if population is None:
        print("File with population data not found!", file=sys.stderr)
        exit(1)
    print(population.shape)
    
    gdps = get_GDP_data(args.GDP_path)
    if gdps is None:
        print("File with gdps data not found!", file=sys.stderr)
        exit(1)
    print(gdps.shape)

    matches = constuct_name_matches(emissions, population)
    # Deletes 3% of inputs from Emission that were agreed to be corrupted
    emissions = emissions[emissions['Country'].isin(matches)] 
    # Maps the names of countries to match
    emissions['Country'] = emissions['Country'].map(matches)

    data = combine_datasources(emissions, population, gdps)

    print(data.shape)

    result1 = task1(data, year_range_start, year_range_end)
    print("##### Subtask 1 - Solution: #####")
    if result1.size > 0:
        print(result1)
    else:
        print("No results for years provided!")
    print()

    result2 = task2(data, year_range_start, year_range_end)
    print("##### Subtask 2 - Solution: #####")
    if result2.size > 0:
        print(result2)
    else:
        print("No results for years provided!")
    print()

    result3_b = task3_best(data)
    result3_w = task3_worst(data)
    print("##### Subtask 3 - Solution: #####")
    print("# Best progress: #")
    print(result3_b)
    print("# Worst progress: #")
    print(result3_w)
    print()
