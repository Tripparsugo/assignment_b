# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = {"Name": ["A", "B", "C"], "TC": [1, 2, 3], "TCBD": [1, 1, 3]}
    df = pd.DataFrame(data=data)


    def evaluate(d: pd.DataFrame):
        points = sum(d.apply(lambda r: 1 if r["TCBD"] > 1 else 0.5 if r["TC"] > 1 else 0, axis=1))
        return points


    bonus_df = df.groupby(["Name"]).apply(evaluate)

    a = 1

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
