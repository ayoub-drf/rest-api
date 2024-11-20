def generateKey():
    import string, random
    characters = str(string.ascii_letters) + str(string.digits)
    counter = 200
    result = ""

    while counter > 0:
        result += random.choice(characters)
        counter -= 1

    return result