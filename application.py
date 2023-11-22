import boto3
import random
from flask import Flask, render_template, Response, request, redirect, url_for

application = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table('Fortunes')

@application.route('/')
def index():
    return render_template('index.html')


@application.route("/addfortune/", methods=['POST'])
def addfortune():
    fortune = request.form['addfortune']
    origin = request.form['addorigin']
    table.put_item(
        Item={
        'FortuneName': fortune,
        'FortuneOrigin': origin
        }
    )
    return render_template('index.html')


@application.route("/scanfortune/", methods=['GET'])
def scanfortune():
    response = table.scan()
    items = response['Items']
    print(items)
    return render_template('index.html', fortunes=items)

@application.route("/readfortune/", methods=['GET', 'POST'])
def readfortune():
    fortune_key = request.form['readfortune']
    origin_key = request.form['readorigin']
    response = table.get_item(
        Key={
            'FortuneName': fortune_key,
            'FortuneOrigin': origin_key
        }
    )
    item = response['Item']
    print(item)
    return render_template('index.html', fortune=item)




@application.route("/updatefortune/", methods=['GET', 'POST'])
def updatefortune():
    fortune_key = request.form['updatefortune']
    origin_key = request.form['updateorigin']
    author = request.form['updateattribute1']
    color = request.form['updateattribute2']
    response = table.update_item(
        Key={
            'FortuneName': fortune_key,
            'FortuneOrigin': origin_key
        },
        AttributeUpdates={
            'FortuneAuthor': {
                'Value'  : author,
                'Action' : 'PUT' # available options -> DELETE(delete), PUT(set), ADD(increment)
            },
            'FortuneColor': {
                'Value'  : color,
                'Action' : 'PUT' # available options -> DELETE(delete), PUT(set), ADD(increment)
            }
        }
    )
    return render_template('index.html')


@application.route("/deletefortune/", methods=['GET', 'POST'])
def deletefortune():
    fortune_key = request.form['deletefortune']
    origin_key = request.form['deleteorigin']
    response = table.delete_item(
        Key={
            'FortuneName': fortune_key,
            'FortuneOrigin': origin_key
        }
    )
    return render_template('index.html')

if __name__ == "__main__":
        application.run()

