import time
import datetime
import argparse
import boto3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

parser = argparse.ArgumentParser(description='Provide AWS keys to send email and SMS alerts')
parser.add_argument('-access', type=str, required=False,
                    help="AWS Access Key")
parser.add_argument('-secret', type=str, required=False,
                    help="AWS Secret Key")
args = parser.parse_args()

AWS_ACCESS_KEY = args.access
AWS_SECRET_KEY = args.secret


client = boto3.client(
    "sns",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="us-east-1"
)
topics = client.list_topics()

# Initiate the browser
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'

while True:
    browser.get(url)
    time.sleep(2)
    try:
        buy_button = browser.find_element_by_class_name('add-to-cart-button')
    except NoSuchElementException:
        print(datetime.datetime.now(), " NoSuchElementException")
        continue
    if buy_button.text == "Add to Cart":
        buy_button.click()
        # send SMS
        print(datetime.datetime.now(), " OMG IN STOCK")
        if AWS_ACCESS_KEY and AWS_SECRET_KEY:
            client.publish(
                TopicArn=topics["Topics"][0]["TopicArn"],
                Message="RTX 3080 IN STOCK AT " + url
            )
        while True:
            time.sleep(100)
    time.sleep(3)
