# efb-wechat-docker

[![github docker status](https://img.shields.io/github/workflow/status/haukeng/efb-wechat-docker/Publish%20Docker%20Image?label=docker&logo=docker)](https://github.com/haukeng/efb-wechat-docker/actions/workflows/docker-image.yml)
[![docker: image size](https://img.shields.io/docker/image-size/thehaukeng/efb-wechat)](https://hub.docker.com/r/thehaukeng/efb-wechat)

EFB Docker image with efb-telegram-master and efb-wechat-slave

## Features

- Container run by non-root user.
- Support add environment variables `PROXY_URL`, `PROXY_USER`, and `PROXY_PASS` to use proxy for ETM.
- Integrate [efb-patch-middleware](https://github.com/ehForwarderBot/efb-patch-middleware) and [efb-search_msg-middleware](https://github.com/ehForwarderBot/efb-search_msg-middleware) by default.

## Build

### Use GitHub Action pre-build image

```shell
docker pull thehaukeng/efb-wechat

# You can use ghcr.io as well
# docker pull ghcr.io/haukeng/efb-wechat
```

### Build image manually

```shell
git clone https://github.com/haukeng/efb-wechat-docker.git
cd efb-wechat-docker && docker build -t thehaukeng/efb-wechat efb-wechat
```

## Usage

### Step 0

Create a Telegram Bot by talking to [@BotFather](https://t.me/botfather) and it will give you the Bot Token

Get your Telegram ID (**Not username**) from [@getidsbot](https://t.me/getidsbot)

### Step 1

**If you prefer to use docker.**

```shell
# Create volumes
docker volume create efb-wechat-data

# Run 
docker run -d -t \
--name "efb-wechat" \
-e BOT_TOKEN=xxxx \
-e BOT_ADMIN=xxxx \
-v efb-wechat-data:/home/efb/efb_config/profiles/default \
thehaukeng/efb-wechat
```

(**Required**) Use your Telegram Bot Token as `BOT_TOKEN` and your Telegram ID as `BOT_ADMIN`

**If you prefer to use docker-compose.**

```shell
mkdir efb-wechat && cd efb-wechat
wget https://git.io/JMR3i -O docker-compose.yml
```

(**Required**) Modify the environment variables by editing docker-compose.yml, and then:

```shell
docker-compose up -d
```

### Step 2

```shell
docker logs -f efb-wechat 
# Ctrl + C to quit after your log in
```

Scan the QR code to log in

## Configuration Options

`BOT_TOKEN`

> (**Required**) Your Telegram bot token.

`BOT_ADMIN`

> (**Required**) Your Telegram account id.

`PROXY_URL`

> (Optional) Proxy url use to connect Telegram by network proxy.
>
> Supported both `http` and `socks5` proxy.
>
> For example: `http://172.17.0.1:1080`

`PROXY_USER`

> (Optional) Use for proxy authentication

`PROXY_PASS`

> (Optional) Use for roxy authentication

`SEND_IMAGE_AS_FILE`

> (Optional) Set the value to `0` to **disable** send all image messages as files (preventing Telegram’s image compression).
>
> _Enabled by default._

`ANIMATED_STICKERS`

> (Optional) Set the value to `0` to **disable** support to animated stickers.
>
> _Enabled by default._

`MESSAGE_MUTED_ON_SLAVE`

> (Optional) Behavior when a message received is muted on slave channel platform. Availiable value: `normal`, `silent` and `mute`. Go to [ehForwarderBot/efb-telegram-master](https://github.com/ehForwarderBot/efb-telegram-master#experimental-flags) to get more information.
>
> _`normal` is the default value_

`YOUR_MESSAGE_ON_SLAVE`

> (Optional) Behavior when a message received is from you on slave channel platform. Availiable value: `normal`, `silent` and `mute`. Go to [ehForwarderBot/efb-telegram-master](https://github.com/ehForwarderBot/efb-telegram-master#experimental-flags) to get more information.
>
> _`silent` is the default value_

`MP_GROUP_ID`

> (Optional) Telegram group id for forwarding every public account message to it. Go to [efb-patch-middleware](https://github.com/ehForwarderBot/efb-patch-middleware#usage) to get more information.

`AUTO_MARK_AS_READ`

> (Optional) Set the value to `0` to **disable** auto mark as read in wechat phone client. Go to [efb-patch-middleware](https://github.com/ehForwarderBot/efb-patch-middleware#usage) to get more information.
>
> _Enabled by default._

`REMOVE_EMOJI_IN_TITLE`

> (Optional) Set the value to `0` to **disable**  remove emoji in telegram group title. Go to [efb-patch-middleware](https://github.com/ehForwarderBot/efb-patch-middleware#usage) to get more information.
>
> _Enabled by default._

`STRIKETHROUGH_RECALL_MSG`

> (Optional) Set the value to `0` to **disable** strikethrough instead of replying to a recall message. Go to [efb-patch-middleware](https://github.com/ehForwarderBot/efb-patch-middleware#usage) to get more information.
>
> _Enabled by default._

## FQA

### How to use host machine proxy?

Try to set `PROXY_URL` as `http://172.17.0.1:YOUR_PORT` (Socks5 works as well)
