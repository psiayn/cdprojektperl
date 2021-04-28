# Perl Mini Compiler
## Python Dependencies
```
tabulate
pydot
```
Install the required libraries by running
```
pip install -r requirements.txt
```
The ```ply``` library is also used. You can install it via
```
pip install ply
```
or you can use the submodule included with this repository.
## Instructions to run
```
git clone https://github.com/psiayn/cdprojektperl.git
cd cdprojektperl/
```
If you wish to use ply as a submodule
```
git clone --recurse-submodules https://github.com/psiayn/cdprojektperl.git
cd cdprojektperl/
```
If you are using git worktrees
```
git clone --bare https://github.com/psiayn/cdprojektperl.git
cd cdprojektperl.git/
git worktree add master
cd master/
```
Populating the submodule(ignore if you used ```git clone --recurse```)
```
cd ply/
git submodule update
cd ..
python parser_yacc.py test.pl
```	
This project was completed as a part of the UE18CS351 course on Compiler Design at PES University