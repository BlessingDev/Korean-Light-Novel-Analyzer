import konlpy

def natural_proccess_sentence(sentence) :
    result = konlpy.tag.Twitter.pos(sentence)

    return result