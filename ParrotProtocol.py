def generateRequest(requestString):
    message = bytearray()
    message.extend(generateHeader(requestString))
    message.extend(bytearray(requestString))
    return message


def generateHeader(requestString):
    header = bytearray([0])
    header.append(len(requestString) + 3)
    header.append("\x80")
    return header


def getRequest(resource):
    return generateRequest("GET " + resource)


def setRequest(resource, args):
    return generateRequest("SET " + resource + "?arg=" + args)
