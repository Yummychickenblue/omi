import os
import shutil

def openmw_home():
    return(os.environ.get('HOME') + '/.config/openmw')



#This function breaks down if someone puts any of the entries in 
#relevant_files in their mods title. I try to mititgate this by 
#testing for Data Files first. Of course some people don't wrap their 
#mods in data files dirs and that makes my life hard. In future I'm 
#thinking of this to verify length for the folder names
def test_relevant(arg):
    relevant_files = ('.esm',
                     '.esp',
                     'bookart',
                     'video',
                     'icons',
                     'music',
                     'meshes',
                     'fonts',
                     'sound',
                     'splash',
                     'textures',)
    flist = []
    fset = set()
    for i in relevant_files:
        f = str(os.listdir()).lower().find(i)
        flist.append(f)
        fset.update(set(flist))
    if len(fset) > 1:
        print(flist)
        print(fset)
        print('test_relevant returned true')
        return True
    else:
        print(fset)
        print('test_relevant returned false')
        return False
    

def normalize(arg):
    i = 0
    dir = os.listdir()[i]
    while test_relevant(os.listdir()) == False:
        try:
            os.chdir(os.getcwd() + '/Data Files')
            print('direct cd to data files successful')
        except FileNotFoundError:
            try:
                dir = os.listdir()[i]
                os.chdir(dir)
                print('direct cd to data files was unsucessful, trying to move down dirs')
                print('cwd is now' + os.getcwd())
            except FileNotFoundError:
                os.chdir(arg)
                i+=1
                print()
                print('ran out of dirs and had to go up again')
                print('cwd is now' + os.getcwd())
                print('i is now %s' %i)
                print()
        else:
            print('the system changed to right directory and is ready to copy files')
    print('ready to copy files!')
    print(os.listdir())

def install(dir):
#maybe want to wrap this in a try block and ask if the user wants to 
#reinstall if we get a FileExissts Error
    print('install is running')
    try:
        shutil.copytree((os.getcwd()), (openmw_home() + '/mods/' 
                                        + get_folder_name(dir)))
        print('openmw now has the dirs:')
        print(os.listdir(openmw_home()+'/mods/'))
    except FileExistsError:
        print('The mod already exists in') 
    
def get_folder_name(arg):
    dir_list = arg.split('/')
    name = dir_list[-1]
    return(name)

#Come back here and later and add support for writing to other places
#than the end of the file.
def write_openmwcfg(arg):
    with open(openmw_home() + '/openmw.cfg', 'a') as f:
        f.write('data="' + openmw_home() 
                + '/mods/'
                + get_folder_name(arg)
                +'"')
    
if __name__ == '__main__':
    pass
            
