#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ -z "$1" ]]; then
        vendor/premake/macos/premake xcode4
    else
        vendor/premake/macos/premake $1
    fi
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    if [[ -z "$1" ]]; then
        vendor/premake/macos/premake gmake2
    else
        vendor/premake/macos/premake $1
    fi
else
    echo "Environment not supported!"
fi