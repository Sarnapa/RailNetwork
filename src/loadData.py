class LoadData:

    def read_localization(self, path):
        file = open (path, 'r')
        localizations = {}

        for line in file:
            row = line.split()
            idx = int(row[0])
            localizations[idx] = []
            localizations[idx].append(int(row[1]))
            localizations[idx].append(int(row[2]))

        file.close()
        return localizations

    def read_config(self, path):
        file = open (path, 'r')
        parameters = []

        for line in file:
            row = line.split()
            parameters.append(row[0])

        file.close()
        return parameters

    def read_testCase(self, path):
        file = open (path,'r')
        files = []
        for line in file:
            row = line.split()
            files.append(row)
        return files