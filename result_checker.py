import argparse 
import re


def main(fileName):
    with open(fileName, "r") as file:
        for line in file.readlines():
            if 'mapped' in line:
                values = re.findall(r'\d+\.\d+', line)
                if len(values) == 1:
                    value = float(values[0])
                    print(f'Result value: {value}')
                    if value > 90:
                        print('OK')
                    else:
                        print('Not ok')
                return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='path to report')
    args = parser.parse_args()
    main(args.filepath)
