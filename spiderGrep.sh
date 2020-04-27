#!/bin/bash
touch brokenLines
echo running grep
cat spiderfile | grep -n " broken" >brokenLines
cat brokenLines
sleep 20s
echo waiting
#sleep 10
cat spiderfile | grep -n " broken" >brokenLines
cat brokenLines
#sleep 20
echo finished grep
