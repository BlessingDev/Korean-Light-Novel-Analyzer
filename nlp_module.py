from konlpy.tag import Kkma, Twitter

def natural_proccess_sentence(sentence) :
    nlp = Twitter()
    result = nlp.pos(phrase=sentence)

    return result

def pos_Kkma(sentence) :
    nlp = Kkma()
    result = nlp.pos(sentence)

    return result


def title_distinguisher(title) :
    result = natural_proccess_sentence(title)

def get_accuracy(title_list, ori_list) :

    print(title_list)
    print(ori_list)

    accuracy = 0
    title_len = len(title_list) - 1
    for i in range(len(ori_list)):
        try:
            if title_list[min(i, title_len)] == ori_list[i] or \
                            title_list[min(i - 1, title_len)] == ori_list[i] or \
                            title_list[min(i + 1, title_len)] == ori_list[i]:
                accuracy += 1
            else:
                if ori_list[i].isdigit():
                    if title_list[min(i, title_len)].isdigit() or \
                            title_list[min(i - 1, title_len)].isdigit() or \
                            title_list[min(i + 1, title_len)].isdigit():
                        accuracy = 0
                    elif ori_list[i] != '1':
                        accuracy = 0
                elif i == len(ori_list) - 1:
                    if title_list[min(i, title_len)] != '1' or \
                                    title_list[min(i - 1, title_len)] != '1' or \
                                    title_list[min(i + 1, title_len)] != '1':
                        accuracy = 0
                if len(ori_list) == len(title_list) and \
                                ori_list[-1] != title_list[-1]:
                    accuracy = 0

                if accuracy == 0 :
                    return 0.0


        except:
            print("tried to access index {}".format(i))
            break

    try:
        rate = accuracy / len(ori_list)
    except:
        print('zero devision error')
        return 0.0

    len_dif = abs(len(title_list) - len(ori_list))
    rate -= (len_dif / max(len(title_list), len(ori_list))) * 0.5

    return rate

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
            if i[1] == 'Noun' or i[1] == 'Number' or i[1] == 'Verb':
                if i[0] != '권' :
                    title_list.append(i[0])

    for i in ori_nlp :
        if i[1] == 'Noun'  or i[1] == 'Number' or i[1] == 'Verb':
            if i[0] != '권' :
                ori_list.append(i[0])


    rate1 = get_accuracy(title_list, ori_list)

    title_list = []

    punc = False
    for i in title_nlp:
        if i[1] == 'Punctuation':
            if i[0] == '(' or i[0] == ')'\
                or i[0] == '/' or i[0] == '~':
                punc = not punc

        if punc :
            if i[1] == 'Noun' or i[1] == 'Number' or i[1] == 'Verb':
                if i[0] != '권' :
                    title_list.append(i[0])

    rate2 = get_accuracy(title_list, ori_list)

    ori_list = []
    for i in ori_nlp:
        if i[1] == 'Punctuation':
            if i[0] == '(' or i[0] == ')' \
                    or i[0] == '/' or i[0] == '~':
                punc = not punc

        if punc:
            if i[1] == 'Noun' or i[1] == 'Number' or i[1] == 'Verb':
                if i[0] != '권':
                    ori_list.append(i[0])

    rate3 = get_accuracy(title_list, ori_list)

    return max(rate1, rate2, rate3)

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
                and ((i + 1) / len(result)) >= 0.6:
            if not comma_found :
                first_comma = i - 1
                comma_found = True

                print(first_comma)

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
    else:
        ori_str = title[:title.find(',')]
        for i in range(len(title_list)) :
            title_list[i] = revive_ori_space(ori_str, title_list[i])

    return title_list

def revive_ori_space(ori_str, new_str) :
    for i in range(len(ori_str)) :
        if ori_str[i] == ' ' and \
            i < len(new_str) and new_str[i] != ' ':
            new_str = new_str[:i] + ' ' + new_str[i:]

    return new_str

def make_alterative_search_set(title) :
    result = natural_proccess_sentence(title)
    title_list = []

    print(result)

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

    if result[-1][1] == 'Number' and result[-1][0] == '1' :
        new_title = ""
        for i in range(len(result) - 1) :
            new_title += result[i][0]

        title_list.append(revive_ori_space(title, new_title))

    return title_list

