import sys
import re

class fst():
    def __init__(self, filename):
        self.fst = dict()
        self.maxlen = 0 # maximum length of input
        self.read(filename)

    def read(self, filename):
        ln = 0
        fo = open(filename)
        for line in fo:
            ln += 1
            if line == "\n":
                continue
            line = line[:-1]
            if not re.search("^\S+ \S+ \S+$", line):
                sys.exit("Syntax error on line %d: %s" % (ln, line))
            s1, s0, c = line.split(" ")
            if c not in self.fst:
                self.fst[c] = dict()
            s1 = s1.split(",")
            for s0 in s0.split(","):
                if s0 not in self.fst[c]:
                    self.fst[c][s0] = set()
                self.fst[c][s0].update(s1)
            if len(c) > self.maxlen:
                self.maxlen = len(c)
        fo.close()

    def find(self, line, i, s0):
        for j in range(self.maxlen):
            j += i + 1
            if j > len(line):
                break
            w = line[i:j]
            if w not in self.fst:
                continue
            if s0 not in self.fst[w]:
                continue
            for s1 in self.fst[w][s0]:
                for j, s1 in self.find(line, j, s1):
                    yield (len(w) + j, s1)
        yield (0, s0)

    def finditer(self, line):
        for i in range(len(line)):
            m = list(self.find(line, i, "0"))
            j, st = max(self.find(line, i, "0"))
            yield (i, i + j, st) if j else None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s fst text" % sys.argv[0])
    fst = fst(sys.argv[1])
    fo = open(sys.argv[2])
    for line in fo:
        line = line.strip()
        print(line)
        for m in fst.finditer(line):
            if not m:
                continue
            i, j, st = m
            print(line[i:j], st)
    fo.close()
