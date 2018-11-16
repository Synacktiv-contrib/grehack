# coding=utf-8


from pwn import *
import traceback
import copy
import pprint


VM_OBJ_REG_RESULT = 9
VM_OBJ_REG_IP = 0xa
VM_OBJ_REG_FLAGS = 0xb
VM_OBJ_ORCHESTRATOR = 0x1 << 12
VM_OBJ_DECODER = VM_OBJ_ORCHESTRATOR | 0x1 << 8
VM_OBJ_EXECUTOR0 = VM_OBJ_DECODER | 0xa
VM_OBJ_EXECUTOR1 = VM_OBJ_DECODER | 0xb
VM_OBJ_START = 0x1 << 20
VM_OBJ_END = 0xf << 20
VM_OBJ_INPUT = 0x1 << 8


def function(func):
    def wrap(self, core):
        try:
            self.prologue(core)
            ret = func(self, core)
            self.epilogue()
        except Exception as e:
            print("function", self.ctx, func)
            traceback.print_exc()
            raise e
        return ret
    return wrap


class Cpu(object):
    def __init__(self, step, offset=0):
        self.step = step
        self.pc = offset
        self.silent = False
        self.lookup_table = []
        self.bytecode = ""
        self.opcodes = ["ADD", "JMPCond", "ReadSTDIN", "WriteSTDOUT", "Exit", "NEG", "NOP",
                        "MemMalloc", "MemMove", "AND", "MemFree", "DecodeInt"]
        self.prepare()

    def prepare(self):
        with open("lookup_table_step%s" % self.step) as f:
            self.lookup_table += eval(f.read())
        bytecode = []
        with open("the_band_patched_jmp") as f:
            content = f.read()
            bytecode.append(content[0x2E048:0x2EE98])
            bytecode.append(content[0x2EE98:0x2F130])
            bytecode.append(content[0x2F130:0x31188])
        self.bytecode = bytecode[self.step]
        self.objs = {}
        for i in range(13):
            self.objs[i] = 0
        self.objs[VM_OBJ_DECODER] = 0
        self.objs[VM_OBJ_EXECUTOR0] = 0
        self.objs[VM_OBJ_EXECUTOR1] = 0

    def MakeObj(self, to, length):
        idx = random.randint(VM_OBJ_START, VM_OBJ_END)
        for i in range(length):
            self.objs[idx+i] = 0
        self.objs[to] = idx
        return idx

    def DecodeBytecode(self, offset):
        return (u8(self.bytecode[offset/8]) >> (7 - offset % 8)) & 1

    def FetchOpcode(self):
        x = self.DecodeBytecode(self.pc)
        self.pc += 2
        return x

    def FetchInstruction(self):
        regs = [None] * 6
        for i in range(3):
            regs[i * 2] = 0
            for _ in range(3):
                x = 2 * regs[i * 2]
                regs[i * 2] = x + self.FetchOpcode()
        for i in range(3):
            regs[(i * 2) + 1] = 0
            for _ in range(9):
                x = 2 * regs[(i * 2) + 1]
                regs[(i * 2) + 1] = x + self.FetchOpcode()
        return regs

    def DecodeInstruction(self, offset):
        return unpack_many(self.lookup_table[offset], 32, endian='little', sign=False)

    def prologue(self, core):
        self.pc = self.objs[VM_OBJ_REG_IP] + core
        self.ctx = self.FetchInstruction()
        log.debug(self.ctx)

    def epilogue(self):
        for i in range(5):
            self.FetchOpcode()

    @function
    def ADD(self, core):
        ret = ""
        # first value
        if self.ctx[0] == 1:
            v0 = self.objs[self.ctx[1]]
        else:
            off = self.objs[self.ctx[1]]
            v0 = self.objs[off]
        # second value
        if self.ctx[2] == 1:
            v1 = self.objs[self.ctx[3]]
            fmt = "obj[0x%02x]" % (self.ctx[3])
        elif self.ctx[2] == 6:
            v1 = self.ctx[3]
            fmt = "0x%02x" % self.ctx[3]
        elif self.ctx[2] == 7:
            v1 = -self.ctx[3]
            fmt = "-0x%02x" % self.ctx[3]
        else:
            v1 = self.objs[self.objs[self.ctx[3]]]
            fmt = "obj[0x%02x]" % self.objs[self.ctx[3]]
        if self.ctx[0] == 1:
            ret += "EXECUTOR%d: add obj[0x%02x], %s = 0x%04x" % (core - 10, self.ctx[1], fmt, v1 + v0)
            self.objs[self.ctx[1]] = v1 + v0
        else:
            ret += "EXECUTOR%d: add obj[0x%02x], %s, 0x%04x = 0x%04x" % (core - 10, off, fmt, v0, v1 + v0)
            self.objs[off] = v1 + v0
        return ret

    @function
    def JMPCond(self, core):
        ret = ""
        jmp_table = [0] * 3
        for i in range(3):
            if self.ctx[2*i] == 6:
                jmp_table[i] = self.ctx[2*i + 1]
            elif self.ctx[2*i] == 7:
                jmp_table[i] = -self.ctx[2*i + 1]
        flags = self.objs[VM_OBJ_REG_FLAGS]
        if flags > 0:
            to = jmp_table[2]
        elif flags < 0:
            to = jmp_table[1]
        else:
            to = jmp_table[0]
        self.objs[VM_OBJ_DECODER | core] = to
        self.lookup_table[(self.objs[VM_OBJ_DECODER | core] * 41) + self.objs[VM_OBJ_REG_IP]]
        ret += "EXECUTOR%d: jmp %d (0x%04x)" % (core - 10, to, ((self.objs[VM_OBJ_DECODER | core] * 41) + self.objs[VM_OBJ_REG_IP]) / 8)
        return ret

    @function
    def ReadSTDIN(self, core):
        ret = ""
        if self.ctx[0] == 1:
            v0 = self.objs[self.ctx[1]]
        else:
            v0 = self.ctx[1]
        if self.ctx[2] == 2:
            v1 = self.objs[self.ctx[3]]
        else:
            v1 = 0
        x = raw_input(">>> give me %d char: " % v0)
        ret += "EXECUTOR%d: Read obj[0x%04x], %s" % (core - 10, v1, x[:5] + "..." if len(x) > 10 else x[:-1])
        for i, l in enumerate(x):
            self.objs[v1+i] = ord(l)
        return ret

    @function
    def WriteSTDOUT(self, core):
        ret = ""
        if self.ctx[0] == 2:
            fmt = "0x%x" % self.objs[self.objs[self.ctx[1]]]
        elif self.ctx[0] == 6:
            fmt = "%c" % self.ctx[1]
        elif self.ctx[0] == 1:
            fmt = "0x%08x" % self.objs[self.ctx[1]]
        else:
            fmt = ""
        ret += "EXECUTOR%d: Write %s" % (core - 10, fmt)
        return ret

    @function
    def Exit(self, core):
        ret = ""
        if self.ctx[0] == 1:
            v0 = self.objs[self.ctx[1]]
        else:
            v0 = self.ctx[1]
        self.objs[VM_OBJ_REG_RESULT] = v0
        self.objs[VM_OBJ_DECODER | core] = 0xffffffff
        ret += "EXECUTOR%d: exit(0x%02x)" % (core - 10, self.objs[VM_OBJ_REG_RESULT])
        return ret

    @function
    def NEG(self, core):
        ret = ""
        v0 = self.objs[self.ctx[1]]
        ret += "EXECUTOR%d: neg obj[0x%02x] = 0x%02x" % (core - 10, self.ctx[1], -v0)
        self.objs[self.ctx[1]] = -v0
        return ret

    @function
    def NOP(self, core):
        return "EXECUTOR%d: NOP" % (core - 10)

    @function
    def MemMalloc(self, core):
        ret = ""
        # offset of the object where to put the new object offset
        if self.ctx[0] == 1:
            v0 = self.ctx[1]
        else:
            v0 = self.objs[self.ctx[1]]
        # length of the new object
        if self.ctx[2] == 1:
            v1 = self.objs[self.ctx[3]]
        elif self.ctx[2] == 6:
            v1 = self.ctx[3]
        else:
            v1 = self.objs[self.objs[self.ctx[3]]]
        idx = self.MakeObj(v0, v1)
        ret += "EXECUTOR%d: alloc obj[0x%x], 0x%02x = 0x%06x" % (core - 10, v0, v1, idx)
        return ret

    @function
    def MemMove(self, core):
        ret = ""
        # offset of the object where to put a value
        if self.ctx[0] == 1:
            v0 = self.ctx[1]
        else:
            v0 = self.objs[self.ctx[1]]
        # value to put in the object (can be an immediate or an offset to an object)
        if self.ctx[2] == 1:
            v1 = self.objs[self.ctx[3]]
            fmt = "obj[0x%02x] = 0x%02x" % (self.ctx[3], v1)
        elif self.ctx[2] == 6:
            v1 = self.ctx[3]
            fmt = "0x%02x" % self.ctx[3]
        elif self.ctx[2] == 7:
            v1 = -self.ctx[3]
            fmt = "-0x%02x" % self.ctx[3]
        else:
            v1 = self.objs[self.objs[self.ctx[3]]]
            fmt = "obj[0x%02x] = 0x%02x" % (self.objs[self.ctx[3]], v1)
        ret += "EXECUTOR%d: mov obj[0x%02x], %s" % (core - 10, v0, fmt)
        self.objs[v0] = v1
        return ret

    @function
    def AND(self, core):
        ret = ""
        # the first value
        if self.ctx[0] == 1:
            v0 = self.objs[self.ctx[1]]
        else:
            off = self.objs[self.ctx[1]]
            v0 = self.objs[off]
        # the second value
        if self.ctx[2] == 1:
            v1 = self.objs[self.ctx[3]]
            fmt = "obj[0x%02x] = 0x%02x" % (self.ctx[3], v1)
        elif self.ctx[2] == 6:
            v1 = self.ctx[3]
            fmt = "0x%02x" % self.ctx[3]
        elif self.ctx[2] == 7:
            v1 = -self.ctx[3]
            fmt = "-0x%02x" % self.ctx[3]
        else:
            v1 = self.objs[self.objs[self.ctx[3]]]
            fmt = "obj[0x%02x] = 0x%02x" % (self.objs[self.ctx[3]], v1)
        if self.ctx[0] == 1:
            ret += "EXECUTOR%d: and obj[0x%x], 0x%02x, %s" % (core - 10, self.ctx[1], v0, fmt)
            self.objs[self.ctx[1]] = v0 & v1
        else:
            ret += "EXECUTOR%d: and obj[0x%x], 0x%02x, %s" % (core - 10, off, v0, fmt)
            self.objs[off] = v0 & v1
        return ret

    @function
    def MemFree(self, core):
        ret = ""
        if self.ctx[0] == 1:
            v0 = self.ctx[1]
        else:
            v0 = self.objs[self.ctx[1]]
        ret += "EXECUTOR%d: free obj[0x%02x]" % (core - 10, v0)
        return ret

    @function
    def DecodeInt(self, core):
        ret = ""
        s = ""
        t = False
        for key, value in self.objs.items():
            if value == self.objs[self.ctx[1]]:
                t = True
            if t is True:
                x = chr(value)
                if x in string.digits or x == "-":
                    s += x
                elif x == ";":
                    break
                else:
                    s = ""
                    t = False
        v0 = string.atoi(s)
        if v0:
            nb_char_to_skip = math.floor(math.log10(math.fabs(v0)) + 1)
        else:
            nb_char_to_skip = 1
        if v0 < 0:
            nb_char_to_skip += 1
        nb_char_to_skip = int(nb_char_to_skip)
        v2 = int((v0 + 0xc0) & 0xff)
        ret += "EXECUTOR%d: int obj[0x%04x], %d, obj[0x%04x], %d, %s" % (core - 10, self.ctx[1], v2, VM_OBJ_REG_RESULT, nb_char_to_skip, v0)
        self.objs[self.ctx[1]] = v2
        self.objs[VM_OBJ_REG_RESULT] = nb_char_to_skip
        return ret

    def run(self, input):
        for i, l in enumerate(input):
            self.objs[VM_OBJ_INPUT+i] = ord(l)
        self.objs[0] = VM_OBJ_INPUT
        i = self.pc
        self.n = 0
        while True:
            i0, c0, i1, c1 = self.DecodeInstruction(i)
            disass = "0x{:04x}: {:3}".format(i/8, "")
            if i0 != 0xffffffff:
                disass += "{:50} ".format(getattr(self, self.opcodes[i0])(c0))
            if i1 != 0xffffffff:
                disass += "%s " % getattr(self, self.opcodes[i1])(c1)
            if 0xffffffff in [i0, i1, self.objs[VM_OBJ_DECODER], self.objs[VM_OBJ_EXECUTOR0], self.objs[VM_OBJ_EXECUTOR1]]:
                break
            else:
                if self.silent is False:
                    log.warning(disass)
                if self.objs[VM_OBJ_EXECUTOR0]:
                    self.objs[VM_OBJ_REG_IP] = (41 * self.objs[VM_OBJ_EXECUTOR0]) + self.objs[VM_OBJ_REG_IP]
                    i = self.objs[VM_OBJ_REG_IP]
                    self.objs[VM_OBJ_EXECUTOR0] = 0
                elif self.objs[VM_OBJ_EXECUTOR1]:
                    self.objs[VM_OBJ_REG_IP] = (41 * self.objs[VM_OBJ_EXECUTOR1]) + self.objs[VM_OBJ_REG_IP]
                    i = self.objs[VM_OBJ_REG_IP]
                    self.objs[VM_OBJ_EXECUTOR1] = 0
                else:
                    self.objs[VM_OBJ_REG_IP] = 82 + self.objs[VM_OBJ_REG_IP]
                    i = self.objs[VM_OBJ_REG_IP]
            self.n += 1
        if self.silent is False:
            log.warning(disass)
            log.success("Exec done; Return: %d" % self.objs[0])
        return self.n

cpu = Cpu(0)
cpu.run(args.INPUT + "\x0a")
