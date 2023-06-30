# What is this?

This is a script to generate file tree for a given directory (default the current).

Excutable file is `dist/gen_file_tree`

The tree will be like:

```markdown
gen_tree                            // 
├─ gen_file_tree.py                 // source code
├─ gen_file_tree.spec               // 
├─ build                            // build file
│  └─ gen_file_tree                 // 
│     ├─ xref-gen_file_tree.html    // 
│     ├─ warn-gen_file_tree.txt     // 
│     ├─ gen_file_tree.pkg          // 
│     ├─ EXE-00.toc                 // 
│     ├─ PYZ-00.toc                 // 
│     ├─ PKG-00.toc                 // 
│     ├─ Analysis-00.toc            // 
│     ├─ base_library.zip           // 
│     ├─ localpycs                  // 
│     │  ├─ pyimod01_archive.pyc    // 
│     │  ├─ pyimod02_importers.pyc  // 
│     │  ├─ struct.pyc              // 
│     │  └─ pyimod03_ctypes.pyc     // 
│     └─ PYZ-00.pyz                 // 
├─ dist                             // 
│  ├─ file_tree.md                  // example
│  └─ gen_file_tree                 // bin
├─ .gitignore                       // 
└─ README.md                        // 
```
# Args explanation

- `-n`, `--name`, the path you want to generate the tree
- `-d`, `--depth`, the max depth you want to generate'
- `-o`, `--only_dir`, only contain dir
- `-e`, `--exclude`, reg patterns you want to exclude, 0 or more
- `-s`, `--save`, the path you want to save the tree, default is `./file_tree.md`