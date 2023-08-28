import gc
from tkinter import Frame, Tk, TOP, Button, Label, Entry, LEFT, RIGHT, BOTTOM

import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class KruskalApp:
    def __init__(self, root):
        self.window = root

        self.window.title("Kruskal Algorithm")
        self.window.geometry('500x600')
        self.window.resizable(False, False)

        self.frame_graph = Frame(root)
        self.frame_edges = Frame(root)
        self.graph = nx.Graph()
        self.cid = None

        # Add edge frame
        self.label_vertex_1 = Label(self.frame_edges, text='Vertex 1:', font=('Arial Bold', 12))
        self.label_vertex_1.grid(row=1, padx=40, sticky='w')
        self.label_vertex_2 = Label(self.frame_edges, text='Vertex 2:', font=('Arial Bold', 12))
        self.label_vertex_2.grid(row=2, padx=40, sticky='w')
        self.label_weight = Label(self.frame_edges, text='Weight:', font=('Arial Bold', 12))
        self.label_weight.grid(row=3, padx=40, sticky='w')

        self.entry_vertex_1 = Entry(self.frame_edges, width=10)
        self.entry_vertex_1.grid(row=1, padx=120, sticky='w')
        self.entry_vertex_2 = Entry(self.frame_edges, width=10)
        self.entry_vertex_2.grid(row=2, padx=120, sticky='w')
        self.entry_add_weight = Entry(self.frame_edges, width=10)
        self.entry_add_weight.grid(row=3, padx=120, sticky='w')

        self.button_add_edge = Button(self.frame_edges, text='Add Edge', command=self.add_edge)
        self.button_add_edge.grid(column=0, row=4, padx=40, pady=0, sticky='w')

        self.button_del_edge = Button(self.frame_edges, text='Delete Edge', command=self.del_edge)
        self.button_del_edge.grid(column=0, row=4, padx=120, pady=0, sticky='w')

        self.button_run_kruskal = Button(self.frame_edges, text='Run Kruskal', command=self.run_kruskal, width=12)
        self.button_run_kruskal.grid(column=1, row=1, padx=0, pady=0, sticky='w')

        self.button_return_graph = Button(self.frame_edges, text='Return base graph', command=self.return_base_graph,
                                          width=14)
        self.button_return_graph.grid(column=1, row=2, padx=0, pady=0, sticky='w')

        self.button_clear_frame = Button(self.frame_edges, text='Clear', command=self.clear_frame, width=12)
        self.button_clear_frame.grid(column=1, row=3, padx=0, pady=0, sticky='w')

        self.draw_graph()
        self.frame_graph.pack(side=TOP)
        self.frame_edges.pack(side=LEFT)

    def clear_frame(self):
        self.graph = nx.Graph()
        self.draw_graph()

    def return_base_graph(self):
        self.draw_graph()

    def show_graph_fullscreen(self, event):
        new_window = Tk()
        new_window.title("Graph")
        new_window.resizable(False, False)

        figure = plt.gcf()
        figure.set_size_inches(12, 10)
        canvas = FigureCanvasTkAgg(figure, new_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        canvas.mpl_disconnect(self.cid)

        def return_connection():
            self.cid = canvas.mpl_connect("button_press_event", self.show_graph_fullscreen)
            new_window.destroy()

        new_window.protocol("WM_DELETE_WINDOW", return_connection)

    def add_edge(self):
        u = self.entry_vertex_1.get()
        v = self.entry_vertex_2.get()
        w = int(self.entry_add_weight.get())
        self.graph.add_edge(u, v, weight=w)
        self.draw_graph()

    def del_edge(self):
        u = self.entry_vertex_1.get()
        v = self.entry_vertex_2.get()
        self.graph.remove_edge(u, v)
        self.graph.remove_nodes_from(list(nx.isolates(self.graph)))
        self.draw_graph()

    @staticmethod
    def clear_canvas():
        objects = gc.get_objects()
        canvas_list = [obj for obj in objects if isinstance(obj, FigureCanvasTkAgg)]
        for canvas in canvas_list:
            canvas.get_tk_widget().destroy()

    def draw_graph(self, graph=None, node_color=None):
        self.clear_canvas()
        plt.clf()
        if graph is None:
            graph = self.graph
        pos = nx.spring_layout(graph, seed=7)

        # nodes
        nx.draw_networkx_nodes(graph, pos, node_size=500, node_color=node_color)

        # edges
        nx.draw_networkx_edges(graph, pos, width=3)
        nx.draw_networkx_edges(graph, pos, style="dashed")

        nx.draw_networkx_labels(graph, pos, font_size=20, font_family="sans-serif")

        edge_labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels)

        figure = plt.gcf()
        figure.set_size_inches(5, 4)
        canvas = FigureCanvasTkAgg(figure, self.frame_graph)
        canvas.get_tk_widget().grid(column=0, row=0)
        self.cid = canvas.mpl_connect("button_press_event", self.show_graph_fullscreen)

    def run_kruskal(self):
        kruskal_graph = nx.Graph()

        R = [(e[2], e[0], e[1]) for e in self.graph.edges.data('weight')]
        # [(13, 1, 2), (18, 1, 3), (17, 1, 4), (14, 1, 5), (22, 1, 6),
        # (26, 2, 3), (22, 2, 5), (3, 3, 4), (19, 4, 6)]

        Rs = sorted(R, key=lambda x: x[0])
        U = set()
        D = {}
        node_colors = ['blue', 'red', 'green', 'purple', 'orange', 'black', 'yellow', 'gray', 'brown', 'pink', 'olive',
                       'cyan',
                       'magenta', 'maroon', 'navy', 'lime', 'teal', 'indigo', 'violet', 'silver']
        k = 0
        for r in Rs:
            if r[1] not in U or r[2] not in U:
                if r[1] not in U and r[2] not in U:
                    D[r[1]] = [r[1], r[2], node_colors[k]]
                    D[r[2]] = D[r[1]]
                    k += 1
                else:
                    if not D.get(r[1]):
                        D[r[2]].append(r[1])
                        D[r[1]] = D[r[2]]
                    else:
                        D[r[1]].append(r[2])
                        D[r[2]] = D[r[1]]

                kruskal_graph.add_edge(r[1], r[2], weight=r[0])
                U.add(r[1])
                U.add(r[2])
        node_color = [v[2] for v in D.values()]

        for r in Rs:
            if r[2] not in D[r[1]]:
                kruskal_graph.add_edge(r[1], r[2], weight=r[0])
                gr1 = D[r[1]]
                D[r[1]] += D[r[2]]
                D[r[2]] += gr1
        self.draw_graph(kruskal_graph, node_color=node_color)


if __name__ == '__main__':
    window = Tk()
    app = KruskalApp(window)
    window.mainloop()
