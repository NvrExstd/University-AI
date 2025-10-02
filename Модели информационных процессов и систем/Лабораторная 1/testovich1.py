import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

from rl_glue import RLGlue
import main_agent
import ten_arm_env
import test_env


def argmax(q_values):
    """
    Принимает список q_values ​​и возвращает индекс элемента
    с наибольшим значением. Разрывает связи случайным образом.

    возвращает: int - индекс самого высокого значения в q_values
    """
    top_value = int()
    ties = []

    for i in range(len(q_values)):
        # Если ценность в q_values ​​больше, чем наивысшая, обновить top_value и сбросить ties в ноль
        if q_values[i] > top_value: 
            top_value = q_values[i] 
            ties.clear()
        # если ценность равна top_value, добавить индекс к ties
        if q_values[i] == top_value:
            ties.append(i) 
        # вернуть случайно выбранный индекс из ties.
    return np.random.choice(ties)

reward = float(1)
q_values = [0, 0, 0.5, 0, 0] # Массив, содержащий, по мнению агента, все ценности действий (рук). \\ Массив из 10 значений
arm_count = [0, 1, 0, 0, 0] # Массив со счетчиком количества опускания каждой руки \\ Массив из 10 значений
last_action = int(1) # Действие, которое агент совершил на предыдущем временном шаге. \\ Индекс действия 
#######################
q_values_next = int()

q_values_next = q_values[last_action] + ((1 / (arm_count[last_action]+1)) * (reward - q_values[last_action]))
arm_count[last_action] += 1
q_values[last_action] = q_values_next
current_action = argmax(q_values)
last_action = current_action

print(q_values)
#for i in range(len(q_values)): # Update Q values Обновление значения Q
#    print('staroe',q_values)
#    print('staroe',arm_count)
#    q_values_next = q_values[i] + ((1 / (arm_count[i]+1)) * (reward - q_values[i])) # Подсказка: посмотрите алгоритм в разделе "Инкрементная реализация" лекции "Многорукий бандит"
#    arm_count[i] += 1 # увеличить счетчик в self.arm_count для действия с предыдущего шага времени
#     # обновление размера шага с использованием self.arm_count
#    q_values[i] = q_values_next # обновление self.q_values для действия с предыдущего шага времени
#    # ВАШ КОД ЗДЕСЬ
#    print(q_values)
#    print(arm_count)

#current_action = argmax(q_values) # текущее действие = ? # Используйте функцию argmax которую вы создали ранее
## ВАШ КОД ЗДЕСЬ
#last_action = current_action
#print(last_action)