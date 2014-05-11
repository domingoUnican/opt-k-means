
class Node:
    '''
    Simple implementation of a Tree
    '''
    def __init__(self, data):
        '''
        Constructor, that takes the name of the node and initialites
        the children of the node to empty
        '''
        self.data = data
        self.children = []

    def add_child(self, obj):
        '''
        Simple method to add a children
        '''
        self.children.append(obj)

    def to_string(self):
        '''
        This method output a string with the Newick format of the
        tree.
        '''
        salida = ''
        if self.children:
            salida += '('
            for child in self.children:
                salida +=  child.to_string() + ','
            salida = salida[:-1]
            salida += ')'
        salida += self.data
        return salida

    def rename(self):
        '''
        This method just rename all the nodes in the tree, where each
        node is called node_[number]. The number is given by the
        preorder of the nodes.
        '''
        n = 0
        s = 'node_'
        self.data =  s + str(n)
        n += 1
        cola = []
        cola.extend(self.children)
        while cola:
            cola_t = []
            for child in cola:
                child.data = s +str(n)
                n += 1
                cola_t.extend(child.children)
            cola = cola_t



def genera_arboles(signos):
    """
    This function generates all the tree from a set of signs
    Arguments:
    - `signos`: an iterable object that contains all possible signs
    """
    conjunto, nodo = set(range(len(signos[0]))), Node('root')
    for arbol in genera_arboles_temp(conjunto,nodo, signos):
        yield arbol
def genera_arboles_temp(conjunto, nodo, signos):
    if not conjunto:
        raise StopIteration
    elif len(conjunto) == 1:
        yield Node(str(conjunto))
    for s in signos:
        c1 = {i for i in conjunto if s[i] >0}
        c2 = conjunto - c1
        if c1 and c2:
            nodo1 = Node(str(c1))
            nodo2 = Node(str(c2))
            for arbol1 in genera_arboles_temp(c1,nodo1, signos):
                for arbol2 in genera_arboles_temp(c2,nodo2, signos):
                    nodo.children = [arbol1,arbol2]
                    yield nodo
