# Currecncy module

## add
Adds a new currency entry; verified for WIO bank.
- Positive: entering valid values saves and the new row appears in the list.
- Negative: leaving mandatory fields blank or providing invalid data (duplicate code, non‑numeric minor digits) yields appropriate validation errors.
- Negative: clicking Cancel after entering data discards the entry and no row is added.
