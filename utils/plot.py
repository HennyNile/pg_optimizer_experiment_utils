from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

plt.switch_backend('agg')


def plot_cost_runtime(cost_list, runtime_list, title, output_filepath, log_scale=False):
    regressor = LinearRegression()
    regressor.fit([[cost] for cost in cost_list], runtime_list)
    y_pred = regressor.predict([[cost] for cost in cost_list])

    plt.figure()
    plt.scatter(cost_list, runtime_list)
    plt.plot(cost_list, y_pred, color='g')
    plt.title(title)
    if log_scale:
        plt.xlabel('cost [log scale]')
        plt.ylabel('runtime [ms] [log scale]')
    else:
        plt.xlabel('cost')
        plt.ylabel('runtime [ms]')
    plt.savefig(output_filepath)
    plt.show()


if __name__ == '__main__':
    plot_cost_runtime([1], [1], 'test', 'test')
