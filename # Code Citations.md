# Code Citations

## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html
```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang
```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang="fr">

```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang="fr">
<head>
    
```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-
```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    
```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device
```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-
```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0
```


## License: unknown
https://github.com/NumericFactory/velibeo/blob/80c883e9226616b96991bee4dcb74d55fa41c4c4/index.html

```
-->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <
```

import qrcode
import shutil
import secrets
import json
import os

roi_code = secrets.token_urlsafe(16)

with open('roi_token.json', 'w') as f:
    json.dump({'roi_token': roi_code}, f)

# Version production Render
base_url = "https://the-only-key.onrender.com"

url = f"{base_url}/auto_login?token={roi_code}"
img = qrcode.make(url)
img.save("roi_qr_prod.png")

os.makedirs("static", exist_ok=True)
shutil.copy("roi_qr_prod.png", "static/roi_qr.png")

print("ROI code (PRODUCTION):", roi_code)
print("QR code saved for production")
print("URL:", url)

