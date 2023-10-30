from __future__ import print_function
import graphviz

from future.utils import viewvalues
from miasm.analysis.binary import Container
from miasm.analysis.machine import Machine
from miasm.core.locationdb import LocationDB

#####################################
# Common section from dis_binary.py #
#####################################

fdesc = open('../samples/box_upx.exe', 'rb')
loc_db = LocationDB()

cont = Container.from_stream(fdesc, loc_db)

machine = Machine(cont.arch)

mdis = machine.dis_engine(cont.bin_stream, loc_db=cont.loc_db)

addr = cont.entry_point
asmcfg = mdis.dis_multiblock(addr)

#####################################
#    End common section             #
#####################################

# Get an IRA converter
# The sub call are modelised by default operators
# call_func_ret and call_func_stack
lifter = machine.lifter_model_call(mdis.loc_db)

# Get the IR of the asmcfg
ircfg = lifter.new_ircfg_from_asmcfg(asmcfg)

# Display each IR basic blocks
for irblock in viewvalues(ircfg.blocks):
    print(irblock)

# Output ir control flow graph in a dot file
open('bin_lifter_model_call_cfg.dot', 'w').write(ircfg.dot())
with open("bin_lifter_model_call_cfg.dot") as f:
    dot_graph = f.read()
src = graphviz.Source(dot_graph)
src.view()
