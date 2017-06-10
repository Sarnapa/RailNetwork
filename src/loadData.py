class LoadData:

    def readLocalization(self, path):
        file = open (path, 'r')
        localizations = set()

        for line in file:
            row = line.split()
            localizations.add((float(row[0]),float(row[1])))

        file.close()
        return localizations

    def readConfig(self, path):
        file = open (path, 'r')
        parameters = []

        for line in file:
            row = line.split()
            parameters.append(row[0])

        file.close();
        return parameters
