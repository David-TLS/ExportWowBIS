import regex

# extract the first result
def extractSingle(re, text, indexGroup = 0):
    groups =  regex.search(re, text)
    if(bool(groups)):
        result = groups.group()
        if(bool(result)):
            return result.strip()
    return False
