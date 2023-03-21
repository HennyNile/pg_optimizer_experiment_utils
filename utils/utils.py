import itertools
import subprocess
import time

from matplotlib import pyplot as plt
from Query import Query


db_user = 'postgres_15_sc'
db = 'imdb'
port = 5431


def parse_query_text(query_path, query_text):
    # remove ;
    query_text = query_text.replace('\n', ' ').replace(';', '').strip()
    while '  ' in query_text:
        query_text = query_text.replace('  ', ' ')
    select_text = query_text.split('FROM')[0].split('SELECT')[1].strip()
    tables_text = [table.strip() for table in query_text.split('FROM')[1].split('WHERE')[0].split(',')]
    predicates_text = ''
    if len(query_text.split('WHERE')) == 2:
        predicates_text = query_text.split('WHERE')[1].strip()

    # parse select
    select = select_text

    # parse tables
    tables = []
    for table_text in tables_text:
        table_name = []
        if 'AS' in table_text:
            table_names = [table_name.strip() for table_name in table_text.split('AS')]
        else:
            table_names = [table_name.strip() for table_name in table_text.split(' ')]
        tables.append([table_names[0], table_names[1]])

    # parse predicates
    brackets_num = 0
    all_predicates = []  # contains join predicates and filter predicates
    predicate = ''
    while len(predicates_text) > 0:
        if predicates_text.startswith('('):
            predicate += '('
            brackets_num += 1
            for i in range(1, len(predicates_text)):
                predicate += predicates_text[i]
                if predicates_text[i] == '(':
                    brackets_num += 1
                elif predicates_text[i] == ')':
                    brackets_num -= 1
                    if brackets_num == 0:
                        predicates_text = predicates_text[i + 1:].strip()
                        break
            all_predicates.append(predicate)
            predicate = ''
        elif predicates_text.startswith('AND'):
            predicates_text = predicates_text[3:].strip()
        else:
            AND_break = True
            for i in range(0, len(predicates_text)):
                if predicates_text[i:].strip().startswith('BETWEEN'):
                    AND_break = False
                predicate += predicates_text[i]
                if AND_break:
                    if predicates_text[i + 1:].strip().startswith('AND'):
                        break
                else:
                    if predicates_text[i + 1:].startswith('AND'):
                        AND_break = True
            predicates_text = predicates_text[len(predicate):].strip()
            all_predicates.append(predicate)
            predicate = ''

    filters = []
    joins = []
    for predicate in all_predicates:
        is_join = False
        if predicate.find('(') == -1:
            if predicate.find('=') != -1:
                sub_parts = [sub_part.strip() for sub_part in predicate.split('=')]
                if len(sub_parts) == 2 and sub_parts[0].find('.') != -1 and sub_parts[1].find('.') != -1:
                    tables_key = [sub_parts[0][0:sub_parts[0].find('.')], sub_parts[1][0:sub_parts[1].find('.')]]
                    columns_keys = [sub_parts[0][sub_parts[0].find('.')+1:], sub_parts[1][sub_parts[1].find('.')+1:]]
                    joins.append([tables_key, columns_keys, predicate])
                    is_join = True
        if not is_join:
            tmp_predicate = predicate
            if tmp_predicate[0] == '(':
                tmp_predicate = tmp_predicate[1:]
            table = tmp_predicate.split('.')[0]
            filters.append([table, predicate])

    # create a Query
    query = Query()
    # set query_path
    query.set_query_path(query_path)
    # set select
    query.set_select(select)
    # set tables
    query.set_tables(tables)
    # set joins
    query.set_joins(joins)
    # set predicates
    query.set_predicates(filters)

    return query


def get_table_encode_map(tables):
    encode_map = dict()
    for i in range(len(tables)):
        encode_map.update({tables[i][1]: 2**(i+1)})
    return encode_map


