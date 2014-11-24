import numpy as np   # gets some useful functions such as special arrays, dot-product, etc.
import sqlite3


def load_data_from_file(f,columns):
    
    matrix = np.loadtxt(f,skiprows = 1, usecols=(columns),delimiter=',')
        
    return matrix

conn = sqlite3.connect('example.db')
c = conn.cursor()
conn.commit()
conn.close()
