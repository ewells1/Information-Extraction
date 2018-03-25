import os

postagged_path = './data/postagged-files'
parsed_path = './data/parsed-files'
train_path = './data/rel-trainset.gold'
features_out_path = './features.txt'

# read rel-trainset.gold, get relations, word itself, and word types
def read_train_gold(path):
    rel_bools = []
    words = []
    types = []
    file = open(path, 'r')
    lines = file.readlines()
    for line in lines:
        relation = line.split()[0]
        relation = "no" if relation == "no_rel" else "yes"
        arg1 = line.split()[7]
        arg2 = line.split()[13]
        arg1_type = line.split()[5]
        arg2_type = line.split()[11]
        rel_bools.append(relation)
        words.append((arg1, arg2))
        types.append((arg1_type, arg2_type))
    return rel_bools, words, types

# read postagged-files, get pos tags
def read_pos_files(path):
    pos_dict = {}
    for filename in os.listdir(path):
        sentID = (".").join(filename.split(".")[:3])
        file_path = path + "/" + filename
        with open(file_path) as f:
            lines = (line.rstrip() for line in f)
            lines = (line for line in lines if line and sentID not in line)
            for line in lines:
                word_pos = line.split()
                word = [wp.split('_')[0] for wp in word_pos]
                pos = [wp.split('_')[1] for wp in word_pos]
                temp = dict(zip(word,pos))
                pos_dict.update(temp)
    return pos_dict

# def read_parsed_files(path):

# write all features to file
def write_to_file(path):
    file_out = open(path, 'w')
    relations, words, types = read_train_gold(train_path)
    pos = read_pos_files(postagged_path)
    for x in range (len(relations)-1):
        arg1,arg2 = words[x][0], words[x][1]
        arg1_type,arg2_type = types[x][0], types[x][1]
        file_out.write(relations[x]+" ")
        file_out.write("arg1=" + arg1 + " " + "arg2=" + arg2 + " ")
        file_out.write("arg1_type=" + arg1_type + " " + "arg2_type=" + arg2_type + " ")
        ### key error: eg. Bshar_Assad (b/c "Bshar_Assad" is one word in rel-trainset.gold, but in postagged files, they are "Bshar" and "Assad" )
        #file_out.write("arg1_pos=" + pos[arg1] + " " + "arg2_pos=" + pos[arg2] + " ")
        file_out.write("\n")

write_to_file(features_out_path)
