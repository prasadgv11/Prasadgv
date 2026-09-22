# Currency module

## Add
Adds a new currency record for the **wio** bank.

- **Positive test:** Enter valid values (Currency Code = "999", Description = "Test Currency", Minor Digits = "2", Symbol = "$"), click **Save**, verify success message and the new row appears in the Currency list.  
- **Negative tests:**  
  - Leaving any required field blank triggers a mandatory‑field error.  
  - Submitting a duplicate Currency Code, invalid Minor Digits (negative, non‑numeric), or invalid Currency Symbol (blank, special chars, exceeding max length) yields validation errors.  
- **Cancel behavior:** Clicking **Cancel** after entering data discards the entry and no currency is added.
