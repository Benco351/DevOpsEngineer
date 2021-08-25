import csv
from datetime import *
import logging
from twilio.rest import Client
import testere
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
account_sid = testere.ferent.decrypt(testere.encAccount_sid).decode()
auth_token = testere.ferent.decrypt(testere.encAuth_token).decode()
client = Client(account_sid, auth_token)
phonenumbernew = list()
TwentyEightPhoneLIST = []
csv_columns = ['Phonenumber', 'DateMessageSent']
with open("TwentyEightPhoneList.csv", "w") as randd:
    writer1 = csv.DictWriter(randd, fieldnames=csv_columns)
    writer1.writeheader()
randd.close()


def CleanLines(path):
    fh = open(path, "r")
    lines = fh.readlines()
    fh.close()

    keep = []
    for line in lines:
        if not line.isspace():
            keep.append(line)

    fh = open(path, "w")
    fh.write("".join(keep))
    # should also work instead of joining the list:
    # fh.writelines(keep)
    fh.close()


def AjustPhonenumberlist(Phonenumber):
    b = list()
    for i in range(len(Phonenumber)):
        s = Phonenumber[i]
        b.append(s.replace("0", "+972", 1))
    return b


def ContinueAppendingCsv(INFO):
    with open("TwentyEightPhoneList.csv", mode='a') as b_file:
        writer_object = csv.DictWriter(b_file, fieldnames=csv_columns)
        writer_object.writerow(INFO)
    b_file.close()
    CleanLines("TwentyEightPhoneList.csv")
    # ---- df = pd.read_csv("TwentyEightPhoneList.csv")
    # ---- print(df)
    # ---- print(df.empty)


def SendCompleteSMS(Phonenumber, ExactTime):
    Phonenumbernew = AjustPhonenumberlist(Phonenumber)
    for i in range(len(Phonenumbernew)):
        client.messages.create(
                   to=Phonenumbernew[i],
                   from_="+972526228764",
                   body=f""" לקוח יקר
         הטעינה למספר {Phonenumber[i]} הושלמה ותכנס לתוקף עד 10 דק
          בברכה
                    """
               )
        info = {
            'Phonenumber': Phonenumbernew[i],
            'DateMessageSent': ExactTime,
        }
        logging.warning('Message sent!')
        ContinueAppendingCsv(info)


def COPYBACKCSV():
    with open("TwentyEightPhoneList.csv", "w") as csv_file:
        csv_file.flush()
        filewriter = csv.DictWriter(csv_file, fieldnames=csv_columns)
        filewriter.writeheader()

        with open("CopyCSV.csv", "r") as Copy_file:
            csv_reader = csv.DictReader(Copy_file)
            for row in csv_reader:
                filewriter.writerow(row)
    CleanLines("TwentyEightPhoneList.csv")
    # ----df = pd.read_csv("TwentyEightPhoneList.csv")
    # ----print("><><><><><><><><><>")
    # ----print(df)
    # ----print("><><><><><><><><><>")
    csv_file.close()
    Copy_file.close()
    logging.warning('28 DAYS CSV updated :)')


def CHECKfor28DAYSSMS():
    logging.warning('Regular check for 28 days sms..')
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    curret_tuple = tuple([int(x) for x in current_date[:10].split('-')])
    dtcurrent_obj = datetime(*curret_tuple[0:3])
    with open("CopyCSV.csv", "w") as copy_file:
        filewriter = csv.DictWriter(copy_file, fieldnames=csv_columns)
        filewriter.writeheader()

        with open("TwentyEightPhoneList.csv", "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                print(row)
                # lines.update(row)
                dt_tuple = tuple([int(x) for x in row['DateMessageSent'][:10].split('-')])
                dt_obj = datetime(*dt_tuple[0:3])
                if (dtcurrent_obj - dt_obj).days == 28:

                    Nextdayschedule = dt_obj.today().replace(day=now.day, hour=0, minute=0, second=0,
                                                             microsecond=0) + timedelta(
                        days=2)
                    # logging.critical(Send28DaysSMS(row['Phonenumber'][:14], Nextdayschedule))
                    print("mispar telephone : " + row['Phonenumber'][:14] + " yom she nigmar : " + str(
                        Nextdayschedule.date()))

                else:
                    filewriter.writerow(row)
    CleanLines("CopyCSV.csv")
    # ---- df = pd.read_csv("CopyCSV.csv")
    # ---- print("----------------------")
    # ---- print(df)
    # ---- print("----------------------")
    copy_file.close()
    csv_file.close()
    COPYBACKCSV()
    # with open('TwentyEightPhoneList.csv', 'w') as writeFile:
    #    writer = csv.writer(writeFile)
    #    writer.writerows(lines)
    # writeFile.close()


def Send28DaysSMS(phonenumber, exactDate):
    client.messages.create(
        to=phonenumber,
        from_="+972526228764",
        body=f"""לקוח יקר
הטעינה שבוצעה מסתיימת {exactDate}ב
ניתן לחדש את הטעינה באתר
            """
    )
