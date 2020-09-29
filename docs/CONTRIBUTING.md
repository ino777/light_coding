# Contributing


## How to add a content

1. Make a directory `/{language}/{section}/` in `app/contents/`.

2. Add template and code.  
<pre>
e.g.)
If you want to add a content about 'variable' in Python basics section, put it in a directory hierarchy like this.
.
├─ app
    ├─ contents
        ├─ python
            ├─ basics
                ├─ variable.html
                ├─ variable.py
</pre>

3. Register relative path and template file name with app/config/routes.py.  
```
router.register(relative path, template file name)
```