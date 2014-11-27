import numpy as np   # gets some useful functions such as special arrays, dot-product, etc.
import pymysql


def loadData():
    
    matrix = []
    columnNames = ['G','W','L','R','AB','H','2B','3B','HR','BB','SO','SB','RA','ER','ERA','HA','HRA','BBA','SOA','E']

    
    conn = pymysql.connect(host='attiyat.net', port=3306, user='dm', passwd='encrypted', db='baseball')

    cur = conn.cursor()

    cur.execute("SELECT a.G,a.W,a.L,a.R,a.AB,a.H,a.2B,a.3B,a.HR,a.BB,a.SO,a.SB,a.RA,a.ER,a.ERA,a.HA,a.HRA,a.BBA,a.SOA,a.E FROM Teams a INNER JOIN Batting b ON a.teamID = b.teamID and a.yearID = b.yearID")

    for row in cur:
        tempRow = []
        for rw in row:
            rw = int(rw or 0)
            tempRow.append(rw)
        matrix.append(tempRow)
    cur.close()
    conn.close()
    matrix = np.array(matrix)
    return matrix, columnNames
