import os

import pandas as pd

from benchmark import analyse

def main():
    table = pd.DataFrame(columns=['bag_file', 'env', 'pkg', 'robot', 'x0', 'y0'])
    # get .rosbag files in cwd
    files = [f for f in os.listdir('.') if f.endswith('.bag')]
    # analyse tests
    for rosbag_file in files:
        row = analyse(rosbag_file)
        table = table.append(row, ignore_index=True)
    # save table
    table.apply(pd.to_numeric, errors='ignore')
    table.to_pickle('analysis_table.pkl')


if __name__ == "__main__":
    main()