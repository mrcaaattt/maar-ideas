import json

general_settings = json.dumps([
    {
        'type': 'title',
        'title': 'These settings are for you!'
    },
    {
        'type': 'bool',
        'title': 'Open Ideas on Startup',
        'desc': 'Open the program when you boot your computer',
        'section': 'General',
        'key': 'Open_On_Startup'
    }
])