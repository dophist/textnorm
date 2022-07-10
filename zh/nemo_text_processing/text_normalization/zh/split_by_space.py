def split_by_space(str):
    Str_final = ""
    m = ""
    for chr in str:
        if '\u4e00' <= chr <= '\u9fa5':
            if m!= "":
                Str_final +=m
                Str_final +=" "
                m = ""
            m+=chr
            Str_final +=m
            Str_final +=" "
            m=""
        else:
            m+=chr
    Str_final +=m
    return Str_final
if __name__=='__main__':
    s = "你好北京123"
    # print(split_by_space(s))