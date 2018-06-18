import sys
import os
import random
from collections import Counter
from collections import defaultdict

class MetaPathGenerator(object):
    def __init__(self):
        self.id2user = dict()
        self.id2app = dict()
        self.id2cat = dict()
        self.user_user = defaultdict(list)
        self.user_cats = defaultdict(list)
        self.cat_users = defaultdict(list)
        self.user_apps = defaultdict(list)
        self.app_users = defaultdict(list)
        self.cat_apps = defaultdict(list)
        self.app_cats = defaultdict(list)  # 这里简单情况，一个app只有一个cat
        self.metapathdict = dict()
    

    def read_data(self, dirpath):
        with open(dirpath + "/id2user.txt") as f:  # index of users
            for line in f:
                toks = line.strip().split(maxsplit=1)
                if len(toks) == 2:
                    self.id2user[int(toks[0])] = toks[1]
        self.id2user = dict(zip(range(len(self.id2user)), range(len(self.id2user))))
        print("#users", len(self.id2user))

        with open(dirpath + "/id2app.txt") as f:  # index of apps
            for line in f:
                toks = line.strip().split(maxsplit=1)
                if len(toks) == 2:
                    self.id2app[int(toks[0])] = toks[1]
        print("#apps", len(self.id2app))

        with open(dirpath + "/id2cat.txt") as f:  # index of cats
            for line in f:
                toks = line.strip().split(maxsplit=1)
                if len(toks) == 2:
                    self.id2cat[int(toks[0])] = toks[1]
        print("#cats", len(self.id2cat))

        with open(dirpath + "/user_app_usage.txt") as f:  # edges of user-app
            edges = 0
            for line in f:
                toks = line.strip().split()
                if len(toks) == 2:
                    u, a = int(toks[0]), int(toks[1])
                    self.user_apps[u].append(a)
                    self.app_users[a].append(u)
                    edges += 1
                    if edges % 10000 == 0: print("load %s edges of user-app." % edges)
        print("#edges of user-app", edges)

        with open(dirpath + "/app_cat.txt") as f:  # edges of app-cat
            edges = 0
            for line in f:
                toks = line.strip().split()
                if len(toks) == 2:
                    a, c = int(toks[0]), int(toks[1])
                    self.app_cats[a].append(c)
                    self.cat_apps[c].append(a)
                    edges += 1
            print("#edges of app-cat", edges)

        edges = 0
        for cat, apps in self.cat_apps.items():  # edges of user-cat
            for app in apps:
                if app not in self.app_users: continue
                for user in self.app_users[app]:
                    self.cat_users[cat].append(user)
                    self.user_cats[user].append(cat)
                    edges += 1
        print("#edges of user-cat", edges)

        self.metapathdict = {
            'u-a': self.user_apps,
            'a-u': self.app_users,
            'a-c': self.app_cats,
            'c-a': self.cat_apps,
            'u-c': self.user_cats,
            'c-u': self.cat_users,
            'u': self.id2user,
            'a': self.id2app,
            'c': self.id2cat
        }

    def randomwalk_of_metapath(self, outfilename, numwalks, walklength, metapath="uau"):
        if not outfilename:
            outfilename = "./data/w%s.l%s.%s.txt" % (numwalks, walklength, metapath)
        outfile = open(outfilename, "w")
        for i in range(numwalks):
            if i % 10 == 0: print("numwalks: %s" % i)
            starttype = metapath[0]  # e.g. 'u-a' start to walk strictly to the metapath
            for startnode in self.metapathdict[starttype]:  # starts with every node of metapath[0]
                node = startnode
                outline = "%s" % self.metapathdict[starttype][node]  # e.g. user
                for j in range(walklength):
                    index = j % (len(metapath) - 1)
                    path = "%s-%s" % (metapath[index], metapath[index + 1])  # path
                    neighbors = self.metapathdict[path][node]  # neibors of the node in the path
                    node = random.choice(neighbors)  # random choice next node
                    outline += " %s" % self.metapathdict[metapath[index + 1]][node]
                outfile.write(outline + "\n")
        outfile.close()
        print("random walk of metapath finished!")


#python genMetaPaths.py 1000 100 "uacau" ./data/w1000.l100.uacau.txt
def main():
    dirpath = "../datasets/nfp/user_app_hin"
    numwalks = int(sys.argv[1])
    walklength = int(sys.argv[2])
    metapath = sys.argv[3]
    # outfilename = sys.argv[4]
    outfilename = None

    mpg = MetaPathGenerator()
    mpg.read_data(dirpath)
    mpg.randomwalk_of_metapath(outfilename, numwalks, walklength, metapath)


if __name__ == "__main__":
    main()

