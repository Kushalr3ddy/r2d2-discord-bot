from purgo_malum import client

#word = "fuck you"
def check(word):
    result = client.contains_profanity(word)
    return result
