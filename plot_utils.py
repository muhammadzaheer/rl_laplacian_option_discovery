import numpy as np
import matplotlib.pyplot as plt


def plot_pi(pi, max_row, max_col):

    # Here we modify Terminate (0,0) to indicate termination with a dot
    # Note these actions denotes direction of (x,y) and not (row,col)
    # Right, Left, Down, Up, Terminate
    action_set = [(1,0), (-1,0), (0,-1), (0,1), (0, 0)]
    vector_pi = [action_set[i] for i in pi]
   
    # Create grid
    Col, Row = np.meshgrid(range(0,max_col,1), range(0,max_row,1))

    # U: x-component of vector
    # V: y-component of vector
    U = []
    V = []

    for action in vector_pi:
        U.append(action[0]*0.1)
        V.append(action[1]*0.1)

    Q = plt.quiver(Col, Row, U, V, pivot='mid', units='xy')

    plt.xticks(range(max_col))
    plt.yticks(range(max_row))
    plt.gca().invert_yaxis() # enable row,col indexing
    plt.show()
