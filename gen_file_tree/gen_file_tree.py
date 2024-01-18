import argparse
import os
import re
from typing import Any

padding_str_inter = '├─ '
padding_str_last = '└─ '
padding_str_none = '│  '

class FileTreeNode:
    """
    a tree node for file tree

    explanation:
        self.name: the name of the file or directory
        self.children: the children of the node (or the files in the directory)
        self.num_children: the number of children (or the number of files in the directory)
        self.parent: the parent of the node (or the parent directory)
        self.type: the type of the node, 'file' or 'dir'
        self.line: hard to explain, just see the code below
    """
    def __init__(self, name: str=None):
        self.name = name
        self.children = []
        self.num_children = 0
        self.parent = None
        self.type = None
        self.line = None

def gen_file_tree(path: str, max_depth: int=None, only_dir: bool=False, exclude: Any=None, cur_depth: int=0) -> FileTreeNode:
    """
    traverse the directory and generate a tree recursively

    Args:
        path (str): the desired path
        max_depth (int, optional): the max depth you want to travers. Defaults to None.
        only_dir (bool, optional): only contain dir. Defaults to False.
        exclude (Any, optional): reg patterns you want to exclude, 0 or more. Defaults to None.
        cur_depth (int, optional): the relative depth for now. Defaults to 0.

    Raises:
        FileNotFoundError: the desired path not found
        ValueError: the max_depth must be positive

    Returns:
        FileTreeNode: the root of the tree
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f'Path {path} not found.')
    if max_depth and max_depth< 1:
        raise ValueError('max_depth must be positive.')
    node_type = 'dir' if os.path.isdir(path) else 'file'
    root = FileTreeNode(os.path.basename(path))
    # turn '.' to the desired dir name
    if root.name in ['.', '..']:
        root.name = os.path.basename(os.path.abspath(os.path.join(os.getcwd(), root.name)))
    root.type = node_type
    # if the path is a file, return the node
    if not os.path.isdir(path):
        return root
    # arrive at the max depth, return the node
    if max_depth is not None and cur_depth >= max_depth:
        return root
    # get all files name in the directory
    all_files = os.listdir(path)
    # exclude the link file
    all_files = [f for f in all_files if not os.path.islink(os.path.join(path, f))]
    if only_dir:
        all_files = [f for f in all_files if os.path.isdir(os.path.join(path, f))]
    if exclude is not None:
        if isinstance(exclude, str):
            exclude = [exclude]
        for reg in exclude:
            all_files = [f for f in all_files if not re.match(reg, f)]
    # recursively generate the tree
    root.children = [gen_file_tree(os.path.join(path, f), max_depth, only_dir, exclude, cur_depth+1) for f in all_files]
    # update the num_children
    for c in root.children:
        c.parent = root
        root.num_children += c.num_children + 1
    return root

def get_file_tree_line(root: FileTreeNode):
    """
    this function is used to generate the vertical line for each node, 
    which is used to generate the tree string

    Args:
        root (FileTreeNode): the root of the tree

    Raises:
        ValueError: root cannot be None
    """
    if root == None:
        raise ValueError('root cannot be None.')
    # the first element of the line is the name of the node
    line = [root.name]
    # if the node is a file, return
    if root.type == 'file':
        root.line = line
        return
    # if the node is a directory, construct the line
    for i, c in enumerate(root.children):
        if i == len(root.children) - 1:
            line.append(padding_str_last)
            # padding the vertical line
            if c.type == 'dir':
                for j in range(c.num_children):
                    line.append('   ')
        else:
            line.append(padding_str_inter)
            if c.type == 'dir':
                for j in range(c.num_children):
                    line.append(padding_str_none)
    root.line = line
    # recursively generate the line for each child (truely row by row)
    for c in root.children:
        get_file_tree_line(c)
    return

def gen_file_tree_str(root) -> str:
    """
    this function turn the tree into a string

    

    Args:
        root (FileTreeNode): the root of the tree

    Raises:
        ValueError: root cannot be None

    Returns:
        str: the string of the tree
    """
    if root == None:
        raise ValueError('root cannot be None.')
    height = 0
    row_num = root.num_children + 1
    tree = [[] for _ in range(row_num)]
    
    def exchan_row_col(node):
        nonlocal height, row_num
        for i in range(height, row_num):
            if i - height < len(node.line): tree[i].append(node.line[i - height])
        height += 1
        for c in node.children:
            exchan_row_col(c)

    exchan_row_col(root)
    lines = [''.join(row) for row in tree]
    max_len = max([len(line) for line in lines])
    # add annotation
    lines = [line + ' ' * (max_len - len(line)) + '  // ' for line in lines]
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, default='.', help='the path you want to generate the tree')
    parser.add_argument('-d', '--depth', type=int, default=None, help='the max depth you want to generate')
    parser.add_argument('-o', '--only_dir', action='store_true', help='only contain dir')
    parser.add_argument('-e', '--exclude', action='append', help='reg patterns you want to exclude, 0 or more')
    parser.add_argument('-s', '--save', type=str, default=None, help='the path you want to save the tree, default is ./file_tree.md')
    parser.add_argument('-p', '--print', action='store_false', help='print the tree')
    args = parser.parse_args()
    file_tree = gen_file_tree(args.name, args.depth, args.only_dir, args.exclude)
    get_file_tree_line(file_tree)
    file_tree_str = gen_file_tree_str(file_tree)
    file_tree_str = '```\n' + file_tree_str + '\n```'
    if args.print:
        print(file_tree_str)
    if args.save:
        if os.path.exists(args.save):
            print(f'File {args.save} already exists, do you want to overwrite it? (y/n)')
            ans = input()
            if ans.lower() not in ['y', 'yes']:
                print('Write failed!')
                exit()
        with open(args.save, 'w') as f:
            f.write(file_tree_str)
    print('Complete!')

if __name__ == '__main__':
    main()
