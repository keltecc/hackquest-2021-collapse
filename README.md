# ZeroNights HackQuest 2021 | Collapse

A quantum challenge from ZeroNights HackQuest 2021.

# Description

> So Einstein was wrong when he said, "God does not play dice." Consideration of black holes suggests, not only that God does play dice, but that he sometimes confuses us by throwing them where they can't be seen.
> 
> `nc quantum.kelte.cc 17171`
> 
> _Note: you might need to install GNU OpenMP library (`libgomp`), example for Ubuntu: `apt install libgomp1`._
> 
> _Note: the flag is human readable, format: `ZN{[A-Za-z0-9_]+}`._

# Files

- [service.zip](service.zip)

# Solution

TBD

Example solver: [solver.py](solver.py)

Model generation:

```
$ time python3 solver.py                 
Reading line... [ 5000 / 5000 ]
Model saved
python3 solver.py  1.95s user 0.16s system 0% cpu 6:32.67 total
```

Flag reconstruction:

```
$ time python3 solver.py quantum.kelte.cc
Model loaded
Reading line... [ 5000 / 5000 ]
Counters loaded
{'ZN{Qu4NtuM_H3ll0_w0RLD_2021}'}
python3 solver.py quantum.kelte.cc  4.86s user 0.84s system 2% cpu 3:47.14 total
```

# Flag

`ZN{Qu4NtuM_H3ll0_w0RLD_2021}`
