# Copied from geeks for geeks website
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1


def splitAt(w, n):
    for i in range(0, len(w), n):
        yield w[i:i + n]
