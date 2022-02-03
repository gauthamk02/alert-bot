import discord
import asyncio
import os
import pandas as pd
import yaml
import datetime
from dateutil.relativedelta import relativedelta
import pytz
import re

config = None

with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

curr_datetime = datetime.datetime.now(pytz.timezone(config['timezone']))
tomorrow = curr_datetime + datetime.timedelta(days = 1)

channelID = int(os.getenv('channelID'))
client = discord.Client()

@client.event
async def on_ready():
    print('Succesfully logged in as {0.user}'.format(client))
    await main()

filelist = []

async def main():

    for fileconfig in config["Files"]:
        dict = {'config': config["Files"][fileconfig], 'df': pd.read_csv(config["Files"][fileconfig]["Filename"])}
        dict['df'].fillna('', inplace = True)
        filelist.append(dict)

    while True:

        curr_datetime = datetime.datetime.now(pytz.timezone(config['timezone']))
        
        for file in filelist:
            
            offset_datetime = curr_datetime
            offset_days, offset_months, offset_years = 0,0,0

            if "Offset" in file['config'].keys():
                if file['config']["Offset"] != None: 
                    if "Days" in file['config']["Offset"].keys():
                        offset_days = file['config']["Offset"]["Days"]
                    if "Months" in file['config']["Offset"].keys():
                        offset_months = file['config']["Offset"]["Months"]
                    if "Years" in file['config']["Offset"].keys():
                        offset_years = file['config']["Offset"]["Years"]

            offset_datetime += relativedelta(days = offset_days, months = offset_months, years = offset_years)#datetime.timedelta(days = offset_days, months = offset_months, years = offset_years)
            
            if "CompareDateFormat" in file['config'].keys():
                df2 = file['df'][file['df'][file['config']["CompareDate"]].str.contains(offset_datetime.strftime(file['config']["CompareDateFormat"]))]
            else:
                df2 = file['df'][file['df'][file['config']["CompareDate"]].str.contains(offset_datetime.strftime("%d-%m-%Y"))]
                            
            if not df2.empty:
                labelsregex = re.compile(r"\{(.*?)\}")
                labels = labelsregex.findall(file['config']["Message"])
                #print(labels)
                for index, row in df2.iterrows():
                    if row["Status"] != 'sent':
                        msg = file['config']["Message"]
                        for label in labels:
                            msg = msg.replace("{%s}"%(label), row[label])

                        print(msg)

                        channel = client.get_channel(channelID)
                        await channel.send(msg)

                        file['df'].at[index,"Status"] = 'sent'
                        file['df'].to_csv(file['config']["Filename"], index= False)


        await asyncio.sleep(5)
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        if message.content.startswith('$reload'):
            
            with open("config.yaml", 'r') as stream:
                config = yaml.safe_load(stream)
            
            filelist.clear()
            for fileconfig in config["Files"]:
                dict = {'config': config["Files"][fileconfig], 'df': pd.read_csv(config["Files"][fileconfig]["Filename"])}
                dict['df'].fillna('', inplace = True)
                filelist.append(dict)
            await message.channel.send('Reload Complete!')

        if message.content.startswith('$alerts today'):
            alerts = getAlerts(0)
            for alert in alerts:
                await message.channel.send(alert)

        if message.content.startswith('$alerts tomorrow'):
            await message.channel.send("Fetching Data")
            alerts = getAlerts(1)
            for alert in alerts:
                await message.channel.send(alert)

def getAlerts(DaysOffset):
    alerts = []
    curr_datetime = datetime.datetime.now(pytz.timezone(config['timezone']))
        
    for file in filelist:
        
        offset_datetime = curr_datetime
        offset_days, offset_months, offset_years = 0,0,0

        if "Offset" in file['config'].keys():
            if file['config']["Offset"] != None:
                if "Days" in file['config']["Offset"].keys():
                    offset_days = file['config']["Offset"]["Days"]
                if "Months" in file['config']["Offset"].keys():
                    offset_months = file['config']["Offset"]["Months"]
                if "Years" in file['config']["Offset"].keys():
                    offset_years = file['config']["Offset"]["Years"]

        offset_datetime += relativedelta(days = offset_days + DaysOffset, months = offset_months, years = offset_years)#datetime.timedelta(days = offset_days, months = offset_months, years = offset_years)

        if "CompareDateFormat" in file['config'].keys():
                df2 = file['df'][file['df'][file['config']["CompareDate"]].str.contains(offset_datetime.strftime(file['config']["CompareDateFormat"]))]
        else:
            df2 = file['df'][file['df'][file['config']["CompareDate"]].str.contains(offset_datetime.strftime("%d-%m-%Y"))]

        if not df2.empty:
            labelsregex = re.compile(r"\{(.*?)\}")
            labels = labelsregex.findall(file['config']["Message"])
            for index, row in df2.iterrows():
                msg = file['config']["Message"]
                for label in labels:
                    msg = msg.replace("{%s}"%(label), row[label])

                alerts.append(msg)
    return alerts

client.run(os.getenv('TOKEN'))
