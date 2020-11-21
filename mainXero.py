import base64
import oauthXero as oauthx
import time

initial_setup = 0

# Initial setup is only run if there is no refresh_token in the refresh_token.txt (one time)
if initial_setup:
    creds = oauthx.loadCredentials()

    client_id = creds[0]
    client_secret = creds[1]
    redirect_url = 'https://xero.com/au'
    scope = 'offline_access accounting.reports.read'
    b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')

    # 1. Send a user to authorize your app
    oauthx.step1(client_id, redirect_url, scope)

    # 2. Users are redirected back to you with a code
    # 3. Exchange the code for a token
    # 4. Receive your tokens
    access_token = oauthx.step2(b64_id_secret, redirect_url)

    # get tenants you are authorized for
    oauthx.XeroTenants(access_token[0])

    # refresh token
    new_access_token = oauthx.XeroRefreshToken(access_token[1], b64_id_secret)


# request profit & loss report from Xero API, store in file
oauthx.XeroRequestReport_ProfitLoss(b64_id_secret)

# wait 15 minutes, let the token expire and see if refresh token works for the executive summary
localtime = time.localtime()
print('before pause: ', time.strftime("%I:%M:%S %p", localtime))
# time.sleep(900)
print('after pause: ', time.strftime("%I:%M:%S %p", localtime))

# request executive summary report from Xero API, print only
oauthx.XeroRequestReport_ExecutiveSummary(b64_id_secret)