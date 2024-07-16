import pickle
from q_learning_agent import QLearningAgent

# Загрузка объекта из файла
with open("agent_first.pkl", "rb") as f:
    loaded_object = pickle.load(f)

print(type(loaded_object))

if isinstance(loaded_object, QLearningAgent):

    print(len(loaded_object.q_table))
    print("Q-таблица агента:")
    print(loaded_object.q_table)

