import h5py
import hashlib

class DB:
    @staticmethod
    def path2md5(path):
        return hashlib.md5(path.encode('utf-8')).hexdigest()

    def __init__(self, dbdir = './'):
        try:
            self.dir = dbdir
            self.data = h5py.File(dbdir + 'index.hdf5', 'r+')
        except Exception as e:
            raise e

    def insert(self, cat, path, data):
        name = DB.path2md5(path)
        try:
            self.data.create_dataset(cat + '/' + name, data = data)
        except Exception as e:
            print(e)

    def getcat(self, cat):
        try:
            return self.data[cat]
        except Exception as e:
            print(e)
            return None

    def get(self, idx):
        try:
            return self.data[idx][:]
        except Exception as e:
            print(e)
            return None

    def getraw(self, cat, path):
        name = DB.path2md5(path)
        try:
            return self.data[cat + '/' + name][:]
        except Exception as e:
            print(e)
            return None

