import networkx as nx
from matplotlib import pyplot
import datetime

class ReportGenerator:

    def __init__(self):
        self,date_format = "%Y_%m_%d_%H_%M_%S_%f"

    def generate_best_individual_report(self):
        figure, axes = pyplot.subplots()
        g = nx.Graph()
