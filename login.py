from seleniumwire import webdriver
import pickle






proxy = input("Enter Proxy")

options = {
            'proxy': {
                'http': 'http://{}'.format(proxy),
                'https': 'https://{}'.format(proxy),
                'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
                }
        }
bot  = webdriver.Firefox( seleniumwire_options=options )

bot.get("https://www.instagram.com/")


username = input("username :")

pickle.dump( bot.get_cookies() , open("{}.pkl".format(username),"wb"))

