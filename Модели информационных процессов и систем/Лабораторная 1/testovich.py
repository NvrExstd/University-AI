#def argmax(q_values):
#    """
#    Принимает список q_values ​​и возвращает индекс элемента
#    с наибольшим значением. Разрывает связи случайным образом.
#
#    возвращает: int - индекс самого высокого значения в q_values
#    """
#    

import numpy as np

top_value = float()
ties = []
q_values = [0,0,0,0,1,0,0]

for i in range(len(q_values)):
        # Если ценность в q_values ​​больше, чем наивысшая, обновить top_value и сбросить ties в ноль
        if q_values[i] > top_value: 
            top_value = q_values[i]
            print('top value =', top_value) 
            ties.clear()
            print(ties)
        # если ценность равна top_value, добавить индекс к ties
        if q_values[i] == top_value:
            ties.append(i)
            print(ties) 
        # вернуть случайно выбранный индекс из ties.
    #return np.random.choice(ties)
