# Script for placing all patents on a single line
# Callable from linux shell

import sys as sys
from re import sub

if __name__ == "__main__":
    patent_separator = ''
    
    # stdin is a file object, "standard input"
    for singlePatentTag in sys.stdin.readlines():
        singlePatentTag = sub('\n', ' <endline> ', singlePatentTag)
        singlePatentTag = sub('\</us-patent-grant\>', '\n', singlePatentTag)
        patent_separator += singlePatentTag
        
sys.stdout.write(patent_separator)