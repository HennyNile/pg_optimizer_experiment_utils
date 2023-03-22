import os
import sys


def load_queries(dirpath):
    path = os.walk(dirpath)
    current_dir_obj = path.__next__()
    query_paths = current_dir_obj[2]

    # sort the path, solid the query order
    query_paths.sort()

    queries = []
    for query_path in query_paths:
        with open(dirpath + query_path, 'r+') as f:
            queries.append(f.read())
    return query_paths, queries


def load_JOB():
    dir_path = sys.path[-1] + 'queries/job/'
    return load_queries(dir_path)


def load_JOB_light():
    dir_path = sys.path[-1] + 'queries/job-light/'
    query_paths, queries = load_queries(dir_path)
    queries = queries[0].split('\n')
    query_paths = ['job-light-' + str(i+1) for i in range(len(queries))]
    return query_paths, queries


def load_TPCH():
    dir_path = sys.path[-1] + 'queries/tpch/'
    return load_queries(dir_path)


def load_TPCH_modified4pg():
    dir_path = sys.path[-1] + 'queries/tpch_modified4pg/'
    return load_queries(dir_path)


def load_cost_runtime(filepath):
    cost_list, runtime_list = [], []
    with open(filepath, 'r+') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split(',')
            cost = float(parts[1].strip())
            runtime = float(parts[2].strip())
            cost_list.append(cost)
            runtime_list.append(runtime)
    return cost_list, runtime_list
