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

Be careful: some symbols may be recognized less accurately. In my case there are only two indistinguishable pairs: `OQ` and `a_`. Solver prints them all, but since the flag is human readable, we can find out the valid symbols:

```
$ python3 solver.py quantum.kelte.cc
ZN{Ou4NtuMaH3ll0aw0RLDa2021}
ZN{Qu4NtuM_H3ll0_w0RLD_2021}
```

# Flag

`ZN{Qu4NtuM_H3ll0_w0RLD_2021}`
