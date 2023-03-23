import math
import sys

from sklearn.linear_model import LinearRegression

sys.path.append('./../../')

from utils.load_data import load_TPCH_modified4pg, load_cost_runtime, load_JOB_light
from utils.run_queries_catch_infos import run_cat_cost_runtime, run_cat_subquery_card
from utils.plot import plot_cost_runtime
from utils.Query import Query


def compute_cost_runtime_error(cost_list, runtime_list):
    regressor = LinearRegression()
    regressor.fit([[cost] for cost in cost_list], runtime_list)
    pred_runtime_list = regressor.predict([[cost] for cost in cost_list])
    errors = []
    total_error = 0
    for i in range(len(cost_list)):
        error = math.fabs(pred_runtime_list[i] - runtime_list[i]) / pred_runtime_list[i]
        errors.append(error)
        total_error += error
    avg_error = total_error / len(cost_list)
    return avg_error


def generate_true_card_tpch(sf=1):
    # cat truth cardinality of tpc_h_sf
    query_paths, JOB_queries = load_TPCH_modified4pg()
    db = 'tpch_' + str(sf)
    # can not generate sub queries for
    # class 1: 3 (13.sql), 5 (19.sql), 7 (4.sql), 10 (7.sql) because can not parse these query
    # class 2: 12 (9.sql) because cost more than 15 hours in TPC-H with sf=1
    run_cat_subquery_card(query_paths=query_paths,
                          queries=JOB_queries,
                          db=db,
                          benchmark_name=db,
                          start_query_order=0,
                          end_query_order=3)
    run_cat_subquery_card(query_paths=query_paths,
                          queries=JOB_queries,
                          db=db,
                          benchmark_name=db,
                          start_query_order=4,
                          end_query_order=5)
    run_cat_subquery_card(query_paths=query_paths,
                          queries=JOB_queries,
                          db=db,
                          benchmark_name=db,
                          start_query_order=6,
                          end_query_order=7)
    run_cat_subquery_card(query_paths=query_paths,
                          queries=JOB_queries,
                          db=db,
                          benchmark_name=db,
                          start_query_order=8,
                          end_query_order=10)
    run_cat_subquery_card(query_paths=query_paths,
                          queries=JOB_queries,
                          db=db,
                          benchmark_name=db,
                          start_query_order=11,
                          end_query_order=12)


def cost_runtime_tpch_1():
    query_paths, queries = load_TPCH_modified4pg()


if __name__ == '__main__':
    # query_paths, queries = load_TPCH_modified4pg()
    # for i in range(3, 4):
    # for i in range(len(query_paths)):
    #     if i == 5 or i == 7 or i == 10:
    #         continue
    #     query = Query()
    #     print(i, query_paths[i])
    #     query.parse_query(query_paths[i], queries[i])
    #     sub_queries = query.generate_sub_queries_rcount()
        # for sub_query in sub_queries:
        #     print(sub_query, sub_queries.get(sub_query))
    # print(query_paths)
    # query = Query()
    # query.parse_query(query_paths[1], queries[1])
    # query.self_print()
    # print(query.generate_sub_queries_rcount())
    # print('{}_{}'.format(1, 2))
    # generate_true_card_tpch('tpch_1', sf=1)
    generate_true_card_tpch(sf=5)
