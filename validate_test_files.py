
import os
import re

try:
    import lxml.etree as etree
except ImportError as e:
    print("Can't import lxml")
    raise e

file11 = './xsd/gpx1_1.xsd'
file10 = './xsd/gpx1_0.xsd'

validator11 = etree.XMLSchema(etree.parse(file11))
validator10 = etree.XMLSchema(etree.parse(file10))


width = 7
print('1.0'.ljust(width) + '1.1'.ljust(width) + 'claim'.ljust(width) + 'filename')
errorlog = []
for filename in os.listdir('./test_files'):
    with open('./test_files/' + filename) as file:
        try:
            utext = file.read()
            text = utext.encode('utf-8')
            xml = etree.XML(text)
            print(str(validator10.validate(xml)).ljust(width), end='')
            print(str(validator11.validate(xml)).ljust(width), end='')
            ver = ''
            if '<gpx' in utext:
                gpxnode = utext.partition('<gpx')[2]
                gpxnode = gpxnode.partition('>')[0]
                if ' version=' in gpxnode:
                    ver = gpxnode.partition(' version=')[2][1:4]
            print(ver.ljust(width), end='')
            print(filename)
            if ver == '1.0':
                if validator10.error_log.last_error is not None:
                    errorlog.append(filename + ': ' + str(validator10.error_log.last_error))
            elif ver == '1.1':
                if validator11.error_log.last_error is not None:
                    errorlog.append(filename + ': ' + str(validator11.error_log.last_error))
            else:
                errorlog.append(filename + ': version unknown')
        except Exception as e:
            print(''.ljust(width*3,'*') + filename)
            errorlog.append(filename + ': ' + str(e))
print()
print("Error log")
for err in errorlog:
    print(err)
    print()


