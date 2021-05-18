# ssh-server-on-cloud-heroku
Running your own separate ssh server on heroku cloud hosting


# Personal SSH-server
## SSH-server-plugin

Click the button below to deploy to Heroku

[![Deploy this repository as App](https://www.herokucdn.com/deploy/button.png)]
(https://heroku.com/deploy?template=https://github.com/AssaToolex/ssh-server-on-cloud-heroku/tree/main)

## 0. Attention

Deployment requires registration of a heroku account, a email is required when registering a heroku account (otherwise the verification code cannot be brushed out). 

An email address that can receive verification codes normally (@qq.com, @163.com are not acceptable):
- gmail (Best) 
- Outlook <https://login.live.com/> here.

## 1. Verification

After the server is deployed, open app to display the webpage normally. After the address is filled with the path (for example: <https://test.herokuapp.com/static>), the 403 page is displayed, which means the deployment is successful.

## 2. Client Configuration

QR code address: https://test.herokuapp.com/qr/vpn.png

(Change test to your own app name. If you changed the QR\_Path (path to qr png, filled during deployment) variable, also change the corresponding qr\_img to the modified one)

Use the SSH-client to scan the QR code.

**or**

Use Configuration file -> Address: https://test.herokuapp.com/qr/

(Change test to your own app name)

Copy the details after opening and import it to the client.

**or**

Manual configuration:

```sh
ssh localhost
```

Those without a client can also download from here (Android):
windows:

# Reference

https://heroku.com/

https://login.live.com/
