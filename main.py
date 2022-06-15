# different languages to use powershell, and python. Couldve used typescript but found pyhton is better and easiert to get started
import csv
import datetime
import pytz
import rfc3339
import sys


def timestamp_transform (timestamp):
    old_timezone = pytz.timezone("US/Pacific")
    new_timezone = pytz.timezone("US/Eastern")
    raw_time = datetime.datetime.strptime(timestamp, '%m/%d/%y %H:%M:%S %p')
    new_timezone_timestamp = old_timezone.localize(raw_time).astimezone(new_timezone) # convert pacific time to eastern

    return rfc3339.rfc3339(new_timezone_timestamp, False, False)


def address_transform (address):
    return address


def zip_transform (zip):
    return zip.zfill(5)


def name_transform (name):
    return name.upper()


def foo_transform (foo):
    h,m,s,ms = foo.replace('.',':').split(':') #what to do with milli seconds?

    return int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())


def bar_transform (bar):
    h,m,s,ms = bar.replace('.',':').split(':') #what to do with milli seconds?
    
    return int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())


def totalDuration_transform (foo, bar):
    return foo + bar


def notes_transform (notes):
    return notes


def get_input():
    if len(sys.argv) > 2:
        normalize_csv(sys.argv[1], sys.argv[2])
    else:
        print('Both CSV file names are needed!')


def normalize_csv(input_csv, output_csv):
    with open(input_csv, 'r', encoding='utf8', errors='ignore') as inputFile:
        reader = csv.reader(inputFile)

        with open(output_csv, 'w', newline='', encoding='utf8') as outputFile:
            writer = csv.writer(outputFile)

            writer.writerow(next(reader))  # headers
            for row in reader:
                # Timestamp=0,Address=1,ZIP=2,FullName=3,FooDuration=4,BarDuration=5,TotalDuration=6,Notes=7
                foo_in_seconds = foo_transform(row[4])
                bar_in_seconds = bar_transform(row[5])
                writer.writerow((
                    timestamp_transform(row[0]),
                    address_transform(row[1]),
                    zip_transform(row[2]),
                    name_transform(row[3]),
                    foo_in_seconds,
                    bar_in_seconds,
                    totalDuration_transform(foo_in_seconds, bar_in_seconds),
                    notes_transform(row[7])))


def main():
    get_input()


if __name__ == '__main__':
    main()
