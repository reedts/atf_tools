import argparse
import re
import sys
import subprocess
import pygal
import matplotlib.pyplot as pp


def extract(atf_program):
    data = []
    # Capture stdout of atf program as list of lines
    result_lines = subprocess.run(atf_program, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
    # This is the output we're interested in   
    relevant_output = [line for line in result_lines if "evaluated" in line]
    
    for line in relevant_output:
        values = [v for v in line.split(' , ') if re.compile(r'^evaluated configs').search(v) or 'program cost' in v]
        if not values:
            continue

        if '18446744073709551615' in values[1]:
            data.append((int(values[0].split(':')[1]), None))
            continue

        data.append(tuple(map(int, [values[0].split(':')[1], values[1].split(':')[1]])))

    return data


def plot_svg(data):
    chart = pygal.Line(show_x_guides=True, truncate_label=-1, show_minor_x_labels=False)
    chart.title = 'Costs'
    chart.x_labels = map(str, [x[0] for x in data])
    chart.x_labels_major = list(map(str, [x[0] for x in data if x[0] % 20 == 0]))
    chart.add('Costs', [x[1] for x in data])

    chart.render_to_file('costs.svg')

def plot_interactive(data):
    filtered_data = [x for x in data if x[1] is not None]
    pp.plot(filtered_data)
    pp.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processes ATF results to plot.')
    parser.add_argument('file', nargs='+', type=str, help='path of a ATF binary')
    parser.add_argument('--interactive', action='store_const', const=True)
    args = parser.parse_args()

    data = extract(args.file)

    if args.interactive:
        plot_interactive(data)
    else:
        plot_svg(data)

