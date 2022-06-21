import random
from collections import OrderedDict, namedtuple

def main():
    random.seed(0)

    FloatRange=namedtuple('FloatRange',['min','max'])

    num_range=FloatRange(0.0,10000.0)

    coldict=OrderedDict()
    coldict={
        '数値': num_range
    }
    make_random_csv(coldict,filename='input.csv',num_rows=1000)

def make_random_csv_row(coldict):
    # ランダムなCSVデータの1行分を生成
    row=''
    for col, elems in coldict.items():
        row += f'{random.uniform(elems.min,elems.max)}'

    row=row.rstrip(',')

    return row

def make_random_csv(coldict,filename,num_rows=1000):
    # 指定した行数のランダムなCSVデータを生成
    output=[]
            # NameError: name 'join' is not defined
    output.append(','.join(coldict.keys()))
    for i in range(num_rows):
        output.append(make_random_csv_row(coldict))
    with open(filename, mode='w')as f:
        output='\n'.join(output)
        f.writelines(output)

if __name__ == "__main__":
    main()
