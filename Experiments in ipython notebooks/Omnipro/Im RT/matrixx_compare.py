import datetime
import getopt
import sys

import matplotlib.pyplot as plt
import numpy as np


class OpgData(object):
    def __init__(self, opg_path):
        self.opg_path = opg_path
        self.x_cm, self.y_cm, self.pixel_data = self.parse_data()

    def parse_data(self):
        with open(self.opg_path, "r") as ins:
            all_data = []
            for line in ins:
                if r'<asciibody>' in line:
                    break
            for line in ins:
                if '</asciibody>' in line:
                    break
                all_data.append(line)
        x_cm = [float(x) for x in all_data[2].split('\t')[1:-1]]
        y_cm = [float(x.split('\t')[0]) for x in all_data[4:-1]]
        pixel_data = [[float(x) for x in y.split('\t')[1:-1]] for y in all_data[4:]]
        return x_cm, y_cm, pixel_data

    def plot_data(self):
        plt.figure()
        plt.scatter(self.x_cm, self.pixel_data[round(len(self.pixel_data) / 2)])
        plt.title('Matrixx plot - x', fontsize=40)
        plt.xlabel("x position (cm)", fontsize=40)
        plt.ylabel("Relative dose", fontsize=40)
        plt.tick_params(axis='both', which='major', labelsize=30)
        plt.grid()
        plt.show()


def make_save_plot(baseline,measurement,dimension):

    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    time_stamp_dir = time_stamp
    time_stamp_dir = time_stamp_dir.replace(' ', '_')
    time_stamp_dir = time_stamp_dir.replace(':', '')

    if dimension == 'x':
        baseline_norm = normalise_plot(baseline.pixel_data[round(len(baseline.pixel_data[0]) / 2)])
        baseline_horz = baseline.x_cm
        measurement_norm = normalise_plot(measurement.pixel_data[round(len(measurement.pixel_data[0]) / 2)])
        measurement_horz = measurement.x_cm
        fig_title = "Matrixx measurement vs. baseline - x"
        fig_output_dir = r'output\\' + time_stamp_dir + '_x.png'

    elif dimension == 'y':
        baseline_norm = normalise_plot([x[round(len(baseline.pixel_data[0]) / 2)] for x in baseline.pixel_data[:-1]])
        baseline_horz = baseline.y_cm
        measurement_norm = normalise_plot([x[round(len(measurement.pixel_data[0]) / 2)] for x in measurement.pixel_data[:-1]])
        measurement_horz = measurement.y_cm
        fig_title = "Matrixx measurement vs. baseline - y"
        fig_output_dir = r'output\\' + time_stamp_dir + '_y.png'

    percentage_diff = [100 * ((x / y) - 1) for x, y in zip(baseline_norm, measurement_norm)]

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(baseline_horz, baseline_norm, '-r')
    ax1.plot(measurement_horz, measurement_norm, '-b')
    ax2.plot(baseline_horz, percentage_diff, '--k')
    ax2.plot(baseline_horz, [-2] * len(baseline_horz), '-g')
    ax2.plot(baseline_horz, [2] * len(baseline_horz), '-g')

    ax1.set_title(fig_title, fontsize=40)
    ax1.set_xlabel("Position (cm)", fontsize=40)
    ax1.set_ylabel("Pixel value (%)", fontsize=40)
    ax2.set_ylabel('Percentage diff (%)', fontsize=40, rotation=270, va='bottom')
    ax1.tick_params(labelsize=30)
    ax2.tick_params(labelsize=30)
    ax2.set_yticks(np.arange(-20, 21, 4))
    ax2.set_yticks(np.arange(-20, 21, 2), minor=True)
    ax1.set_xticks(np.arange(-12, 12, 2))
    ax1.set_xticks(np.arange(-12, 12, 1), minor=True)
    ax1.set_yticks(np.arange(0, 35, 1), minor=True)
    ax1.set_yticks(np.arange(0, 101, 20))
    ax1.set_yticks(np.arange(0, 101, 10), minor=True)
    ax1.legend(['Baseline', 'Measurement'], loc='lower center', ncol=1, fontsize=30)
    ax2.grid(which='minor', alpha=0.2)
    ax2.grid(which='major', alpha=0.5)
    ax1.grid(which='minor', alpha=0.3)
    ax1.grid(which='major', alpha=0.6)
    ax1.set_ylim([0, 105])
    ax2.set_ylim([-12, 12])
    fig.set_size_inches(20, 10)
    plt.savefig(fig_output_dir)
    print("Figures saved to: %s" % fig_output_dir)
    return percentage_diff


def normalise_plot(input_data):
    return [100 * (float(i) / max(input_data)) for i in input_data]


def compare_opg_data(baseline, measurement):
    percentage_diff_x = make_save_plot(baseline, measurement, dimension='x')
    percentage_diff_y = make_save_plot(baseline, measurement, dimension='y')

    percentage_diff_x_np = np.array(percentage_diff_x)
    percentage_diff_y_np = np.array(percentage_diff_y)

    percentage_diff_x_mean = np.around(np.mean(percentage_diff_x_np), decimals=3)
    percentage_diff_y_mean = np.around(np.mean(percentage_diff_y_np), decimals=3)

    print("Percentage x error = %.2f %%"%percentage_diff_x_mean)
    print("Percentage y error = %.2f %%"%percentage_diff_y_mean)

    # percDiff_median = np.around(np.median(percDiff_np_nonan),decimals = 3)
    # percDiff_range = np.around(np.ptp(percDiff_np_nonan, axis=0),decimals = 3)
    # percDiff_max = np.around(np.max(percDiff_np_nonan),decimals = 3)

    return None


def main(argv):

    baseline_file = ''
    measurement_file = ''
    try:
        opts, args = getopt.getopt(argv, "hb:m:", ["bfile=", "mfile="])
    except getopt.GetoptError:
        print('matrixx_compare.py -b <baselinefile> -m <measurementfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('matrixx_compare.py -b <baselinefile> -m <measurementfile>')
            sys.exit()
        elif opt in ("-b", "--bfile"):
            baseline_file = arg
        elif opt in ("-m", "--mfile"):
            measurement_file = arg

    base_opg = OpgData(opg_path=baseline_file)
    meas_opg = OpgData(opg_path=measurement_file)
    compare_opg_data(base_opg, meas_opg)


if __name__ == "__main__":
    main(sys.argv[1:])
