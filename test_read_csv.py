import csv




target_path=r"D:\work\amazon\易仓AM02-美国\US\2022-8-01_2022-8-3_1659680076.9159417_MonthlyTransaction_US.csv"
with open(target_path,  'rt', newline='', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    print(type(reader))

    result = list(reader)
    print(result[7])
    
    # for row in reader:
    #     print(row)