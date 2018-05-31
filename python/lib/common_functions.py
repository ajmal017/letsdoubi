import sys

# Print out things without changing line
def print_no_newline(str):
    sys.stdout.write(str)
    sys.stdout.flush()