#!/bin/bash
echo running grep
touch brokenLines
cat spiderfile|grep " broken" >brokenLines
