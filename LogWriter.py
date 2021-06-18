import datetime
import os
from csv import DictWriter


class LogWriter():
    def __init__(self, filename, last_pull_filename, fieldnames, timeformat):
        self.writefile = open(filename, "a+")
        self.timefile = open(last_pull_filename, "a+")
        self.writer = DictWriter(self.writefile, fieldnames=fieldnames, dialect="excel")
        self.last_pull_filename = last_pull_filename
        self.timeformat = timeformat

        self.firstwrite = os.path.getsize(filename) == 0
        if os.path.getsize(last_pull_filename) == 0:
            self.timefile.write(str(datetime.datetime.now()).split('.')[0] + '\n')
            self.timefile.close()

    def write_to_file(self, list_of_dicts):
        self.timefile = open(self.last_pull_filename, "r")
        line = self.timefile.readlines()[-1].rstrip()
        last_ingest = datetime.datetime.strptime(line, self.timeformat)

        self.writer.writeheader()
        for row in list_of_dicts:
            if self.firstwrite or datetime.datetime.strptime(row['last_modified'], self.timeformat) > last_ingest:
                self.writer.writerow(row)

        self.firstwrite = False
        self.timefile = open(self.last_pull_filename, "a")
        self.timefile.write(str(datetime.datetime.now()).split('.')[0] + '\n')

        self.writefile.flush()
        self.timefile.close()
