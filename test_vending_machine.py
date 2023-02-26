import pytest
from VendingMachine import VendingMachine
import random


class ParametersForTests:
    CORRECT_ID = 117345294655382
    MAX_COUNT_OF_COIN_1 = 50
    MAX_COUNT_OF_COIN_2 = 50
    COIN_1_VALUE = 1
    COIN_2_VALUE = 2
    MAX_COUNT_OF_PRODUCT_1 = 30
    MAX_COUNT_OF_PRODUCT_2 = 40


@pytest.fixture(scope="function")
def operation_machine():
    return VendingMachine()


@pytest.fixture(scope='function')
def administrator_machine(operation_machine):
    operation_machine.enterAdminMode(ParametersForTests.CORRECT_ID)
    return operation_machine


def test_get_price_1(operation_machine):
    assert operation_machine.getPrice1() == 8
    operation_machine.enterAdminMode(ParametersForTests.CORRECT_ID)
    assert operation_machine.getPrice1() == 8


def test_get_price_2(operation_machine):
    assert operation_machine.getPrice2() == 5
    operation_machine.enterAdminMode(ParametersForTests.CORRECT_ID)
    assert operation_machine.getPrice2() == 5


def test_current_sum_initial(operation_machine):
    assert operation_machine.getCurrentSum() == 0
    operation_machine.enterAdminMode(ParametersForTests.CORRECT_ID)
    assert operation_machine.getCurrentSum() == 0


def test_fill_coins_illegal(operation_machine):
    assert operation_machine.fillCoins(4, 5) == VendingMachine.Response.ILLEGAL_OPERATION


@pytest.mark.parametrize("first_count,second_count,expected_response",
                         [(-50, 20, VendingMachine.Response.INVALID_PARAM),
                          (0, 20, VendingMachine.Response.INVALID_PARAM),
                          (51, 20, VendingMachine.Response.INVALID_PARAM),
                          (25, -15, VendingMachine.Response.INVALID_PARAM),
                          (25, 0, VendingMachine.Response.INVALID_PARAM),
                          (25, 51, VendingMachine.Response.INVALID_PARAM),
                          (1, 50, VendingMachine.Response.OK),
                          (50, 1, VendingMachine.Response.OK),
                          (20, 25, VendingMachine.Response.OK)])
def test_fill_coins(administrator_machine, first_count, second_count, expected_response):
    assert administrator_machine.fillCoins(first_count, second_count) == expected_response


@pytest.mark.parametrize("first_count,second_count,expected", [(30, 45, 120),
                                                               (23, 15, 53),
                                                               (17, 24, 65),
                                                               (12, 14, 40)])
def test_current_sum_changed(administrator_machine, first_count, second_count, expected):
    administrator_machine.fillCoins(first_count, second_count)
    assert administrator_machine.getCurrentSum() == expected
    administrator_machine.exitAdminMode()
    assert administrator_machine.getCurrentSum() == 0


def test_enter_admin_mode_negative(operation_machine):
    assert operation_machine.enterAdminMode(202) == VendingMachine.Response.INVALID_PARAM
    assert operation_machine.getCurrentMode() == VendingMachine.Mode.OPERATION
    operation_machine.putCoin1()
    operation_machine.putCoin2()
    assert operation_machine.enterAdminMode(ParametersForTests.CORRECT_ID) == VendingMachine.Response.CANNOT_PERFORM
    assert operation_machine.getCurrentMode() == VendingMachine.Mode.OPERATION


def test_enter_admin_mode(operation_machine):
    assert operation_machine.getCurrentMode() == VendingMachine.Mode.OPERATION
    assert operation_machine.enterAdminMode(ParametersForTests.CORRECT_ID)
    assert operation_machine.getCurrentMode() == VendingMachine.Mode.ADMINISTERING


def test_exit_admin_mode(operation_machine):
    operation_machine.enterAdminMode(ParametersForTests.CORRECT_ID)
    assert operation_machine.getCurrentMode() == VendingMachine.Mode.ADMINISTERING
    operation_machine.exitAdminMode()
    assert operation_machine.getCurrentMode() == VendingMachine.Mode.OPERATION


def test_put_coin_1_overflow(operation_machine):
    iterator = 0
    while iterator < ParametersForTests.MAX_COUNT_OF_COIN_1:
        operation_machine.putCoin1()
        iterator += 1
    assert operation_machine.putCoin1() == VendingMachine.Response.CANNOT_PERFORM


