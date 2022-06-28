                                                # WEBSITE SCRAPPING PROJECT 
                                                
                                                
import env #contains my access keys and secret my secret access keys for AWS rolethat has the SNS publish permission associated with it
import requests #this allows us to make HTTP request via python
import json #allows us to convert between strings and python objects
import boto3 #library to interact with AWS services and it is unique to python
from datetime import datetime #because we're gpoing to print the date and time throughout this script
import time
print('AWS Website Scrapping Project')
URL = 'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=&postalCode=M5G2C3&skus=15507363'
#we store API call in a variable
headers = { #we store headers in an object
	'authority': 'www.bestbuy.ca',
	'pragma': 'no-cache',
	'cache-control': 'no-cache',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
	'accept': '*/*',
	'sec-fetch-site': 'same-origin',
	'sec-fetch-mode': 'cors',
	'sec-fetch-dest': 'empty',
	'referer': 'https://www.bestbuy.ca/en-ca/product/zotac-nvidia-geforce-rtx-3080-ti-amp-holo-12gb-gddr6x-video-card/15507363',
	'accept-language': 'en-US,en;q=0.9'
}
def main():
    quantity = 0 #so as to run the while loop for very first time
    attempt = 0 #no of attempts counter

    while (quantity < 1):  # this loop runs until the quantity is greater than 1 for the very 1st time.
        response = requests.get(URL,headers=headers) # makes an API call to this endpoint
        response_formatted = json.loads(response.content.decode('utf-8-sig').encode('utf-8'))# formatting the response of API call

        quantity = response_formatted['availabilities'][0]['shipping']['quantityRemaining']#we want to extract all the keys out so that we can get the real value from the response

        if (quantity < 1): #out of stock
            #Out Of stock
            print('Time=' + str(datetime.now()) + "- Attempt=" + str(attempt)) # display real time of a particular attempt
            attempt += 1 #increment the counter by 1
            time.sleep(5) # wait for sometime then again iterate the loop
        else: # in stock
            print('Hey its in stock! Quantity=' + str(quantity))
            publish(quantity) #publishes to SNS topic which is going to send us an email/SMS 


def publish(quantity):# defining publish method
    arn = 'arn:aws:sns:us-east-1:206070559467:InStockTopic' #Amazon Resourse Name(ARN) used to uniquely identify AWS Resources
    sns_client = boto3.client( #It is an SNS client
        'sns',
        aws_access_key_id=env.accessKey, 
        aws_secret_access_key=env.secretKey,
        region_name='us-east-1'
    )

    response = sns_client.publish(TopicArn=arn, Message='Its in stock! Quantity=' + str(quantity))#prints/sends message to email/phone no
    print(response) # display the same message in our local terminal

main() #program starts from this main() call