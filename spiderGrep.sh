#!/bin/bash
echo running grep
cat spiderfile|grep " broken" >brokenLines
