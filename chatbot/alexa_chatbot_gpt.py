import time
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


from openaiutils import generate_alexa_answers
from openai import OpenAI
import logging
import re #Import the regex library
import datetime

def print_current_time():
    """Prints the current time in HH:MM:SS format."""
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")  # Format as HH:MM:SS
    print(current_time)





DEPTH_THRESHOLD = 30
DUP_COUNT = 3
CONVERSATION_THRESHOLD = 50
RETRY_THRESHOLD = 20
KEY2 = "Api key."
MAX_DURATION = 300
MAX_PROMPT_DURATION = 120
MAX_TREE_DURATION = 60

client = OpenAI(
    # This is the default and can be omitted
    api_key=KEY2,
)

import speech_recognition as sr
import requests
from pydub import AudioSegment

from itertools import groupby

from selenium.webdriver.common.by import By

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)





def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)
class ChatWithAlexa:
    '''Class that handles data storage and interactions.'''
    def __init__(self, test_url, usrname, passwd):
        self.url = test_url
        self.usrname = usrname
        self.passwd = passwd
        self.audio_url = ""
        self.img_url = ""
        self.text2 = []
        self.urls = set()
        self.conversation_count = 0
        self.skill_count = 0
        self.overall_elapsed_time = 0
        client = OpenAI(
            api_key=KEY2,
        )
        self.client = client
        self.driver = webdriver.Chrome()
        self.stringList = []

    def get_text_with_exponential_backoff(self, max_retries=3, base_delay=1):
        """
        Retrieves text with exponential backoff if the last message is a request.

        Args:
            max_retries: The maximum number of retry attempts.
            base_delay: The initial delay in seconds.

        Returns:
            True if a response is found, False if max retries reached and still a request.
        """

        for attempt in range(max_retries):
            self.get_text()  # Get the text
            if self.text and self.text[-1][1] == "request":  # Check if text exists and last message is a request
                if attempt == max_retries - 1:
                    return False  # Max retries reached, still a request
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)  # Calculate delay with jitter
                print(f"Retrying in {delay:.2f} seconds (attempt {attempt + 1}/{max_retries})...")  # Informative message
                time.sleep(delay)
            else:
                return True  # Found a response or text is empty

        return False #Should not reach here, but added just in case

    def start_browser(self):
        """Sign in to the dev portal."""
        self.browser = self.driver
        self.browser.get(self.url) # You have to replace the url with your own skills' testing page url
        self.driver.implicitly_wait(1)
        try:
            self.browser.find_element(By.ID, "ap_email").send_keys(self.usrname)
        except NoSuchElementException:
            input("Press Enter to continue...")
            self.browser.find_element(By.ID, "ap_email").send_keys(self.usrname)

        self.browser.find_element(By.ID, "continue").click()
        self.driver.implicitly_wait(2)
        self.browser.find_element(By.ID, "ap_password").send_keys(self.passwd)

        self.browser.find_element(By.ID, "signInSubmit").click()
        time.sleep(2)

    def get_final_interaction(self):
        """Get data after a disable command."""
        self.get_text()
        urls = []
        links = self.get_http_links()
        self.urls |= links

        self.stringList.append(((self.text), (self.urls)))
 
    def sent_request(self, request):
        """This function sends a prompt or request ot Alexa.
        It then grabs all hrefs, and specifically grabs bucket image references and audio references."""
        # self.driver.maximize_window() # For maximizing window. Don't do this, it's a pain
        self.driver.implicitly_wait(15) # gives an implicit wait for 25 seconds. This allows all audio to be found.
        self.browser.find_element(By.CSS_SELECTOR,'input.react-autosuggest__input').send_keys(request)
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR,"input.react-autosuggest__input").send_keys(Keys.RETURN)
        time.sleep(2)
        i = 0
        urls = []
        continueSearch = True
        new_audio_url = self.get_audio_url()
        new_img_url = self.get_img_url()
        if(new_img_url == "no image url"):
            continueSearch = False
        while i < 3: # check utls 3 times.
            new_audio_url = self.get_audio_url()
            if(continueSearch == True):
                new_img_url = self.get_img_url()
            if self.audio_url != new_audio_url:
                i = 0
                urls.append(new_audio_url)
                self.audio_url = new_audio_url 
            i += 1
            if self.img_url != new_img_url and (continueSearch == True):
                i = 0
                urls.append(new_img_url)
                self.img_url = new_img_url 
            time.sleep(0.2)
            i += 1
        self.get_text()
        links = self.get_all_hrefs()
        self.urls |= links
        self.urls |= set(urls)
        self.stringList.append(((self.text), (self.urls)))
        
    def chat_with_alexa(self, prompt_list):
        """Chat with alexa. Includes timeouts and depth counters, all adjustable with globals
        at the top of the file."""
        overall_start_time = time.time()
        self.skill_count += 1
        for prompt in prompt_list:
            # Iterate through given prompts.
            overall_elapsed_time = time.time() - overall_start_time
            if overall_elapsed_time > MAX_DURATION:
                    print(f"Time limit of {MAX_DURATION} seconds exceeded.")
                    self.sent_request(prompt_list[-1])
                    self.get_final_interaction()
                    self.overall_elapsed_time = self.overall_elapsed_time + overall_elapsed_time
                    print("Skill timed out")
                    print(f"Average time: {self.overall_elapsed_time/self.skill_count}")
                    break
            gpt_generated_multiple_choice_responses = {}
            tried_questions = []
            origional_prompt = prompt  
            retry_count = 0
            start_time = time.time()
            while True:
                # interact with a prompt tree.
                elapsed_time = time.time() - start_time
                if elapsed_time > MAX_PROMPT_DURATION:
                    print(f"Time limit of {MAX_PROMPT_DURATION} seconds exceeded.")
                    break
                if "nga" == prompt:
                    print("Invalid question")
                    break
                
                self.sent_request(prompt)
                if "Alexa, disable" in prompt:
                    time.sleep(2)
                    self.get_final_interaction()
                    self.overall_elapsed_time = self.overall_elapsed_time + overall_elapsed_time
                    print("Skill completed")
                    print(f"Average time: {self.overall_elapsed_time/self.skill_count}")
                    break
                # We do this to prevent endlessly generated requests if the resonse from Alexa is slow.
                if not self.get_text_with_exponential_backoff():
                    break
                result = self.get_newest_response()
                
                if result in tried_questions:
                    self.sent_request(origional_prompt)
                    if not self.get_text_with_exponential_backoff():
                        break
                    result = self.get_newest_response()
                depth_count = 0
                start_time_2 = time.time()
                while True:
                    elapsed_time_2 = time.time() - start_time_2
                    overall_elapsed_time_log = time.time() - overall_start_time
                    print(f"still Running: elapsed_time = {overall_elapsed_time_log}, current time: {print_current_time()}")
                    if elapsed_time_2 > MAX_TREE_DURATION:
                        print(f"Time limit of {MAX_TREE_DURATION} seconds exceeded.")
                        break
                    depth_count = depth_count+ 1
                    self.text2.append(f"Quesion: {prompt}, Response: {result}") 
                    if "ok, here's" not in result.lower():
                        # Skip first response after successful invocation
                        if result in gpt_generated_multiple_choice_responses:
                            # if we have tried this question before, get the list of untried potential responses.
                            new_prompts = gpt_generated_multiple_choice_responses[result]
                            if gpt_generated_multiple_choice_responses[result] == []:
                                # Remove the branch when completed
                                gpt_generated_multiple_choice_responses.pop(result)
                                # Make sure we know we have finished this branch
                                tried_questions.append(result)
                                break
                        else:
                            new_prompts = (generate_alexa_answers(self.client, result))
                            if "nga" == new_prompts[0].lower():
                                # Quit if there is no good answer
                                prompt = "nga"
                                break
                        prompt = random.choice(new_prompts)
                        new_prompts.remove(prompt)
                        if result not in tried_questions:
                            # Make a new branch interaction list
                            gpt_generated_multiple_choice_responses[result] = new_prompts
                        self.sent_request(prompt)
                        if not self.get_text_with_exponential_backoff():
                            break
                        result = self.get_newest_response()
                        self.conversation_count = self.conversation_count + 1
                        if depth_count >= DEPTH_THRESHOLD:
                            break
                        if len(self.text) >= 6:
                            if self.check_last_three():
                                break

                    else:
                        self.get_text()
                        result = self.get_newest_response()
                    
                if len(gpt_generated_multiple_choice_responses) == 0:
                            # We have run out of branches
                            print("Stopped on completed paths")
                            break
                if retry_count >= RETRY_THRESHOLD:
                            break


    def chat_input(self, input_to_skill):
        """
        input to the test portal
        """
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR,'input.askt-utterance__input').send_keys(input_to_skill)
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR,"input.askt-utterance__input").send_keys(Keys.RETURN)
        time.sleep(15)

    def get_all_hrefs(self):
        """
        Gets all unique href values from <a> tags on the page.

        Args:
            driver: A Selenium WebDriver instance.

        Returns:
            A set of unique href values.
        """
        hrefs = set()
        # We do this with js code for speed and accuracy

        js_code = """
        const hrefs = new Set();

        // Get all elements with an href *attribute*
        const elementsWithHref = document.querySelectorAll('[href]');

        elementsWithHref.forEach(element => {
            const href = element.getAttribute('href'); // Use getAttribute for attributes
            if (href) {
                hrefs.add(String(href)); // Convert to string (important!)
            }
        });

        return Array.from(hrefs);
        """
        hrefs_list = self.driver.execute_script(js_code)
        # print(hrefs_list)
        # input("Press Enter to continue...")
        hrefs.update(hrefs_list)  # Add the hrefs to the Python set

        return hrefs


    def get_http_links(self):
        """Make sure we have all links"""
        links = set()

        # Combined XPath for href and src attributes (most efficient)
        link_elements = self.driver.find_elements(By.XPATH, "//a[@href[contains(.,'http') or contains(.,'https')]] | //*[@src[contains(.,'http') or contains(.,'https')]]")
        for element in link_elements:
            href = element.get_attribute("href")
            if href:
                links.add(href)
            src = element.get_attribute("src")
            if src:
                links.add(src)

        return links

    def get_audio_url(self):
        """
        if this skill uses a recording, get it from the test portal

        we call this skill as a one line
        """

        audio_url = self.browser.find_element(by=By.ID, value='asf-player-Dialog').get_attribute('src')

        return audio_url
    def get_img_url(self):
        """
        if this skill uses an image, get it from the test portal

        we call this skill as a one line
        """
        img_url = ""
        try:
            image_url = self.browser.find_element(by = By.XPATH, value = ("//*[contains(@href, 's3')]")).get_attribute('href')#
        except:
            image_url = "no image url"
            print("No image URL")


        return image_url

    def get_text(self):
        """Get the request response pair."""
        
        text = []
        
        for xx in self.browser.find_elements(by = By.CSS_SELECTOR,value = ("p.askt-dialog__message")):

            xx_attribute = xx.get_attribute("class").split(" ")[1]

            if xx_attribute == "askt-dialog__message--request":
                xx_attribute = 'request'
                text.append([xx.text,xx_attribute])
            elif xx_attribute == "askt-dialog__message--active-response" or xx_attribute == "askt-dialog__message--response" :
                xx_attribute = 'response'
                text.append([xx.text,xx_attribute])

        self.text = text
    
    def get_newest_response(self):
        #this function assumes that self.get_text() is already run
        for t in self.text[::-1]:
            if t[1] == 'response':
                return t[0]
            else:
                continue
        # print(self.text)
        raise "no response found"

    def check_last_three(self):
        #to prevent looping, we check last three element of the response
        #if all equal(same string), we assume it's stuck in a dead loop
        last_three = []
        for t in self.text[::-1]:
            if len(last_three) >= 3:
                break
            if t[1] == 'response':
                last_three.append(hash(t[0]))
        if len(set(last_three)) == 1:
            return True

