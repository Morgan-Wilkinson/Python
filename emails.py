#!/usr/bin/env python3

# Morgan Wilkinson
# 07/27/2019

import smtplib

smtpObj = smtplib.SMTP("smtp-mail.outlook.com", 587)
smtpObj = smtplib.SMTP_SSL("smtp-mail.outlook.com", 465)
smtpObj.ehlo()