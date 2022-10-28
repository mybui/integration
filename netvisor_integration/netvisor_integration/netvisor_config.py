import hashlib
import random
import time
from typing import Tuple

from netvisor_integration import settings

get_customer_list_url = "https://isvapi.netvisor.fi/customerlist.nv"
update_customer_url = "https://isvapi.netvisor.fi/customer.nv?method=edit&id={}"
create_customer_url = "https://isvapi.netvisor.fi/customer.nv?method=add"


def h_mac(
        url: str
) -> Tuple[str, str, str]:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    transaction_id = "TRANSID" + "%0.12d" % random.randint(0, 99999999)
    string = url + \
             "&" + settings.settings.CLIENT + \
             "&" + settings.settings.CUSTOMER_ID + \
             "&" + timestamp + \
             "&" + settings.settings.LANGCODE + \
             "&" + settings.settings.CID + \
             "&" + transaction_id + \
             "&" + settings.settings.PRIVATE_KEY.get_secret_value() + \
             "&" + settings.settings.PARNER_PRIVATE_KEY.get_secret_value()
    return (
        timestamp,
        transaction_id,
        hashlib.sha256(string.encode('utf-8')).hexdigest()
    )
