from ibm_cloud_security_advisor import NotificationsApiV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(
    apikey='abc')
notifications_service =NotificationsApiV1(authenticator=authenticator)
notifications_service.set_service_url("https://us-south.secadvisor.cloud.ibm.com/notifications")

data = {
    "name": "sdk_test_notification1",
    "description": "test1 description",
    "type": "Webhook",
    "endpoint": "http://test.com",
    "enabled": True,
    "severity": [
        "high",
        "medium",
        "low"
    ],
    "alert_source": [
        {
            "provider_name": "VA",
            "finding_types": [
                "ALL"
            ]
        },
        {
            "provider_name": "CERT",
            "finding_types": [
                "ALL"
            ]
        }
    ]
}
response = notifications_service.update_notification_channel(
    account_id="abc",
    channel_id="123"
    **data
)

print(response)
