# cstack compression
# getting an idea of effectivity
# Christian Tismer
# 2002-09-18

import stackless, struct, sys

def get_stack(t):
	st = t.frame.cstack
	stack = struct.unpack("%di" % st.size, str(st))
	return stack

class CStack:
    def __init__(self, template, values, patches):
        self.template = template
        self.values = values
        self.patches = patches

class Compressor:
    # template stacks, indexed by size
    templates = {}
    # stack patches, indexed by value
    patches = {}

    def compress(self, cstack):
        data = get_stack(cstack)
        template = self.templates.get(len(data))
        if not template:
            ret = CStack(data, (), ())
            self.templates[len(data)] = data
            return ret
        values = []
        patch = []
        for i in range(len(data)):
            val = data[i]
            if template[i] == val:
                continue
            try:
                p = values.index(val)
            except ValueError:
                p = len(values)
                values.append(val)
            patch.append( (i, p) )
        patch = tuple(patch)
        p2 = self.patches.get(patch)
        if p2:
            patch = p2
        else:
            self.patches[patch] = patch
        return CStack(template, values, patch)

def test(n=100):
	global comp
	comp = Compressor()
	chan = stackless.channel()
	def f():
		chan.send(42)
	for i in range(n):
		t = stackless.tasklet(f)()
		t.run()
	res = []
	t = chan.queue
	for i in range(chan.balance):
		res.append(comp.compress(t))
		t = t.next
	print "Size of uncompressed stack:", len(res[-1].template)
	print "Size of compressed stack:", len(res[-1].values)
	print "Number of templates:", len(comp.templates)
	print "Patch lengths and patterns:"
	for p in comp.patches:
		print len(p), p

if __name__ == "__main__":
	test()
	