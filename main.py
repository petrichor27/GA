# задача нахождения макс потока в графе
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib import rcParams
import matplotlib.pyplot as plt
import networkx as nx
import sys

from ga_darwin import GADarwin
from generate_graph import generate_random_digraph
from form import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.n = None
        self.canvas = None
        self.fig = None
        self.graph_edges = None
        self.nx_graph = None
        self.gridlayout = None
        self.base_parameters_for_form()

    def base_parameters_for_form(self):
        self.setupUi(self)
        rcParams['font.family'] = 'Segoe Print'
        rcParams['font.size'] = 11
        self.pushButton_graph.clicked.connect(self.buttonGraph_clicked)
        self.pushButton_start.clicked.connect(self.buttonStart_clicked)
        self.fig = plt.figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        llayout = QVBoxLayout(self.groupBox_graph)
        llayout.addWidget(self.canvas, 88)
        methods = ['Выбрать', 'Эволюция Дарвина', 'Эволюция Гюго де Фриза', 'Искусственная иммунная сеть']
        self.comboBox_algorithm.clear()
        self.comboBox_algorithm.addItems(methods)
        # self.comboBox_algorithm.activated.connect(self.comboBox_activated)

    def draw_graph(self):
        self.fig = plt.cla()
        self.nx_graph = nx.DiGraph(directed=True)
        self.nx_graph.add_nodes_from([v for v in range(1,self.n-1)])
        self.nx_graph.add_node(0, color='red', style='filled', fillcolor='red')
        self.nx_graph.add_node(self.n - 1, color='red', style='filled', fillcolor='red')
        colored_dict = nx.get_node_attributes(self.nx_graph, 'color')
        default_color = 'blue'
        color_seq = [colored_dict.get(node, default_color) for node in self.nx_graph.nodes()]
        for i, j, w in self.graph_edges:
            self.nx_graph.add_edge(i, j, weight=w)
        try:
            pos = nx.circular_layout(self.nx_graph)
            nx.draw(self.nx_graph, pos, with_labels=True, node_color=color_seq)
            nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels={(i, j): self.nx_graph[i][j]['weight'] for i, j in self.nx_graph.edges()})
        except nx.NetworkXError as e:
            self.fig = plt.cla()
            print(f'draw_graph error: {e}')
        self.fig = plt.figure(1, figsize=(3, 3))
        self.canvas.draw()

    def buttonStart_clicked(self):
        self.plainTextEdit_result.clear()
        if not nx.has_path(self.nx_graph, 0, self.n - 1):
            self.plainTextEdit_result.insertPlainText(f"Нет пути из вершины 0 в вершину {self.n - 1}")
            return
        max_flow_value, max_flow_dict = nx.maximum_flow(self.nx_graph, 0, self.n - 1, capacity='weight')

        result_max_flow, result_path = 0, []
        index = self.comboBox_algorithm.currentIndex()
        start_time = time.time()
        if index == 1 or index == 2:
            method = GADarwin(
                nx_graph=self.nx_graph,
                graph_size=self.n,
                population_size=int(self.textEdit_population_size.toPlainText()),
                iterations=int(self.textEdit_iterations.toPlainText()),
                mutation_probability=float(self.textEdit_mutation_probability.toPlainText()),
                do_catastrophe=True if index == 2 else False
            )
            result_max_flow, result_path = method.genetic_algorithm()

        elif index == 3:
            pass

        work_time = time.time() - start_time
        self.plainTextEdit_result.insertPlainText(
            f'Точное значение максимального потока: {max_flow_value}\nЗначение максимального потока для ГА: {result_max_flow}\nПуть: {result_path}\nВремя работы алгоритма: {round(work_time, 3)}мс'
        )

    def buttonGraph_clicked(self):
        try:
            self.n = int(self.textEdit_n.toPlainText())
            self.graph_edges = generate_random_digraph(self.n)
            self.draw_graph()
        except Exception as e:
            print(f'buttonGraph_clicked error: {e}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
