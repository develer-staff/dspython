# create a new stackless version include.

SLP_MAJOR = "3.1b3"

import sys, os, time
pth, script = os.path.split(sys.argv[0])
fname = os.path.join(pth, "../Stackless/stackless_version.h")

content = """\
/*
 * Stackless Python version string
 * created at %s by %s
 */

/* keep this entry up-to-date */
#define STACKLESS_VERSION "%s %02d%02d%02d"
"""

y, m, d = time.localtime()[:3]
tims = time.ctime(time.time())
file(fname, "w").write(content % (tims, script, SLP_MAJOR, y%100, m, d) )
                     