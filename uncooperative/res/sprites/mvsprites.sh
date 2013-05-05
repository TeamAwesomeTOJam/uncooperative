#!/usr/bin/bash

#usage: sh mvsprites.sh Team_Awesome...zip
#assumes the thing extracted is a "Team Awesome..." dir
sprites_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $sprites_dir
unzip Team_* -d $sprites_dir
mv Team\ */* .
rmdir Team\ *
mkdir tiles
mv BG\ Tiles bg_tiles
mv Items items
mkdir -p chars
mv "Good Guys/Doda" chars/good_guys
mv "Bad Guys" chars/bad_guys


for m in chars/good_guys chars/bad_guys
do 
    pushd "$m"
    echo "Moving into $m"
    pwd
    mv *Up* up
    mv *Down* down
    mv *Left* left
    mv *Right* right
    for dir in *
    do 
        pushd $dir 
        for file in *
        do 
            newfile=$(echo ${file%%.png} | sed 's/[a-z]//g' | sed 's/[A-Z]//g' | sed 's/_*//' | sed 's/0*//')
            mv $file ${newfile}.png
        done
        popd
    done
    popd
done
popd



