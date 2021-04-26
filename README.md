# cdprojektperl
## Python Dependencies
```
tabulate
pydot
```
## Instructions to run
```
git clone https://github.com/psiayn/cdprojektperl.git
cd cdprojektperl/
```
or if using git worktrees
```
git clone --bare https://github.com/psiayn/cdprojektperl.git
cd cdprojektperl.git/
git worktree add master
cd master/
```

```
cd ply/
git submodule update
cd ..
python parser_yacc.py test.pl
```	
