import os

os.system(
    """
varPkg=(git python3 python3-pip)
if [[ -x $(command -v xcode-select) ]]; then
  if ![[ -x $(command -v brew) ]]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    wait; fi
  if [[ -x $(command -v brew) ]]; then
    brew install -y $varPkg
  elif [[ -d /opt/homebrew ]]; then
    /opt/homebrew/bin/brew install -y $varPkg
  else echo no; fi
elif [[ -x $(command -v apt-get) ]]; then
  sudo apt-get install -y $varPkg
elif [[ -x $(command -v dnf) ]]; then
  sudo dnf install -y $varPkg
elif [[ -x $(command -v yum) ]]; then
  sudo yum install -y $varPkg
else
  echo no $varPkg
fi
"""
)
