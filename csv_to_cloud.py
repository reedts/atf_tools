import sys
import pygal


def process():
    values = {}
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        key = 1
        values[str(key)] = []
        for line in lines:
            print("doing line: {}".format(line))
            if line is '\n':
                key += 1
                values[str(key)] = []
                continue

            values[str(key)].append(tuple(map(float, line.split(','))))
    
    chart = pygal.XY(stroke=False)
    
    for key, values in values.items():
        chart.add(key, values)

    chart.render_to_file('chart.svg')

if __name__ == "__main__":
    process()
