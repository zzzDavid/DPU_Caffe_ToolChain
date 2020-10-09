"""
This script is for power measuring with OFA
and mobilenet networks. It does three things:
1. run the compiled networks (in .so library format) one by one
2. wait a moment in between each run
3. record the start and end time stamp for each run
"""
import csv
import os
from datetime import datetime
from time import sleep

months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

latency_binary = '/home/root/niansong/auto_deploy/utils/build/latency'


def convert_time(string='Sat Jul 25 21:04:36 2020'):
    """
    convert time format
    :return: a datetime object
    """
    _, month, day, time, year = string.split(" ")
    month = months[month]
    day = int(day)
    hour, min, sec = [int(item) for item in time.split(':')]
    year = int(year)
    # my time stamp was in wrong timezone
    hour -= 15
    return datetime(year=year, month=month, day=day, hour=hour, minute=min, second=sec)


def to_so():
    """
    convert all .elf to .so, 
    save it to a dir called so
    """
    elfs = os.listdir('./elf')
    so_dir = './so'
    os.mkdir(so_dir)
    for elf in elfs:
        kernel_name = elf.replace('.elf', '').split('_')[1]
        so_name = 'libdpumodel' + kernel_name + '.so'
        cmd = "g++ -nostdlib -fPIC -shared ./elf/{} -o ./so/{}".format(elf, so_name)
        print(cmd)
        os.system(cmd)

    # note: ya'll need to copy the .so files to /usr/lib
    # setting LD_LIBRARY_PATH doesn't work, I tried.    


def run(so_name='libdpumodelfpga10.so', time=100000):
    kernel_name = so_name.replace('libdpumodel', '')
    kernel_name = kernel_name.split('/')[-1]
    kernel_name = kernel_name.split('.')[0]
    # kernel_name = kernel_name + "_0"
    cmd = latency_binary + " " + kernel_name + " " + str(time) + " > " + './latency/' +kernel_name + ".txt"
    print(cmd)
    start = datetime.now()
    os.system(cmd)
    end = datetime.now()
    return kernel_name, start, end


def run_power_profiling():
    # kernels = os.listdir('./so')
    import glob
    kernels = glob.glob('/usr/lib/libdpumodel*put*')
    print("preparing...")
    sleep(1)
    time_stamps = list()
    for kernel in kernels:
        kernel_name, start, end = run(kernel)
        print("waiting...")
        sleep(5)
        net_name = kernel_name
        time_stamps.append([net_name, start, end])
    print("done")

    # write time stamp file
    with open('test_time_stamps.txt', 'w') as f:
        for test_run in time_stamps:
            net_name, start, end = test_run
            f.write("{} {} {}\n".format(net_name, start, end))


def divide_power_data():
    """
    cut `datalog.csv` according to time stamps,
    and save them to smaller csv files
    """
    # read time stamp
    time_stamps = dict()
    with open('test_time_stamps.txt', 'r') as f:
        for line in f:
            net_name, start0, start1, end0, end1 = line.split(' ')
            end1 = end1.replace('\n', '')
            start = datetime.fromisoformat(start0 + ' ' + start1)
            end = datetime.fromisoformat(end0 + ' ' + end1)
            time_stamps[net_name] = [start, end]
    # read csv
    whole_data = []
    legend = []
    with open('datalog.csv', newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(lines):
            if i == 0: legend = line
            else: whole_data.append(line)
    collection = dict()
    # cut the data in parts
    for name, time_stamp in time_stamps.items():
        start, end = time_stamp
        for line in whole_data:
            win_time_stamp = convert_time(line[0])
            # print("this={}, start={}, end={}, in={}".format(
            #     win_time_stamp, start, end,
            #     (win_time_stamp >= start and win_time_stamp <= end)
            # ))
            if win_time_stamp < start: continue
            if win_time_stamp > end: continue
            if name not in collection.keys():
                collection[name] = list()
            collection[name].append(line)
    # write out csv files
    base_path = './results_csv'
    if os.path.exists(base_path):
        import shutil
        shutil.rmtree(base_path)
    os.mkdir(base_path)
    for orig_name, data in collection.items():
        full_path = os.path.join(base_path, orig_name+'.csv')
        # write to one csv file
        with open(full_path, 'w', newline='') as csvfile:
            wr = csv.writer(csvfile, delimiter=',')
            # write lines
            wr.writerow(legend)
            for line in collection[orig_name]:
                wr.writerow(line)

if __name__ == "__main__":
    # to_so()
    run_power_profiling()