def generate_sub_queries_rcount(query):
    tables = query.tables
    encode_map = get_table_encode_map(tables)
    joins = query.joins
    sub_queries_text = []
    select = 'SELECT count(*) FROM '
    sub_queries_count = 0
    for join_table_count in range(1, len(joins) + 2):
        for com in itertools.combinations(tables, join_table_count):
            query_text = select
            joins_predicates = []

            all_tables_key = [table[1] for table in com]

            # check whether selected tables have a join graph
            if not query.check_subJoin(all_tables_key):
                continue
            sub_queries_count += 1

            join_tables_key_set = set()
            for com2table in itertools.combinations(com, 2):
                # tables_key = com2table[0][0] + com2table[1][0]
                tables_key = com2table[0][1] + com2table[1][1]
                joins = query.joins.get(tables_key)
                if joins is not None:
                    join_tables_key_set.add(com2table[0][1])
                    join_tables_key_set.add(com2table[1][1])
                    for join in joins:
                        joins_predicates.append(join)

            relids = 0
            for table in com:
                relids += encode_map[table[1]]
                query_text += table[0] + " AS " + table[1] + ", "
                predicates = query.predicates.get(table[1])
                if predicates is not None:
                    for predicate in predicates:
                        joins_predicates.append(predicate)
            query_text = query_text[:len(query_text) - 2]

            if len(joins_predicates) > 0:
                query_text += ' WHERE ' + joins_predicates[0]
                for i in range(1, len(joins_predicates)):
                    query_text += ' AND ' + joins_predicates[i]
            query_text += ';'
            sub_queries_text.append([tuple([t[1] for t in com]), relids, query_text])
    print('total ' + str(sub_queries_count) + ' sub queries.')
    return sub_queries_text


def execute_sub_queries_rcount(queries, sub_queries_rcount_list):
    command_head = '/usr/local/pgsql/bin/psql -h localhost -p 5431 -U postgres_15_sc imdb -c "{}"'

    output_file_path = 'truth_cardinality_job.txt'
    output_file = open(output_file_path, 'w+')
    output_file.write('Join6 Benchmark\n')

    # query_orders = []
    truth_cardinality = dict()
    for i in range(len(queries)):
        t = time.time()
        query_path = queries[i].query_path
        sub_queries_rcount = sub_queries_rcount_list.get(query_path)
    # for query_path, sub_queries_rcount in sub_queries_rcount_list.items():
        print('[INFO] Query : ' + query_path)
        coms = []
        res = []
        query_count = 0
        for com, _, query in sub_queries_rcount:
            query_count += 1
            print('[INFO]', query_count, com)
            # print('[INFO] query = ', query)
            coms.append(com)
            command = str.format(command_head, query)
            subp = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
            (out, err) = subp.communicate()
            result_card = out.decode().split('\n')[2].strip()
            res.append(result_card)
            # print('[INFO] Truth Cardinality =', result_card)
        if len(res) != len(coms):
            print('[ERROR] Meet a error during parsing result')
            exit()

        output_file.write('    ' + query_path + '\n')
        cardinalities = dict()
        table_encode_map = get_table_encode_map(queries[i].tables)
        for j in range(len(res)):
            table_encode = 0
            for table_key in coms[j]:
                table_encode += table_encode_map.get(table_key)
            cardinalities.update({coms[j]: [table_encode, res[j]]})
            output_file.write('      ' + coms[j].__str__() + ': ' + str(res[j]) + '\n')
            output_file.write('      ' + str(table_encode) + ': ' + str(res[j]) + '\n')
        truth_cardinality.update({query_path: cardinalities})
        print('[INFO] Generate truth cardinalities use time = ' + str(time.time()-t) + ' s')
    output_file.close()
    return truth_cardinality


