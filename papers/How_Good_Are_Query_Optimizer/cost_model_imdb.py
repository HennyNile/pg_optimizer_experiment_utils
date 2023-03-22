import math
import sys

from sklearn.linear_model import LinearRegression

sys.path.append('./../../')

from utils.load_data import load_JOB, load_cost_runtime, load_JOB_light
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


# initial PG
def cost_runtime_1():
    store_filepath = 'parallelism=0/cost_runtime/cost_runtime_a.csv'
    title = 'Initial Postgres'
    output_filepath = 'parallelism=0/cost_model_a'
    query_paths, JOB_queries = load_JOB()
    run_cat_cost_runtime(queries=JOB_queries,
                         run_times=3,
                         start_query_order=0,
                         end_query_order=len(JOB_queries),
                         store_filepath=store_filepath,
                         enable_truth_card=False,
                         max_parallel_workers_per_gather=0)
    cost_list, runtime_list = load_cost_runtime(store_filepath)
    error = compute_cost_runtime_error(cost_list, runtime_list)
    print('Cost Model - Experiment 1 - Error:', error)
    plot_cost_runtime(cost_list=cost_list, runtime_list=runtime_list, title=title,
                      output_filepath=output_filepath)


# PG with true card
def cost_runtime_2():
    store_filepath = 'parallelism=0/cost_runtime/cost_runtime_b.csv'
    title = 'Postgres with true card'
    output_filepath = 'parallelism=0/cost_model_b'
    store_plan_dir = 'parallelism=0/plans/'
    in_memory = True
    store_plan = True
    query_paths, JOB_queries = load_JOB()
    run_cat_cost_runtime(query_paths=query_paths,
                         queries=JOB_queries,
                         run_times=3,
                         start_query_order=0,
                         end_query_order=1,
                        #  end_query_order=len(JOB_queries),
                         store_filepath=store_filepath,
                         enable_truth_card=True,
                         benchmark=3,
                         max_parallel_workers_per_gather=0,
                         in_memory=in_memory, 
                         store_plan=store_plan, 
                         store_plan_dir=store_plan_dir)
    cost_list, runtime_list = load_cost_runtime(store_filepath)
    error = compute_cost_runtime_error(cost_list, runtime_list)
    print('Cost Model - Experiment 2 - Error:', error)
    plot_cost_runtime(cost_list=cost_list, runtime_list=runtime_list, title=title,
                      output_filepath=output_filepath)


# PG with tuned cost model (enlarge cpu_tuple_cost to 50 times)
def cost_runtime_3():
    store_filepath = 'parallelism=0/cost_runtime/cost_runtime_c.csv'
    title = 'Postgres with tuned cost model'
    output_filepath = 'parallelism=0/cost_model_c'
    query_paths, JOB_queries = load_JOB()
    run_cat_cost_runtime(queries=JOB_queries,
                         run_times=3,
                         start_query_order=0,
                         end_query_order=len(JOB_queries),
                         store_filepath=store_filepath,
                         enable_truth_card=False,
                         max_parallel_workers_per_gather=0)
    cost_list, runtime_list = load_cost_runtime(store_filepath)
    error = compute_cost_runtime_error(cost_list, runtime_list)
    print('Cost Model - Experiment 3 - Error:', error)
    plot_cost_runtime(cost_list=cost_list, runtime_list=runtime_list, title=title,
                      output_filepath=output_filepath)


# PG with true cards and tuned cost model
def cost_runtime_4():
    store_filepath = 'parallelism=0/cost_runtime/cost_runtime_d.csv'
    title = 'Postgres with true card and tuned cost model'
    output_filepath = 'parallelism=0/cost_model_d'
    query_paths, JOB_queries = load_JOB()
    run_cat_cost_runtime(queries=JOB_queries,
                         run_times=3,
                         start_query_order=72,
                         end_query_order=113,
                         # end_query_order=len(JOB_queries),
                         store_filepath=store_filepath,
                         enable_truth_card=True,
                         benchmark=3,
                         max_parallel_workers_per_gather=0)
    cost_list, runtime_list = load_cost_runtime(store_filepath)
    error = compute_cost_runtime_error(cost_list, runtime_list)
    print('Cost Model - Experiment 4 - Error:', error)
    plot_cost_runtime(cost_list=cost_list, runtime_list=runtime_list, title=title,
                      output_filepath=output_filepath)


