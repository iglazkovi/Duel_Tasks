# Smart Games

A system for creating contests in competetive programming with interactive tasks of a new type (duel tasks).

## Duel Tasks
Unlike regular interactive tasks, in duel tasks the participants' solutions collide directly. Instead of interacting with a standard interactor, a participant's solution interacts with another participant's solution. Compliance with the interaction protocol is checked in the runner - an analogue of the interactor program in a regular task. At the same time, from the participant's point of view, the way the program is written is no different.

An example of the implementation of the game Rock-Paper-Scissors can be found in the source files:
- [Runner file] (now_runner_file.py)
- [Solutions files] (run_files)

## How to write runners

```python
from run_files.runner import Solution
from run_files.runner import SolException

sol1 = Solution
sol2 = Solution


def run(sol1_name, sol2_name):
    global sol1, sol2
    try:
        sol1 = Solution(sol1_name, 1, 1)
        sol2 = Solution(sol2_name, 2, 1)
        
        #Here you describe all interactions via the output and read methods

    except SolException as e:
        sol1.proc.kill()
        sol2.proc.kill()
        if str(e) == sol1_name:
            return -1
        else:
            return -2

```


#### The runner must return one of the following values:
- 1 - player 1 wins
- 2 - player 2 wins
- -1 - player 1 violated the interaction protocol
- -2 - player 2 violated the interaction protocol


## Supported languages
- С++
- Python


