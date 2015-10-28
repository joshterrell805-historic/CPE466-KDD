#!/usr/bin/env bats

setup() {
    testdata='./tests/test_data'
}

@test "Basic run" {
    . ./bin/activate
    run induceC45 "$testdata/domain_basic.xml" "$testdata/training_basic.csv"
    diff -q 
}

@test "Restricted run" {
    . ./bin/activate
    run induceC45 "$testdata/domain_basic.xml" "$testdata/training_basic.csv" "$testdata/restictions.csv"
}
