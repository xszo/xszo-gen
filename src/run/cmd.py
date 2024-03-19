# lower python

from os import system


# format code
def fmt() -> None:
    system(
        """
    npx prettier . --write;
    python3 -m black .;
    python3 -m isort . --profile black;
    """
    )


def ini_dev() -> None:
    system(
        """
    pipenv install --dev;
    """
    )


# install git repo
def ini_git() -> None:
    system(
        """
    git submodule update --init --recursive --remote;
    if ! git worktree list | grep -q out; then
        if [ -e out ]; then rm -rf out; fi;
        git worktree add out;
        fi;
    wait;

    git switch main;
    cd doc;
    git switch master;
    cd ../out;
    git switch etc;
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
    git switch etc;
    rm -rf *;
    cd ..;
    """
    )
