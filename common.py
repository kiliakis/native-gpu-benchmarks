from optparse import OptionParser
import subprocess
import re
import os
import yaml
# from collections import deque, OrderedDict


def parse_app_yml(app_yml):
    benchmark_yaml = yaml.load(open(app_yml), Loader=yaml.FullLoader)
    benchmarks = []
    for suite in benchmark_yaml['run']:
        for exe in benchmark_yaml[suite]['execs']:
            exe_name = exe.keys()[0]
            args_list = exe.values()[0]
            benchmarks.append((benchmark_yaml[suite]['exec_dir'],
                               benchmark_yaml[suite]['data_dirs'],
                               exe_name, args_list))
    return benchmarks




def get_cuda_version():
    # Get CUDA version
    nvcc_out_filename = os.path.join("/tmp", "nvcc_out.txt")
    nvcc_out_file = open(nvcc_out_filename, 'w+')
    subprocess.call(["nvcc", "--version"],
                    stdout=nvcc_out_file)
    nvcc_out_file.seek(0)
    cuda_version = re.sub(r".*release (\d+\.\d+).*", r"\1",
                          nvcc_out_file.read().strip().replace("\n", " "))
    nvcc_out_file.close()
    os.remove(nvcc_out_filename)
    return cuda_version

# This function exists so that this file can accept both absolute and relative paths
# If no name is provided it sets the default
# Either way it does a test if the absolute path exists and if not, tries a relative path

def file_option_test(name, default, this_directory):
    if name == "":
        if default == "":
            return ""
        else:
            name = os.path.join(this_directory, default)
    try:
        with open(name):
            pass
    except IOError:
        name = os.path.join(os.getcwd(), name)
        try:
            with open(name):
                pass
        except IOError:
            exit("Error - cannot open file {0}".format(name))
    return name


def dir_option_test(name, default, this_directory):
    if name == "":
        name = os.path.join(this_directory, default)
    if not os.path.isdir(name):
        name = os.path.join(os.getcwd(), name)
        if not os.path.isdir(name):
            exit("Error - cannot open file {0}".format(name))
    return name


def parse_run_simulations_options():
    parser = OptionParser()
    # parser.add_option("-c", "--configs_file", dest="configs_file",
    # help="configs_file used to determine which configurations are run",
    # default="")
    parser.add_option("-b", "--benchmark_file", dest="benchmark_file",
                      help="the yaml file used to define which benchmarks are run",
                      default="")
    # parser.add_option("-m", "--apps_configs_file", dest="apps_configs_file",
    # help="the yaml file used to define which configs and benchmarks to run",
    # default="")
    parser.add_option("-r", "--run_directory", dest="run_directory",
                      help="Name of directory in which to run simulations",
                      default="")
    parser.add_option("-n", "--no_launch", dest="no_launch", action="store_true",
                      help="When set, no torque jobs are launched.  However, all" +
                      " the setup for running is performed. ie, the run" +
                      " directories are created and are ready to run." +
                      " This can be useful when you want to create a new" +
                      " configuration, but want to test it locally before " +
                      " launching a bunch of jobs.")
    parser.add_option("-N", "--launch_name", dest="launch_name", default="",
                      help="Pass if you want to name the launch. This will determine the name of the logfile.\n" +
                      "If you do not name the file, it will just use the current date/time.")

    (options, args) = parser.parse_args()
    # Parser seems to leave some whitespace on the options, getting rid of it
    options.benchmark_file = options.benchmark_file.strip()
    options.run_directory = options.run_directory.strip()
    options.launch_name = options.launch_name.strip()
    return (options, args)
