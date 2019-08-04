class CodeBuilder:
    """Literally generate code string"""
    def __init__(self, root_name):
        self.root_name = root_name
        self.__root = CodeElement(root_name)

    def add_field(self, name, value):
        self.__root.fields.append(
            Field(name, value)    
        )
        return self

    def __str__(self):
        return str(self.__root)

class CodeElement:
    indent_size = 2
    def __init__(self, name):
        self.name = name
        self.fields = []
    
    def __str__(self):
        ind = ' ' * self.indent_size
        fields = ''.join([str(i) for i in self.fields])
        if fields:
            string = 'class ' + self.name + ':\n' \
                + ind + 'def __init__(self):' + '\n' \
                + fields
        else:
            string = 'class ' + self.name + ':\n' \
                + ind + 'pass'
        return string

class Field:
    indent_size = 2
    def __init__(self, name, value):
        self.name = name
        try:
            self.value = int(value)
        except:
            self.value = value
        
    def __str(self):
        """Helper function to make up the actual string"""
        ind = ' ' * self.indent_size * 2
        if isinstance(self.value, int):
            value_str = str(self.value)
        if isinstance(self.value, str):
            if self.value == '""':
                self.value = ""
            value_str = '"' + self.value + '"'
        string = ind + 'self.' + self.name + ' = ' + value_str + '\n'
        return string
    
    def __str__(self):
        return self.__str()
