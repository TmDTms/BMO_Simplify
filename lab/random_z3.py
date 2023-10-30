import pandas as pd
import random

df = pd.read_excel("../example/samples/handler_code.xlsx")
handle = df.groupby(df.columns[0])
result = []
for name, group in handle:
    if name == '짝':
        df = group.loc[:, 'Unnamed: 2':'Unnamed: 70']
        lst = df.values.tolist()
        lst2 = sum(lst, [])
        for i in range(450):
            choice = random.choice(lst2)
            if choice != 'nan' and choice not in result:
                result.append(choice)
print(result)
with open('random_z3.txt', 'w') as f:
    for z3 in result:
        f.write(str(z3) + '\n')