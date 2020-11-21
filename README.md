# Business_Dashboard
A python integration between Xero OAuth 2.0 API and the Gsheets API

## Required Files
- mainXero.py
- oauthxero.py
- credentials.csv
- xero_output.txt
- refresh_token.txt

## credentials.csv
Example format
```
Consumer Key,YOUR_CONSUMER_KEY,
Consumer Secret,YOUR_CONSUMER_SECRET,
```
Sample contents
```
Consumer Key,C63F3919BF81412AB744251306211D45,
Consumer Secret,0507eyQ22ZyhO0tuwrMtJS0lyA1tjOJKPv8zJWPCWNFSeO2sgv,
```

## refresh_token.txt 
Example format
```
YOUR_REFRESH_TOKEN
```
Sample contents
```
857cc0a5737faa032342ad0ffc59de4189jadef90c38f220393a80adf22804ac0fd7
```

## xero_output.txt

This has the output retrieved from the Xero API request

## Notes
You only need to run the initial setup once. The process and code does the following for us:
- Submit authorization request, retrieve authorization code
- Submit authorization code, retrieve access token and refresh token
- Submit Access token, retrieve tenant IDs
- Submit Access token & Tenant IDs, retrieve API data

Anytime you need to use the API
- Request new refresh token when requesting from Xero API

![The OAuth Flow](https://developer.xero.com/static/images/documentation/authflow.svg)

## Documentation
https://developer.xero.com/documentation/getting-started/getting-started-guide
https://developer.xero.com/documentation/oauth2/auth-flow
https://developer.xero.com/documentation/oauth2/troubleshooting

## Other helpful resources
https://www.youtube.com/watch?v=t0DgAMgN8VY
https://edgecate.com/articles/how-to-access-xero-apis/
