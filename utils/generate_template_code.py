import itertools


def generate_c_code(truth_cardinality, queries, start_query_order, generated_code_filepath='generated_c_code.txt'):
    all_c_code = ''

    # print function declaration
    query_order = start_query_order
    declaration = ''
    for i in range(len(queries)):
        declaration += str.format('double get_truth_cardinality_job_query_{}(int total_relids);\n', query_order)
        query_order += 1
    all_c_code += declaration + '\n\n'

    # print switch case in main function
    query_order = start_query_order
    switch_case = ''
    for i in range(len(queries)):
        switch_case += str.format('\t\t\t\tcase {}:\n', query_order)
        switch_case += str.format('\t\t\t\t\treturn get_truth_cardinality_job_query_{}(total_relids);\n', query_order)
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

        c_code += str.format('double\nget_truth_cardinality_job_query_{}(int total_relids)\n', query_order)
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
    with open(generated_code_filepath, 'a+') as f:
        f.write(all_c_code)
        f.close()
    return all_c_code
