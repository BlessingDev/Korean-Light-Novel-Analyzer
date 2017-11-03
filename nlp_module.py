from konlpy.tag import Twitter

def natural_proccess_sentence(sentence) :
    nlp = Twitter()
    result = nlp.pos(phrase=sentence)

    return result

def title_distinguisher(title) :
    result = natural_proccess_sentence(title)

def search_accsuracy_examine(book) :
    ori_nlp = natural_proccess_sentence(book.ori_title)
    title_nlp = natural_proccess_sentence(book.title)

    print(book.title)
    print(book.ori_title)

    title_list = list()
    ori_list = list()

    punc = False
    for i in title_nlp :
        if i[1] == 'Punctuation' :
            if i[0] == '(' or i[0] == "'":
                punc = True
            else :
                punc = False

        if not punc :
            if i[1] == 'Noun' or i[1] == 'Number':
                title_list.append(i[0])

    for i in ori_nlp :
        if i[1] == 'Noun'  or i[1] == 'Number':
            ori_list.append(i[0])

    print(title_list)
    print(ori_list)

    accuracy = 0
    for i in range(len(ori_list)) :
        try :
            if title_list[i] == ori_list[i] or \
                title_list[i - 1] == ori_list[i] or\
                title_list[i + 1] == ori_list[i] :
                accuracy += 1

        except:
            if ori_list[i].isdigit() :
                accuracy = 0
                print('숫자가 틀림')
                break

            print("tried to access index {}".format(i))

    try:
        rate = accuracy / len(ori_list)
    except:
        print('zero devision error')
        return 0.4

    return rate