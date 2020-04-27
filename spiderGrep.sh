#!/bin/bash
touch brokenLines
echo running grep
cat spiderfile | grep -n " broken" >brokenLines
cat brokenLines
echo finished grep
