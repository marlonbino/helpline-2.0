# Helpline 2.0: Endpoints Asterisk Resources

To reference this `endpoints` directory, make sure to edit `/etc/asterisk/pjsip.conf` and add the following at the very end of the file:

```sh
#include /home/helpline/asterisk/phones/*.conf
```

Make sure the default PJSIP file `helpline.conf` is present, else Asterisk will throw `include file` errors

## Reload Asterisk
```sh
asterisk -rx "core reload"
```