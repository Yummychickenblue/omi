import os
import shutil

#Writes an entry to openmw.cfg.
def write_openmwcfg(arg):
    with open(openmw_home() + '/openmw.cfg', 'a') as f:
        f.write('data="' + openmw_home() 
                + '/mods/'
                + get_folder_name(arg)
                +'"')

#Returns the name of the folder selected by the user.
#Used to name the directory that mod files get copied to.
#Example if someone gives the folder "Empire Alpha" this will return
#"Empire Alpha".
def get_folder_name(arg):
    dir_list = arg.split('/')
    name = dir_list[-1]
    return(name)

#Returns the directory of OpenMW's installation,
#assuming it's installed in the default location.
def openmw_home():
    return(os.environ.get('HOME') + '/.config/openmw')

#Tests to see if there are any mod files in the given directory of arg.
#Theoretically it breaks down if someone puts these words in
#in their mod name and doesn't wrap their files in a Data Files
#directory. In the future I'm thinking of verifying the length of
#folder names to protect against hat.
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
        return True
    else:
        return False
    
#This function is used to put the system in the directory where the
#mod files are located. First it tries to change to a Data Files dir
#to avoid running the above function. If that fails it moves down the
#first directory in os.listdir() until it can't go farther, at which 
#point it goes back to the top and goes down the next tree ad infinitum.
#As of now the only way to get insight into this function's status is to
#watch the log. Eventually gui cues should be added to reflect what 
#this is doing.
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
    

    
if __name__ == '__main__':
    pass
