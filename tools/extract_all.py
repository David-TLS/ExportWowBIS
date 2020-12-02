import regex

# extract all results
def extractAll(re, text):
    result =  regex.findall(re, text)
    if(bool(result)):
        return result
    return False
