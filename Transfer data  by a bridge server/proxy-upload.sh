#!/bin/bash
scp -o proxycommand="ssh -q web@202.114.78.136 nc %h %p" "proxy-upload.sh" yuanru@cartesius.surfsara.nl:/home/yuanru/zwwu/
