#!/bin/python

from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Webpage is opened.
        self.browser.get('http://localhost:8000')

        #Page title and header should mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        #Invite to enter a to-do item straight away.

        #User types "Buy milk" into a text box.

        #When user hit enter, page updates, and now the page lists.
        # "1: Buy milk" as an item in a to-do list.

        #There is still a text box inviting user to add another item.
        #User enters "Drink milk".

        #Page updates again, and now shows both item on list.

        #User gets unique URL and there is explanation text for it.

        #User visits unique URL and list is still there.

        #User closes browser.
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
