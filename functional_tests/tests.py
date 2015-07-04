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

        #When user hit enter, page updates, and now the page lists.
        # "1: Buy milk" as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')

        #There is still a text box inviting user to add another item.
        #User enters "Drink milk".
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Drink milk')
        inputbox.send_keys(Keys.ENTER)

        #Page updates again, and now shows both item on list.
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Drink milk')

        #User gets unique URL and there is explanation text for it.
        self.fail('Finish the tests!')

        #User visits unique URL and list is still there.

        #User closes browser.
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
