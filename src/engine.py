import os
from database import DB
from evals import Histogram

class Engine:
    def __init__(self, datadir, dbdir = './'):
        self.datadir = datadir
        self.dbdir = dbdir

        self.db = DB(dbdir)

    ## walk in datadir recursively to lookup for files, then calculate its
    ## vectors, save it to database
    def index(self, method):
        method.index(self.db, self.datadir)

    ## get the value of picture
    def getval(self, cat, path):
        val = self.db.getraw(cat, path)
        return val

    ## search the
    def search(self, path, cat = 'histogram', limit = 10):
        val = Histogram.calc(path)
        print(val)

        ## loop all over the database to find the lowest dirrerences
        data = self.db.getcat(cat)

        for img in data:
            val = self.db.get(cat + '/' + img)


    def look(self, path, method):
        target = self.getval('histogram', path)
        ddict = {}

        try:
            for (root, dirs, files) in os.walk(self.datadir):
                for f in files:
                    if f.endswith('jpg') or f.endswith('png'):
                        path = os.path.join(root, f)
                        val = self.db.getraw('histogram', path)

                        ## then compare two values, save to a dict, and
                        ## get top n best closest values
                        d = Histogram.distance(target, val)
                        ddict[path] = d

        except Exception as e:
            raise e

        for k in sorted(ddict, key=ddict.get):
            print(f'{k}: [{ddict[k]}]')
