import pickle


def load_agent(filename):
    with open(filename, 'rb') as f:
        agent = pickle.load(f)
    return agent


def compare_q_tables(q_table1, q_table2):
    all_keys = set(q_table1.keys()).union(set(q_table2.keys()))
    differences = {}

    for key in all_keys:
        value1 = q_table1.get(key, None)
        value2 = q_table2.get(key, None)
        if value1 != value2:
            differences[key] = (value1, value2)

    return differences


agent_first = load_agent("agent_first.pkl")
agent_first_update = load_agent("agent_first_updated.pkl")

q_table_first = agent_first.q_table
q_table_first_update = agent_first_update.q_table

differences = compare_q_tables(q_table_first, q_table_first_update)

for state_action, (q1, q2) in differences.items():
    print(f"State-Action: {state_action}")
    print(f"  agent_first.pkl Q-value: {q1}")
    print(f"  agent_first_updated.pkl Q-value: {q2}")
