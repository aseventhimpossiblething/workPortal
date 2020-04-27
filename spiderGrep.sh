#!/bin/bash
touch brokenLines
echo running grep
cat spiderfile | grep " broken" >brokenLines
