#!/bin/bash

eval $(find . -type f -name $1) "${@:2}"
