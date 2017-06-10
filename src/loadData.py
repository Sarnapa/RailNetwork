class LoadData:

    def readLocalization(self, path):
        file = open (path, 'r')
        localizations = set()

        for line in file:
            row = line.split()
            localizations.add((float(row[0]),float(row[1])))

