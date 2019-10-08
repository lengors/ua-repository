#!/bin/bash
#echo "${@:2:}"
#echo "${@:2}"
eval $(find . -type f -name $1) "${@:2}"
