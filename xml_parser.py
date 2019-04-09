''' Function to read and extract data from XMl files, treating the branch/path as column name
    with nodes separated by "//". Returns None if Leaf Node value is None. If there are
    multiple tags with the same name at same level of depth, they will be numbered in the order
    they are read while parsing the file. Does not follow Xpath notations.'''

import xml.etree.ElementTree as ET
import pandas as pd

def print_tree(pre, node, suff):
    '''Traverse the tree.'''
    tree = []
    if list(node) == []:
        if node.text is None:
            tree.append([pre+suff+'//'+node.tag, 'None'])
        else:
            tree.append([pre+suff+'//'+node.tag, node.text])
    else:
        count = 0
        if list(set([x.tag for x in node]))*len(list(node)) == [x.tag for x in node]\
        and len(list(node)) > 1:
            for child in node:
                count = count + 1
                for ele in print_tree(pre+'//'+node.tag, child, '-'+str(count)):
                    tree.append(ele)
        else:
            for child in node:
                for ele in print_tree(pre+'//'+node.tag, child, suff):
                    tree.append(ele)
    return tree

def read_xml(file_b):
    '''Read xml file.'''
    data = ET.parse(file_b)
    root = data.getroot()
    return pd.DataFrame(print_tree('', root, ''), columns=['xmlpath', 'value'])
