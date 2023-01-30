from typing import List, Tuple, Callable
import timeit
import time

from nbprint import Printer


def nullfunc(*args, **kwargs):
    """
    A function that takes in any arguments but does absolutely nothing.
    In this situation, used to test the speed of not printing at all.
    """
    return


def triangle_number_print(number: int, print_func: Callable[..., None]) -> None:
    """
    For benchmark purposes, print the additive factorials for numbers from 1 to `number`.
    print_func is the function that is used for printing.
    """
    for j in range(1, number + 1):
        sum = 0
        for i in range(1, j + 1):
            sum += i
        print_func(sum)
    

def print_up_to(number: int, print_func: Callable[..., None]) -> None:
    for i in range(1, number + 1):
        print_func(i)


def benchmark_prints(print_funcs: List[Callable[..., None]], depth: int, delay: float) -> Tuple[List[float], List[float], List[float]]:
    """
    Run the print functions through two benchmarks and return a tuple with two lists of times, and a list with one element representing total benchmark time.
    Each element in the list correlates to the function in the same index of the passed-in list.
    The higher the `depth` number, the longer the benchmark will take, and the more times each function will be called.
    Delay is used to add a delay between each print function benchmark.
    """
    total_before = timeit.default_timer()
    func_times = ([], [], [])
    for func in print_funcs:
        before = timeit.default_timer()
        triangle_number_print(depth, func)
        func_times[0].append(timeit.default_timer() - before)
        time.sleep(delay)

    for func in print_funcs:
        before = timeit.default_timer()
        print_up_to(depth * 5, func)
        func_times[1].append(timeit.default_timer() - before)
        time.sleep(delay)

    func_times[2].append(timeit.default_timer() - total_before)

    return func_times


def print_results(times: Tuple[List[float], List[float], List[float]]):
    """
    Print the results of the benchmarks.
    """
    total_time = times[2][0]

    std1 = times[0][0]
    std2 = times[1][0]
    mt1 = times[0][1]
    mt2 = times[1][1]
    no1 = times[0][2]
    no2 = times[1][2]

    ratio1 = ((std1 - mt1) / mt1) * 100
    ratio2 = ((std2 - mt2) / mt2) * 100

    print("==========================================================")
    print("----------------------------------------------------------")
    print("Results for the I/O and CPU compound benchmark:")
    print("----------------------------------------------------------")
    print(f"Standard print: {std1:.3f} s")
    print(f"Multithreaded (non-blocking) print: {mt1:.3f} s")
    print(f"No printing: {no1:.3f} s")
    print()
    print(f"Under both CPU and I/O load, multithreaded print is {ratio1:.3f}% faster than standard printing.")
    print()
    print()
    print("----------------------------------------------------------")
    print("Results for I/O bound benchmark:")
    print("----------------------------------------------------------")
    print(f"Standard print: {std2:.3f} s")
    print(f"Multithreaded (non-blocking) print: {mt2:.3f} s")
    print(f"No printing: {no2:.3f} s")
    print()
    print(f"Under both CPU and I/O load, multithreaded print is {ratio2:.3f}% faster than standard printing.")
    print()
    print()
    print(f"Total time to complete benchmark: {total_time:.3f}")



def main():
    mt_printer = Printer()

    funcs = [print, mt_printer.print, nullfunc]
    test_depth = 25000
    delay = 15   # Delay needs to be longer than the time it would take to do the actual print

    times = benchmark_prints(funcs, test_depth, delay)

    mt_printer.end()

    print_results(times)



if __name__ == "__main__":
    main()
