from glob import escape
import pandas as pd

def main():
    # load table
    table = pd.read_pickle('analysis_table.pkl')
    # save small table
    small_table = table[['env', 'pkg', 'robot', 'x0', 'y0', 'final_coverage', 'cov_90', 'similarity_score']]
    small_table.to_latex('detailed_table.tex', index=True, header=['Environment', 'Package', 'Robot', 'x_0', 'y_0', 'Coverage', 't @ Cov=0.9', 'ORB Score'])

if __name__ == "__main__":
    main()