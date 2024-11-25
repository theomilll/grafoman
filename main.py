import matplotlib.pyplot as plt
import networkx as nx


def create_graph():
    directed = input("O grafo é direcionado? (S/N): ").upper()
    directed = directed == 'S'
    weighted = input("O grafo é valorado? (S/N): ").upper()
    weighted = weighted == 'S'

    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    return G, weighted

def insert_batch_info(filename, graph, vertices):
    try:
        with open(filename, 'r') as file:
            for line in file:
                line_info = line.strip().split()
                if not line_info:
                    continue
                command = line_info[0].lower()
                if command == 'v':
                    for vertex in line_info[1:]:
                        if vertex not in vertices:
                            vertices.add(vertex)
                            graph.add_node(vertex)
                elif command == 'e':
                    if len(line_info) < 3:
                        print("Linha de aresta inválida. Uso: e vertice1 vertice2 [peso]")
                        continue
                    u = line_info[1]
                    v = line_info[2]
                    if u not in vertices or v not in vertices:
                        print(f"Vértice(s) não encontrado(s): '{u}' ou '{v}'.")
                        continue
                    if len(line_info) == 4 and 'weighted' in globals() and weighted:
                        weight = float(line_info[3])
                        graph.add_edge(u, v, weight=weight)
                    else:
                        graph.add_edge(u, v)
                else:
                    print(f"Comando desconhecido '{command}' na linha: {line.strip()}")
        print("Informações em lote do arquivo inseridas com sucesso!")
    except FileNotFoundError:
        print("Arquivo não encontrado!")

def insert_batch_items(G, weighted):
    vertices_input = input("Digite os vértices separados por espaço: ").split()
    G.add_nodes_from(vertices_input)

    edges_input = input("Digite as arestas no formato 'v1 v2 [peso]', separadas por vírgula:\n").split(',')
    for edge_str in edges_input:
        edge_info = edge_str.strip().split()
        if len(edge_info) < 2:
            print(f"Aresta inválida: {edge_str}")
            continue
        u, v = edge_info[0], edge_info[1]
        if weighted and len(edge_info) == 3:
            weight = float(edge_info[2])
            G.add_edge(u, v, weight=weight)
        else:
            G.add_edge(u, v)

def create_graph_from_file(filename):
    print("\nBem-vindo ao Criador de Grafos!")

    graph, weighted = create_graph()

    vertices = set()

    if filename:
        insert_batch_info(filename, graph, vertices)

    while True:
        print("\nOpções:")
        print("1. Adicionar vértice")
        print("2. Adicionar aresta")
        print("3. Inserir informações em lote de um arquivo")
        print("4. Inserir itens em lote manualmente")
        print("5. Visualizar grafo")
        print("6. Obter ordem e tamanho do grafo")
        print("7. Obter lista de adjacentes de um vértice")
        print("8. Obter grau de um vértice")
        print("9. Verificar se dois vértices são adjacentes")
        print("10. Encontrar o caminho mais curto entre dois vértices")
        print("11. Verificar se o grafo é Euleriano")
        print("12. Sair")

        option = input("\nEscolha uma opção: ")

        if option == '1':
            vertex = input("Insira o nome do vértice: ")
            if vertex in vertices:
                print(f"Vértice '{vertex}' já existe.")
            else:
                vertices.add(vertex)
                graph.add_node(vertex)
                print(f"Vértice '{vertex}' adicionado com sucesso!")

        elif option == '2':
            if not vertices:
                print("Não há vértices criados ainda!")
                continue

            print("Vértices disponíveis:", vertices)
            start_vertex = input("Insira o nome do vértice de partida: ")
            end_vertex = input("Insira o nome do vértice de chegada: ")

            if start_vertex not in vertices or end_vertex not in vertices:
                print("Vértice não encontrado!")
                continue

            if weighted:
                weight = input("Insira o peso da aresta: ")
                graph.add_edge(start_vertex, end_vertex, weight=float(weight))
            else:
                graph.add_edge(start_vertex, end_vertex)
            print(f"Aresta adicionada entre '{start_vertex}' e '{end_vertex}'!")

        elif option == '3':
            filename = input("Insira o nome do arquivo: ")
            insert_batch_info(filename, graph, vertices)

        elif option == '4':
            insert_batch_items(graph, weighted)
            vertices.update(graph.nodes)

        elif option == '5':
            print("Visualizando grafo...")
            print("Vértices:", list(graph.nodes))
            print("Arestas:", list(graph.edges(data=True)))
            if any('weight' in data for u, v, data in graph.edges(data=True)):
                print("Pesos das arestas:", [(u, v, data['weight']) for u, v, data in graph.edges(data=True) if 'weight' in data])
            nx.draw(graph, with_labels=True)
            plt.show()

        elif option == '6':
            print("Ordem do grafo (número de vértices):", graph.number_of_nodes())
            print("Tamanho do grafo (número de arestas):", graph.number_of_edges())

        elif option == '7':
            vertex = input("Insira o vértice para obter suas adjacências: ")
            if vertex in graph:
                if graph.is_directed():
                    print("Vértices adjacentes de entrada:", list(graph.predecessors(vertex)))
                    print("Vértices adjacentes de saída:", list(graph.successors(vertex)))
                else:
                    print("Vértices adjacentes:", list(graph.neighbors(vertex)))
            else:
                print("Vértice não encontrado!")

        elif option == '8':
            vertex = input("Insira o vértice para obter seu grau: ")
            if vertex in graph:
                if graph.is_directed():
                    print("Grau de entrada:", graph.in_degree(vertex))
                    print("Grau de saída:", graph.out_degree(vertex))
                else:
                    print("Grau:", graph.degree(vertex))
            else:
                print("Vértice não encontrado!")

        elif option == '9':
            v1 = input("Insira o primeiro vértice: ")
            v2 = input("Insira o segundo vértice: ")
            if v1 in graph and v2 in graph:
                if graph.has_edge(v1, v2) or (not graph.is_directed() and graph.has_edge(v2, v1)):
                    print(f"Os vértices '{v1}' e '{v2}' são adjacentes.")
                else:
                    print(f"Os vértices '{v1}' e '{v2}' não são adjacentes.")
            else:
                print("Um ou ambos os vértices não foram encontrados!")

        elif option == '10':
            v1 = input("Insira o vértice de origem: ")
            v2 = input("Insira o vértice de destino: ")
            if v1 in graph and v2 in graph:
                try:
                    if weighted:
                        path = nx.dijkstra_path(graph, v1, v2)
                        cost = nx.dijkstra_path_length(graph, v1, v2)
                    else:
                        path = nx.shortest_path(graph, v1, v2)
                        cost = nx.shortest_path_length(graph, v1, v2)
                    print(f"Custo do menor caminho: {cost}")
                    print(f"Menor caminho: {' -> '.join(path)}")
                except nx.NetworkXNoPath:
                    print(f"Não existe caminho entre '{v1}' e '{v2}'.")
            else:
                print("Um ou ambos os vértices não foram encontrados!")

        elif option == '11':
            if nx.is_eulerian(graph):
                print("O grafo é Euleriano.")
            else:
                print("O grafo não é Euleriano.")

        elif option == '12':
            print("Encerrando o programa...")
            break

        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    filename = input("Se desejar inserir informações iniciais de um arquivo, insira o nome do arquivo (ou pressione Enter para continuar): ")
    create_graph_from_file(filename.strip())