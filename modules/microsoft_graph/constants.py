IMPORTANCES = ["high", "normal", "low"]
BODY_TYPES = ["Text", "html"]
ENDPOINTS = {
    "create_message": {
        "url": "users/{mailbox}/messages",
        "headers": {"Content-Type": "application/json"},
    },
    "create_attachment_session": {
        "url": "/users/{self.mailbox}/messages/{self.message_id}/attachments/createUploadSession",
        "headers": {"Content-Type": "application/json"},
    },
    "add_attachments": {
        "url": "{url}",
        "headers": {
            "Content-Type": "application/json",
            "Content-Length": "{attachment_len}",
            "Content-Range": "bytes 0-{attachment_len_max}/{attachment_len}",
        },
    },
    "add_img_attachments": {
        "url": "/users/{mailbox}/messages/{message_id}/attachments",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": "{attachment_name}",
            "contentBytes": "{attachment_content}",
            "isInline": "true",
        },
    },
    "send_message": {
        "url": "/users/{mailbox}/messages/{self.message_id}/send",
        "headers": {"Content-Type": "application/json"},
    },
}
