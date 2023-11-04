import os

os.system(
    """
cd out
git add --all
git commit -qm gen --amend --reset-author
git push -qf
cd ..
"""
)
