# Discord Alert-bot
Alert-bot is a simple and easy to setup Discord bot used to automate sending custom alerts.
There is an example config file and corresponding CSV files provided to show the basic working of the bot.
### Setting Up
1. Download the repository into your system which will host the bot.
2. Update the environment variables Bot token in `TOKEN=YOUR-BOT-TOKEN` and the ChannelID of the default channel to which the alerts should be sent to in `channelID=CHANNELID-TO-SEND-ALERTS` in the `.env` file.
3. Copy all the CSV files with the alert data into the same directory.
4. Update the `config.yaml` file to format the alert messages and to set the features of the bot. Feaures of config file is explained in detail [here](#config-file).

### Config File
Config file is used to configure all the workings of the bot and to format the alert messages. In this section all the available options in the config file will be explained.

The options in the config file exists in the `key: value` form and make the neccessary modifications as per your need.
1.  `version: 1.0.0` shows the version of the bot.
2.  `timezone: Asia/Kolkata` represents the target timezone of the bot.
3.  `Files: ` contain all the alert objects and their properties. Each object's properties should be come under the object name as shown below.

```
Files:
  Assignment:
    Filename: assignments.csv
    Offset:
      Days: 1
      Months: 0
      Years: 0
    CompareDate: DueDate
    Message: Assignment due tomorrow - {Assignment} at {DueTime}

  Birthday:
    Filename: birthdays.csv
    Offset:
      Days: 0
    CompareDate: DOB
    CompareDateFormat: "%d-%m"
    Message: Happy Birthday {Name}!

```  
4. Functions and Usage of different properties and mentioned below. The properties marked * is necessary for the functioning of the object.
    1. `Filename: `* contains the name of the CSV file that contains the data for the alerts.
    2. `Message: `* should contain the alert message that should be sent to the discord server. Message can contain column names in the CSV file enclosed by `{}` in it which will be replaced by the corresponding column value of the selected row in the alert message being sent.
    3. `CompareDate: `*  should have the column name in the CSV file that holds the dates based on which the alerts should be sent. The values in this column should be in the `DD-MM-YYYY` format as default. If the values are in any other format then the comparison format should be entered in `CompareDateFormat: `.  
    4. `CompareDateFormat: ` contains the format in which the Offset date should be compared to the value in `ComapareDate: ` column. The format code list is given below:


        | Directive | Meaning                                                   | Example                  |
        |-----------|-----------------------------------------------------------|--------------------------|
        | %a        | Abbreviated weekday name.                                 | Sun, Mon, ...            |
        | %A        | Full weekday name.                                        | Sunday, Monday, ...      |
        | %w        | Weekday as a decimal number.                              | 0, 1, ..., 6             |
        | %d        | Day of the month as a zero-padded decimal.                | 01, 02, ..., 31          |
        | %-d       | Day of the month as a decimal number.                     | 1, 2, ..., 30            |
        | %b        | Abbreviated month name.                                   | Jan, Feb, ..., Dec       |
        | %B        | Full month name.                                          | January, February, ...   |
        | %m        | Month as a zero-padded decimal number.                    | 01, 02, ..., 12          |
        | %-m       | Month as a decimal number.                                | 1, 2, ..., 12            |
        | %y        | Year without century as a zero-padded decimal number.     | 00, 01, ..., 99          |
        | %-y       | Year without century as a decimal number.                 | 0, 1, ..., 99            |
        | %Y        | Year with century as a decimal number.                    | 2013, 2019 etc.          |
        | %H        | Hour (24-hour clock) as a zero-padded decimal number.     | 00, 01, ..., 23          |
        | %-H       | Hour (24-hour clock) as a decimal number.                 | 0, 1, ..., 23            |
        | %I        | Hour (12-hour clock) as a zero-padded decimal number.     | 01, 02, ..., 12          |
        | %-I       | Hour (12-hour clock) as a decimal number.                 | 1, 2, ... 12             |
        | %p        | Locale’s AM or PM.                                        | AM, PM                   |
        | %M        | Minute as a zero-padded decimal number.                   | 00, 01, ..., 59          |
        | %-M       | Minute as a decimal number.                               | 0, 1, ..., 59            |
        | %S        | Second as a zero-padded decimal number.                   | 00, 01, ..., 59          |
        | %-S       | Second as a decimal number.                               | 0, 1, ..., 59            |
        | %Z        | Time zone name.                                           |                          |
        | %j        | Day of the year as a zero-padded decimal number.          | 001, 002, ..., 366       |
        | %-j       | Day of the year as a decimal number.                      | 1, 2, ..., 366           |

        For example, to send alerts for birthdays, the date of birth in the CSV could be of the format `DD-MM-YYYY` but we only need to compare the Day and months to send the alerts. So we can set the property as `CompareDateFormat: "%d-%m"`
    5. `Offset: ` this property is useful is we want to send the alert on a day other than the comparison date. `Offset: ` has three sub properties `Days: ` `Months: ` and `Years: ` whose values can be set as per the need. In the given assignment example there is an offset of 1 day (`Days: 1`) which will result in the alert being send 1 day before the comparison date.

    ### Bot Commands
    The bot also has a few commands that can be used as per the need:
    1. `$alerts today` shows all the alerts that was/will be send today.
    2. `$alerts tomorrow` shows all the alerts that will be send tomorrow.
    3. `$reload` reloads all the CSV files. This command must be used if any changes were made to the CSV files while the bot was running.
    4. `$hello` returns a hello message. This alert can be used to check if the bot is online.


