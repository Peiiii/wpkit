import chardet
import os,shutil,glob
def read_bytes(f):
    return open(f,'rb').read()
def read_utf8(f):
    return open(f,'r',encoding='utf-8').read()
n=0
res=''
def det_dir(dir):
    global n,res
    for f in os.listdir(dir):
        nf=dir+'/'+f
        if os.path.isfile(nf) and nf.endswith('.py'):
            n+=1
            # print("n:",n)
            type=chardet.detect(read_bytes(nf))
            if type["confidence"] not in [0,1]:
                print("file:",nf,type)
            r=read_utf8(nf)
            open(nf,'w',encoding='utf-8').write(r)
            res+=r
            # print(len(r),len(res))
        elif os.path.isdir(nf):
            det_dir(nf)

if __name__ == '__main__':
    det_dir('./')
    print(res.count('\n'))
