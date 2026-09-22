import requests
import json


class PurchaseService:

    PURCHASE_URL = "https://adapayuat.bankfab.com/ADPAY/V1/purchaseRequest"

    def create_purchase(self, payload):

        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

        print("\n================ REQUEST BODY ================\n")
        print(json.dumps(payload, indent=4))
        print("\n==============================================\n")

        response = requests.post(
            self.PURCHASE_URL,
            json=payload,     # IMPORTANT
            headers=headers
        )

        print("REQUEST HEADERS:", response.request.headers)
        print("REQUEST BODY:", response.request.body)

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        return response.json()