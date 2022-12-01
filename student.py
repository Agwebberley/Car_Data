# For every file in the directory, check if the output is the same as the expected output.
# print the name of the file and the result.

import os
import subprocess

# Get the list of files in the directory.
files = os.listdir()

# Remove current file from the list.
files.remove('student.py')

EXPECTED_OUTPUT = """
******************************
Printing main() source code:
******************************
def main():
    print("*" * 30 + "\nPrinting main() source code:\n" + "*" * 30)
    import inspect
    print(str(inspect.getsource(main)))
    print("*" * 30 + "\nPrinting main() source output:\n" + "*" * 30)
    f1 = Fraction(1, 2)
    f2 = Fraction(-7, 3)
    f3 = Fraction(-1, 4)
    f4 = Fraction(21, 5)
    f5 = f1 + f2 + f3 + f4

    print("f1: " + str(f1))
    print("f2: " + str(f2))
    print("f3: " + str(f3))
    print("f4: " + str(f4))
    print("f5: " + str(f5))
    print("isinstance(f5, Fraction): " + str(isinstance(f5, Fraction)))
    print("isinstance(f5, MixedFraction): " + str(isinstance(f5, MixedFraction)))

    m1 = MixedFraction(f1)
    m2 = MixedFraction(f2)
    m3 = MixedFraction(f3)
    m4 = MixedFraction(f4)
    m5 = m1 + m2 + m3 + m4

    print("m1: " + str(m1))
    print("m2: " + str(m2))
    print("m3: " + str(m3))
    print("m4: " + str(m4))
    print("m5: " + str(m5))
    print("isinstance(m5, Fraction): " + str(isinstance(m5, Fraction)))
    print("isinstance(m5, MixedFraction): " + str(isinstance(m5, MixedFraction)))

    print("(f5==m5) : " + str(f5==m5))

******************************
Printing main() source output:
******************************
f1: 1/2
f2: -7/3
f3: -1/4
f4: 21/5
f5: 127/60
isinstance(f5, Fraction): True
isinstance(f5, MixedFraction): False
m1: 0_(1/2)
m2: -2_(1/3)
m3: -0_(1/4)
m4: 4_(1/5)
m5: 2_(7/60)
isinstance(m5, Fraction): True
isinstance(m5, MixedFraction): True
(f5==m5) : True
"""

# For every file in the directory, check if the output is the same as the expected output.
# print the name of the file and the result.
for file in files:
    # If the file is a python file, run it.
    if file[-3:] == '.py':
        # Run the file.
        output = subprocess.run(['python', file], stdout=subprocess.PIPE)
        # Get the output
        output = output.stdout.decode('utf-8')
        # Check if the output is the same as the expected output.
        if output == EXPECTED_OUTPUT:
            print(file, 'passed')
        else:
            print(file, 'failed')

