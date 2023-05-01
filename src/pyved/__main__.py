import argparse
from pathlib import Path
import os
from .ver_info import version_num as pyved_ver_num


parser = argparse.ArgumentParser(
    prog='pyved',
    description='runs PYVED and opens a new/existing project',
    epilog="pyved (=PY Visual Editor) is a new toolbox for easy game development. For more information, please visit https://github.com/wktab/gamedev-pyved/"
)
# configuration --
# besoin d'utiliser des sub parsers car on a plusieurs cmd
subparser = parser.add_subparsers(dest='command', required=True)
new = subparser.add_parser('new')
new.add_argument('--project', type=str, required=True)

register = subparser.add_parser('open')
register.add_argument('--filepath', type=str, required=True)
# -- fin configuration


# definition implem {{
def create_new_project(pname):
    target_dir = Path(pname)
    if target_dir.exists():
        print(f"ERROR: folder {target_dir} already exists")
    else:
        os.mkdir(target_dir)
        print(f" +Initializing a new project named \"{target_dir}\"...")
        DB_QT = '"'
        with open(os.path.join(target_dir, 'pyved.json'), 'w') as fout:
            fout.write("{\n")
            fout.write(' '*4 + '"tag":'+DB_QT+'pyved'+pyved_ver_num+DB_QT+",\n")
            fout.write(' '*4 + '"project":'+DB_QT+pname+DB_QT+",\n")
            fout.write("}")

def open_project(desc_ptr, dirname):
    print('*'*32)
    print(' Welcome to PYVED')
    print('*'*32)

    print()
    print(desc_ptr.read())
    print('---')

    print('Listing files:')
    
    t_dir = Path(dirname)
    for entry in t_dir.iterdir():
        print(entry.name)

# }} definition implem


# ------
#  main chunk of code
# -----
def main():
    args = parser.parse_args()
    if args.command == 'new':
        create_new_project(args.project)

    elif args.command == 'open':
        filepath = os.path.abspath(args.filepath)
        dirname = os.path.dirname(filepath)
        fptr = open(filepath, 'r')
        open_project(fptr, dirname)
        fptr.close()

    else:
        print(f"ERROR: command {args.command} is not a valid command!")
