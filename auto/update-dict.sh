#!/bin/bash

collection_id=$1
dir=../dict

mkdir -p $dir
touch $dir/prevdict.txt

python download.py $collection_id

diff --unchanged-line-format= \
  $dir/prevdict.txt $dir/newdict.txt >> $dir/vocabulary.txt
