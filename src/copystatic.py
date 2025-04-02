import os
import shutil

def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"{src_path} successfully copied to {dst_path}")
        else:
            copy_directory(src_path, dst_path)

 #src = "static/"
    #path = "public/"
    #src_lst = os.listdir(src)
    #pub_dir = os.path.exists('public/')
    
    #print(f"public:{pub_dir}")
    #print(src_lst)
    
    #if not pub_dir:
    #    os.mkdir(path)
    #else:
    #    dir_lst = os.listdir(path)
    #    if dir_lst != []:
    #        shutil.rmtree(path)
    #        os.mkdir(path)

    #for file in src_lst:
    #    print(file)
    #    file_path = os.path.join(src, file)
    #    print(os.path.exists(file_path))
    #    if os.path.isfile(file_path):
    #        copy = shutil.copy(file_path, path)
    #    else:
    #        files = os.listdir(file_path)
    #        print(f"image: {files}")
    #        copy_to_path = os.path.join(path, file)
    #        print(f"public/images path: {copy_to_path}")
    #        make_dir = os.mkdir(copy_to_path)
    #        for f in files:
    #            print(f"file: {f}")
    #            f_path = os.path.join(file_path, f)
    #            print(f_path)
    #            print(os.path.exists(f_path))
    #            if os.path.isfile(f_path):
    #                shutil.copy(f_path, copy_to_path)