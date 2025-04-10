def error(target, current):
    error = []
    if len(target) != len(current):
        raise ValueError("Target and current lists must be of the same length.")
    for i in range(0,len(target)):
        error.append(current[i]- target[i])
    return error
def PID(error):
    # if len(error) < 3:
    #     return None, None, None
    P = error[-1]
    I = sum(error)
    D = error[-1]-error[-2]

    return P, I, D

target = [1, 2, 3, 4, 5]
current = [0, 1, 2, 3, 4]

error_list = error(target, current)
print(error_list)
P, I, D = PID(error_list)
print(P, I, D)


