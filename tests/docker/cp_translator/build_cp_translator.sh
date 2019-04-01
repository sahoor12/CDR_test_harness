#!/usr/bin/env bash


BASE_IMAGE_NAME=harborreg01.revionics.local/cdr/cp_translator


if [ ! -z "$1" ]
then
    pushd "$(dirname "$0")"
    cp Dockerfile ../..
    pushd ../..
    docker build -t $BASE_IMAGE_NAME:$1 .
    rm ./Dockerfile
    popd
    popd
    echo $BASE_IMAGE_NAME:$1
fi
