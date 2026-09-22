from pages.payment.purchase_service import PurchaseService
from pages.payment.adpay_payment_page import PurchasePage
from utils.payment_utils import PaymentUtils


def test_purchase(page):

    payload = {
        "id": "PGFABICP1",
        "amt": "1900",
        "udf6": "905550",
        "udf10": "",
        "udf9": "soniya",

        "servicedata": [
            {
                "amount": "220",
                "adgeId": "FABICPVEN1",
                "serviceId": "PGICPSERV2",
                "isFeeExempted": "Yes",
                "dynamicFeeAmount": [
                    {
                        "ticket": "11",
                        "amount": "100.00"
                    },
                    {
                        "ticket": "12",
                        "amount": "120.00"
                    }
                ]
            },
            {
                "amount": "50.01",
                "noOfTransactions": "1",
                "adgeId": "FABICPVEN1",
                "serviceId": "PGICPSERV7",
                "isFeeExempted": "No",
                "dynamicFeeAmount": [
                    {
                        "ticket": "21",
                        "amount": "49.01"
                    },
                    {
                        "ticket": "22",
                        "amount": "1.00"
                    }
                ]
            },
            {
                "amount": "220",
                "noOfTransactions": "1",
                "adgeId": "FABICPVEN2",
                "serviceId": "PGICPSERV3",
                "isFeeExempted": "Yes",
                "dynamicFeeAmount": [
                    {
                        "ticket": "11211",
                        "amount": "100.00"
                    },
                    {
                        "ticket": "132",
                        "amount": "120.00"
                    }
                ]
            },
            {
                "amount": "1150",
                "noOfTransactions": "1",
                "adgeId": "FABICPVEN3",
                "serviceId": "PGICPSERV4",
                "isFeeExempted": "No",
                "dynamicFeeAmount": [
                    {
                        "ticket": "1131",
                        "amount": "1000.00"
                    },
                    {
                        "ticket": "123",
                        "amount": "150.00"
                    }
                ]
            }
        ],

        "udf3": "عربي",
        "udf4": "عربي",
        "udf1": "784210000000445",
        "udf2": "soniyas@fss.co.in",
        "password": "Fab@123",
        "udf7": "ADPay",
        "udf8": "",
        "action": "1",
        "correlationid": "12345666",
        "udf5": "03022020",
        "langid": "EN",
        "currencyCode": "784",
        "version": "1.0.7"
    }

    # Add URLs after payload creation
    payload["responseURL"] = "https://adapayuat.bankfab.com/PGRPTG/jsp/fss/HostedPaymentResultHTTP.jsp"
    payload["errorURL"] = "https://adapayuat.bankfab.com/PGRPTG/jsp/fss/HostedPaymentResultHTTP.jsp"

    print("responseURL =", payload["responseURL"])
    print("errorURL =", payload["errorURL"])

    purchase_service = PurchaseService()

    purchase_response = purchase_service.create_purchase(payload)

    print("\n================ PURCHASE RESPONSE ================\n")
    print(purchase_response)
    print("\n===================================================\n")

    assert purchase_response["status"] == "1", \
        f"Purchase Failed : {purchase_response}"

    tokenid = purchase_response["tokenid"]

    print(f"Token ID : {tokenid}")

    payment_details = PaymentUtils.extract_payment_details(tokenid)

    payment_id = payment_details["payment_id"]
    payment_url = payment_details["payment_url"]
    final_payment_url = payment_details["final_url"]

    print(f"Payment ID       : {payment_id}")
    print(f"Payment URL      : {payment_url}")
    print(f"Final Payment URL: {final_payment_url}")

    payment_page = PurchasePage(page)

    payment_page.open_payment_page(final_payment_url)

    current_url = payment_page.get_current_url()

    print(f"Opened URL : {current_url}")

    assert payment_id in current_url