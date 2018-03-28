import pandas as pd

format = pd.read_csv("D:/Programs/Python/AutoML_new/data/test/test.csv")
result = pd.read_csv("D:/Programs/Python/AutoML_new/data/result/result_final.csv",header=None)
format["Survived"] = result
format = format[["PassengerId", "Survived"]]
format.to_csv("D:/Programs/Python/AutoML_new/data/result/result_final_formatted.csv", index=None)