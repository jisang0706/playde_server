from firebase_admin import messaging

def send_to_firebase_cloud_messaging(registration_tocken, title, body):

    message = messaging.Message(
        notification=messaging.Notification(
            title = title,
            body = body,
        ),
        token=registration_tocken,
    )

    response = messaging.send(message)
    return response