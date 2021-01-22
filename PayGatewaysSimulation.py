import random

# Simulation of the Pyament Gateways is done by generating random number
# Where 0 indicates payment failed and 1 indicates payment successful
# Details of the Payemnt is paased as parameter to the payment gateway
# Status is again returned to the Flask API for further processing
class PayGatewaysSimulation():
    def CheapPaymentGateway(details):
        success_status = random.randint(0,1)
        return success_status

    def ExpensivePaymentGateway(details):
        success_status = random.randint(0,1)
        return success_status

    def PremiumPaymentGateway(details):
        success_status = random.randint(0,1)
        return success_status

    

    