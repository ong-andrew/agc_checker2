import time
import requests
import smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage
from discord_webhook import DiscordWebhook

results = requests.get("http://www.federalgazette.agc.gov.my/eng_main/main_warta_harian.php?jenis_pu=pua&&y=2021")
src = results.content
soup = BeautifulSoup(src, 'lxml')
table = soup.find('table', attrs={'id': 'theTable'})
row = table.find('td', attrs={'id': 'tarikh_1', 'class': 'sized2'})

webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/820682768706306049/f23662mfiRcIGGYFUgup-i60BgxFCUMCD17zNBnLoBRpCYzOGs0lbBhlitFwICis2l-k',
    content="PU_A checker start - Aizu's server")
execute = webhook.execute()

while True:
    try:
        old_legislationNumber = row.getText()
        time.sleep(1800)
        new_legislationNumber = row.getText()
        if old_legislationNumber == new_legislationNumber:
            continue
        else:
            content = '''
            
            New Federal Gazette [test]
             
            Click: http://www.federalgazette.agc.gov.my/eng_main/main_warta_harian.php?jenis_pu=pua&&y=2021
            
            - AO
            '''
            webhook2 = DiscordWebhook(
                url='https://discord.com/api/webhooks/820682768706306049/f23662mfiRcIGGYFUgup-i60BgxFCUMCD17zNBnLoBRpCYzOGs0lbBhlitFwICis2l-k',
                content=content)
            execute = webhook2.execute()

            msg = EmailMessage()
            msg.set_content(content)
            recipients = ['andrew@malaysiakini.com', 'editor@malaysiakini.com']
            msg['From'] = 'newsdesk.bot@malaysiakini.com'
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = 'Changes on Federal Gazette website'

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('newsdesk.bot@malaysiakini.com', 'mkini@KINI2021')
            server.send_message(msg)
            server.quit()
            time.sleep(3600)
            continue

    except Exception as e:
        webhook3 = DiscordWebhook(
            url='https://discord.com/api/webhooks/820682768706306049/f23662mfiRcIGGYFUgup-i60BgxFCUMCD17zNBnLoBRpCYzOGs0lbBhlitFwICis2l-k',
            content=e)
        execute = webhook3.execute()
