from dropbox import files


class Arbol:

    def __init__(self, lista_archivos):
        self.nodos = []
        self.armar_arbol(lista_archivos)

    def find_parent(self, nombre):
        parent = [n for n in self.nodos if n.nombre == nombre and n.folder][0]
        return parent

    def armar_arbol(self, l):
        n = 0
        while len(l) > 0:
            n += 1
            paths_nivel = [p for p in l if p[0].count("/") == n]
            for p_ in paths_nivel:
                l.remove(p_)
                p = p_[0].split("/")
                path = p[n]
                new_node = Nodo(path, p_[1])
                if n == 1:
                    new_node.cabeza = True
                parent = p[n - 1]
                if parent == "":
                    self.nodos.append(new_node)
                else:
                    parent_ = self.find_parent(parent)
                    self.nodos.append(new_node)
                    parent_.hijos.append(new_node)

    def get_heads(self):
        return [n for n in self.nodos if n.cabeza]


class Nodo:

    def __init__(self, nombre, metadata):
        self.nombre = nombre
        self.hijos = []
        self.cabeza = False
        self.meta = metadata
        if type(self.meta) == files.FolderMetadata:
            self.folder = True
