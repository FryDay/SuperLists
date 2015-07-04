#!/bin/python

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Webpage is opened.
        self.browser.get(self.live_server_url)

        #Page title and header should mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #Invite to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #User types "Buy milk" into a text box.
        inputbox.send_keys('Buy milk')

        #When user hits enter, they are taken to a new URL,
        #and now the page lists "1: Buy milk" as an item in
        #a to-do list table.
        inputbox.send_keys(Keys.ENTER)
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy milk')

        #There is still a text box inviting user to add another item.
        #User enters "Drink milk".
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Drink milk')
        inputbox.send_keys(Keys.ENTER)

        #Page updates again, and now shows both item on list.
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Drink milk')

        #User 2 comes to site.

        #New browser session to make sure that no information
        #from User is coming though from cookies.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #User 2 visits home page. There is no sign of User's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy milk', page_text)
        self.assertNotIn('Drink milk', page_text)

        #User 2 start a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do homework')
        inputbox.send_keys(Keys.ENTER)

        #User2 gets own unique URL
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user_list_url)

        #No trace of User's list.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy milk', page_text)
        self.assertIn('Do homework', page_text)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