if __name__ == '__main__':
    # cost_runtime_1()
    cost_runtime_2()
    exit()
    # cost_runtime_3()
    # cost_runtime_4()

    # cat truth cardinality of JOB
    # query_paths, JOB_queries = load_JOB()
    # run_cat_subquery_card(query_paths=query_paths, queries=JOB_queries, start_query_order=0, end_query_order=40)

    # query_paths, JOB_queries = load_JOB()
    # query_paths, JOB_queries = load_JOB_light()
    # print(len(query_paths))
    # print(query_paths)
    # query_paths.sort()
    # print(query_paths)
    # print(query_paths[60])
    # print(JOB_queries[60])

    # store_filepath = 'parallelism=0/cost_runtime/cost_runtime_a.csv'
    # title = 'Initial Postgres'
    # cost_list, runtime_list = load_cost_runtime(store_filepath)
    # print('Cost Model - Experiment 1 - Error:', compute_cost_runtime_error(cost_list, runtime_list))

    # output_filepath = 'parallelism=0/cost_model_a'
    # plot_cost_runtime(cost_list=cost_list, runtime_list=runtime_list, title=title,
    #                   output_filepath=output_filepath)

    # output_filepath = 'parallelism=0/cost_model_a_log_scale'
    # log_cost_list = [math.log(cost) for cost in cost_list]
    # log_runtime_list = [math.log(runtime) for runtime in runtime_list]
    # plot_cost_runtime(cost_list=log_cost_list, runtime_list=log_runtime_list, title=title,
    #                   output_filepath=output_filepath, log_scale=True)

    store_filepath = 'parallelism=0/cost_runtime/cost_runtime_b.csv'
    title = 'Postgres with true cards'
    cost_list, runtime_list = load_cost_runtime(store_filepath)
    print('Cost Model - Experiment 2 - Error:', compute_cost_runtime_error(cost_list, runtime_list))

    output_filepath = 'parallelism=0/cost_model_b'
    plot_cost_runtime(cost_list=cost_list, runtime_list=runtime_list, title=title,
                      output_filepath=output_filepath)

    output_filepath = 'parallelism=0/cost_model_b_log_scale'
    log_cost_list = [math.log(cost) for cost in cost_list]
    log_runtime_list = [math.log(runtime) for runtime in runtime_list]
    plot_cost_runtime(cost_list=log_cost_list, runtime_list=log_runtime_list, title=title,
                      output_filepath=output_filepath, log_scale=True)

    # store_filepath = 'parallelism=0/cost_runtime/cost_runtime_c.csv'
    # title = 'Postgres with tuned cost model'
    # cost_list, runtime_list = load_cost_runtime(store_filepath)
    # print('Cost Model - Experiment 3 - Error:', compute_cost_runtime_error(cost_list, runtime_list))

    # output_filepath = 'parallelism=0/cost_model_c'
    # plot_cost_runtime(cost_list=cost_list, runtime_list=runtime_list, title=title,
    #                   output_filepath=output_filepath)

    # output_filepath = 'parallelism=0/cost_model_c_log_scale'
    # log_cost_list = [math.log(cost) for cost in cost_list]
    # log_runtime_list = [math.log(runtime) for runtime in runtime_list]
    # plot_cost_runtime(cost_list=log_cost_list, runtime_list=log_runtime_list, title=title,
    #                   output_filepath=output_filepath, log_scale=True)

    # store_filepath = 'parallelism=0/cost_runtime/cost_runtime_d.csv'
    # title = 'Postgres with true cards and tuned cost model'
    # cost_list, runtime_list = load_cost_runtime(store_filepath)
    # print('Cost Model - Experiment 4 - Error:', compute_cost_runtime_error(cost_list, runtime_list))

    # output_filepath = 'parallelism=0/cost_model_d'
    # plot_cost_runtime(cost_list=cost_list, runtime_list=runtime_list, title=title,
    #                   output_filepath=output_filepath)

    # output_filepath = 'parallelism=0/cost_model_d_log_scale'
    # log_cost_list = [math.log(cost) for cost in cost_list]
    # log_runtime_list = [math.log(runtime) for runtime in runtime_list]
    # plot_cost_runtime(cost_list=log_cost_list, runtime_list=log_runtime_list, title=title,
    #                   output_filepath=output_filepath, log_scale=True)

    # cost_list, runtime_list = load_cost_runtime('cost_runtime_a.csv')
    # error = compute_cost_runtime_error(cost_list, runtime_list)
    # print('Cost Model - Experiment 1 - Error:', error)
    #
    # cost_list, runtime_list = load_cost_runtime('cost_runtime_b.csv')
    # error = compute_cost_runtime_error(cost_list, runtime_list)
    # print('Cost Model - Experiment 2 - Error:', error)
    #
    # cost_list, runtime_list = load_cost_runtime('cost_runtime_c.csv')
    # error = compute_cost_runtime_error(cost_list, runtime_list)
    # print('Cost Model - Experiment 3 - Error:', error)
    #
    # cost_list, runtime_list = load_cost_runtime('cost_runtime_d.csv')
    # error = compute_cost_runtime_error(cost_list, runtime_list)
    # print('Cost Model - Experiment 4 - Error:', error)

