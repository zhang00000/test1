from subgradient import subgradient_2, next_y_from_v


def lloyd_max(y0, max_step, subgradient_max_step, step_size_func, eps=0.693147, weight=None):
    history = []
    y = y0
    for step in range(max_step):
        g, v = subgradient_2(
            y, subgradient_max_step, step_size_func=step_size_func, eps=eps, weight=weight
        )
        y = next_y_from_v(v, y, weight)
        print(step, g)
        print(y)
        history.append((g, y, v))
    return g, y, v, history