def generate_c_code(truth_cardinality, queries, start_query_order):
    all_c_code = ''
    output_file_path = 'generated_c_code.txt'

    # print function declaration
    query_order = start_query_order
    declaration = ''
    for i in range(len(queries)):
        declaration += str.format('double get_truth_cardinality_cost_model_query_{}(int total_relids);\n', query_order)
        query_order += 1
    all_c_code += declaration + '\n\n'

    # print switch case in main function
    query_order = start_query_order
    switch_case = ''
    for i in range(len(queries)):
        switch_case += str.format('\t\t\t\tcase {}:\n', query_order)
        switch_case += str.format('\t\t\t\t\treturn get_truth_cardinality_cost_model_query_{}(total_relids);\n', query_order)
        query_order += 1
    all_c_code += switch_case + '\n\n'

    query_order = start_query_order
    for query in queries:
        c_code = ''
        query_path = query.query_path
        tables = query.tables
        table_keys = [table[1] for table in tables]
        table_names = [table[0] for table in tables]
        cardinality = truth_cardinality.get(query_path)
        c_code += '// ['
        for table in tables:
            c_code += table[0] + ' ' + table[1] + ', '
        c_code += ']\n'

        c_code += str.format('double\nget_truth_cardinality_cost_model_query_{}(int total_relids)\n', query_order)
        c_code += '{\n'
        c_code += '\tswitch (total_relids) {\n'
        for join_table_count in range(1, len(tables) + 1):
            # for com in itertools.combinations(table_names, join_table_count):
            for com in itertools.combinations(table_keys, join_table_count):
                if cardinality.get(com) is None:
                    continue
                com_text = query.tables_dict.get(com[0]) + ' ' + com[0]
                for i in range(1, len(com)):
                    com_text += ', ' + query.tables_dict.get(com[i]) + ' ' + com[i]
                c_code += str.format('\t\t// {}\n', com_text)
                single_cardinality = cardinality.get(com)
                c_code += str.format('\t\tcase {}:\n\t\t\treturn {};\n', single_cardinality[0], single_cardinality[1])
        c_code += '\t};\n}\n\n'
        all_c_code += c_code
        query_order += 1
    with open(output_file_path, 'a+') as f:
        f.write(all_c_code)
        f.close()
    return all_c_code


def modify_pg_conf_parameters(enable_truth_card=False, benchmark=0, query_order=0):
    command_head = str.format('/usr/local/pgsql/bin/psql -U {} -p {} -d {}', db_user, port, db) + ' -c "{}"'

    # modify enable_truth_card
    cmd = 'alter system set enable_truth_card=true;'
    subp = subprocess.Popen([command_head.format(cmd)], shell=True, stdout=subprocess.PIPE)
    subp.communicate()

    # modify benchmark
    cmd = 'alter system set benchmark={};'.format(benchmark)
    subp = subprocess.Popen([command_head.format(cmd)], shell=True, stdout=subprocess.PIPE)
    subp.communicate()

    # modify query_order
    cmd = 'alter system set query_order={};'.format(query_order)
    subp = subprocess.Popen([command_head.format(cmd)], shell=True, stdout=subprocess.PIPE)
    subp.communicate()

    # reload conf
    cmd = 'select pg_reload_conf();'
    subp = subprocess.Popen([command_head.format(cmd)], shell=True, stdout=subprocess.PIPE)
    subp.communicate()


def run_cat_cost_running_time(queries, run_times, start_query_order, enable_print_plan=False):
    command_head = str.format('/usr/local/pgsql/bin/psql -U {} -p {} -d {}', db_user, port, db) + ' -c "{}"'
    cost_list, running_time_list = [], []
    query_order = start_query_order
    for i in range(len(queries)):
        modify_pg_conf_parameters(enable_truth_card=True, benchmark=4, query_order=query_order)
        query_order += 1
        # if query_order == 36:
        #     query_order += 1
        query = queries[i]
        print('[INFO] query ' + str(i) + ': ' + query)
        # run query and catch running time
        command = str.format(command_head, "explain analyze " + query)
        running_time = 0
        cost = 0
        for _ in range(run_times):
            subp = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
            (out, err) = subp.communicate()
            out_str_lines = out.decode().split('\n')
            if enable_print_plan:
                print(out.decode())
            out_str_lines_len = len(out_str_lines)
            # extract running time info
            planning_time_str, execution_time_str = out_str_lines[out_str_lines_len - 5], out_str_lines[
                out_str_lines_len - 4]
            planning_time = float(planning_time_str.split(':')[1].strip().split(' ')[0])
            execution_time = float(execution_time_str.split(':')[1].strip().split(' ')[0])
            running_time += planning_time + execution_time
            # extract cost info
            cost_line_parts = out_str_lines[2].strip().split(' ')
            for part in cost_line_parts:
                if 'cost' in part:
                    cost = float(part.strip().split('..')[1])
        print('[INFO] query ' + str(i) + ': ' + query + " : " + str(running_time/run_times) + 's')
        cost_list.append(cost)
        running_time_list.append(running_time/run_times)
    return cost_list, running_time_list


def plot_cost_running_time(cost, running_time, output_filepath):
    plt.figure()
    plt.scatter(cost, running_time)
    plt.xlabel('Cost')
    plt.ylabel('Running time / ms')
    plt.savefig(output_filepath)

