// lambda
const AWS = require('aws-sdk')

const firehose = new AWS.Firehose()
const StreamName = "SensorDataStream"

exports.handler = async (event) => {

    console.log('Received IoT event:', JSON.stringify(event, null, 2))

    let payload = {
        time: event.time,
        current: event.current,
        load_voltage: event.load_voltage,
        power: event.power,
        coordinate_x: event.coordinate_x,
        coordinate_y: event.coordinate_y,
        coordinate_z: event.coordinate_z,
        date: event.date
    }

    let params = {
            DeliveryStreamName: StreamName,
            Record: { 
                Data: JSON.stringify(payload)
            }
        }

    return await firehose.putRecord(params).promise()
}