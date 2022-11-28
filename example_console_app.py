"""This is to serve as an example of a console app that
sends a variable number of lines with no delimiter to show
how it would be useful to have a non-hanging readline()
"""
import random

if __name__ == '__main__':
    while True:
        msg = input('Enter test command:')
        print('\n')
        for _ in range(random.randint(3, 6)):
            print('<Random buffer>')
        print('Line of interest: ' + msg[::-1])
        for _ in range(random.randint(2, 5)):
            print('<Random buffer>')