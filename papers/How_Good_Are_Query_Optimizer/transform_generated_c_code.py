import sys

sys.path.append('../../')

from utils.load_data import load_JOB


if __name__ == '__main__':
    filepath = 'generated_c_code.txt'
    functions = open(filepath, 'r+').read().split('\n\n')
    print(len(functions))

    query_paths, JOB_queries = load_JOB()
    transformed_query_paths = query_paths.copy()
    transformed_query_paths.sort()

    # print(query_paths)
    # print(transformed_query_paths)

    new_filepaths = []
    transform_index = dict()
    for i in range(len(transformed_query_paths)):
        transform_index.update({i: query_paths.index(transformed_query_paths[i])})
        new_filepaths.append(query_paths[transform_index.get(i)])
    print(transform_index)

    # assert len(transformed_query_paths) == len(new_filepaths)
    # for i in range(len(new_filepaths)):
    #     if transformed_query_paths[i] != new_filepaths[i]:
    #         print(i, 'error')
    # print('finished')

    new_code = ''
    for i in range(len(functions)):
        init_idx = transform_index.get(i)
        function = functions[init_idx]
        function = function.replace('job_query_' + str(init_idx), 'job_query_' + str(i))
        new_code += function + '\n\n'

    filepath = 'transformed_generated_c_code.txt'
    open(filepath, 'w+').write(new_code)






