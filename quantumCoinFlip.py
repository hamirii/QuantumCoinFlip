# 1. Import tools
from dwave.system import DWaveSampler, EmbeddingComposite
#from utilities import visualize_map

def load_problem(filename):
    
    ''' Returns a representation of the input graph.

    This is a tuple containing an integer, the number of nodes,
    as well as a tuple of tuples representing each pair of neighbours.
    Nodes are 0-indexed.
    
    :param filename: A text string with the file to be loaded

    :return: A tuple. The first item is the number of nodes.
        The second item is a tuple representing the binary
        relations of connected nodes.
        Each relation is a tuple with two neighbouring node indices.
    '''
    with open(filename, 'r') as f:
        content = f.readlines()
    
    n = int(content[0].rstrip())

    neighbours = tuple( tuple(int(x) for x in line.rstrip().split()) for line in content[1:] )

    return n, neighbours

filename = 'flipCoinProblem.txt'

n_vertices, neighbours = load_problem(filename)

# 2. Define problem

h = [0 for x in range(n_vertices)]
# Make sure to set coupling to -10 to force all nodes to have the same state/color/spin.
J = dict( (tuple(neighbour), -10) for neighbour in neighbours )

# 3. Instantiate solver
sampler = EmbeddingComposite(DWaveSampler(token=''))

# 4. Sample problem

solution = sampler.sample_ising(h, J, chain_strength=50, num_reads=50)

# 5. Use response

best_solution = [int(solution.first.sample[x]) for x in range(n_vertices)]

# print( best_solution )
print(best_solution)
