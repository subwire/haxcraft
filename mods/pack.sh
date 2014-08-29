#!/bin/sh
slug=$1
ver=$2
file=$3

if [ ! -d $slug ]; then
   mkdir $slug
fi
mkdir $slug/mods
mv "$file" $slug/mods/
cd $slug
zip -r $slug-$ver.zip mods
rm -r mods
cd ..

