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

    def show_graph(self, Graph):
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
                                   format(4.4345, '.5f')) + '\n'
                                     + 'KT: ' + str(
                                   3414.3434) + '\n',
                               ax=axes)
        nx.draw_networkx_nodes(Graph, electricity, electricity.keys(), node_color='blue', node_size=150, node_shape='h',
                               label='Elektroenia' + '\n' + 'DT: ' + str(
                                   format(4.4345, '.5f')) + '\n'
                                     + 'KT: ' + str(
                                   3414.3434) + '\n',
                               ax=axes)
        # nx.draw_networkx_edges(Graph, edges_cities, edge_color="black" )
        nx.draw_networkx_edges(Graph, edges_cities, keysC)
        nx.draw_networkx_edges(Graph, edges_electricity, keysE, edge_color="red")
        # nx.draw_networkx(Graph)
        plt.show()

    def print_best_individual(self, individual, cities, powers, cost_traction, cost_power_lines, raport_out_dir,
                              filename, params):
        figure, axes = plt.subplots()
        g = nx.Graph()

        traction_len, powers_len = individual.traction_powers_lengths()

        cityNodes = {i: i for i in cities}
        nx.draw_networkx_nodes(g, cityNodes, cityNodes.keys(), node_color='red', node_size=75, label='Miasto' + '\n'
                                                                                                     + 'DT: ' + str(
            format(traction_len, '.5f')) + '\n'
                                                                                                     + 'KT: ' + str(
            cost_traction) + '\n',
                               ax=axes)
        powerNodes = {i: i for i in powers}
        nx.draw_networkx_nodes(g, powerNodes, powerNodes.keys(), node_color='yellow', node_size=25,
                               label='Elektrownia' + '\n'
                                     + 'DE: ' + str(format(powers_len, '.5f')) + '\n'
                                     + 'KE: ' + str(cost_power_lines) + '\n',
                               ax=axes)
        nullNodes = {(0, 0): (0, 0)}
        nx.draw_networkx_nodes(g, nullNodes, nullNodes.keys(), node_color='white', node_size=0,
                               label='FC: ' + str(individual.goal_func)
                                     + '\nKC: ' + str(1 / individual.goal_func)
                                     + '\nP: ' + str(params[0])
                                     + '\nE: ' + str(params[1])
                                     + '\nI: ' + str(params[2])
                                     + '\nM: ' + str(params[3]),
                               ax=axes)

        for seg in individual.segments:
            if seg.conn_to_powerstation is True:
                for power_seg in seg.powers_line_segment:
                    points_set = power_seg.points.copy()
                    if len(points_set) == 2:
                        point1 = points_set.pop()
                        if point1 not in cityNodes and point1 not in powerNodes:
                            pos = {point1: point1}
                            nx.draw_networkx_nodes(g, pos, pos.keys(), node_color='green', node_size=10, ax=axes)
                        point2 = points_set.pop()
                        if point2 not in cityNodes and point2 not in powerNodes:
                            pos = {point2: point2}
                            nx.draw_networkx_nodes(g, pos, pos.keys(), node_color='green', node_size=10, ax=axes)
                        pos = {point1: point1, point2: point2}
                        nx.draw_networkx_edges(g, pos, [(point1, point2)], edge_color='green', ax=axes)
            points_set = seg.points.copy()
            point1 = points_set.pop()
            point2 = points_set.pop()
            pos = {point1: point1, point2: point2}
            nx.draw_networkx_edges(g, pos, [(point1, point2)], edge_color='black', ax=axes)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Najlepszy osobnik')
        handles, labels = axes.get_legend_handles_labels()
        legend = axes.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, -0.1))
        legend.get_frame().set_alpha(0.5)
        # file_out = filename + '_' + datetime.datetime.today().strftime(self.format) + '_best.png'
        print("Generate best individual raport: \t" + file_out)
        plt.savefig(raport_out_dir + "/" + file_out,
                    bbox_extra_artists=(legend,), bbox_inches='tight')
        plt.close(figure)
