# ZeroNights HackQuest 2021 | Collapse

# Description

> So Einstein was wrong when he said, "God does not play dice." Consideration of black holes suggests, not only that God does play dice, but that he sometimes confuses us by throwing them where they can't be seen. Stephen Hawking
> 
> Note: you might need to install `libgomp1`, if you are using Ubuntu.
> 
> `nc quantum.kelte.cc 17171`
> 
> Flag is human readable. Format: `ZN{[A-Za-z0-9_]+}`.
> 
> Files: service.zip

# Solution

TBD

Example solver: [solver.py](solver.py)

Note: some symbols may be recognized less accurately. In my case there are only two pairs: `OQ` and `a_`. Since the flag is human readable, we can recover the correct symbols:

```
$ python3 solver.py quantum.kelte.cc
ZN{Ou4NtuMaH3ll0aw0RLDa2021}
   Q      _     _     _ 
```

# Flag

`ZN{Qu4NtuM_H3ll0_w0RLD_2021}`
