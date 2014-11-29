class Item(object):
    # Upper Limit */    
    u = 0
    # Lower Limit */    
    l = 0
    name = ''

    # Next interval
    next = None

    def __init__(self,name,l,u):
        self.name = name
        self.u = u
        self.l = l

    def __str__(self):
        return 'name:' + self.name + '\nLower:'+ str(self.l) + '\nUpper:' + str(self.u) + '\nNext: ' + str(self.next != None)

    def hStr(self):
        return self.name + ':' + str(self.l) +'-' + str(self.u)

    def __hash__(self):
        return hash(self.hStr())
    
    def __lt__(self, other):
        if(self.name == other.name):
            return self.l < other.l and self.u < other.u
        return self.name < other.name

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.name == other.name and self.l == other.l and self.u == other.u
