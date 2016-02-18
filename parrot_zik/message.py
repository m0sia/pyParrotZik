class Message:
    def __init__(self, resource, method, arg=None):
        self.method = method
        self.resource = resource
        self.arg = arg

    def __str__(self):
        return str(self.request)

    @property
    def request(self):
        message = bytearray()
        message.extend(self.header)
        message.extend(bytearray(self.request_string))
        return message

    @property
    def header(self):
        header = bytearray([0])
        header.append(len(self.request_string) + 3)
        header.append("\x80")
        return header

    @property
    def request_string(self):
        if self.method == 'set':
            return 'SET {}/{}?arg={}'.format(self.resource, self.method,
                                             str(self.arg).lower())
        else:
            return 'GET {}/{}'.format(self.resource, self.method)
