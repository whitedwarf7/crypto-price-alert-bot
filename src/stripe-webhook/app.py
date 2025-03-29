import stripe
import os
import json
import boto3

stripe.api_key = os.environ['STRIPE_SECRET_KEY']
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('Users')

def lambda_handler(event, context):
    payload = event['body']
    sig_header = event['headers']['stripe-signature']
    
    try:
        # Verify webhook signature
        webhook_event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ['STRIPE_WEBHOOK_SECRET']
        )
        
        if webhook_event['type'] == 'checkout.session.completed':
            session = webhook_event['data']['object']
            user_id = session['client_reference_id']
            
            # Update user subscription in DynamoDB
            users_table.update_item(
                Key={'user_id': user_id},
                UpdateExpression="SET subscription_status = :status, subscription_end_date = :end",
                ExpressionAttributeValues={
                    ':status': 'active',
                    ':end': int(time.time()) + 30*24*3600  # 30 days
                }
            )
        
        return {'statusCode': 200}
    except Exception as e:
        return {'statusCode': 400}