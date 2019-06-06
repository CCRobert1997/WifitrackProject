import numpy as np

def noiseProcess(sensitivity, epsilon):
    beta = sensitivity / epsilon
    u1 = np.random.random()
    u2 = np.random.random()
    if u1 <= 0.5:
        n_value = -beta * np.log(1. - u2)
    else:
        n_value = beta * np.log(u2)
   
    return n_value


def laplace(data, sensitivity, epsilon):
    for i in range(len(data)):
        data[i] += noiseProcess(sensitivity, epsilon)
    return data


if __name__ == '__main__':
    x = [1., 1., 0.]
    sensitivity = 1
    epsilon = 1
    data = laplace(x, sensitivity, epsilon)
    