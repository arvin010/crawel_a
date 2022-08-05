import csv

target_path=r"D:\work\amazon\易仓AM02-美国\US\2022-8-01_2022-8-3_1659680076.9159417_MonthlyTransaction_US.csv"

with open(target_path,'rt', newline='', encoding='utf-8', errors='ignore') as f:
    lines = open(target_path,encoding='utf-8', errors='ignore').readlines()
    open(target_path.replace("-","_"),'w', newline='', encoding='utf-8', errors='ignore').writelines(lines[6:])


with open(target_path,  'rt', newline='', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    print(type(reader))

    result = list(reader)
    print(result[7])

    for row in reader:
        print(row[0])




import pandas as pd
from io import StringIO
# data = pd.read_csv(target_path)
# print (data)

df = pd.read_csv(target_path, sep='\t',index_col=False,header=None)

print(type(df))
print(df)
row7=df.iloc[7:8]
print(row7.values.tolist()[0][0])
# df_new=df.iloc[7:]
# df_new=df_new.reset_index(drop=True)  # 重置index
# print(1111111111111,list(row7))
# df_new.columns = list(row7)
# # df.rename(index=str.lower, columns=str.upper)
# print(df_new)
# print (data.head())

# print("*"*100)
# print(row7)



df = pd.DataFrame(data= [[1, 2, 3],[4, 5, 6], [7, 8, 9]], index=['e', 'f', 'g'], columns=['a','b','c'])
print(df.iloc[1:2,:])


data = ('a,b,c\n1,Yes,2\n3,No,4')
d=pd.read_csv(StringIO(data),
            true_values=['Yes'], false_values=['No'])
print(d)