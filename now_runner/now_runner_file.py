from run_files.runner import Solution
from run_files.runner import SolException

sol1 = Solution
sol2 = Solution


def run(sol1_name, sol2_name):
    global sol1, sol2
    try:
        sol1 = Solution(sol1_name, 1, 1)
        sol2 = Solution(sol2_name, 2, 1)
        x1 = sol1.read_int()
        x2 = sol2.read_int()
        sol1.proc.kill()
        sol2.proc.kill()
        if x1 < x2:
            return 1
        else:
            return 2
    except SolException as e:
        sol1.proc.kill()
        sol2.proc.kill()
        if str(e) == sol1_name:
            return -1
        else:
            return -2
