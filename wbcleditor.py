import requests

requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': 'editwbcl', 'data': '''
print("Hello World")
'''})