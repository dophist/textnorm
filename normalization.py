

TYPE_NUM = 7


# get_data
def read_file(file_name):
    with open(file_name) as f:
        return f.readlines()

# search according to type
def get_type(type_num):
    lines = read_file('test.txt')
    lines_list = []
    for i in range(TYPE_NUM):
        lines_list += [[]]
    for i in range(len(lines)):
        line = lines[i].strip()
        _index = int(line[0]) - 1
        lines_list[_index] += [[i,line[1:]]]
    # type_num == -1 return all results
    if type_num == -1:   
        return lines_list
    else:
        return lines_list[type_num - 1]

# calculate accuracy
def calc_accuracy(type_num):
    gt_lines = read_file('gt.txt')
    test_li = get_type(type_num)
    for index in range(len(gt_lines)):
        gt_lines[index] = gt_lines[index].strip()
        gt_lines[index] = gt_lines[index].replace(' ','')
    if type_num == -1:
        count0 = 0
        count = len(gt_lines)
        err_list = []
        for i in range(TYPE_NUM):
            for item in test_li[i]:
                index = item[0]
                line = item[1]
                line = line.replace(' ','')
                line = normalize(line)
                if line == gt_lines[index]:
                    count0 += 1
                else:
                    err_list += [line]
        return count0/count,err_list
    else:
        count0 = 0
        count = len(test_li[type_num - 1])
        err_list = []
        for item in test_li:
            index = item[0]
            line = item[1]
            line = line.replace(' ','')
            line = normalize(line)
            if line == gt_lines[index]:
                count0 += 1
            else:
                err_list += [line]
        return count0/count,err_list

def normalize(line):
    return line 

print(calc_accuracy(2))


