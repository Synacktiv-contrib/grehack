# coding=utf-8


import collections


with open("strace.dmp") as f:
    content = f.read()
action = 0
actions = {}
# sort by pids first
for line in content.splitlines():
    if line.startswith("[pid "):
        key = line.split("] ")[0]
        try:
            actions[key].append("%d::: %s" % (action, line))
        except KeyError:
            actions[key] = ["%d::: %s" % (action, line)]
    else:
        try:
            actions[-1].append("%d::: %s" % (action, line))
        except KeyError:
            actions[-1] = ["%d::: %s" % (action, line)]
    action += 1
# group by actions
real_actions = {}
for key, lines in actions.items():
    u = False
    real_actions[key] = []
    for line in lines:
        if "unfinished" in line:
            rebuild = line.split("<unfinished")[0].rstrip()
            u = True
        if "resumed" in line and u is True:
            rebuild += line.split("resumed>")[1].lstrip(" ")
            u = False
            real_actions[key].append(rebuild)
        if "unfinished" not in line and "resumed" not in line:
            real_actions[key].append(line)
# sort by action index
actions = {}
for lines in real_actions.values():
    for line in lines:
        key, action = line.split("::: ")
        actions[int(key)] = action
real_actions = collections.OrderedDict(sorted(actions.items()))
with open("strace_rebuilt.dmp", "w") as f:
    for v in real_actions.values():
        f.write("%s\n" % v)
