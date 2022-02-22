# shopping-cart

## Prerequisites

### Install dotenv package
```sh
pip install python-dotenv
```

### Install sengrid package
```sh
pip install sendgrid==6.6.0
```

### Set up environment variables
Create a file called `.env` under the same directory.

Edit the file by replacing the following information with yours.
```
TAX_RATE=0.0875
SENDGRID_API_KEY=YOUR_API_KEY
SENDER_ADDRESS=YOUR_EMAIL_ADDRESS
```

## Usage

```sh
python shopping_cart.py
```