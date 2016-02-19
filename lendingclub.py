__author__ = 'andresdelgado'
import requests
import pprint
import json
import machine_models
import datetime
import pickle
import os
import resources


account_resources = {
    'Summary': 'summary',
    'Available cash': 'availablecash',
    'Transfer Funds': 'funds/add',
    'Pending Transfers': 'funds/pending',
    'Cancel Transfers': 'funds/cancel',
    'Notes owned': 'notes',
    'Detailed notes owned': 'detailednotes',
    'Portfolio owned': 'portfolios',
    'Create portfolio': 'portfolios',  # needs to add payload with the info on new portfolio
    'Submit order': 'orders'  # needs to add payload

}


version = 'v1'
headers = {
    'content-type': 'application/json',
    'Accept': 'application/json',
    'Authorization': resources.Authorization
}
investor_id = resources.investor_id
portfolioId = resources.portfolioId
account_resources_url = 'https://api.lendingclub.com/api/investor/{version}/accounts/{investor_id}/{resource}'
base_directory = os.path.dirname(os.path.realpath(__file__))


def get_current_balance():

    url = account_resources_url.format(version=version, investor_id=investor_id, resource=account_resources['Available cash'])
    response = json.loads(requests.get(url, headers=headers).text)
    return response['availableCash']


def get_loans_listed():

    payload = {'showAll': 'true'}
    loans = requests.get('https://api.lendingclub.com/api/investor/v1/loans/listing', headers=headers, params=payload)
    loans = json.loads(loans.text)['loans']
    return loans

def get_loans_owned_by_cldt_class():
    pass

def get_cdt_age(str_date):

    #d = '2011-03-14T17:00:00.000-07:00'
    date_object = datetime.datetime.strptime(str_date[:-6].replace('T', ' '), '%Y-%m-%d %H:%M:%S.%f')
    today_date_object = datetime.datetime.now()
    diff = today_date_object - date_object
    return diff.days/365.0


def get_good_class_variables(loan):

    loan_id = loan['id']
    funded_amnt = loan['loanAmount']
    is_36_months = 1 if loan['term'] == 36 else 0
    int_rate = loan['intRate']
    installment = loan['installment']
    home_ownership_own = 1 if loan['homeOwnership'] == 'OWN' else 0
    home_ownership_rent = 1 if loan['homeOwnership'] == 'RENT' else 0
    annual_inc = loan['annualInc']
    home_improvement = 1 if loan['purpose'] == 'home_improvement' else 0
    medical = 1 if loan['purpose'] == 'medical' else 0
    other = 1 if loan['purpose'] == 'other' else 0
    small_buss = 1 if loan['purpose'] == 'small_business' else 0
    dti = loan['dti']
    crdt_age = get_cdt_age(loan['earliestCrLine']) # in years needs function to calculate
    fico = (loan['ficoRangeHigh'] + loan['ficoRangeLow']) / 2
    inq_last_6_months = loan['inqLast6Mths']
    open_acc = loan['openAcc']
    pub_recods = loan['pubRec']
    revol_util = loan['revolUtil']
    total_accts = loan['totalAcc']

    return [funded_amnt, is_36_months, int_rate, installment, home_ownership_own, home_ownership_rent,
    annual_inc, home_improvement, medical, other, small_buss, dti, crdt_age, fico, inq_last_6_months,
    open_acc, pub_recods, revol_util, total_accts], loan_id

def get_great_class_variables(loan):

    loan_id = loan['id']
    funded_amnt = loan['loanAmount']
    is_36_months = 1 if loan['term'] == 36 else 0
    int_rate = loan['intRate']
    installment = loan['installment']
    annual_inc = loan['annualInc']
    educational = 1 if loan['purpose'] == 'educational' else 0
    home_improvement = 1 if loan['purpose'] == 'home_improvement' else 0
    medical = 1 if loan['purpose'] == 'medical' else 0
    moving = 1 if loan['purpose'] == 'moving' else 0
    other = 1 if loan['purpose'] == 'other' else 0
    renewable_energy = 1 if loan['purpose'] == 'renewable_energy' else 0
    small_buss = 1 if loan['purpose'] == 'small_business' else 0
    vacations = 1 if loan['purpose'] == 'vacation' else 0
    dti = loan['dti']
    crdt_age = get_cdt_age(loan['earliestCrLine']) # in years needs function to calculate
    fico = (loan['ficoRangeHigh'] + loan['ficoRangeLow']) / 2
    inq_last_6_months = loan['inqLast6Mths']
    open_acc = loan['openAcc']
    pub_recods = loan['pubRec']
    revol_util = loan['revolUtil']
    total_accts = loan['totalAcc']

    return [funded_amnt, is_36_months, int_rate, installment, annual_inc,
            educational, home_improvement,medical, moving, other,
            renewable_energy,small_buss, vacations, dti, crdt_age, fico,
            inq_last_6_months, open_acc, pub_recods, revol_util, total_accts], loan_id

