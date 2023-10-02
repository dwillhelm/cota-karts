#%% 
from os import PathLike
from typing import Union
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sb 


def parse_html(filepath:Union[str, PathLike]) -> pd.DataFrame:
    """Parse the COTA HTML."""
    with open(filepath, 'r') as fh: 
        html = fh.read()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'dg'})

    # extract data 
    data = [] 
    if table:
        table_rows = table.find_all('tr')
        for row in table_rows:
            row_data = [cell.text.strip() for cell in row.find_all('td')]
            
            # format last row
            _x = row_data[-1]
            _x = _x.split("\n")[0]
            row_data[-1] = _x
            data.append(row_data)
        
    else:
        print("Table not found in HTML.")

    columns = ['racer_position', 'racer_id', 'best_lap', 'num_laps', 'avg_lap', 'gap', 'pro_skill', ]
    _dtypes = [int, str, float, int, float, float, float]
    data = pd.DataFrame(data[1:], columns=columns) 
    data.loc[0]['gap'] = 0.0 
    data = data.astype(dict(zip(columns, _dtypes)))
    return data

if __name__ == '__main__':
    # test
    filepath = "./data/races/raw/race-results-1.html"
    out = parse_html(filepath)
    out 




