class Item(object):
    
    u = 0
    l = 0
    name = ''

    def __init__(self,name,u,l):
        self.name = name
        self.u = u
        self.l = l
    def __str__(self):
        return 'name:' + self.name + '\nu:'+ str(self.u) + '\nl:' + str(self.l)