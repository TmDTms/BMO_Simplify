from miasm.analysis.binary import Container
from miasm.analysis.machine import Machine
from miasm.core.locationdb import LocationDB

# Load the binary and set up the necessary components
target_binary = open('example/samples/box_upx.exe', 'rb')
loc_db = LocationDB()
cont = Container.from_stream(target_binary, loc_db)
machine = Machine(cont.arch)
mdis = machine.dis_engine(cont.bin_stream, loc_db=cont.loc_db)

# Disassemble and analyze the binary
target_addr = cont.entry_point
asmcfg = mdis.dis_multiblock(target_addr)

# Extract assembly instructions and operands
instructions = []
for block in asmcfg.blocks:
    for line in block.lines:
        instructions.append(line)

# Generate AST based on the extracted information
ast_nodes = []
for instr in instructions:
    opcode = instr.name
    operands = [str(op) for op in instr.args]
    ast_node = {'opcode': opcode, 'operands': operands}
    ast_nodes.append(ast_node)

# Print the generated AST
for node in ast_nodes:
    print(node)