#!/bin/bash

for i in $(ls *.lab)
do
	COSA=$(cat $i | wc -l)
	if [ "$COSA" != "0" ]
	then
		echo "$i tiene mas de una label."
	fi
done
