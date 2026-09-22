class PaymentUtils:

    @staticmethod
    def extract_payment_details(tokenid):

        payment_id, payment_url = tokenid.split(":", 1)

        final_url = f"{payment_url}?PaymentID={payment_id}"

        return {
            "payment_id": payment_id,
            "payment_url": payment_url,
            "final_url": final_url
        }