// lambda
const AWS = require('aws-sdk')

const firehose = new AWS.Firehose()
const StreamName = "SensorDataStream"

exports.handler = async (event) => {

    console.log('Received IoT event:', JSON.stringify(event, null, 2))

    // let payload = {
    //     id: new Date(event.time),
    //     sensor_value: event.sensor_a0
    // }

    let payload = {
        id: event.id ,
        temperature: event.temp,
        humidity: event.humid
    }

    let params = {
            DeliveryStreamName: StreamName,
            Record: { 
                Data: JSON.stringify(payload)
            }
        }

    return await firehose.putRecord(params).promise()
}