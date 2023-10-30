import graphviz
from Tools.scripts.dutree import display

from miasm.core.locationdb import LocationDB
from miasm.analysis.machine import Machine
from miasm.analysis.binary import Container

fdesc = open('example/samples/box_upx.exe', 'rb')
loc_db = LocationDB()
cont = Container.from_stream(fdesc, loc_db)
machine = Machine(cont.arch)

print('='*10 + 'Print cont.arch' + '='*10)
print(cont.arch)

mdis = machine.dis_engine(cont.bin_stream, loc_db=cont.loc_db)
addr = cont.entry_point
asmcfg = mdis.dis_multiblock(addr)
tree_lst = []

print('='*10 + 'ASM Block' + '='*10)

for block in asmcfg.blocks:
    print(block)
    tree_lst.append(str(block) + '\n\n')

print('=' * 30)
fdesc.close()
with open('bin_disasm_tree.txt', 'w') as f:
    f.writelines(tree_lst)

with open('dis_binary_tree.dot') as f:
    dot_graph = f.read()
graph = graphviz.Source(dot_graph)
graph.view()