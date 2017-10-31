from konlpy.tag import Twitter

def natural_proccess_sentence(sentence) :
    twitter = Twitter()
    result = twitter.pos(phrase=sentence)

    return result