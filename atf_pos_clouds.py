import sys
import subprocess
import matplotlib.pyplot as pp


def extract(atf_program):
    data = []

    result_lines = subprocess.run(atf_program, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

    relevant_output = []

if __name__ == "__main__":
    extract(sys.argv[1])
