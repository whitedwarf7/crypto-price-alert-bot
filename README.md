# Crypto Price Alert Bot 🤖💰

A serverless Telegram bot that monitors cryptocurrency prices and sends alerts when user-defined conditions are met. Built with AWS serverless technologies and integrated with Stripe for subscription management.

[![AWS Serverless](https://img.shields.io/badge/AWS-Serverless-orange?logo=amazon-aws)](https://aws.amazon.com)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://core.telegram.org/bots)
[![Stripe](https://img.shields.io/badge/Payment-Stripe-635bff?logo=stripe)](https://stripe.com)

## Architecture Overview 🏗️

### Core Components
- **AWS Lambda Functions**
  - `Telegram Webhook Handler`: Processes user commands (/setalert, /subscribe)
  - `Price Checker`: Scheduled job (5-min intervals) for price monitoring
  - `Stripe Webhook Handler`: Manages subscription payments

- **Data Storage**
  - **DynamoDB Tables**
    - `Users`: Stores user subscription data
    - `Alerts`: Manages price alert configurations

- **Integrations**
  - **Telegram API**: Bot communication
  - **Stripe API**: Payment processing
  - **CoinGecko API**: Real-time crypto prices
  - **API Gateway**: Lambda function routing

## Database Structure 🗃️

### Users Table
| Attribute              | Type    | Description                          |
|------------------------|---------|--------------------------------------|
| `user_id` (Primary Key)| String  | Unique Telegram user ID             |
| subscription_status    | String  | `active` or `inactive`              |
| subscription_end_date  | Number  | Unix timestamp of subscription end  |
| stripe_customer_id     | String  | Stripe customer reference           |

### Alerts Table
| Attribute              | Type    | Description                          |
|------------------------|---------|--------------------------------------|
| `alert_id` (Primary Key)| String  | UUID for alert identification       |
| `user_id` (Sort Key)   | String  | Associated user ID                  |
| cryptocurrency         | String  | Crypto symbol (e.g., BTC, ETH)      |
| target_price           | Number  | Price threshold for alert           |
| condition              | String  | `above` or `below` threshold        |
| active                 | Boolean | Alert activation status             |
| created_at             | Number  | Unix timestamp of alert creation    |

## Features ✨

- Real-time cryptocurrency price monitoring
- Custom price alerts with conditions
- Subscription management ($5/month)
- Serverless architecture (AWS Lambda + DynamoDB)
- Automated payment processing (Stripe)
- RESTful API endpoints via API Gateway

## Getting Started 🚀

### Prerequisites
- AWS account with necessary permissions
- Telegram Bot Token ([@BotFather](https://t.me/BotFather))
- Stripe API keys
- Python 3.9+

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/crypto-price-alert-bot.git
cd crypto-price-alert-bot

# Install dependencies
pip install -r requirements.txt

# Deploy with AWS SAM
sam build
sam deploy --guided