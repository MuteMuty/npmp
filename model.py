import numpy as np 

def solve_model(T,state):
    X1, X2, Y, W = state
    dX1 = -X1*0
    dX2 = -X2*0
    dY = -Y*0.1+10*(((X1/5)**2))/(1+((X1/5)**2)+((X2/5)**3)+((X1/5)**2)*((X2/5)**3))
    dW = -W*0.3
    return np.array([dX1, dX2, dY, dW])

def solve_model_steady(state):
    return solve_model(0, state)
