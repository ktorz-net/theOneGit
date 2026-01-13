# The One Git: a project to rule them all

_The One Git_ is mainly designed to manage recursivelly a collection of git repos.

## Get-stated:

```bash
git clone https://github.com/imt-mobisyst/theOneGit
theOneGit/bin/instal.sh
# in a fresh new shell:
tog help
```

## Manual install...

Install commands tools with pip.

We recommand to set set an environnement variable `$THE_ONE_GIT` with the path to your `theOneGit` directory and to source the `bin/run-commands` in your favorit shell' run-commands file (`~/.bashrc` for bash).

`bash` for instance:

```bash
echo """
# The One Git
export THE_ONE_GIT=/home/you/path/to/theOneGit
source \$THE_ONE_GIT/run-commands.bash
""" >> ~/.bashrc
source ~/.bashrc
```
