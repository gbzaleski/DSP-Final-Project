import pytest
from analysis import *

@pytest.mark.parametrize("path, is_correct", [("wrong/path.csv", False), \
    ("co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv", True)])
def test_read_emission(path, is_correct):
    result = get_emission_data(path)
    if is_correct:
        assert result.size > 0
    else:
        assert result is None


@pytest.mark.parametrize("path, is_correct", [("wrong/path.csv", False), \
    ("API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv", True)])
def test_read_GDP(path, is_correct):
    result = get_GDP_data(path)
    if is_correct:
        assert result.size > 0
    else:
        assert result is None


@pytest.mark.parametrize("path, is_correct", [("wrong/path.csv", False), \
    ("API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv", True)])
def test_read_population(path, is_correct):
    result = get_population_data(path)
    if is_correct:
        assert result.size > 0
    else:
        assert result is None


def test_matching():
    first_country_list = ['poland', 'zanzibar', 'china (mainland)', 'old republic of imaginery state']
    second_country_list = ['poland, rep', 'china', 'the new republic of imaginery state']
    matches = constuct_name_matches(pd.DataFrame(first_country_list, columns=['Country']),
        pd.DataFrame(second_country_list, columns=['Country Name']))
    
    assert 'zanzibar' not in matches
    assert 'ussr' not in matches
    assert matches['old republic of imaginery state'] == 'the new republic of imaginery state'
    assert matches['slovakia'] == 'slovak republic'
    assert matches['china (mainland)'] == 'china'
    assert matches['poland'] == 'poland, rep'


def test_combining():
    mock_emission = {'Year':['2000','2001','2000','2001'],
           'Country':['Czechia','Czechia','Poland','Poland'],
           'Emissions':[35, 40, 50, 20]}
    mock_emission = pd.DataFrame.from_dict(mock_emission)

    mock_population = {
        'Country Name':['Czechia','Poland'],
        '2000':[3*1e6, 30*1e6],
        '2001':[4*1e6, 50*1e6],
        }
    mock_population = pd.DataFrame.from_dict(mock_population)

    mock_gdp = {
        'Country Name':['Czechia','Poland'],
        '2000':[9*1e8, 20*1e8],
        '2001':[8*1e6, 22*1e8],
        }
    mock_gdp = pd.DataFrame.from_dict(mock_gdp)

    result = combine_datasources(mock_emission, mock_population, mock_gdp)

    assert result is not None
    assert result.shape == (4, 5)
    assert result.size == 20
    assert list(result.columns) == ['Year', 'Country', 'Emissions', 'Population', 'GDP']
    assert result[result['Country'] == 'Czechia'].iloc[1, 2] == 40