def test_put_coin1_illegal(administrator_machine):
    assert administrator_machine.putCoin1() == VendingMachine.Response.ILLEGAL_OPERATION


def test_put_coin1_positive(operation_machine):
    count = random.randint(1, ParametersForTests.MAX_COUNT_OF_COIN_1 - 1)
    iterator = 0
    while iterator < count:
        operation_machine.putCoin1()
        iterator += 1
    assert operation_machine.putCoin1() == VendingMachine.Response.OK
    assert operation_machine.getCurrentBalance() == ParametersForTests.COIN_1_VALUE * (count + 1)


def test_put_coin_2_overflow(operation_machine):
    iterator = 0
    while iterator < ParametersForTests.MAX_COUNT_OF_COIN_2:
        operation_machine.putCoin2()
        iterator += 1
    assert operation_machine.putCoin2() == VendingMachine.Response.CANNOT_PERFORM


def test_put_coin2_illegal(administrator_machine):
    assert administrator_machine.putCoin2() == VendingMachine.Response.ILLEGAL_OPERATION


def test_put_coin2_positive(operation_machine):
    count = random.randint(1, 16)
    iterator = 0
    while iterator < count:
        operation_machine.putCoin2()
        iterator += 1
    assert operation_machine.putCoin2() == VendingMachine.Response.OK
    assert operation_machine.getCurrentBalance() == ParametersForTests.COIN_2_VALUE * (count + 1)


def test_fill_products(operation_machine):
    assert operation_machine.fillProducts() == VendingMachine.Response.ILLEGAL_OPERATION
    operation_machine.enterAdminMode(ParametersForTests.CORRECT_ID)
    assert operation_machine.fillProducts() == VendingMachine.Response.OK


def test_get_number_of_product_1(administrator_machine):
    assert administrator_machine.getNumberOfProduct1() == 0
    administrator_machine.fillProducts()
    assert administrator_machine.getNumberOfProduct1() == ParametersForTests.MAX_COUNT_OF_PRODUCT_1


def test_get_number_of_product_2(administrator_machine):
    assert administrator_machine.getNumberOfProduct2() == 0
    administrator_machine.fillProducts()
    assert administrator_machine.getNumberOfProduct2() == ParametersForTests.MAX_COUNT_OF_PRODUCT_2


def test_set_prices_illegal(operation_machine):
    assert operation_machine.setPrices(4, 6) == VendingMachine.Response.ILLEGAL_OPERATION


@pytest.mark.parametrize("first_price,second_price,expected_response", [(-13, 4, VendingMachine.Response.INVALID_PARAM),
                                                                        (4, -13, VendingMachine.Response.INVALID_PARAM),
                                                                        (0, 4, VendingMachine.Response.INVALID_PARAM),
                                                                        (4, 0, VendingMachine.Response.INVALID_PARAM),
                                                                        (-5, -2, VendingMachine.Response.INVALID_PARAM),
                                                                        (1, 1, VendingMachine.Response.OK),
                                                                        (23, 15, VendingMachine.Response.OK)])
def test_set_prices(administrator_machine, first_price, second_price, expected_response):
    assert administrator_machine.setPrices(first_price, second_price) == expected_response


def test_give_product_1_illegal(administrator_machine):
    assert administrator_machine.giveProduct1(5) == VendingMachine.Response.ILLEGAL_OPERATION


@pytest.mark.parametrize("number, expected_response", [(-20, VendingMachine.Response.INVALID_PARAM),
                                                       (0, VendingMachine.Response.INVALID_PARAM),
                                                       (ParametersForTests.MAX_COUNT_OF_PRODUCT_1,
                                                        VendingMachine.Response.INVALID_PARAM),
                                                       (ParametersForTests.MAX_COUNT_OF_PRODUCT_1 + 20,
                                                        VendingMachine.Response.INVALID_PARAM)])
def test_give_product_1_technical_limitations(operation_machine, number, expected_response):
    assert operation_machine.giveProduct1(number) == expected_response


def test_give_product_1_existence_boundaries(operation_machine):
    assert operation_machine.giveProduct1(1) == VendingMachine.Response.INSUFFICIENT_PRODUCT


