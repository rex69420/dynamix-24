import base64

import qrcode

username = "Dr. Whiter!"
password = "testaccount!"

credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(encoded_credentials)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="#fff2e7")
print(f"{credentials} -> {encoded_credentials}")
img.save(f"qr_code_{username}.png")
