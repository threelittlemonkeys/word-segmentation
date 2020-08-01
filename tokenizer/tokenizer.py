import sys
import re

from tokenizer_en import tokenize_en
from tokenizer_ko import tokenize_ko

RE_SPACE = re.compile("[\s\u3000]+") # whitespace
RE_NON_ALNUM = re.compile("([^ a-z0-9\u4E00-\u9FFF\uAC00-\uD7AF])", re.I) # non-alphanumeric

def normalize(line):
    line = RE_NON_ALNUM.sub(" \\1 ", line)
    line = RE_SPACE.sub(" ", line)
    line = line.strip()
    return line

def tokenize(lang, filename):
    fo = open(filename)
    for line in fo:
        line = normalize(line)
        line = tokenize_en(line)
        line = tokenize_ko(line)
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s lang text" % sys.argv[0])
    tokenize(*sys.argv[1:])