@pytest.mark.parametrize("first_coin,second_coin,number,price_one,price_two,one_coins,two_coins,expected_response",
                         [(0, 0, 2, 2, 1, 1, 1, VendingMachine.Response.INSUFFICIENT_MONEY),
                          (0, 0, 1, 1, 1, 2, 0, VendingMachine.Response.OK),
                          (1, 1, 2, 3, 1, 2, 4, VendingMachine.Response.OK),
                          (0, 0, 1, 3, 1, 0, 4, VendingMachine.Response.UNSUITABLE_CHANGE),
                          (0, 0, 2, 3, 1, 1, 4, VendingMachine.Response.OK)])
def test_give_product_1(administrator_machine, first_coin, second_coin, number, price_one, price_two, one_coins,
                        two_coins, expected_response):
    administrator_machine.fillProducts()
    administrator_machine.fillCoins(first_coin, second_coin)
    administrator_machine.setPrices(price_one, price_two)
    administrator_machine.exitAdminMode()
    iterator = 0
    while iterator < one_coins:
        administrator_machine.putCoin1()
        iterator += 1
    iterator = 0
    while iterator < two_coins:
        administrator_machine.putCoin2()
        iterator += 1
    assert administrator_machine.giveProduct1(number) == expected_response


def test_give_product_2_illegal(administrator_machine):
    assert administrator_machine.giveProduct2(5) == VendingMachine.Response.ILLEGAL_OPERATION


@pytest.mark.parametrize("number, expected_response", [(-20, VendingMachine.Response.INVALID_PARAM),
                                                       (0, VendingMachine.Response.INVALID_PARAM),
                                                       (ParametersForTests.MAX_COUNT_OF_PRODUCT_2,
                                                        VendingMachine.Response.INVALID_PARAM),
                                                       (ParametersForTests.MAX_COUNT_OF_PRODUCT_2 + 20,
                                                        VendingMachine.Response.INVALID_PARAM)])
def test_give_product_2_technical_limitations(operation_machine, number, expected_response):
    assert operation_machine.giveProduct2(number) == expected_response


def test_give_product_2_existence_boundaries(operation_machine):
    assert operation_machine.giveProduct2(1) == VendingMachine.Response.INSUFFICIENT_PRODUCT


@pytest.mark.parametrize("first_coin,second_coin,number,price_one,price_two,one_coins,two_coins,expected_response",
                         [(2, 3, 4, 3, 5, 1, 3, VendingMachine.Response.INSUFFICIENT_MONEY),
                          (10, 10, 2, 4, 5, 32, 0, VendingMachine.Response.OK),
                          (10, 10, 2, 4, 5, 20, 6, VendingMachine.Response.OK),
                          (0, 0, 1, 3, 1, 0, 4, VendingMachine.Response.UNSUITABLE_CHANGE),
                          (0, 0, 2, 3, 1, 1, 4, VendingMachine.Response.OK)])
def test_give_product_2(administrator_machine, first_coin, second_coin, number, price_one, price_two, one_coins,
                        two_coins, expected_response):
    administrator_machine.fillProducts()
    administrator_machine.fillCoins(first_coin, second_coin)
    administrator_machine.setPrices(price_one, price_two)
    administrator_machine.exitAdminMode()
    iterator = 0
    while iterator < one_coins:
        administrator_machine.putCoin1()
        iterator += 1
    iterator = 0
    while iterator < two_coins:
        administrator_machine.putCoin2()
        iterator += 1
    assert administrator_machine.giveProduct2(number) == expected_response


def test_return_money_illegal(administrator_machine):
    assert administrator_machine.returnMoney() == VendingMachine.Response.ILLEGAL_OPERATION


@pytest.mark.parametrize("one_coins,two_coins,expected_response", [(0, 0, VendingMachine.Response.OK),
                                                                   (3, 3, VendingMachine.Response.OK),
                                                                   (0, 3, VendingMachine.Response.OK)])
def test_return_money(operation_machine, one_coins, two_coins, expected_response):
    iterator = 0
    while iterator < one_coins:
        operation_machine.putCoin1()
        iterator += 1
    iterator = 0
    while iterator < two_coins:
        operation_machine.putCoin2()
        iterator += 1
    assert operation_machine.returnMoney() == expected_response


def test_get_coins_1(administrator_machine):
    administrator_machine.fillCoins(4, 5)
    assert administrator_machine.getCoins1() == 4
    administrator_machine.exitAdminMode()
    assert administrator_machine.getCoins1() == 0


def test_get_coins2(administrator_machine):
    administrator_machine.fillCoins(4, 5)
    assert administrator_machine.getCoins2() == 5
    administrator_machine.exitAdminMode()
    assert administrator_machine.getCoins2() == 0
