# Riskprofile module

## Add Risk Profile (ecentric)

Creates a new risk profile via the Administration → Risk setup → PG → Risk profile flow.

- **Positive:** All fields filled correctly → profile saved and “saved successfully” toast appears.  
- **Negative – missing name:** Leaving Risk profile name empty triggers a required‑field validation error.  
- **Negative – duplicate name:** Using an existing profile name results in a duplicate‑entry error.  
- **Negative – invalid currency:** Selecting a non‑existent currency code fails with an invalid‑selection message.
