from string import atoi
from struct import pack
import sys
filename=sys.argv[1]
name,extention=filename.split(".")
f=open(filename,"rb")
mask_begin=".word "
mask_end="\r\n\r\n@}}BLOCK(%s)" % name
all=f.read()
f.close()
all_temp=all[all.find("Total"):]
all_temp=all_temp[all_temp.find("="):]
size=all_temp[2:all_temp.find("\r\n")]
b=all.find(mask_begin)
e=all.find(mask_end)
all=all[b:e]
all=all.replace(".word ","")
all=all.replace("\r\n\r\n\t",",")
all=all.replace("\r\n\t",",")
all=all.split(",")
f=open(sys.argv[2],"wb")
f.write(pack("I",atoi(size,10)))
for i in xrange(len(all)):
    f.write(pack("I",atoi(all[i],16)))
f.close()
print "done"
