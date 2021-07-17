#!/bin/bash

add_service () {
  [[ -z $1 ]] && { echo Specify the absolute path to a dictionary.; exit 1; }
  local path2vocab=$1

  cat /dev/null > memo.service

  memoservice=$(cat auto/service.stencil)
  memoservice+="\n
  User=$(whoami)
  WorkingDirectory=$PWD/base

  ExecStart=$(which python) \\
  $PWD/base/main.py \\
  $path2vocab"

  echo -e "$memoservice" >> memo.service
  chmod +x memo.service

  echo "To create a symlink in /etc/systemd/system and enable"
  echo "a service, password is required on the first run."

  sudo ln -sf "$PWD"/memo.service /etc/systemd/system/memo.service
  sudo systemctl enable memo.service && \
    { echo -e "\n";
      echo Successfully installed! Now memo service runs at startup.;
      echo One can abolish runs on boot, start the service immediately;
      echo after installation, or stop it with:;
      echo
      echo "    sudo systemctl disable memo.service";
      echo "    sudo systemctl start memo.service";
      echo "    sudo systemctl stop memo.service"; }
}


add_anacron_job () {
  [[ -z $1 ]] && exit
  local collection_id=$1
  cmd="bash $PWD/auto/update-dict.sh $collection_id\n"

  period=$2
  delay=15

  if ! grep -q "update-dict.memo" /etc/anacrontab
  then
    echo -e "$period $delay update-dict.memo $cmd" \
      | sudo tee -a /etc/anacrontab > /dev/null
    [[ $? -eq 0 ]] && echo Success! Added anacron job!
  else
    echo Anacron job is already set!
  fi
}



####################################
##########     MAIN     ############
####################################
if ! [[ "$0" =~ ^(./)?install.sh$ ]]
then
  echo Running outside the memo project! Aborted.
  exit 1
fi

[[ $# -ne 1 ]] && { echo The script takes exactly one argument; exit 1; }
{ [[ -f $1 ]] && code=1; } || { bash script.sh $1 2> /dev/null && code=2; } \
  || { echo Neither a path to vocabulary nor a collection id passed.; exit 1; }

[[ $code -eq 1 ]] && path2vocab=$1
[[ $code -eq 2 ]] && path2vocab=$PWD/dict/vocabulary.txt && collection_id=$1

add_service $path2vocab
add_anacron_job $collection_id
