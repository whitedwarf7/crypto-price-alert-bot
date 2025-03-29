import os
import boto3
import requests
from requests.exceptions import RequestException

dynamodb = boto3.resource('dynamodb')
alerts_table = dynamodb.Table('Alerts')
users_table = dynamodb.Table('Users')
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

def fetch_prices(cryptos):
    crypto_ids = {'BTC': 'bitcoin', 'ETH': 'ethereum'}  # Add more mappings
    ids = [crypto_ids[c] for c in cryptos if c in crypto_ids]
    params = {'ids': ','.join(ids), 'vs_currencies': 'usd'}
    response = requests.get(COINGECKO_URL, params=params)
    return response.json()

def lambda_handler(event, context):
    # Fetch all active alerts
    alerts = alerts_table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('active').eq(True))['Items']
    
    # Group alerts by cryptocurrency
    crypto_alerts = {}
    for alert in alerts:
        crypto = alert['cryptocurrency']
        if crypto not in crypto_alerts:
            crypto_alerts[crypto] = []
        crypto_alerts[crypto].append(alert)
    
    # Fetch prices for all cryptos
    prices = fetch_prices(crypto_alerts.keys())
    
    # Check each alert
    for crypto, alerts in crypto_alerts.items():
        current_price = prices.get(crypto.lower(), {}).get('usd')
        if not current_price:
            continue
        
        for alert in alerts:
            user_id = alert['user_id']
            target_price = alert['target_price']
            condition = alert['condition']
            
            # Check if condition is met
            trigger = (condition == 'above' and current_price > target_price) or \
                      (condition == 'below' and current_price < target_price)
            
            if trigger:
                # Send Telegram alert
                message = f"🚨 {crypto} is now ${current_price} ({condition} ${target_price})!"
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={'chat_id': user_id, 'text': message}
                )
                
                # Deactivate alert
                alerts_table.update_item(
                    Key={'alert_id': alert['alert_id']},
                    UpdateExpression="SET active = :active",
                    ExpressionAttributeValues={':active': False}
                )
    
    return {'statusCode': 200}