import argparse
import re
import sys
import subprocess


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processes ATF results to plot.')
    parser.add_argument('file', nargs='+', type=str, help='path of a ATF binary')
    args = parser.parse_args()

    data = extract(args.file)
    
    with open('costs.csv', 'w+') as f:
        for t in data:
            f.write(str(t[0]) + ',' + str(t[1]) + '\n')
