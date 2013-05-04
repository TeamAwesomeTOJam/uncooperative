class Vec2:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y
    def __add__(self,other):
        return Vec2(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return Vec2(self.x-other.x,self.y-other.y)
    def __mult__(self,other):
        return Vec2(self.x*other,self.y*other)
    def __str__(self):
        return "["+str(self.x) + "," + str(self.y) + "]"

class Grid:
    def __init__(self, rows=1, cols = 1):
        self.ni = rows
        self.nj = cols

        self.data = [[1 for m in range(cols)] for m in range(rows)]

#    def __delitem__(self, key):
    def __getitem__(self, key): #key: int
        return self.data[key]
    def __setitem__(self, key, value):
        return self.data[key]

    def get(self, key): #Vec2 key
        return self.data[key.x][key.y]


    def set(self, key,value): #Vec2 key
        self.data[key.x][key.y]=value


    def __str__(self):
        ret = ""
        for row in self.data:
            for d in row:
                ret += str(d) + " "
            ret += "\n"
        return ret



