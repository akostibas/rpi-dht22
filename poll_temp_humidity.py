import Adafruit_DHT
import boto3
import time

sensor = Adafruit_DHT.AM2302
# RaspberryPi pinout:
# https://pinout.xyz/pinout/pin18_gpio24
pin = 18

cloudwatch = boto3.client('cloudwatch')

while True:
    humidity_pct, temp_c = Adafruit_DHT.read_retry(sensor, pin)

    if humidity_pct is None or temp_c is None:
        print("Unable to read sensor. Retrying.")
        time.sleep(2)
        continue

    temp_f = temp_c * 9/5.0 + 32

    print("%sºF, %s%", temp_f, humidity_pct)

    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'Temperature',
                'Dimensions': [
                    {
                        'Name': 'Unit',
                        'Value': 'F'
                    },
                ],
                'Unit': 'None',
                'Value': temp_f
            },
        ],
        Namespace='HOME/STATS'
    )

    time.sleep(15)
