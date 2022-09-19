import networkx as nx


def crearGrafoDirigido(aristas):
    #Genero grafo dirigido con los datos originales del archivo
    myGrafo = nx.DiGraph()
    myGrafo.add_weighted_edges_from(aristas)

    return myGrafo


def crearGrafo(aristas):
    # Genero grafo NO dirigido para buscar el camino optimo si las calles fueran doblemano
    myGrafo = nx.Graph()
    myGrafo.add_weighted_edges_from(aristas)

    return myGrafo


def Dijkstra(miGrafo, fuente, sumidero):
    #Aplico dijkstra y busco el camino minimo y su respectivo peso.
    camino = nx.dijkstra_path(miGrafo, fuente, sumidero)
    peso = nx.path_weight(miGrafo, camino, 'weight')
    return camino, peso


def compararGrafos(grafoOG, grafoDijkstra, aristasOG):
    #Utilizando el camino de Dijkstra generado sobre el grafo NO dirigido, me fijo que aristas utilizo, y si estas no
    #existen en el grafo original, son las calles que hay que cambiar de mano.
    callesCambiadas = []
    for i in range(len(grafoDijkstra)-1):
        #Compruebo si la arista generada en el camino optimo existe en el grafo Original
        if not grafoOG.has_edge(grafoDijkstra[i], grafoDijkstra[i+1]):
            x = 1
            for j in range(len(aristasOG)):
                if aristasOG[j][0] == grafoDijkstra[i+1] and aristasOG[j][1] == grafoDijkstra[i]:
                    #Al encontrar una arista que no existe en el grafo orginal, recorro la lista de Aristas originales
                    #Busco el numero/etiqueta de esa arista(orden en la que se genero en el archivo)
                    #Agrego esa etiqueta a una lista la cual contendra todas las aristas que se les cambio la mano
                    callesCambiadas.append(int(x))
                    break
                x += 1

    callesCambiadas.sort()
    return callesCambiadas


def leerArchivo(archivo):
    with open(archivo, 'r') as f:
        fContenido = f.readlines()

    # Obtengo el vertice de inicio y llegada.
    # Spliteo la primer linea y obtengo los datos a utilizar.
    lineaDatos = fContenido[0].split()
    fuente, sumidero = lineaDatos[1], lineaDatos[2]

    aristas = []
    #Obtengo los vertices/aristas a crear
    for linea in fContenido[2:len(fContenido)]:
        # Elimino el sufijo \n de cada linea y luego creo una lista con cada valor de cada linea
        linea = linea.replace('\n', '')
        linea = linea.split(' ')

       #Creo las aristas, al crearlas se generan los vertices automaticamente.
        aristas.append([linea[0], linea[1], int(linea[2])])

    return aristas, fuente, sumidero


def escribirArchivo(peso, listaCalles):
    with open('cambioOUT.OUT', 'w') as f:
        f.write(str(peso)+'\n')
        for calle in listaCalles:
            f.write(str(calle)+' ')


def Resolver(archivo):
    aristas, fuente, sumidero = leerArchivo(archivo)
    #Creo 2 grafos, 1 dirigido(Como es originalmente) y otro Bidireccional(en el voy a buscar la ruta optima)
    miGrafoOG = crearGrafoDirigido(aristas)
    miGrafo = crearGrafo(aristas)

    #Aplico Dijkstra al grafo Bidireccional para buscar el camino minimo, y de el obtengo el camino y su peso
    miGrafoDijkstra, miGrafoDijkstraPeso = Dijkstra(miGrafo, fuente, sumidero)

    #Comparo la discrepancias de aristas entre mi grafo original y la ruta optima generada, esas discrepancias son
    #las calles que habria que aplicar el cambio de mano.
    callesCambiadas = compararGrafos(miGrafoOG, miGrafoDijkstra, aristas)

    escribirArchivo(miGrafoDijkstraPeso, callesCambiadas)
    print('Resultado en el txt:\n', miGrafoDijkstraPeso, '\n', callesCambiadas)

Resolver('cambio.IN')
#Resolver('cambio1.IN') #Caso minimo
#Resolver('cambio2.IN') #Caso Etiquieta del nodo Mayor a la cantidad de Nodos
#Resolver('fatiga.IN') #Caso Fatiga
