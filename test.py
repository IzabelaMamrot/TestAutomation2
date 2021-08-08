"""
Test for rent a car
"""

import unittest

from selenium import webdriver, common
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class TestRantCar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("http://qalab.pl.tivixlabs.com/")

    def test_search_and_rent_a_car(self):
        self._fill_the_search_form()
        self._check_details()
        self._click_the_rent_in_details_page()
        self._fill_the_personal_form(name="test", last_name="test", card_number="123", email="test@test")
        self._click_the_submit_rent_button()

    def test_card_number_validator_in_personal_form(self):
        self._fill_the_search_form()
        self._check_details()
        self._click_the_rent_in_details_page()
        self._fill_the_personal_form(name="test", last_name="test", card_number="test", email="test@test")
        self._click_the_submit_rent_button()
        self.assertTrue(self.driver.find_element_by_class_name('alert-danger').text, "Card number contains wrong chars")
        self._check_the_user_is_still_on_rent_page()

    def test_email_validator_in_personal_form(self):
        self._fill_the_search_form()
        self._check_details()
        self._click_the_rent_in_details_page()
        self._fill_the_personal_form(name="test", last_name="test", card_number="123", email="test.eu")
        self._click_the_submit_rent_button()
        self.assertTrue(self.driver.find_element_by_class_name('alert-danger').text, "Please provide valid email")
        self._check_the_user_is_still_on_rent_page()

    def test_name_is_required_in_personal_form(self):
        self._fill_the_search_form()
        self._check_details()
        self._click_the_rent_in_details_page()
        self._fill_the_personal_form(name="", last_name="test", card_number="123", email="test.eu")
        self._click_the_submit_rent_button()
        self.assertTrue(self.driver.find_element_by_class_name('alert-danger').text, "Name is required")
        self._check_the_user_is_still_on_rent_page()

    def test_navigate_from_details_to_search_page(self):
        self._fill_the_search_form()
        self._click_the_search_button()

    def _check_details(self):
        country = self._get_country_name()
        city = self._get_city_name()
        details = self._get_car_body_information(country=country, city=city, pickup="2021-08-08", dropoff="2021-08-08")
        car_name = self._get_car_name()
        self._click_rent_button_in_search_page()
        self._assert_details_information(car_name=car_name, car_details=details)

    def _get_country_name(self):
        return self.driver.find_element_by_xpath("//div[1]/div/select/option[3]").text

    def _get_city_name(self):
        return self.driver.find_element_by_xpath("//div[2]/div/select/option[4]").text

    def _get_car_name(self):
        first_row = self._get_information__from_first_row_in_search_form_and_switch_to_list()
        return first_row[2] + " " + first_row[3]

    def _click_rent_button_in_search_page(self):
        self.driver.find_element_by_xpath("//div/table/tbody/tr[1]/td[6]/a").click()

    def _get_car_body_information(self, country, city, pickup, dropoff):
        first_row = self._get_information__from_first_row_in_search_form_and_switch_to_list()
        location = country + " " + city
        license = first_row[4] + " " + first_row[5]
        dict = {
            "Company": first_row[1],
            "Price per day": first_row[-2],
            "Location": location,
            "License plate": license,
            "Pickup date": pickup,
            "Dropoff date": dropoff
        }

    def _get_information__from_first_row_in_search_form_and_switch_to_list(self, number_of_row=1):
        get_first_row = self.driver.find_element_by_xpath("//div/table/tbody/tr[{}]".format(number_of_row)).text
        return get_first_row.split(" ")

    def _assert_details_information(self, car_name, car_details):
        name = self.driver.find_element_by_class_name("card-header").text
        self.assertTrue(name, car_name)
        body = self.driver.find_element_by_class_name("card-body").text
        self.assertTrue(body, car_details)

    def _fill_the_search_form(self):
        self.driver.find_element_by_xpath("//div[1]/div/select/option[3]").click()
        self.assertTrue(self.driver.find_element_by_xpath("//div[1]/div/select/option[3]").text, "Poland")
        self.driver.find_element_by_xpath("//div[2]/div/select/option[4]").click()
        self.assertTrue(self.driver.find_element_by_xpath("//div[2]/div/select/option[4]").text, "Wroclaw")
        pickup = self.driver.find_element_by_id("pickup")
        ActionChains(self.driver).move_to_element(pickup).click().send_keys(Keys.LEFT).send_keys(Keys.LEFT).send_keys(
            '08082021').perform()
        dropoff = self.driver.find_element_by_id("dropoff")
        ActionChains(self.driver).move_to_element(dropoff).click().send_keys(Keys.LEFT).send_keys(Keys.LEFT).send_keys(
            '08082021').perform()
        self.driver.find_element_by_xpath("//div/form/button").click()

    def _click_the_rent_in_details_page(self):
        self.driver.find_element_by_xpath("//div/div[2]/a").click()

    def _fill_the_personal_form(self, name, last_name, card_number, email):
        name_field = self.driver.find_element_by_id("name")
        ActionChains(self.driver).move_to_element(name_field).click().send_keys(name).perform()
        last_name_field = self.driver.find_element_by_id("last_name")
        ActionChains(self.driver).move_to_element(last_name_field).click().send_keys(last_name).perform()
        card_number_field = self.driver.find_element_by_id("card_number")
        ActionChains(self.driver).move_to_element(card_number_field).click().send_keys(card_number).perform()
        email_field = self.driver.find_element_by_id("email")
        ActionChains(self.driver).move_to_element(email_field).click().send_keys(email).perform()

    def _click_the_submit_rent_button(self):
        self.driver.find_element_by_xpath("//div/form/button").click()

    def _click_the_search_button(self):
        self.driver.find_element_by_class_name("nav-link").click()

    def _check_the_user_is_still_on_rent_page(self):
        self.driver.find_element_by_id("name").is_displayed()
        self.driver.find_element_by_id("last_name").is_displayed()
        self.driver.find_element_by_id("card_number").is_displayed()
        self.driver.find_element_by_id("email").is_displayed()

    def _check_the_user_is_on_start_page(self):
        self.assertTrue(self.driver.find_element_by_class_name("alert-danger").text,
                        "Please fill pickup and drop off dates")

    def tearDown(self):
        self.driver.get("http://qalab.pl.tivixlabs.com/")

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
