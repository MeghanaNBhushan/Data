import os
import sys

class upload_in_chunks(object):
    def __init__(self, filename, chunksize=1 << 13):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            while True:
                data = file.read(self.chunksize)
                if not data:
                    sys.stderr.write("\n")
                    break
                self.readsofar += len(data)
                done = int(50 * self.readsofar / self.totalsize)
                sys.stdout.write("\r[%s%s]  %s MBytes/ %s MBytes" % ('=' * done, ' ' * (50-done), round(self.readsofar/(1024 * 1024), 3), round(self.totalsize/(1024 * 1024), 3)) )    
                sys.stdout.flush()
                yield data

    def __len__(self):
        return self.totalsize