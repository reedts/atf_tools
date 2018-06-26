import sys
import subprocess
import matplotlib.pyplot as pp
from sklearn.decomposition import PCA

def run(atf_program):
    result_lines = subprocess.run(atf_program, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
    
    return result_lines


def extract(result_lines):
    relevant_output = []
    
    # find all indices where the 'BEGIN_COORD_DATA' and 'END_COORD_DATA' is
    beginnings = [i + 1 for i, line in enumerate(result_lines) if 'BEGIN_COORD_DATA' in line]
    endings = [i for i, line in enumerate(result_lines) if 'END_COORD_DATA' in line]

    for begin, end in zip(beginnings, endings):
        relevant_output.append(result_lines[begin:end])

    return relevant_output


def plot(data):
    plots = []
    for iteration in data:
        points = [tuple(map(float, p.split(','))) for p in iteration]
        pca = PCA(n_components=2)
        pca.fit(points)
        transformed_points = pca.transform(points)
        plot = pp.scatter(transformed_points[:,0], transformed_points[:,1])
        plots.append(plot)
    
    pp.legend(plots, map(str, range(len(data))), loc='upper right')


if __name__ == "__main__":
    data = extract(sys.argv[1])
    plot(data)
    pp.show()
