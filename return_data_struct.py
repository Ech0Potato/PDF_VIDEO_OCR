import copy
def get_pdf_ocr_return_json(code,message,ocr_return_data_list):
    
    json = {
        "code" : int,
        "message" : str,
        "data" : list()
    }

    page_data_struct = {
        "page" : int,
        "words_block_list" : list(),
    }

    words_block_struct = {
        "words" : str,
        "location" : list
    }

    json["code"] = code
    json["message"] = message
    
    for  idx, page in enumerate(ocr_return_data_list,0):
        page_info = copy.deepcopy(page_data_struct)
        page_info["page"] = (idx + 1)
        for location,contents in page:
            words_block = copy.deepcopy(words_block_struct)
            words_block["words"] = contents
            words_block["location"] = location
            page_info["words_block_list"].append(words_block)
        json["data"].append(page_info)
    
    return json
        

def get_voice_2_word_return_json(code,message,voice_ocr_return_data):
    
    json = {
        "code":int,
        "message":str,
        "data":str
    }
    
    json["code"] = code
    json["message"] = message
    json["data"] = voice_ocr_return_data
    
    return json