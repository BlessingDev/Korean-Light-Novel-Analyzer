import BookData
import numpy

def list_to_json(list, func):
    out_str = "["
    for val in list:
        out_str += func(val)
        out_str += ", "

    if len(out_str) > 2:
        out_str = out_str[:-2]

    out_str += "]"
    return out_str

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

    return dict_to_json(book_dict, data_to_json)

def dict_to_json(dict, func) :
    out_str = "{"
    for key in dict.keys() :
        out_str += ('"' + key.__str__() + '"')
        out_str += ": "
        out_str += func(dict[key])
        out_str += ", "
    if len(out_str) > 2:
        out_str = out_str[:-2]

    out_str += "}"
    return out_str

def data_to_json(data) :
    if type(data) is str :
        data = data.replace('"', "'")
        return '"' + data + '"'
    elif type(data) is BookData.BookData :
        return book_to_json(data)
    elif type(data) is list :
        return list_to_json(data, data_to_json)
    elif type(data) is int or type(data) is float :
        return data.__str__()
    elif type(data) is dict :
        return dict_to_json(data, data_to_json)
    elif type(data) is numpy.float64 :
        return data.__str__()
    else :
        print("type은 {}".format(type(data)))
        return '""'