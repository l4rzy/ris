import os
from database import DB
from evals import Histogram

class Engine:
    def __init__(self, datadir, dbdir = './'):
        self.limit = 20
        self.datadir = datadir
        self.dbdir = dbdir

        self.db = DB(dbdir)

    ## walks in datadir recursively to lookup for files, then calculate its
    ## vectors, save it to database
    def index(self, method):
        method.index(self.db, self.datadir)

    ## gets the value of picture
    def getraw(self, cat, path):
        val = self.db.getraw(cat, path)
        return val

    ## sets search limit
    def setlimit(self, limit):
        self.limit = limit

    ## looks for similar images
    def look(self, path, method):
        ddict = {}
        target = self.getraw(method.name, path)

        if target is None:
            kp, target = method.calc(path)

        try:
            for (root, dirs, files) in os.walk(self.datadir):
                for f in files:
                    if f.endswith('jpg') or f.endswith('png'):
                        path = os.path.join(root, f)
                        val = self.getraw(method.name, path)
                        if val is None:
                            print(f'error getraw for {path}: {DB.path2md5(path)}')
                            kp, val = method.calc(path)

                        ## then compare two values, save to a dict, and
                        ## get top n best closest values
                        d = method.distance(target, val)
                        ddict[path] = d

        except Exception as e:
            raise e

        results = {}
        i = 1
        for k in sorted(ddict, key=ddict.get):
            if i == self.limit:
                return results

            results[k] = ddict[k]
            i += 1
