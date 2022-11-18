from tests.helper.samples import BasicFullInterval10, BasicInitialOnly, BasicStepOnly


def basicStepOnly(name):
    St = BasicStepOnly
    St.name = name
    return St


def basicInitialOnly(name):
    St = BasicInitialOnly
    St.name = name
    return St


def basicFullInterval10(name):
    St = BasicFullInterval10
    St.name = name
    return St
