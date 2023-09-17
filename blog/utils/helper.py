def find_item_in_list(list, cb):
    for index, item in enumerate(list):
        if cb(item, index, list): 
            return item


def sub_words(text, length):
    words = text.split(" ")
    # print(words)
    if length > len(words): return text
    return " ".join(words[0:length])

sub_words("i am obi", 2)