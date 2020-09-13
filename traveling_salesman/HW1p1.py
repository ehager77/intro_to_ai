from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
import numpy as np

loc_file = './locations.txt'
dist_file = './distances.csv'

def loadData():
    locations = []
    count = 0
    lf = open(loc_file, 'r') 
    while True: 
        count += 1
        line = lf.readline() 
        if not line: 
            break
        locations.append(line.strip())
    lf.close() 
    
    distances = pd.read_csv(dist_file, header=None)
    data = {'distances': distances, 'locations': locations}
    return data

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = loadData()['distances']
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


# def print_solution(manager, routing, solution):
#     locations = loadData()['locations']
#     print(locations)
#     """Prints solution on console."""
#     print('Objective: {} miles'.format(solution.ObjectiveValue()))
#     index = routing.Start(0)
#     plan_output = 'Route for vehicle 0:\n'
#     route_distance = 0
#     while not routing.IsEnd(index):
#         plan_output += ' {} ->'.format(manager.IndexToNode(index))
#         previous_index = index
#         index = solution.Value(routing.NextVar(index))
#         route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#     plan_output += ' {}\n'.format(manager.IndexToNode(index))
#     print(plan_output)
#     plan_output += 'Route distance: {}miles\n'.format(route_distance)

def get_routes(solution, routing, manager):
  """Get vehicle routes from a solution and store them in an array."""
  # Get vehicle routes and store them in a two dimensional array whose
  # i,j entry is the jth location visited by vehicle i along its route.
  routes = []
  for route_nbr in range(routing.vehicles()):
    index = routing.Start(route_nbr)
    route = [manager.IndexToNode(index)]
    while not routing.IsEnd(index):
      index = solution.Value(routing.NextVar(index))
      route.append(manager.IndexToNode(index))
    routes.append(route)
  return routes

def print_solution(solution, routing, manager):
    distances = loadData()['distances']
    locations = loadData()['locations']
    routes = get_routes(solution, routing, manager)
    solution = routes[0]
    solution = [locations[num] for num in solution]
    solution_str = ''
    for s in solution:
        solution_str += s + ' -> ' 
    print('Optimal Route:')
    print(solution_str[:-3])
         
def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(solution, routing, manager)


if __name__ == '__main__':
    main()