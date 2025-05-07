import re

A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

A_COMMAND_PATTERN = re.compile(r'@([0-9a-zA-Z_\.\$:]+)')
L_COMMAND_PATTERN = re.compile(r'\(([0-9a-zA-Z_\.\$:]*)\)')
C_COMMAND_PATTERN = re.compile(r'(?:(A?M?D?)=)?([^;]+)(?:;(.+))?')

class Parser():
    def __init__(self,filepath):
        self.file = open(filepath)
        self.current_command = None
    
    def __enter__(self):
        return self
    
    def __exit__(self,ex_type,ex_value,trace):
        self.file.close()
    
    def advance(self):
        while True:
            line = self.file.readline()
            if not line:
                self.current_command = None
                break
            
            line_trimmed = line.strip().replace(' ','')
            comment = line_trimmed.find('//')
            if comment != -1:
                line_trimmed = line_trimmed[:comment]
            
            if line_trimmed != '':
                self.current_command = line_trimmed
                break
        return self.current_command
            
    def command_type(self):
        if self.current_command[0]=='@':
            return A_COMMAND
        elif self.current_command[0]=='(':
            return L_COMMAND
        else:
            return C_COMMAND
        
    def symbol(self):
        cmd_type = self.command_type()
        if cmd_type == A_COMMAND:
            matched = A_COMMAND_PATTERN.match(self.current_command)
            if not matched:
                raise Exception('Parsing symbol failed')
            return matched.group(1)
        elif cmd_type == L_COMMAND:
            matched = L_COMMAND_PATTERN.match(self.current_command)
            if not matched:
                raise Exception('Parsing symbol failed')
            return matched.group(1)
        else:
            raise Exception('Current command is no A or L COMMAND')
    
    def dest(self):
        cmd_type = self.command_type()
        if cmd_type == C_COMMAND:
            matched = C_COMMAND_PATTERN.match(self.current_command)
            return matched.group(1)
        else:
            raise Exception('Current command is no C COMMAND')
            
    def comp(self):
        cmd_type = self.command_type()
        if cmd_type == C_COMMAND:
            matched = C_COMMAND_PATTERN.match(self.current_command)
            return matched.group(2)
        else:
            raise Exception('Current command is no C COMMAND')
    
    def jump(self):
        cmd_type = self.command_type()
        if cmd_type == C_COMMAND:
            matched = C_COMMAND_PATTERN.match(self.current_command)
            return matched.group(3)
        else:
            raise Exception('Current command is no C COMMAND')
        
