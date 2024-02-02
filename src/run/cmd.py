# lower python

from os import system

from . import ren


# format code
def c() -> None:
    system(
        """
    npx prettier . --write
    isort . --profile black
    """
    )


# install modules with pip
def ini_pip() -> None:
    system(ren.PIP_BIN + " install -r " + ren.PIP_REQ)


# install git repo
def ini_git() -> None:
    system(
        """
    git submodule update --init --recursive --remote;
    if ! git worktree list | grep -q out; then
        if [ -e out ]; then rm -rf out; fi
        git worktree add out;
        fi
    wait;

    git switch -f main;
    cd doc;
    git switch -f master;
    cd ../out;
    git switch -f etc;
    git pull -r;
    cd ..;
    """
    )


# push dir out/ to branch etc
def out_push() -> None:
    system(
        """
    cd out;
    git switch etc;
    git add -A;
    git commit --amend --reset-author -qm run;
    git push -qf;
    cd ..;
    """
    )


# remove dir out/
def out_rm() -> None:
    system(
        """
    cd out;
    git switch -f etc;
    rm -rf *;
    cd ..;
    """
    )
