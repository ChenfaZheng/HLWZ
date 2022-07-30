import numpy as np
import pandas as pd
import os

HOME = '../'
ATOM_MASS_PATH = os.path.join(HOME, 'atomic_mass.tsv')


def _trans(s: str) -> float:
    '''
    Convert data into float

    Used in `name2mass` function
    '''
    tag = 0 # if atom mass is estimated
    if pd.notna(s):
        if s == '———':
            return -1   # null data
        if s == '':
            return -1
        if s.startswith('(') and s.endswith(')'):
            tag = 1
            s = s[1:-1]
    else:
        return -1   # not a number
    # convert to float
    m = float(s)
    return m


def symbol2mass(name: str, datapath: str=os.path.join(HOME, 'atomic_mass.tsv')) -> int:
    '''
    Convert moleculer's symbol to mass (rounded to integer)

    See also: https://www.angelo.edu/faculty/kboudrea/periodic/structure_mass.htm
    '''
    # load atomic mass data
    df = pd.read_csv(
        datapath, 
        delimiter='\t', 
        memory_map=True, 
        converters={3: _trans},     # convert atomic mass data to float
    )
    df.to_csv(datapath + 'new.tsv')




def main():
    df = pd.read_csv(
        '/home/zhengcf/Documents/GitHub/HLWZ/data/atomic_mass.tsv', 
        delimiter='\t', 
        memory_map=True, 
        converters={3: _trans},     # convert atomic mass data to float
    )
    df.to_csv('/home/zhengcf/Documents/GitHub/HLWZ/data/atomic.tsv', sep='\t', index=False)
    pass


if __name__ == '__main__':
    main()