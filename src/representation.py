import datetime
import os

import matplotlib.pyplot as plt
import networkx as nx


class Representation:
    def __init__(self):
        self.iterations =[]
        self.values_fc = []

    def reset_chart(self):
        self.iterations= []
        self.values_fc= []

    def add_point_to_chart(self,iteration, value):
        self.iterations.append(iteration)
        self.values_fc.append(value)

    def save_chart(self,path,testCase,test,bests,iterations):
        figure, axes = plt.subplots()
        plt.ylabel('Uzyskany kosz sieci w danej iteracji')
        plt.xlabel('Iteracja')
        plt.plot(range(int(iterations)), bests, linewidth=2.0)
        #plt.show()
        plt.savefig(path + "/" + testCase + "_" + test + '_chart.png',
                     bbox_inches='tight', format='png')
        plt.close(figure)

    def generate_out_files(self):
        plt.ylabel('Wartość funkcji celu')
        plt.xlabel('Iteracja')
        print(self.iterations)
        plt.plot(self.iterations, self.values_fc, linewidth=2.0)
        #plt.grid(True)
        plt.title("Funkcja celu")
        plt.show()

    def save_graph(self, Graph, path, testCase, test, config_parameters, cost, cost_cities, cost_ps, show):
        figure, axes = plt.subplots()
        cities = {}
        electricity = {}
        edges_electricity = {}
        edges_cities = {}
        keysC = set()
        keysE = set()
        for node in Graph.nodes():
            if node >= 0:
                cities.update({node: (Graph.node[node]['x'], Graph.node[node]['y'])})
            else:
                electricity.update({node: (Graph.node[node]['x'], Graph.node[node]['y'])})

        for edge in Graph.edges():
            if edge[0] < 0 or edge[1] < 0:
                # edges_electricity.update({edge: ((Graph.node[edge[0]]['x'], Graph.node[edge[0]]['y']),
                #                                               (Graph.node[edge[1]]['x'], Graph.node[edge[1]]['y']))})
                edges_electricity.update({(Graph.node[edge[0]]['x'], Graph.node[edge[0]]['y']):
                                              (Graph.node[edge[0]]['x'], Graph.node[edge[0]]['y']),
                                          (Graph.node[edge[1]]['x'], Graph.node[edge[1]]['y']):
                                              (Graph.node[edge[1]]['x'], Graph.node[edge[1]]['y'])})
                keysE.add(((Graph.node[edge[0]]['x'], Graph.node[edge[0]]['y']),
                           (Graph.node[edge[1]]['x'], Graph.node[edge[1]]['y'])))
            else:
                # edges_cities.update({edge[0]: ((Graph.node[edge[0]]['x'], Graph.node[edge[0]]['y']),
                #                                             (Graph.node[edge[1]]['x'], Graph.node[edge[1]]['y']))})
                edges_cities.update({(Graph.node[edge[0]]['x'], Graph.node[edge[0]]['y']):
                                         (Graph.node[edge[0]]['x'], Graph.node[edge[0]]['y']),
                                     (Graph.node[edge[1]]['x'], Graph.node[edge[1]]['y']):
                                         (Graph.node[edge[1]]['x'], Graph.node[edge[1]]['y'])})
                keysC.add(((Graph.node[edge[0]]['x'], Graph.node[edge[0]]['y']),
                           (Graph.node[edge[1]]['x'], Graph.node[edge[1]]['y'])))

        nx.draw_networkx_nodes(Graph, cities, cities.keys(), node_color='red', node_size=150,
                               label='Miasto',
                               ax=axes)
        nx.draw_networkx_nodes(Graph, electricity, electricity.keys(), node_color='blue', node_size=150, node_shape='h',
                               label='\nElektrownia\n',
                               ax=axes)

        # nx.draw_networkx_edges(Graph, edges_cities, edge_color="black" )
        nx.draw_networkx_edges(Graph, edges_cities, keysC,
                               label="Rail network cost:" + str(format(cost_cities, '.7f')) + '\nK: ' +
                                     config_parameters[0], ax=axes)
        nx.draw_networkx_edges(Graph, edges_electricity, keysE, edge_color="red",
                               label="Power grid cost:" + str(format(cost_ps, '.7f')) + '\nKe: ' +
                                     config_parameters[1],ax=axes)
        empty = {(0, 0): (0, 0)}
        nx.draw_networkx_nodes(Graph, empty, empty.keys(), node_color='white', node_size=0,
                               label='\n\nCAPEX: ' + str(format(cost, '.7f'))
                                     + '\nPopulation: ' + str(config_parameters[2])
                                     + '\nSelection: ' + str(config_parameters[3])
                                     + '\nIterations: ' + str(config_parameters[4]),
                               ax=axes)
        # nx.draw_networkx(Graph)
        handles, labels = axes.get_legend_handles_labels()
        legend = axes.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, -0.1))
        # legend.get_frame().set_alpha(0.5)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.title("Najlepsze uzyskane rozwiązanie")

        if show:
            plt_copy = plt
            plt_copy.show()

        # plt.imsave(path+ folder_out+"/"+ testCase + "_" + test + '_bestIm.png', format='png')
        plt.savefig(path + "/" + testCase + "_" + test + '_theBest.png',
                    bbox_extra_artists=(legend,), bbox_inches='tight', format='png')
        plt.close(figure)
