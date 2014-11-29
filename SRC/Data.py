import numpy as np   # gets some useful functions such as special arrays, dot-product, etc.
import pymysql
import Item

class Data(object):
    columnNames = ['G','W','L','R','AB','H','2B','3B','HR','BB','SO','SB','RA','ER','ERA','HA','HRA','BBA','SOA','E']

    def __init__(self):
        pass

    def loadData(self):
        
        matrix = []

        
        conn = pymysql.connect(host='attiyat.net', port=3306, user='dm', passwd='encrypted', db='baseball')

        cur = conn.cursor()

        cur.execute("SELECT " + ', '.join(map(str,self.columnNames)) + " FROM Teams WHERE yearID >= '2000'")

        for row in cur:
            tempRow = []
            for rw in row:
                rw = int(rw or 0)
                tempRow.append(rw)
            matrix.append(tempRow)
        cur.close()
        conn.close()
        matrix = np.array(matrix)
        return matrix

    def createColumnIntervals(self, minSupp, k):
        matrix = []
        
        n = len(self.columnNames)
        numOfIntervals = int((2*n)/(minSupp*(k-1)))
        print("Number of Intervals: " + str(numOfIntervals))

        conn = pymysql.connect(host='attiyat.net', port=3306, user='dm', passwd='encrypted', db='baseball')

        cur = conn.cursor()
        columnIntervals = [[] for x in range(len(self.columnNames))]
        for i in range(len(self.columnNames)):
            colItems = columnIntervals[i]
            sqlStat = "SELECT "
            sqlStat += self.columnNames[i]
            sqlStat += " FROM Teams WHERE yearID >= '2000' ORDER BY "
            sqlStat += self.columnNames[i]
            sqlStat += " ASC"
            cur.execute(sqlStat)
            rows = cur.fetchall()
            totalPoints = len(rows)
            if (numOfIntervals > totalPoints):
                sizeOfInterval = 1
                numOfIntervals = totalPoints
            else:
                sizeOfInterval = int(totalPoints/numOfIntervals)

            tempRow = []
            prevItem = None

            for j in range (numOfIntervals):
                u = rows[j * sizeOfInterval + (sizeOfInterval-1)][0]
                l = rows[j * sizeOfInterval][0]
                
                if (not prevItem or prevItem.u < l):
                    it =  Item.Item(self.columnNames[i], l, u)
                    colItems.append(it)
                    if prevItem != None:
                        prevItem.next = it
                    prevItem = it

        cur.close()
        conn.close()


        return columnIntervals
