import numpy as np
def tv_distance(p, q):
    return 0.5 * np.sum(np.abs(p - q))