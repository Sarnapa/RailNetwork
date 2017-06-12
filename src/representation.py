import matplotlib.pyplot as ppt
class Representation:

    def __init__(self):
        self.generate_out_files([1,2,3,4,5,6],[4,5,1,2,7,8])

    def generate_out_files(self, iterations, values_fc):
        ppt.ylabel('Wartość funkcji celu')
        ppt.xlabel('Iteracja')
        ppt.plot(iterations,values_fc, linewidth=2.0)
        ppt.grid(True)
        ppt.title("Funkcja celu")
        ppt.show()
Representation()