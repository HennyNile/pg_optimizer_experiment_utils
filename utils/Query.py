import itertools


def get_table_encode_map(tables):
    encode_map = dict()
    for i in range(len(tables)):
        encode_map.update({tables[i][1]: 2**(i+1)})
    return encode_map


class Query:
    def __init__(self):
        self.query_path = None
        self.select = None
        self.tables = []  # [[table_name1, table_key1], [table_name2, table_key2], ...]
        self.tables_dict = dict()  # {table_key: table_name}
        self.joins = dict()  # {table_key1+table_key2: [join_predicates]}
        self.predicates = dict()  # {table_key: [filter_predicates]}
        self.join_tables = dict()  # {table_key: [join_table_keys]}
        self.join_column_tables = dict()  # {table_key: {column_key:[[table_keys],[column_keys]]}}

    def parse_query(self, query_path, query_text):
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
                        columns_keys = [sub_parts[0][sub_parts[0].find('.') + 1:],
                                        sub_parts[1][sub_parts[1].find('.') + 1:]]
                        joins.append([tables_key, columns_keys, predicate])
                        is_join = True
            if not is_join:
                tmp_predicate = predicate
                if tmp_predicate[0] == '(':
                    tmp_predicate = tmp_predicate[1:]
                table = tmp_predicate.split('.')[0]
                filters.append([table, predicate])

        # set query_path
        self.set_query_path(query_path)
        # set select
        self.set_select(select)
        # set tables
        self.set_tables(tables)
        # set joins
        self.set_joins(joins)
        # set predicates
        self.set_predicates(filters)

    def set_query_path(self, query_path):
        self.query_path = query_path

    def set_select(self, select):
        self.select = select

    def set_tables(self, tables):
        self.tables = tables
        for table in tables:
            self.tables_dict.update({table[1]: table[0]})
            self.predicates.update({table[1]: list()})
            self.join_tables.update({table[1]: list()})
            self.join_column_tables.update({table[1]: dict()})

    def set_joins(self, joins):
        for join in joins:
            join_table_keys = join[0]
            join_columns_keys = join[1]
            join_text = join[2]

            # add join column to join_column_tables if not in
            if self.join_column_tables.get(join_table_keys[0]).get(join_columns_keys[0]) is None:
                self.join_column_tables.get(join_table_keys[0]).update(
                    {join_columns_keys[0]: [[join_table_keys[1]], [join_columns_keys[1]]]})
            else:
                tables_columns = self.join_column_tables.get(join_table_keys[0]).get(join_columns_keys[0])
                find = False
                for i in range(len(tables_columns[0])):
                    if join_table_keys[1] == tables_columns[0][i] and join_columns_keys[1] == tables_columns[1][i]:
                        find = True
                if not find:
                    tables_columns[0].append(join_table_keys[1])
                    tables_columns[1].append(join_columns_keys[1])

            if self.join_column_tables.get(join_table_keys[1]).get(join_columns_keys[1]) is None:
                self.join_column_tables.get(join_table_keys[1]).update(
                    {join_columns_keys[1]: [[join_table_keys[0]], [join_columns_keys[0]]]})
            else:
                tables_columns = self.join_column_tables.get(join_table_keys[1]).get(join_columns_keys[1])
                find = False
                for i in range(len(tables_columns[0])):
                    if join_table_keys[0] == tables_columns[0][i] and join_columns_keys[0] == tables_columns[1][i]:
                        find = True
                        break
                if not find:
                    tables_columns[0].append(join_table_keys[0])
                    tables_columns[1].append(join_columns_keys[0])

            # check neighbor join tables
            tables_columns_1 = self.join_column_tables.get(join_table_keys[0]).get(join_columns_keys[0])
            tables_columns_2 = self.join_column_tables.get(join_table_keys[1]).get(join_columns_keys[1])
            # print("table_columns_1", tables_columns_1)
            # print("table_columns_2", tables_columns_2)
            for i in range(len(tables_columns_1[0])):
                find = False
                if tables_columns_1[0][i] == join_table_keys[1]:
                    continue
                for j in range(len(tables_columns_2[0])):
                    if tables_columns_1[0][i] == tables_columns_2[0][j] and tables_columns_1[1][i] == tables_columns_2[1][j]:
                        find = True
                        break
                if not find:
                    tables_columns_2[0].append(tables_columns_1[0][i])
                    tables_columns_2[1].append(tables_columns_1[1][i])
                    tables_columns_3 = self.join_column_tables.get(tables_columns_1[0][i]).get(tables_columns_1[1][i])
                    find = False
                    for l in range(len(tables_columns_3[0])):
                        if join_table_keys[1] == tables_columns_3[0][l] and join_columns_keys[1] == tables_columns_3[1][l]:
                            find = True
                            break
                    if not find:
                        tables_columns_3[0].append(join_table_keys[1])
                        tables_columns_3[1].append(join_columns_keys[1])

            for i in range(len(tables_columns_2[0])):
                find = False
                if tables_columns_2[0][i] == join_table_keys[0]:
                    continue
                for j in range(len(tables_columns_1[0])):
                    if tables_columns_2[0][i] == tables_columns_1[0][j] and tables_columns_2[1][i] == tables_columns_1[1][j]:
                        find = True
                        break
                if not find:
                    tables_columns_1[0].append(tables_columns_2[0][i])
                    tables_columns_1[1].append(tables_columns_2[1][i])
                    tables_columns_3 = self.join_column_tables.get(tables_columns_2[0][i]).get(tables_columns_2[1][i])
                    find = False
                    for l in range(len(tables_columns_3[0])):
                        if join_table_keys[0] == tables_columns_3[0][l] and join_columns_keys[0] == tables_columns_3[1][l]:
                            find = True
                            break
                    if not find:
                        tables_columns_3[0].append(join_table_keys[0])
                        tables_columns_3[1].append(join_columns_keys[0])

            # # initialize Query.joins
            # init_joins = self.joins.get(join_table_keys[0] + join_table_keys[1])
            # if init_joins is not None:
            #     self.joins.update({join_table_keys[0] + join_table_keys[1]: init_joins.append(join_text),
            #                        join_table_keys[1] + join_table_keys[0]: init_joins.append(join_text)})
            # else:
            #     self.joins.update({join_table_keys[0] + join_table_keys[1]: [join_text],
            #                        join_table_keys[1] + join_table_keys[0]: [join_text]})

        # initialize Query.join_tables and Query.joins
        tables = self.tables
        join_key_set = set()
        for table in tables:
            tables_columns_items = list(self.join_column_tables.get(table[1]).items())
            join_table_keys = set()
            for tables_columns_item in tables_columns_items:
                table_1_key = table[1]
                column_1_key = tables_columns_item[0]
                for i in range(len(tables_columns_item[1][0])):
                    table_2_key = tables_columns_item[1][0][i]
                    column_2_key = tables_columns_item[1][1][i]
                    if table_1_key+column_1_key+table_2_key+column_2_key not in join_key_set:
                        # update Query.join_tables
                        if table_1_key not in self.join_tables.get(table_2_key):
                            self.join_tables.get(table_2_key).append(table_1_key)
                        if table_2_key not in self.join_tables.get(table_1_key):
                            self.join_tables.get(table_1_key).append(table_2_key)

                        # update Query.joins
                        join_key_set.add(table_1_key+column_1_key+table_2_key+column_2_key)
                        join_key_set.add(table_2_key+column_2_key+table_1_key+column_1_key)
                        init_joins = self.joins.get(table_1_key + table_2_key)
                        join_text = table_1_key + '.' + column_1_key + '=' + table_2_key + '.' + column_2_key
                        if init_joins is not None:
                            self.joins.update({table_1_key + table_2_key: init_joins.append(join_text),
                                               table_2_key + table_1_key: init_joins.append(join_text)})
                        else:
                            self.joins.update({table_1_key + table_2_key: [join_text],
                                               table_2_key + table_1_key: [join_text]})

    def set_predicates(self, predicates):
        for predicate in predicates:
            table_key, predicate_text = predicate[0], predicate[1]
            self.predicates.get(table_key).append(predicate_text)
            # table = self.tables_dict.get(table_key)
            # predicate_text = predicate[1]
            # self.predicates.get(table).append(predicate_text)

    def self_print(self):
        print('select:\n', self.select)
        print('tables:\n', self.tables)
        print('joins:\n', self.joins)
        print('predicates:\n', self.predicates)

    def check_subJoin(self, tables_key):
        # root node to walk graph
        root_key = tables_key[0]
        join_graph_tables_key = []

        # walk graph with BFS
        index = 0
        queue = [root_key]
        while index < len(queue):
            node_key = queue[index]
            index += 1
            # check whether this table is included into graph
            if node_key in join_graph_tables_key:
                continue
            join_graph_tables_key.append(node_key)
            join_tables = self.join_tables.get(node_key)
            for table_key in join_tables:
                if table_key not in join_graph_tables_key and table_key not in queue and table_key in tables_key:
                    queue.append(table_key)

        # print('join_graph_tables_key =', join_graph_tables_key, ', tables_key =', tables_key)
        if len(join_graph_tables_key) == len(tables_key):
            return True
        else:
            return False

    def generate_sub_queries_rcount(self):
        tables = self.tables
        encode_map = get_table_encode_map(tables)
        joins = self.joins
        sub_queries_text = dict()
        select = 'SELECT count(*) FROM '
        sub_queries_count = 0
        for join_table_count in range(1, len(joins) + 2):
            for com in itertools.combinations(tables, join_table_count):
                query_text = select
                joins_predicates = []

                all_tables_key = [table[1] for table in com]

                # check whether selected tables have a join graph
                if not self.check_subJoin(all_tables_key):
                    continue
                sub_queries_count += 1

                join_tables_key_set = set()
                for com2table in itertools.combinations(com, 2):
                    # tables_key = com2table[0][0] + com2table[1][0]
                    tables_key = com2table[0][1] + com2table[1][1]
                    joins = self.joins.get(tables_key)
                    if joins is not None:
                        join_tables_key_set.add(com2table[0][1])
                        join_tables_key_set.add(com2table[1][1])
                        for join in joins:
                            joins_predicates.append(join)

                relids = 0
                for table in com:
                    relids += encode_map[table[1]]
                    query_text += table[0] + " AS " + table[1] + ", "
                    predicates = self.predicates.get(table[1])
                    if predicates is not None:
                        for predicate in predicates:
                            joins_predicates.append(predicate)
                query_text = query_text[:len(query_text) - 2]

                if len(joins_predicates) > 0:
                    query_text += ' WHERE ' + joins_predicates[0]
                    for i in range(1, len(joins_predicates)):
                        query_text += ' AND ' + joins_predicates[i]
                query_text += ';'
                # sub_queries_text.append([tuple([t[1] for t in com]), relids, query_text])
                sub_queries_text.update({tuple([t[1] for t in com]): query_text})
        print('total ' + str(sub_queries_count) + ' sub queries.')
        return sub_queries_text
