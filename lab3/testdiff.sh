#!/bin/bash
runranker() {
    mkdir -p "$(dirname "$2")"
    ranker "$1" | sed '0,/Outdegree:/d' > "$2"
}

if [ "$1" == "--help" -o "$1" == "-h" ]
then
    cat <<EOF
testdiff [--help|--update|--diff filepath]
EOF
    exit
fi

if [ "$1" == "--update" ]
then
    for i in data/*
    do
        echo "Computing results for $i"
        runranker "$i" "testResults/$i"
    done
elif [ "$1" == "--diff" ]
then
    file="$2"
    shift
    shift
    diff "$@" "testResults/$file" <(ranker "$file" | sed '0,/Outdegree:/d')
else
    for i in data/*
    do
        runranker "$i" "temp/tempResults/$i"
        echo diff "testResults/$i" "temp/tempResults/$i"
        if diff -q "testResults/$i" "temp/tempResults/$i"
        then
            echo "[32mPass $i[0m"
        else
            echo "[31mFail $i[0m"
        fi
    done
fi

