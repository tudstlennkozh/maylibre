# Known errors

## exchangelib.errors.AutoDiscoverFailed

When you encounter this kind of error :

> exchangelib.errors.AutoDiscoverFailed: All steps in the autodiscover protocol failed for email 'xxxxxx'. If you think this is an error, consider doing an official test at https://testconnectivity.microsoft.com

try a complete exchangelib install :

```
pip install exchangelib[complete]
```

or check your network connectivity.