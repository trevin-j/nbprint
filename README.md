# NBPrint

A simple experiment in Python to test a non-blocking print function. The print works by submitting arguments for a print statement into a queue, which gets executed in a separate thread.

## Usage

Using the non-blocking print statement is very easy, and the non-blocking print accepts all of the same arguments as the builtin print function.

First, import the `Printer` class.

```Python
from nbprint import Printer
```

Next, before usage you must initialize the Printer object. This starts the thread that will be doing all the printing.

```Python
printer = Printer()
```

At this point, you can use the `printer.print` function to print to the terminal. You can use *any* argument or keyword argument that the builtin print supports.

```Python
printer.print("Hello,", "world", end="!\n", flush=True)
```

Finally, before the program exits, you *must* end the printer. This will send a message to the printer thread that the program is done, and it will close the thread. Note that this call will block the main thread up until the printer finishes printing everything that is on the queue.

```Python
printer.end()
```

## Benchmarking

You can run a script to test the speed difference between the standard print, the non-blocking print, and no printing. The benchmark works by repeatedly printing and checking the amount of time it takes to finish. Note that this doesn't keep track of the amount of time it takes to finish printing, rather just the time it takes to finish the calculations with the call to print. This means the time will likely stop before the print thread has actually finished printing everything in the queue.

Run the script via `py bench.py`. You may want to tweak some values in the script, but in general it should give you an idea of the performance differences. Following is an example output of the benchmark.

```
==========================================================
----------------------------------------------------------
Results for the I/O and CPU compound benchmark:
----------------------------------------------------------
Standard print: 13.068 s
Multithreaded (non-blocking) print: 10.670 s
No printing: 9.838 s

Under both CPU and I/O load, multithreaded print is 22.473% faster than standard printing.


----------------------------------------------------------
Results for I/O bound benchmark:
----------------------------------------------------------
Standard print: 6.469 s
Multithreaded (non-blocking) print: 0.155 s
No printing: 0.010 s

Under both CPU and I/O load, multithreaded print is 4073.920% faster than standard printing.


Total time to complete benchmark: 130.212
```

## Notes and limitations

This project is just a simple experiment to see the potential performance differences if the print function is used in a separate thread. In reality, any performance gains would likely be negligible as in most situations you wouldn't be constantly printing. That said, here are some notes and limitations:

* Because prints are put into a queue before printing in another thread, the printing can fall behind and become unsynchronized. However, each print will still be in proper order, and will eventually catch up at points of less printing.

* Failing to call `Printer.end` before exiting will cause the program to hang due to an open thread. Originally the idea was to implement the `__del__` method to automatically close at application end. However, since the printing thread is still open, the interpreter doesn't exit and won't call `del`.

* I'm looking into the idea of concatenating multiple queued prints into a single print to attempt to improve performance.

* I'm also looking into the idea of instead of a queue, having one queued print at a time. This would mean losing some calls to preserve synchronization and still allowing the better performance.

This project was just a simple experiment to test multithreaded printing, and it is unlikely I will spend much more time tweaking this project.

