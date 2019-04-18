import book_data, json

def list_to_json(list, func):
    json_list = []
    for val in list:
        json_list.append(func(val))

    return json_list

def book_to_json(book) :
    book_dict = dict()
    book_dict["title"] = book.title
    book_dict["ori title"] = book.ori_title
    book_dict["author"] = book.author
    book_dict["translator"] = book.translator
    book_dict["image_url"] = book.image_url
    book_dict["publisher"] = book.publisher
    book_dict["description"] = book.description.replace('"', "'").replace('\n', '')
    book_dict["isbn"] = book.isbn
    book_dict["error_code"] = book.error_code
    book_dict["search_accuracy"] = book.search_accuracy
    book_dict["searched_title"] = book.searched_title
    book_dict["pubdate"] = book.pubdate
    book_dict["genre"] = book.genre

    return book_dict

def dict_to_json(dict, func) :
    for key in dict.keys() :
        dict[key] = func(dict[key])

    return dict

def data_to_json(data) :
    if type(data) is str :
        return data
    elif type(data) is book_data.BookData :
        return book_to_json(data)
    elif type(data) is list :
        return list_to_json(data, data_to_json)
    elif type(data) is dict :
        return dict_to_json(data, data_to_json)

    else :
        print("type은 {}".format(type(data)))
        return data