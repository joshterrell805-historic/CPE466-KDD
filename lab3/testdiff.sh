#!/bin/bash
if [ "$1" == "--help" -o "$1" == "-h" ]
then
    cat <<EOF
testdiff [--help|--update]
EOF
    exit
fi

if [ "$1" == "--update" ]
then
    for i in data/*
    do
        echo "Computing results for $i"
        mkdir -p "$(dirname "testResults/$i")"
        ranker "$i" | sed '0,/Outdegree:/d' > "testResults/$i"
    done
elif [ "$1" == "--diff" ]
then
    diff -q "testResults/$i" <(ranker "$i" | sed '0,/Outdegree:/d')
else
    for i in data/*
    do
        if diff -q "testResults/$i" <(ranker "$i" | sed '0,/Outdegree:/d')
        then
            echo "[32mPass $i[0m"
        else
            echo "[31mFail $i[0m"
        fi
    done
fi

