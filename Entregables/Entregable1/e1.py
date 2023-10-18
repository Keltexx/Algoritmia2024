import sys
from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.queues import Fifo
from algoritmia.viewers.labyrinth_viewer import LabyrinthViewer

if sys.version_info.major != 3 or sys.version_info.minor < 10:
    raise RuntimeError("This program needs Python3, version 3.10 or higher")

from typing import TextIO, Optional

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]



from random import shuffle


Vertex = tuple[int, int]


def read_data(f: TextIO) -> tuple[UndirectedGraph[Vertex], int, int]:
    values = []
    line = f.readline().split(" ")
    R,C = int(line[0]), int(line[1])
    lab = []
    edges = []
    for line in f.readlines():
        values.append(line.strip("\n"))
    for r in range(R):
        lab.append([])
        for c in range(C):
            lab[r].append(int(values[r][c]))
    for row in range(len(lab)):
        for col in range(len(lab[row])):
            # if lab[row][col] == 0:
            #     edge = ((row,col), (row,col))
            #     edges.append(edge)
            if lab[row][col] == 1:
                edge = ((row,col), (row,col+1))
                edges.append(edge)
            if lab[row][col] == 2:
                edge = ((row,col),(row+1, col))
                edges.append(edge)
            if lab[row][col] == 3:
                edge1 = ((row,col), (row,col+1))
                edge2 = ((row, col), (row + 1, col))
                edges.append(edge1)
                edges.append(edge2)
    g = UndirectedGraph(E=edges)

    return g, R, C

def traverse_bf(graph: UndirectedGraph[Vertex], v_initial: Vertex) -> list[Edge]:
    queue: Fifo[Edge] = Fifo() # Cola de aristas
    seen: set[Vertex] = set() # Conjunto de vértices vistos
    queue.push((v_initial, v_initial)) # Añadimos la arista fantasma inicial
    seen.add(v_initial)
    res = []
    cont = 0
    while len(queue) > 0:
        cont+=1
        u, v = queue.pop()
        res.append((u, v)) # Añadimos una arista
        sucesores = orden_suc(graph.succs(v),v)
        for suc in sucesores:
            if suc not in seen:
                queue.push((v, suc))
                seen.add(suc)
    return res

def orden_suc(succs: set[Vertex], v: Vertex) -> list[Vertex]:
    orden = []

    if (v[0] -1, v[1]) in succs:
        orden.append((v[0] -1, v[1]))
    if (v[0], v[1]-1) in succs:
        orden.append((v[0], v[1]-1))
    if(v[0], v[1] + 1) in succs:
        orden.append((v[0], v[1] + 1))
    if(v[0]+1, v[1]) in succs:
        orden.append((v[0]+1, v[1]))

    return orden


def bf_search(g: UndirectedGraph[Vertex], source: Vertex, target: Vertex) -> list[Edge]:
    res: list[Edge] = []
    queue = Fifo()
    seen: set[Vertex] = set()
    queue.push((source,source))
    seen.add(source)
    while len(queue) > 0:
        u, v = queue.pop()
        res.append((u, v))
        if v == target:
            return res
        for suc in g.succs(v):
            if suc not in seen:
                seen.add(suc)
                queue.push((v, suc))
    return res

def path_recover(edges: list[Edge], target: Vertex) -> list[Vertex]:
    #Construir bp (Diccionario de punteros hacia atras) Al hablar de vertices, hablamos del padre
    bp: dict[Vertex, Vertex] = {}
    for u, v in edges:
        bp[v] = u

    #Recuperarel camino desde target (while)
    v = target
    path: list[Vertex] = [v]
    while bp[v] != v:
        v = bp[v]
        path.append(v)

    #Reverse del camino
    path.reverse()

    #Devolver el camino
    return path

def shortest_path(g,source, target) -> list[Vertex]:
    edges: list[Edge] = bf_search(g, source, target) #Aristas utilizadas en recorrido en anchura
    path = path_recover(edges, target) #Recupera el camino mas corto
    return path #Grafo inicial y el camino final

def process(ug: UndirectedGraph[Vertex], rows: int, cols: int) -> int:
    contador = 0
    res = traverse_bf(ug,(0,0))
    orden = [v for (u, v) in res]
    orden.reverse()
    while len(orden)>1:
        source = orden.pop()
        target = orden[-1]
        cont = len(shortest_path(ug,source,target))-1
        contador+= cont

    return contador

def show_results(steps: int):
    print(steps)


if __name__ == "__main__":
    ug0, rows0, cols0 = read_data(sys.stdin)
    steps0 = process(ug0, rows0, cols0)
    show_results(steps0)