#!/usr/bin/bash
for i in {1..10}
do
for var in {1..6}
do
	x=$(( var + ( i * 6 ) ))
	echo "testfiles/$var.json -> testfiles/$x.json"
	cp "testfiles/$var.json" "testfiles/$x.json"
done
done
