
from engine import Engine
import os, sys
import evals
import server

def ask(question):
    ans = input(question)
    return ans

class GUIProg:
    def __init__(self, datadir, dbdir='./'):
        print(datadir, dbdir)
        self.e = Engine(datadir, dbdir)
        self.server = server.Server(self.e)

    def run(self, method):
        self.server.run(method)
        pass

class CLIProg:
    def __init__(self, datadir, dbdir='./'):
        print(datadir, dbdir)
        self.engine = Engine(datadir, dbdir)

    def run(self, method):
        if os.path.isfile('index.hdf5'):
            ans = ask('Index file available, run it again? [y/N] ')
            if ans == 'y' or ans == 'Y':
                self.engine.index(method)

        while True:
            ans = ask('Search for (enter `stop` to stop): ')
            if ans == 'stop':
                return
            results = self.engine.look(ans, method)

            for r in results:
                print(f'{r} [{results[r]}]')

def help():
    print(f'{sys.argv[0]} - a simple reverse image search\n\n\
How to run:\n\
\t{sys.argv[0]} cli - run as a CLI app\n\
\t{sys.argv[0]} gui - run as a GUI application, requires a working browser')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        help()
        sys.exit(0)
    elif sys.argv[1] == 'cli':
        prog = CLIProg('/home/l4/Pictures/CBIR/')
        prog.run(evals.SIFT)

    elif sys.argv[1] == 'gui':
        prog = GUIProg('/home/l4/Pictures/CBIR/')
        prog.run(evals.SIFT)
