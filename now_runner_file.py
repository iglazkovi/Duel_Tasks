from run_files.runner import Solution
from run_files.runner import SolException

sol1 = Solution
sol2 = Solution


def run(sol1_name, sol2_name):
    global sol1, sol2
    try:
        sol1 = Solution(sol1_name, 1, 1)
        sol2 = Solution(sol2_name, 2, 1)
        n = 10
        sol1.output(n)
        sol2.output(n)
        cnt1 = 0
        cnt2 = 0
        dependencies = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
        for i in range(n):
            ans1 = sol1.read_line()
            ans2 = sol2.read_line()
            if ans1 not in dependencies.keys():
                if ans2 not in dependencies.keys():
                    return 0
                else:
                    return -1
            elif ans2 not in dependencies.keys():
                return -2
            else:
                if ans1 == ans2: continue
                if dependencies[ans1] == ans2:
                    cnt1 += 1
                else:
                    cnt2 += 1

        if cnt1 > cnt2:
            return 1
        elif cnt1 < cnt2:
            return 2
        return 0

    except SolException as e:
        sol1.proc.kill()
        sol2.proc.kill()
        if str(e) == sol1_name:
            return -1
        else:
            return -2
