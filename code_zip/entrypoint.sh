#!/bin/bash

# init new repository
mkdir code/
cd code/
git init

# set arbitary name
git config --global user.name "bob"
git config --global user.email "bob@security.org"

# phase 1
cp -r ../samples/phase1/* .
git add .
git commit -m "initial commit"
git commit --amend --date="Sat Feb 8 14:12 2019 +0100" --no-edit

# phase 2
cp -r ../samples/phase2/* .
# change to correct flag
sed -i 's/PLACEHOLDER/'"$FLAG"'/' lib/security.py
git add .
git commit -m "add security.py"
git commit --amend --date="Sun Feb 9 08:16 2019 +0100" --no-edit

# phase 3
cp -r ../samples/phase3/* .
git add .
git commit -m "update security.py"
git commit --amend --date="Mon Feb 10 23:14 2019 +0100" --no-edit

# phase 4
cp -r ../samples/phase4/* .
git add .
git commit -m "add geometry.py"
git commit --amend --date="Tue Feb 11 11:32 2019 +0100" --no-edit

# phase 5
cp -r ../samples/phase5/* .
git add .
git commit -m "add shapes.py"
git commit --amend --date="Thu Feb 13 15:47 2019 +0100" --no-edit

# zip the code
cd ..
zip -r code.zip code/

# run the program
python service.py
