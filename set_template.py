import sys
import sqlite3

if len(sys.argv) < 2:
    print("nope")
    sys.exit(1)

jid = sys.argv[1]

data = sys.stdin.readlines()

print ("".join(data))
print (jid)
