#!/bin/bash

prefix=$(dirname $0)
dir=$prefix/../dict
collection_id=$1

python3 $prefix/download.py $collection_id
touch $dir/prevdict.txt

# diff returns   1 if differences were found.
# ------------  >1 if an error occurred.
diff --unchanged-line-format= \
  $dir/prevdict.txt $dir/newdict.txt >> $dir/vocabulary.txt

err_code=$?
[[ $err_code -gt 1 ]] && exit $err_code

mv $dir/newdict.txt $dir/prevdict.txt
