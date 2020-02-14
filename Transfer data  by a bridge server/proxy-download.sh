#!/bin/bash
scp -o proxycommand="ssh -q web@202.114.78.136 nc %h %p" yuanru@cartesius.surfsara.nl:/home/yuanru/zwwu/filename .
