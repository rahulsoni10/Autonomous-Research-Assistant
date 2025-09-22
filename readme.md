Create a set_proxy.py file and paste and fill the below code: 
 
"""
import os

os.environ['http_proxy']  = "http://CWID:PASSWORD@10.185.190.100:8080"
os.environ['https_proxy'] = "http://CWID:PASSWORD@10.185.190.100:8080"

"""