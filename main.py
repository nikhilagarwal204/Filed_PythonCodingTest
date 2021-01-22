# import the necessary packages
from flask import Flask, request, render_template
from flask_api import status
import datetime
from PayGatewaysSimulation import PayGatewaysSimulation


app = Flask(__name__)
@app.route("/", methods=['GET','POST'])
def upload_details():
    # CreditCardNumber (mandatory, string, it should be a valid credit card number)
    # CardHolder: (mandatory, string)
    # ExpirationDate (mandatory, DateTime, it cannot be in the past)
    # SecurityCode (optional, string, 3 digits)
    # Amount (mandatoy decimal, positive amount)
    return """
        <!doctype html>
        <title>Enter details</title>
        <h1>Enter Payment Details:</h1>
        <form action="/result" method="post" enctype="multipart/form-data">
            <h2>Enter CreditCardNumber</h2>
                <input type="text" name="ccnum" required/>
            <h2>Enter CardHolder</h2>
                <input type="text" name="holder" pattern="[A-Za-z]+" title="Enter Name" required/>
            <h2>Enter ExpirationDate</h2>
                <input type="date" name="expdate" required/>
            <h2>Enter SecurityCode</h2>
                <input type="number" min="000" value="000" maxlength="3" name="sec_code"/>
            <h2>Enter Amount</h2>
                <input type="number" min="0" value="0.00" step=".01" name="amount" required/>
          <input type="submit" value="Upload">        
        </form>
        """
    # All Payment details are entered via HTML Form above


@app.route('/result', methods = ['POST'])
def payment_result():
    # Details are fetched and stored in the variables to be processed further
    ccnum = request.form.get("ccnum")
    holder = request.form.get("holder")
    expdate = datetime.datetime.strptime(request.form.get("expdate"), "%Y-%m-%d")
    sec_code = request.form.get("sec_code")
    amount = float(request.form.get("amount"))

    # Deatils are stored in the form of Dictionary and passed to the Simulated Payment Gateway
    details = {
        'CreditCardNumber':ccnum,
        'CardHolder':holder,
        'ExpirationDate':expdate,
        'SecurityCode':sec_code,
        'Amount':amount,
    }
    print(details)

    # CreditCardNumber (mandatory, string, it should be a valid credit card number)
    # ExpirationDate (mandatory, DateTime, it cannot be in the past)
    # Checking the above Criteria otherwise Request Invalid
    if (len(ccnum)!=1) or (expdate < datetime.datetime.today()):
        payment_mode = 'Payment Not Processed'
        return "The request is invalid: 400 bad request", status.HTTP_400_BAD_REQUEST

    # The payment gateway that should be used to process each payment follows the next set of business rules
    # If the success_status is 1 then payment is successful for that gateway
    # Else it will show Internal server error with 500 status code
    if (amount>=0 and amount<=20):
        success_status = PayGatewaysSimulation.CheapPaymentGateway(details)
        print(success_status)
        if(success_status==1):
            payment_mode = 'CheapPaymentGateway'
        else:
            return "500 internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR

    elif (amount>=21 and amount<=500):
        success_status = PayGatewaysSimulation.ExpensivePaymentGateway(details)
        print(success_status)
        if(success_status==1):
            payment_mode = 'ExpensivePaymentGateway'
        else:
            success_status = PayGatewaysSimulation.CheapPaymentGateway(details)
            print(success_status)
            if(success_status==1):
                payment_mode = 'CheapPaymentGateway'
            else:
                return "500 internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR
            
    elif (amount>500):
        flag = False
        for count in range(1,4):
            success_status = PayGatewaysSimulation.PremiumPaymentGateway(details)
            print(success_status)
            if(success_status==1):
                payment_mode = 'PremiumPaymentGateway'
                flag = True
                break
        if(flag!=True):   
            return "500 internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        return "500 internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR

    # If Payment is Successful, payment gateway will be shown in new HTML page
    return render_template("result.html", payment_mode = payment_mode), status.HTTP_200_OK

# App Runs on http://localhost:8000/
if __name__ == "__main__":
    app.debug = False
    app.run(host="localhost", port=8000) 