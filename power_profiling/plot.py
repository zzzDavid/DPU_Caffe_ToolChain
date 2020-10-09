import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams


rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['DejaVu Serif']
names = ['timestamp', 'VCCINT', 'VCCBRAM', 'VCCAUX', 'VCC1V2'
         'VCC3V3', 'MGTAVCC', 'MGTAVTT', 'VCCPSINTFP', 'MGTRAVCC'
         'MGTRAVTT','VCCO_PSDDR_504', 'VCCPSDDRPLL']

def plot_all():
    filename = 'datalog.csv'

    table = dict()

    with open(filename, newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(lines):
            if i <= 1: continue
            for idx, string in enumerate(line):
                if idx > len(names) - 1: break
                name = names[idx]
                if name not in table.keys():
                    table[name] = list()
                if idx > 0: string = int(string)
                table[name].append(string)
    plt.style.use('seaborn-paper')
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(10, 6)
    ax.autoscale(True)

    for label in names:
        if label == 'timestamp': continue
        data = table[label]
        length = len(data)
        ax.plot(range(length), data, label=label)
    ax.set_xlabel('time steps', fontsize=15)
    ax.set_ylabel('value', fontsize=15)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', prop={'size': 12}, ncol=1, bbox_to_anchor=(1, 0.8),
               frameon=True)

    plt.savefig("plot.png")


def plot_each():
    import os, shutil
    base_path = './results_plot'
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    os.mkdir(base_path)
    for _csv in os.listdir('./results_csv'):
        filename = _csv.replace('.csv', '')
        table = dict()
        _csv = os.path.join('./results_csv', _csv)
        with open(_csv, newline='') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for i, line in enumerate(lines):
                if i <= 1: continue
                for idx, string in enumerate(line):
                    if idx > len(names) - 1: break
                    name = names[idx]
                    if name not in table.keys():
                        table[name] = list()
                    if idx > 0: string = int(string)
                    table[name].append(string)
        plt.style.use('seaborn-paper')
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(10, 6)
        ax.autoscale(True)

        for label in names:
            if label == 'timestamp': continue
            data = table[label]
            length = len(data)
            ax.plot(range(length), data, label=label)
        ax.set_xlabel('time steps', fontsize=15)
        ax.set_ylabel('value', fontsize=15)
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right', prop={'size': 12}, ncol=1, bbox_to_anchor=(1, 0.8),
                   frameon=True)
        full_path = os.path.join(base_path, filename + ".png")
        plt.savefig(full_path)


if __name__ == "__main__":
    plot_each()
