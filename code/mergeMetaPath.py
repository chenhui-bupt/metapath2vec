# -*-  coding: utf-8 -*-
import os

def mergeMetaPath(numwalks, walklength, metapaths=["uau", "uacau"]):
    out =  []
    for metapath in metapaths:
        mpfilename = os.path.join("./data", "w%s.l%s.%s.txt" % (numwalks, walklength, metapath))
        with open(mpfilename) as f:
            out += f.readlines()
    with open(os.path.join("./data", "w%s.l%s.txt" % (numwalks, walklength)), "w") as f:
        f.write("\n".join(out))
    print("metapath has been merged successfully!")

if __name__ == "__main__":
    mergeMetaPath(100, 100)
