import sys

from utils.Query import Query

sys.path.append('../../')

from utils.load_data import load_JOB
from utils.generate_template_code import generate_c_code

if __name__ == '__main__':
    filepath = 'output_cards'
    with open(filepath, 'r+') as f:
        lines = f.readlines()

        # generate truth_cardinality from txt
        truth_cardinality = dict()
        query_path = ''
        cardinalities = {}
        index = 0
        while index < len(lines):
            line_1 = lines[index]
            if '.sql' in line_1:
                if not index == 0:
                    truth_cardinality.update({query_path: cardinalities.copy()})
                    cardinalities = {}
                query_path = line_1.strip()
                index += 1
                continue

            com = eval(line_1.split(':')[0].strip())
            line_2 = lines[index + 1]
            relid = int(line_2.split(':')[0].strip())
            card = float(line_2.split(':')[1].strip())
            cardinalities.update({com: [relid, card]})

            index += 2
            if index == len(lines):
                truth_cardinality.update({query_path: cardinalities.copy()})

        # generate queries
        query_paths, JOB_queries = load_JOB()
        queries = []
        for i in range(60, 71):
            query = Query()
            query.parse_query(query_paths[i], JOB_queries[i])
            queries.append(query)

        # print(truth_cardinality.keys())
        # print(query_paths[60:71])
        # print(queries[0].query_path)

        generate_c_code(truth_cardinality, queries, 60,
                        generated_code_filepath='new_generated_code.txt')
