#!/bin/bash

eval $(find . -name $1) "${@:2:}"