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

    title_list = list()
    ori_list = list()

    punc = False
    for i in title_nlp :
        if i[1] == 'Punctuation' :
            if i[0] == '('\
                or i[0] == '/':
                punc = True
            else :
                punc = False

        if not punc :
            if i[1] == 'Noun' or i[1] == 'Number':
                if i[0] != '권' :
                    title_list.append(i[0])

    for i in ori_nlp :
        if i[1] == 'Noun'  or i[1] == 'Number':
            if i[0] != '권' :
                ori_list.append(i[0])

    print(title_list)
    print(ori_list)

    accuracy = 0
    title_len = len(title_list) - 1
    for i in range(len(ori_list)) :
        try :
            if title_list[min(i, title_len)] == ori_list[i] or \
                title_list[min(i - 1, title_len)] == ori_list[i] or\
                title_list[min(i + 1, title_len)] == ori_list[i] :
                accuracy += 1
            else :
                if ori_list[i].isdigit() :
                    if title_list[min(i, title_len)].isdigit() or \
                        title_list[min(i - 1, title_len)].isdigit() or \
                        title_list[min(i + 1, title_len)].isdigit() :
                        accuracy = 0
                    elif ori_list[i] != '1' :
                        accuracy = 0
                elif i == len(ori_list) - 1:
                    if title_list[min(i, title_len)] != '1' or \
                            title_list[min(i - 1, title_len)] != '1' or \
                            title_list[min(i + 1, title_len)]!= '1':
                        accuracy = 0
                if len(ori_list) == len(title_list) and \
                        ori_list[-1] != title_list[-1]:
                    accuracy = 0


        except:
            print("tried to access index {}".format(i))
            break

    try:
        rate = accuracy / len(ori_list)
    except:
        print('zero devision error')
        return 0.4

    len_dif = abs(len(title_list) - len(ori_list))
    rate -= (len_dif / max(len(title_list), len(ori_list))) * 0.5

    return rate

def preprocess_title(title) :
    result = natural_proccess_sentence(title)
    title_list = []

    print(result)

    i = 0
    comma_found = False
    first_comma = 0
    for chunk in result:
        if chunk[1] == 'Punctuation' and \
                        chunk[0] == ',' \
                and chunk != result[-1]\
                and (i / len(result)) >= 0.8:
            if not comma_found :
                first_comma = i - 1
                comma_found = True

                new_title = ""
                for j in range(first_comma):
                    new_title += result[j][0]

                new_title += result[i - 1][0]
                title_list.append(new_title)


            new_title = ""
            for j in range(first_comma) :
                new_title += result[j][0]

            new_title += result[i + 1][0]
            title_list.append(new_title)

        i += 1

    if len(title_list) == 0 :
        title_list.append(title)

    return title_list



def make_alterative_search_set(title) :
    result = natural_proccess_sentence(title)
    title_list = []

    i = 0
    for chunk in result :
        if chunk[0] == '시리즈' :
            new_title = ""
            for j in range(len(result)) :
                if result[j][0] != '시리즈' :
                    new_title += result[j][0]

            title_list.append(new_title)
        if chunk[1] == 'Punctuation' and \
                chunk[0] == '~' or chunk[0] == "'" :
            new_title = ""
            for j in range(i + 1, len(result)) :
                if result[j][1] == 'Punctuation' :
                    break
                new_title += result[j][0]
            title_list.append(new_title)

            new_title = ""
            for j in range(i) :
                new_title += result[j][0]
            title_list.append(new_title)

            new_title = ""
            for j in range(len(result)) :
                if j > i - 1 :
                    if result[j][1] != 'Punctuation' :
                        new_title += result[j][0]
                else :
                    new_title += result[j][0]
            title_list.append(new_title)

            break

        i += 1

    return title_list
