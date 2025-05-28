# Helpline Asterisk Dialplan Resources

To reference this dialplan directory, make sure to edit `/etc/asterisk/extensions.conf` and add the following at the very end of the file:

```sh
#include /home/helpline/asterisk/dialplan/*.conf
```

Make sure the default dialplan file `helpline.conf` is present, else Asterisk will throw `include file` errors

## Reload Dialplan
```sh
asterisk -rx "dialplan reload"
```

# Asterisk RUNTIME
The file module `runtime.py` encapsulates Asterisk REST API (ARI) and should be started at application runtime. The initialization is called using the function `indexinit`