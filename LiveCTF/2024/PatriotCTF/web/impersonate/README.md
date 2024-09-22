# Write-up for CTF: Exploiting a Flask Application to Retrieve the Flag

## Challenge Description

The challenge involves a Flask application that manages authentication through session cookies to access the `/admin` endpoint. The goal is to retrieve the flag present on this page, which is accessible only to the "administrator" user with the correct session cookie. The session cookie is signed using a secret key (`secure_key`) derived from the server's start time (`server_start_time`).

## Secure Key Generation

From the provided source code of the challenge, we know how the Flask application generates the secret key. It is based on the server's startup time:

```python
app = Flask(__name__)
server_start_time = datetime.now()
server_start_str = server_start_time.strftime('%Y%m%d%H%M%S')
secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
app.secret_key = secure_key
```

The `secure_key` is calculated using the server's startup time, formatted as a string. This key is then used to sign session cookies.

## Application Code Overview

1. **`secure_key` Generation**: The secret key is calculated by taking a timestamp (`server_start_time`), formatting it as a string, and passing this string through the `sha256` algorithm.

   ```python
   secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
   ```

2. **Flask Session Management**: Flask uses signed session cookies to authenticate users. The session cookie contains information like `username` and `is_admin`, and is signed using the `secure_key`.

3. **`/admin` Endpoint**: Only users with `username = "administrator"` and `is_admin = True` can access the `/admin` page and see the flag.

4. **`/status` Endpoint**: This exposes useful information, including the server's `uptime` and the current server time (`server_time`), which we can use to derive the server's start time (`server_start_time`).

## Exploitation Steps

### 1. **Retrieve Uptime and Server Time**

Using the `/status` route, we retrieve two critical pieces of information:

- **Uptime**: How long the server has been running.
- **Server time**: The current time on the server.

These allow us to calculate the exact server start time, which is the basis for generating the `secure_key`.

### 2. **Calculate `server_start_str`**

We use the `uptime` and `server_time` to calculate the server's start time by subtracting the `uptime` from the `server_time`. Once obtained, we format the result as a string (`%Y%m%d%H%M%S`) to get the `server_start_str`.

### 3. **Generate `secure_key`**

With `server_start_str`, we can recreate the secret key Flask uses to sign session cookies. This secret key is calculated as follows:

```python
secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
```

### 4. **Forge a Valid Session Cookie**

Using the secret key, we can sign a session cookie that impersonates a user with `username="administrator"` and `is_admin=True`. We use `flask-unsign` to sign the cookie and make it valid:

```python
cookie = {'username': 'administrator', 'is_admin': True}
signed_cookie = sign(cookie, secret=secure_key)
```

### 5. **Send the GET Request to `/admin`**

Once the cookie is signed, we include it in a GET request to the `/admin` endpoint. If the signature is valid, we will receive the flag in response.

## Summary

By leveraging the `/status` endpoint to determine the server's start time, we can derive the secret key used to sign session cookies. Using this, we forge a valid session cookie with administrative privileges and gain access to the `/admin` page, where the flag is displayed.

### Flag

Once the correctly signed session cookie is sent, the flag is returned in the response from the `/admin` page.
