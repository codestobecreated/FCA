Implementation Plan - Razorpay Integration
This plan outlines the steps to integrate the Razorpay payment gateway into the FCA shop website.

Proposed Changes
Shop App Configuration
[MODIFY] 
settings.py
Add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET settings.
[MODIFY] 
models.py
Create an Order model to store order details and payment status.
Fields: full_name, email, amount, order_id (Razorpay), payment_id, status (Paid/Unpaid), created_at.
[MODIFY] 
views.py
razorpay_checkout: View to create a Razorpay order and render the payment page.
payment_status: View to handle the callback from Razorpay and verify the signature.
[MODIFY] 
urls.py
Add paths for checkout and payment status.
Frontend Integration
[MODIFY] 
detail.html
Add Razorpay Checkout script.
Update the "INITIATE TRANSACTION" button to trigger the Razorpay flow.
Add extensive comments explaining each part of the integration.
Verification Plan
Automated Tests
I will write a simple test case to mock the Razorpay client and ensure the Order model is saved correctly.
Manual Verification
Verify that the "INITIATE TRANSACTION" button opens the Razorpay modal (using test keys).
Verify that the callback view renders a success or failure message.