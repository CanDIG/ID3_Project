#!/usr/bin/env python3
import numpy
import pytest
from src.id3_variants_training.__train__ import train
from src.id3_variants_training.__predict__ import predict

@pytest.fixture
def model_case1_train():
    trainfile = 'test_cases/case1/config.json'
    return train(True, trainfile, verbose=False)

@pytest.fixture
def model_case2_train():
    trainfile = 'test_cases/case2/config.json'
    return train(True, trainfile, verbose=False)

@pytest.fixture
def model_case3_train():
    trainfile = 'test_cases/case3/config.json'
    return train(True, trainfile, verbose=False)

def test_case1_on_train(model_case1_train):
    trainfile = 'test_cases/case1/config.json'
    expected = numpy.array([[3, 0], [0, 3]])

    results = predict(trainfile, model_case1_train).conf_matrix
    assert (results == expected).all()

def test_case1_on_test(model_case1_train):
    testfile = 'test_cases/case1/test-config.json'
    expected = numpy.array([[3, 0], [0, 3]])

    results = predict(testfile, model_case1_train).conf_matrix
    assert (results == expected).all()

def test_case2_on_train(model_case2_train):
    trainfile = 'test_cases/case2/config.json'
    expected = numpy.array([[4, 0, 0], [0, 4, 0], [0, 0, 4]])

    results = predict(trainfile, model_case2_train).conf_matrix
    assert (results == expected).all()

def test_case2_on_test(model_case2_train):
    testfile = 'test_cases/case2/test/config.json'
    expected = numpy.array([[4, 0, 0], [0, 4, 0], [0, 0, 4]])

    results = predict(testfile, model_case2_train).conf_matrix
    assert (results == expected).all()

def test_case3_on_train(model_case3_train):
    trainfile = 'test_cases/case3/config.json'
    expected = numpy.array([[15, 0, 0, 0, 0, 0],
                            [ 0, 9, 0, 0, 6, 0],
                            [ 0, 5, 9, 0, 1, 0],
                            [ 0, 0, 0,10, 5, 0],
                            [ 0, 0, 0, 0,15, 0],
                            [ 0, 0, 0, 0, 0,15]])

    results = predict(trainfile, model_case3_train).conf_matrix
    assert (results == expected).all()

def test_case3_on_test(model_case3_train):
    testfile = 'test_cases/case3/test-config.json'
    expected = numpy.array([[14, 0, 1, 0, 0, 0],
                            [ 0, 5, 1, 0, 9, 0],
                            [ 0, 3,12, 0, 0, 0],
                            [ 0, 0, 0,14, 1, 0],
                            [ 0, 0, 0, 0,15, 0],
                            [ 0, 0, 0, 0, 0,15]])

    results = predict(testfile, model_case3_train).conf_matrix
    assert (results == expected).all()

if __name__ == "__main__":
    model1 = model_case1_train()
    model2 = model_case2_train()
    model3 = model_case3_train()
    test_case1_on_train(model1)
    test_case1_on_test(model1)
    test_case2_on_train(model2)
    test_case2_on_test(model2)
    test_case3_on_train(model3)
    test_case3_on_test(model3)