def get_ok_class_variables(loan):

    loan_id = loan['id']
    int_rate = loan['intRate']
    annual_inc = loan['annualInc']
    dti = loan['dti']
    crdt_age = get_cdt_age(loan['earliestCrLine'])
    fico = (loan['ficoRangeHigh'] + loan['ficoRangeLow']) / 2
    inq_last_6_months = loan['inqLast6Mths']
    open_acc = loan['openAcc']
    revol_util = loan['revolUtil']
    total_accts = loan['totalAcc']
    is_36_months = 1 if loan['term'] == 36 else 0
    is_renter = 1 if loan['homeOwnership'] == 'RENT' else 0
    is_buss = 1 if loan['purpose'] == 'small_business' else 0

    return [int_rate, annual_inc, dti, crdt_age, fico, inq_last_6_months, open_acc, revol_util,
            total_accts, is_36_months, is_renter, is_buss], loan_id




def get_loans_owned():

    url = account_resources_url.format(version=version, investor_id=investor_id, resource=account_resources['Notes owned'])
    response = json.loads(requests.get(url, headers=headers).text)
    mynotes = {loan['loanId'] for loan in response['myNotes']}
    return mynotes

def invest(loan_id):

    pl = {
            "aid": resources.investor_id,
            "orders":[
                {
                    "loanId": loan_id,
                    "requestedAmount": 25.0,
                    "portfolioId": resources.portfolioId
                }
             ]
        }
    pl = json.dumps(pl)
    url = account_resources_url.format(version=version, investor_id=investor_id, resource=account_resources['Submit order'])
    response = requests.post(url, headers=headers, data=pl)
    return response

def select_best_loans(list_of_loans, cdt_class, cash_available):


    current_models = {
    'AB' : pickle.load(open(os.path.join(base_directory, 'great_classes_model.p'), 'r')),
    'CD' : pickle.load(open(os.path.join(base_directory, 'good_classes_model.p'), 'r')),
    'EFG': pickle.load(open(os.path.join(base_directory, 'ok_classes_model.p'), 'r')),
    }

    selected_loans = []
    for loan in list_of_loans:
        loan_id  = loan[1]
        try:
            paid_proba = current_models[cdt_class].predict_proba(loan[0])[0][1]
            if paid_proba >= machine_models.model_params[cdt_class]:
                selected_loans.append((paid_proba, loan_id))

        except:
            continue
        #print(loan_id)
        #print(paid_proba)
    selected_loans.sort(reverse=True)
    #print(selected_loans)
    for prob, loan_id in selected_loans:
        if cash_available >= 25:
            invest(loan_id)
            cash_available = cash_available - 25

    return cash_available



def main():

    current_balance = get_current_balance()
    if current_balance >= 25 :
        loans_owned = get_loans_owned()
        good_credit_loans = []
        great_credit_loans = []
        ok_credit_loans = []
        for loan in get_loans_listed():
            if loan['grade'] in 'CD' and loan['reviewStatus'] != 'NOT_APPROVED' and loan['loanAmount'] - loan['fundedAmount'] > 0 and loan['id'] not in loans_owned:
                good_credit_loans.append(get_good_class_variables(loan))
            elif loan['grade'] in 'AB' and loan['reviewStatus'] != 'NOT_APPROVED' and loan['loanAmount'] - loan['fundedAmount'] > 0 and loan['id'] not in loans_owned:
                great_credit_loans.append(get_great_class_variables(loan))
            elif loan['grade'] in 'EFG'  and loan['reviewStatus'] != 'NOT_APPROVED' and loan['loanAmount'] - loan['fundedAmount'] > 0 and loan['id'] not in loans_owned:
                ok_credit_loans.append(get_ok_class_variables(loan))
        current_balance = select_best_loans(ok_credit_loans, 'EFG', current_balance)
        current_balance = select_best_loans(good_credit_loans, 'CD', current_balance)
        current_balance = select_best_loans(great_credit_loans, 'AB', current_balance)



main()







