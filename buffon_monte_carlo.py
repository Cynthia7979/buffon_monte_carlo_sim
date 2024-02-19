# buffon monte carlo simulation
# simulation of buffon's needle to estimate the value of pi
# enhancement fork by Cynthia

# imports
import matplotlib.pyplot as plt
import numpy as np
import random as rd

def main():
    # parameters ===========================================================================================================
    # Sample size: Determines the number of needles thrown
    # Sig figs: Determines the rounding of decimals for needles that cross the lines, keep to multiples of 10
    # Width: Width of a single strip
    # Length: Length of a needle
    # Range: Length and width of the field

    sample_size = 1000
    sig_figs = 1e13
    width = 1
    length = 0.8
    assert length < width, "Needle length cannot be longer than tile width"
    board_range = width * 10

    plot_single_attempt(sample_size, sig_figs, width, length, board_range)
    plt.show()

def stupid_digits_count(num, ref):
    a = str(num)
    b = str(ref)
    in_common = 0
    while a and b:
        if a[0] == '.':
            a = a[1:]
            b = b[1:]
            continue
        if a[0] == b[0]:
            in_common += 1
            a = a[1:]
            b = b[1:]
        else:
            break
    return in_common

def generate_needle(sig_figs, width, length, board_range):
    # establish the first point and the angle
    x = rd.randrange(0, (board_range - length) * sig_figs) / sig_figs
    y = rd.randrange(0, (board_range - length) * sig_figs) / sig_figs
    theta = rd.randrange(0,360*sig_figs) / sig_figs

    # find end point
    x_end = x + length * np.sin(np.deg2rad(theta))
    y_end = y + length * np.cos(np.deg2rad(theta))

    # check if it crossed a yard line
    crossed = False
    left_yard_line = (x // width) * width
    if (x > left_yard_line and x_end < left_yard_line) or (x == left_yard_line) or (x_end == left_yard_line):
        crossed = True
    right_yard_line = ((x // width) + 1) * width
    if (x < right_yard_line and x_end > right_yard_line) or (x == right_yard_line) or (x_end == right_yard_line):
        crossed = True

    new_needle = {'x': [x, x_end], 'y': [y, y_end], 'crossed': crossed}
    return new_needle


# initializing plot ====================================================================================================
def plot_single_attempt(sample_size, sig_figs, width, length, board_range):
    fig = plt.figure(figsize=[board_range-1, board_range-1])
    fig.suptitle('Buffon\'s Needle Simulation with {} samples'.format(sample_size))
    fig.subplots_adjust(hspace=.4)
    board = fig.add_subplot(1, 1, 1)

    # Generate needles
    yard_lines = [[[i, i], [0, board_range]] for i in range(0, board_range, width)]
    for yl in yard_lines:
        board.plot(yl[0], yl[1],'0.01', linewidth=0.1)

    needles = []
    for _ in range(0, sample_size):
        needle = generate_needle(sig_figs, width, length, board_range)
        print(needle)
        needles.append(needle)

        # plot needle
        board.plot(needle['x'], needle['y'], color=('red' if needle['crossed'] else 'black'))

    # Estimate pi
    crossed_count = len(list(filter(lambda ne : ne['crossed'], needles)))
    pi_est = (2 * length * sample_size) / (width * crossed_count)
    fig.text(.01, .9, f'Estimated value of pi: {pi_est}, Actual Value of pi: {np.pi}, Digits in common: {stupid_digits_count(pi_est, np.pi)}')
    fig.text(.01, .92, f'Counted crossing needles: {crossed_count}, Diff ={pi_est - np.pi}')

if __name__ == "__main__":
    main()