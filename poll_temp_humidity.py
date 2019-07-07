import Adafruit_DHT
import boto3
import socket
import time

sensor = Adafruit_DHT.AM2302
# RaspberryPi pinout:
# https://pinout.xyz/pinout/pin18_gpio24
pin = 24

hostname = socket.gethostname()

cloudwatch = boto3.client('cloudwatch')

while True:
    humidity_pct, temp_c = Adafruit_DHT.read_retry(sensor, pin)

    if humidity_pct is None or temp_c is None:
        print("Unable to read sensor. Retrying.")
        time.sleep(2)
        continue

    temp_f = temp_c * 9/5.0 + 32

    print("%s: %0.2fºF, %0.2f%%" % (hostname, temp_f, humidity_pct))

    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'Temperature',
                'Dimensions': [
                    {
                        'Name': 'Temperature',
                        'Value': hostname
                    },
                ],
                'Unit': 'None',
                'Value': temp_f
            },
            {
                'MetricName': 'Humidity',
                'Dimensions': [
                    {
                        'Name': 'Humidity',
                        'Value': hostname
                    },
                ],
                'Unit': 'None',
                'Value': humidity_pct
            },
        ],
        Namespace='Home/Atmosphere'
    )

    time.sleep(15)
