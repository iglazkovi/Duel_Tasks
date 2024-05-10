from subprocess import Popen, PIPE
import subprocess
from func_timeout import func_timeout


class SolException(Exception):
    pass


class Solution:
    def __init__(self, file, number, timeout):
        number = str(number)
        self.timeout = timeout
        if file[-3:] == 'cpp':
            self.language = 'C++'
            subprocess.run(["g++", file, "-o", number])
            self.proc = Popen(['./' + number], stdin=PIPE, stdout=PIPE, shell=True, stderr=PIPE)
        else:
            self.language = 'python'
            self.proc = Popen(f"python '{file}'", stdin=PIPE, stdout=PIPE, shell=True, stderr=PIPE)
        self.file = file
        self.text = ""

    def read_string(self):
        try:
            if not self.text:
                func_timeout(self.timeout, self.input)
            lst = self.text.split()
            self.text = ' '.join(lst[1:])
            return lst[0]
        except:
            self.proc.kill()
            raise SolException(self.file)

    def read_line(self):
        try:
            if not self.text:
                func_timeout(self.timeout, self.input)
            ans = self.text
            self.text = ''
            return ans
        except:
            self.proc.kill()
            raise SolException(self.file)

    def read_int(self):
        try:
            if not self.text:
                func_timeout(self.timeout, self.input)
            lst = self.text.split()
            self.text = ' '.join(lst[1:])
            try:
                return int(lst[0])
            except ValueError:
                self.proc.kill()
                raise SolException(self.file)
        except:
            self.proc.kill()
            raise SolException(self.file)

    def read_float(self):
        try:
            if not self.text:
                func_timeout(self.timeout, self.input)
            lst = self.text.split()
            self.text = ' '.join(lst[1:])
            try:
                return float(lst[0])
            except ValueError:
                self.proc.kill()
                raise SolException(self.file)
        except:
            self.proc.kill()
            raise SolException(self.file)

    def input(self):
        self.text = self.proc.stdout.readline().decode("utf-8").strip()
        if self.proc.returncode:
            self.proc.kill()
            raise SolException(self.file)
        if not self.text:
            self.proc.kill()
            raise SolException(self.file)

    def output(self, text):
        text = str(text)
        self.proc.stdin.write((text + '\n').encode())
        self.proc.stdin.flush()

# sol1 = Solution("test.py")
# sol2 = Solution("test2.py")
#
# for i in range(4):
#     ans1 = sol1.read_string()
#     ans2 = sol2.read_string()
#     print(ans1, ans2)
