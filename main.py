from flask import Flask, render_template, redirect
from hashlib import sha256
import requests
import logging
from forms import TestForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ssnawn&DFS0892'



logger = logging.getLogger('my_loger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('test.log')
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s %(levelname)s] requested:%(module)s: %(message)s'))
logger.addHandler(handler)



def sha(params):
    secret_key = 'SecretKey01'
    params_sort_str = {i: str(k) for i, k in sorted(params.items())}
    str_to_sha = ':'.join(params_sort_str.values()) + secret_key
    return sha256(str_to_sha.encode('utf-8'))


def eur_payment(form):
    params = {
        "currency": "643",
        "shop_id": "5",
        "shop_order_id": 101,
        form.amount.name: form.amount.data,
    }
    sing = sha(params).hexdigest()
    params.update({'sign': sing, form.description.name: form.description.data})
    redir_url = requests.get('https://pay.piastrix.com/en/pay', params=params).url
    return redir_url


def usd_payment(form):
    headers = {'content-type': 'application/json'}
    params = {
        "payer_currency": 643,
        "shop_amount": float(form.amount.data),
        "shop_currency": 643,
        "shop_id": "5",
        "shop_order_id": 4239,
    }
    sing = sha(params).hexdigest()
    params.update({'sign': sing, form.description.name: form.description.data})
    resp_json = requests.post(url='https://core.piastrix.com/bill/create', headers=headers, json=params).json()
    return resp_json.get('data').get('url')

def rub_payment(form):
    headers = {'content-type': 'application/json'}
    params = {
        "currency" : "643",
        "payway" : "advcash_rub",
        "amount" : float(form.amount.data),
        "shop_id" : "5",
        "shop_order_id" : 4126,
    }
    sing = sha(params).hexdigest()
    params.update({'sign': sing, form.description.name: form.description.data})
    resp_json = requests.post(url='https://core.piastrix.com/invoice/create', headers=headers, json=params).json()
    return resp_json.get('data').get('url'), resp_json.get('data').get('data'), resp_json.get('data').get('method')


@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = TestForm()

    if form.validate_on_submit():
        logger.info(f"Amount = {form.amount.data}, Payway = {form.payway.data}, Description = {form.description.data}")
        if form.payway.data == 'EUR':
            return redirect(location=eur_payment(form), code=301)
        elif form.payway.data == 'USD':

            url = usd_payment(form)
            return redirect(location=url, code=301)
        elif form.payway.data == 'RUB':
            url, data, method = rub_payment(form)
            return render_template('invoice.html', url=url, data=data, method=method)

    return render_template('main_form.html', form=form)


