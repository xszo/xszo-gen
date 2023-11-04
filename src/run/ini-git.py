import os

# install submodules
os.system(
    """
git submodule update --init --recursive
"""
)
# install worktrees
os.system(
    """
if ! git worktree list | grep -q out; then
  if [[ -e out ]]; then rm -rf out; fi
  git worktree add out etc
fi
"""
)
# correct branch
os.system(
    """
wait
git checkout -qf main
cd doc
git checkout -qf master
cd ../out
git checkout -qf etc
git pull -q --rebase
cd ..
"""
)
