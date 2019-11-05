import random

def monte_carlo_approximation(num_points):
    domain_area = 4
    inside_counter = 0
    for i in range(num_points):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1.0:
            inside_counter += 1
    return (inside_counter / num_points) * domain_area

if __name__ == '__main__':
    print(monte_carlo_approximation(10))
    print(monte_carlo_approximation(100))
    print(monte_carlo_approximation(1000))
    print(monte_carlo_approximation(1000000))