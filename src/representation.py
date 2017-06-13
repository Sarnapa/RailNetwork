import datetime
import os

import matplotlib.pyplot as plt
import networkx as nx


class Representation:
    def __init__(self):
        # self.generate_out_files([1, 2, 3, 4, 5, 6], [4, 5, 1, 2, 7, 8])
        print("Representation")

    def generate_out_files(self, iterations, values_fc):
        plt.ylabel('Wartość funkcji celu')
        plt.xlabel('Iteracja')
        plt.plot(iterations, values_fc, linewidth=2.0)
        plt.grid(True)
        plt.title("Funkcja celu")
        plt.show()

    def save_graph(self, Graph, path, testCase, test ,cost, show):
        folder_out =  testCase+"_"+str(datetime.datetime.today().strftime("%Y.%m.%d-%H.%M.%S"))
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
                               label='Miasto' + '\n' + 'DT: ' + str(
                                   format(4.4345, '.5f')) + '\n',
                               ax=axes)
        nx.draw_networkx_nodes(Graph, electricity, electricity.keys(), node_color='blue', node_size=150, node_shape='h',
                               label='Elektrownia' + '\n' + 'CAPEX: ' + str(
                                   format(cost, '.5f')) + '\n',
                               ax=axes)
        # nx.draw_networkx_edges(Graph, edges_cities, edge_color="black" )
        nx.draw_networkx_edges(Graph, edges_cities, keysC)
        nx.draw_networkx_edges(Graph, edges_electricity, keysE, edge_color="red")
        # nx.draw_networkx(Graph)
        handles, labels = axes.get_legend_handles_labels()
        legend = axes.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, -0.1))
        #legend.get_frame().set_alpha(0.5)
        plt.gca().set_aspect('equal',adjustable= 'box')
        plt.title("Najlepsze uzyskane rozwiązanie")


        if show:
            plt.show()

        print(folder_out+"/" + test)
        if not os.path.exists(path+folder_out):
            os.makedirs(path + folder_out)
#       plt.imsave(path+ folder_out+"/"+ testCase + "_" + test + '_bestIm.png', format='png')
        plt.savefig(path+ folder_out+"/"+ testCase + "_" + test + '_best.png',
                        bbox_extra_artists=(legend,), bbox_inches='tight', format='png')
        plt.close(figure)

