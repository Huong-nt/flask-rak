
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
		"dialog": {
			"type": "dialog",
			"context": {
				"intent": {
					"label": "set_alarm"
				},
				"entities": [
					{
						"start":10,
						"end":17,
						"value":"hôm nay",
						"real_value":{"day":"hôm nay","result":"2019-04-03T12:00:00.000+07:00"},
						"entity":"$datetime"
					}
				]
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