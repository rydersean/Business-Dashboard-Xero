import requests
from werkzeug.urls import url_fix
import webbrowser
import csv

def loadCredentials():
    CONSUMER_KEY, CONSUMER_SECRET = 0, 0
    with open('credentials.csv') as csv_file:
        cred = csv.reader(csv_file, delimiter = ',')
        for row in cred:
            if row[0] == 'Consumer Key':
                CONSUMER_KEY = row[1]
            elif row[0] == 'Consumer Secret':
                CONSUMER_SECRET = row[1]

    return [CONSUMER_KEY, CONSUMER_SECRET]

def step1(client_id, redirect_url, scope):
    # 1. Send a user to authorize your app
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' +
                '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url +
                '''&scope=''' + scope +
                '''&state=123''')

    webbrowser.open_new(url_fix(auth_url))

def step2(b64_id_secret, redirect_url):
    # 2. Users are redirected back to you with a code
    auth_res_url = input('What is the response URL? ')
    start_number = auth_res_url.find('code=') + len('code=')
    end_number = auth_res_url.find('&scope')
    auth_code = auth_res_url[start_number:end_number]
    print(auth_code)
    print('\n')

    # 3. Exchange the code for a token
    exchange_code_url = 'https://identity.xero.com/connect/token'
    response = requests.post(exchange_code_url,
                            headers = {
                                'Authorization': 'Basic ' + b64_id_secret
                            },
                            data = {
                                'grant_type': 'authorization_code',
                                'code': auth_code,
                                'redirect_uri': redirect_url
                            })
    json_response = response.json()
    print(json_response)
    print('\n')

    # 4. Receive your tokens
    return [json_response['access_token'], json_response['refresh_token']]

# 5. Check the full set of tenants you've been authorized to access
def XeroTenants(access_token):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                            headers={
                                'Authorization': 'Bearer ' + access_token,
                                'Content-Type': 'application/json'
                            })
    json_response = response.json()
    print(json_response)

    for tenants in json_response:
        json_dict = tenants
    return json_dict['tenantId']

# 6.1 Refreshing access tokens
def XeroRefreshToken(refresh_token, b64_id_secret):
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                             headers={
                                 'Authorization': 'Basic ' + b64_id_secret,
                                 'Content-Type': 'application/x-www-form-urlencoded'
                             },
                             data={
                                 'grant_type': 'refresh_token',
                                 'refresh_token': refresh_token
                             })
    json_response = response.json()
    print('XeroRefreshToken json_response: ', json_response)

    new_refresh_token = json_response['refresh_token']
    rt_file = open('refresh_token.txt', 'w')
    rt_file.write(new_refresh_token)
    rt_file.close()

    return [json_response['access_token'], json_response['refresh_token']]

# 6.2 Call the API for Profit & Loss report
def XeroRequestReport_ProfitLoss(b64_id_secret):
    # refresh your token (only 12 mins and expires)
    old_refresh_token = open('refresh_token.txt', 'r').read()
    new_tokens = XeroRefreshToken(old_refresh_token, b64_id_secret)
    xero_tenant_id = XeroTenants(new_tokens[0])

    get_url = 'https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss?fromDate=2019-02-01&toDate=2019-05-28'
    response = requests.get(get_url,
                            headers={
                                # 'Authorization': 'Bearer ' + tokens[0],
                                'Authorization': 'Bearer ' + new_tokens[0],
                                'Xero-tenant-id': xero_tenant_id,
                                'Accept': 'application/json'
                            })
    json_response = response.json()
    print(json_response)

    xero_output = open('xero_output.txt', 'w')
    xero_output.write(response.text)
    xero_output.close()

# 6.2 Call the API for Profit & Loss report
def XeroRequestReport_ExecutiveSummary(b64_id_secret):
    # refresh your token (only 12 mins and expires)
    old_refresh_token = open('refresh_token.txt', 'r').read()
    new_tokens = XeroRefreshToken(old_refresh_token, b64_id_secret)
    xero_tenant_id = XeroTenants(new_tokens[0])

    get_url = 'https://api.xero.com/api.xro/2.0/Reports/ExecutiveSummary'
    response = requests.get(get_url,
                            headers={
                                # 'Authorization': 'Bearer ' + tokens[0],
                                'Authorization': 'Bearer ' + new_tokens[0],
                                'Xero-tenant-id': xero_tenant_id,
                                'Accept': 'application/json'
                            })
    json_response = response.json()
    print('Executive Summary: ', json_response)

