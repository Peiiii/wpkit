import os,shutil,glob

def alter_dir(src,dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    fs=glob.glob(src+'/*.jpg')
    for i,f in enumerate(fs):
        name=os.path.basename(f)
        f2=dst+'/'+name.replace('.jpg','_car0.jpg')
        shutil.copy(f,f2)
        print(i,f,f2)
def alter_annot(annot_path,dst_path,new_dir):
    lines=open(annot_path).read().strip().split('\n')
    # print(lines)
    def change_line(line):
        p,rest=line.split(' ',maxsplit=1)
        p=new_dir+'/'+os.path.basename(p).replace('.jpg','_car0.jpg')
        return ' '.join([p,rest])
    lines=[change_line(line) for line in lines]
    lines='\n'.join(lines)
    with open(dst_path,'w') as f:
        f.write(lines)

def alter_dataset():
    src_dir='/home/ars/disk/chaoyuan/dataset/车灯'
    dst_dir='/home/ars/disk/chaoyuan/dataset/more_datasets/车灯v2'
    annot_path=src_dir+'/annotations.txt'
    new_annot_path=dst_dir+'/annotations.txt'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    raw_dir=src_dir+'/raw'
    new_raw_dir=dst_dir+'/raw'
    train_dir=src_dir+'/train'
    new_train_dir=dst_dir+'/train'
    val_dir=src_dir+'/val'
    new_val_dir=dst_dir+'/val'

    alter_dir(raw_dir,new_raw_dir)
    alter_dir(train_dir,new_train_dir)
    alter_dir(val_dir,new_val_dir)

    alter_annot(annot_path,new_annot_path,new_train_dir)

if __name__ == '__main__':
    alter_dataset()