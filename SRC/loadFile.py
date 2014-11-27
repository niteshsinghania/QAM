import numpy as np   # gets some useful functions such as special arrays, dot-product, etc.
import pymysql
import Item


def createColumnIntervals(minSupp, k):
    matrix = []
    
    columnNames = ['G','W','L','R','AB','H','2B','3B','HR','BB','SO','SB','RA','ER','ERA','HA','HRA','BBA','SOA','E']
    
    n = len(columnNames)
    numOfIntervals = int((2*n)/(minSupp*(k-1)))

    conn = pymysql.connect(host='attiyat.net', port=3306, user='dm', passwd='encrypted', db='baseball')

    cur = conn.cursor()
    columnIntervals = [[] for x in range(len(columnNames))]
    for i in range(len(columnNames)):
        colItems = columnIntervals[i]
        sqlStat = "SELECT "
        sqlStat += columnNames[i]
        sqlStat += " FROM Teams WHERE yearID >= '2000' ORDER BY "
        sqlStat += columnNames[i]
        sqlStat += " ASC"
        cur.execute(sqlStat)
        rows = cur.fetchall()
        totalPoints = len(rows)
        sizeOfInterval = int(totalPoints/numOfIntervals)

        tempRow = []
        oldItem = None
        for j in range (numOfIntervals):
            u =  rows[j * sizeOfInterval][0]
            l = rows[j * sizeOfInterval + sizeOfInterval-1][0]
            if (oldItem == None or oldItem.l < u):
                it =  Item.Item(columnNames[i],u,l)
                colItems.append(it)
                oldItem = it

    cur.close()
    conn.close()


    return columnIntervals
