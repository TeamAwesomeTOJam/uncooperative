#!/usr/bin/bash

#usage: sh mvsprites.sh Team_Awesome...zip
#assumes the thing extracted is a "Team Awesome..." dir
sprites_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $sprites_dir
unzip $1 -d $sprites_dir
mv Team\ */* .
rmdir Team\ *
mkdir tiles
mv BG\ Tiles bg_tiles
mv Items items
mkdir -p chars
rm -rf chars/*
mv "Good Guys" chars/good_guys
ls chars/good_guys
read -p "press enter"
mv "Bad Guys" chars/bad_guys


for m in chars/good_guys/*  chars/bad_guys
do 
    pushd "$m"
    echo "Moving into $m"
    read -p "pause"
    pwd
    mv *Up* up
    mv *Down* down
    mv *Left* left
    mv *Right* right
    for dir in *
    do 
        if [ -d $dir ]
        then 
            pushd $dir 

            for file in *
            do 
                newfile=$(echo ${file%%.png} | sed 's/[a-z]//g' | sed 's/[A-Z]//g' | sed 's/_*//'| sed 's/-*//')
                echo $file " -> "  ${newfile}.png
                mv $file ${newfile}.png
            done
            popd
        fi 
    done
    popd
done
popd



