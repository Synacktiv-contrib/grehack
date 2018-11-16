# coding=utf-8


from miasm2.analysis.sandbox import Sandbox_Linux_x86_64
from miasm2.analysis.machine import Machine
from miasm2.os_dep.linux_stdlib import linobjs
from miasm2.analysis.binary import Container
from miasm2.core.utils import hexdump
from pwn import *


step0 = open("the_band_patched_jmp").read()[0x2E048:0x2EE98]
step1 = open("the_band_patched_jmp").read()[0x2EE98:0x2F130]
step2 = open("the_band_patched_jmp").read()[0x2F130:0x31DB8]
lookup_table_step0 = []
lookup_table_step1 = []
lookup_table_step2 = []
lookup_table_stepX = []
lookup_table = None
bytecode = None


def GetMem(jitter):
    global lookup_table
    lookup_table.append(jitter.cpu.get_mem(jitter.cpu.RAX, 16))
    return True


def GetBytecode(jitter):
    try:
        jitter.cpu.RAX = (u8(bytecode[jitter.cpu.RDI/8]) >> ((7 - jitter.cpu.RDI) % 8)) & 1
    except:
        pass
    return True


def Malloc(jitter):
    jitter.cpu.RAX = linobjs.heap.alloc(sb.jitter, 0x10)  # simulate malloc (the jmp malloc was rewritten by a ret to prevent MIASM error)
    return True


def emulate(sb, x, bc, lt):
    global bytecode, lookup_table
    bytecode = bc
    lookup_table = lt
    p = log.progress("emulating step%d" % x)
    for i in range((len(bytecode) * 8) - 1):
        if i % 100 == 0:
            p.status("%d/%d" % (i, (len(bytecode) * 8) - 1))
        sb.call(0x5DD9, i)  # VMDecodeInstruction
    # with open("all_steps", "w") as f:
    #     import json
    #     json.dump(lt, f)
    print(lt)


parser = Sandbox_Linux_x86_64.parser(description="ELF sandboxer")
parser.add_argument("filename", help="ELF Filename")
options = parser.parse_args()
sb = Sandbox_Linux_x86_64(options.filename, options, globals())
machine = Machine('x86_64')
cont = Container.from_stream(open(options.filename))
mdis = machine.dis_engine(cont.bin_stream)
sb.jitter.add_breakpoint(0x2C87F, GetMem)  # break on return of VMDecodeInstruction
sb.jitter.add_breakpoint(0x21B0, Malloc)  # Break on call to _malloc because for some reason MIASM can't find the symbol
sb.jitter.add_breakpoint(0x4A9C, GetBytecode)  # break on return of VMDecodeBytecode to return the good value that could not be loaded because of global variable not set
emulate(sb, 0, step0, lookup_table_step0)
emulate(sb, 1, step1, lookup_table_step1)
emulate(sb, 2, step2, lookup_table_step2)
emulate(sb, -1, step1 + step2, lookup_table_stepX)
