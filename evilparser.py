import os
class parser:
    config = {}
    def __init__(self):
        config = {}
    def getconf(self, configlocate):
        if os.path.exists(configlocate):
            with open(configlocate, 'r') as f:
                cconf = 0
                for line in f.readlines():
                    line = line.strip()
                    if line.startswith("//"):
                        continue
                    elif line.startswith("::"):
                        cconf = line.split("::")[1]
                        continue
                    if cconf == 0:
                        continue
                    if not line.startswith("&") and not line.startswith("-") and not line.startswith("!"):
                        continue
                    if line.startswith("&"):
                        current = line[1:]
                        self.config[cconf] = current.split("|")
                        continue
                    elif line.startswith("-"):
                        current = line[1:]
                        self.config[cconf] = current
                        continue
                    elif line.startswith("!"):
                        current = line[1:]
                        try:
                            self.config[cconf] = int(current)
                        except:
                            print("\n\n[EVILPARSER] Error while setting integer {} at config {} in {}\n\n".format(current, cconf, configlocate))
                            exit(99)
                        continue
        return self.config
