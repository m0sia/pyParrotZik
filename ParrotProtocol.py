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


def getRequest(apiString):
    return generateRequest("GET " + apiString)


def setRequest(apiString,args):
    return generateRequest("SET " + apiString + "?arg=" + args)
