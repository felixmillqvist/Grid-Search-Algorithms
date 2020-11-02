from random import randint
import numpy as np

def AntSystem(locs):
    n_locs = len(locs)

    n_ants = n_locs
    alpha = 1.0
    beta = 3.0
    rho = 0.5

    nn_path, nn_path_length = GetNNPath(locs)
    tau0 = n_ants/nn_path_length

    pheromone_level = InitializePheromoneLevel(n_locs, tau0)
    visibility = GetVisibility(locs)

    min_path_length = 100000000

    max_iterations = 100

    for iteration in range(max_iterations):
        path_collection = []
        path_length_collection = []
        for ant in range(n_ants):
            path = GeneratePath(pheromone_level, visibility, alpha, beta)
            path_length = GetPathLength(path, locs)
            if path_length < min_path_length:
                min_path_length = path_length
                yield iteration, ant, path_length, path

            path_collection.append(path)
            path_length_collection.append(path_length)

        delta_pheromone_level = ComputeDeltaPheromoneLevels(path_collection,
                                                        path_length_collection)
        pheromone_level = UpdatePheromoneLevel(pheromone_level,
                                               delta_pheromone_level, rho)


def GetNNPath(locs):
    n_locs = len(locs)
    current_loc_index = randint(0, n_locs-1)

    nn_path = np.ones(n_locs, dtype=int)*-2
    nn_path[0] = current_loc_index

    for i in range(1, n_locs):
        shortest_edge = np.inf
        nn_index = -1
        current_loc = locs[current_loc_index]
        for j in range(n_locs):
            if not j in nn_path:
                tmp_loc = locs[j]
                current_edge = np.linalg.norm(np.array(current_loc) -
                                                            np.array(tmp_loc))
                if current_edge < shortest_edge:
                    shortest_edge = current_edge
                    nn_index = j

        current_loc_index = nn_index
        nn_path[i] = nn_index
    nn_path_length = GetPathLength(nn_path, locs)
    return nn_path, nn_path_length

def GetPathLength(path, locs):
    n_locs = len(locs)

    length = 0

    for i in range(n_locs):

        loc1 = locs[path[i]]
        loc2 = locs[path[(i+1)%n_locs]]
        length += np.linalg.norm(np.array(loc1) - np.array(loc2))

    return length

def InitializePheromoneLevel(n_locs, tau0):
    return tau0*np.ones((n_locs, n_locs))

def GetVisibility(locs):
    n_locs = len(locs)
    visibility = np.zeros((n_locs, n_locs))

    for i in range(n_locs):
        for j in range(n_locs):
            locs_i = locs[i]
            locs_j = locs[j]

            edge_len = np.linalg.norm(np.array(locs_i) - np.array(locs_j))

            if not edge_len == 0:
                visibility[i,j] = 1/edge_len

    return visibility

def GeneratePath(pheromone_level, visibility, alpha, beta):
    n_locs = len(pheromone_level)
    start_node = randint(0, n_locs-1)
    path = np.zeros(n_locs, dtype=int)
    tabu = [start_node]

    for i in range(n_locs-1):
        node = GetNode(tabu, pheromone_level, visibility, alpha, beta)
        path[i] = node
        tabu.append(node)
    path[n_locs-1] = start_node
    return path

def GetNode(tabu, pheromone_level, visibility, alpha, beta):
    n_locs = len(pheromone_level)
    from_node = tabu[-1]
    probability = np.zeros(n_locs)

    den_sum = 0
    for loc in range(n_locs):
        if not loc in tabu:
            den_tau_alpha = pheromone_level[loc, from_node]**alpha
            den_eta_beta = visibility[loc, from_node]**beta
            den_sum += den_tau_alpha * den_eta_beta

    for to_node in range(n_locs):
        if not to_node in tabu:
            num_tau_alpha = pheromone_level[to_node, from_node]**alpha
            num_eta_beta = visibility[to_node, from_node]**beta
            probability[to_node] = (num_tau_alpha * num_eta_beta) / den_sum

    node = np.random.choice(n_locs, 1, False, probability)
    return node


def ComputeDeltaPheromoneLevels(path_collection, path_length_collection):
    n_ants = len(path_collection)
    n_locs = len(path_collection[0])

    delta_p_l = np.zeros((n_locs, n_locs))

    for ant in range(n_ants):
        for loc_index in range(n_locs):
            pheromone = 1/path_length_collection[ant]
            #pheromone = [1/path_len for path_len in path_length_collection]
            from_node = path_collection[ant][loc_index]
            to_node = path_collection[ant][(loc_index+1)%n_locs]
            delta_p_l[from_node, to_node] += pheromone

    return delta_p_l

def UpdatePheromoneLevel(pheromone_level, delta_pheromone_level, rho):
    return (1-rho)*pheromone_level + delta_pheromone_level
