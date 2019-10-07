#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ -z "$1" ]]; then
        vendor/premake/macos/premake5 xcode4
    else
        vendor/premake/macos/premake5 $1
    fi
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    if [[ -z "$1" ]]; then
        vendor/premake/linux/premake5 gmake2
    else
        vendor/premake/linux/premake5 $1
    fi
else
    echo "Environment not supported!"
fi