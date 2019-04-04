
### Execute skill:
```
Request:
{
	"version": "1.0",
	"session": {
		"new": true|false,
		"sessionid": "string",
		"skillid": "string",
		"deviceid": "string",
		"user":{
			"userid": "string"
		},
		"attributes": {
			"state": "_COMMANDMODE"
		}
	},
	"context": {
		"type": "LaunchRequest|IntentRequest",
		"intent": {
			"label": "nhacthieunhi"
		},
		"entities": [
			{
				"entity": "action",
				"value": "bat"
			},
			{
				"entity": "file_name",
				"value": "co be lo lem"
			}
		]
	}
}
```
```
Response:
{
	"version": "1.0",
	"response" {
		"speech": {
			"type": "raw",
			"value": "string"
		},
		"reprompt": {
			"speech": {
				"type": "raw",
				"value": "string"
			}
		},
		"action": {
			"audio": {
				"interface": "new"
				"sources": []
			}
		},
		"shouldEndSession": false
	},
	"attributes": {
		"state": "_COMMANDMODE"
		"some_store_variables": "values"
	}
}
```