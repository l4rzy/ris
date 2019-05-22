
from engine import Engine
import os
import evals

def ask(question):
    ans = input(question)
    return ans


class Prog:
    def __init__(self, datadir):
        self.engine = Engine(datadir)

    def run(self):
        method = evals.Histogram

        if os.path.isfile('index.hdf5'):
            ans = ask('Index file available, rerun it? [y/N] ')
            if ans == 'y' or ans == 'Y':
                self.engine.index(method)

        while True:
            ans = ask('Image path to search for (enter `stop` to stop): ')
            if ans == 'stop':
                return
            print('=== results ===')
            self.engine.look(ans, method)
            print('=== end results ===')


