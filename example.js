//Remove background

const fs = require('fs');
var request = require('request');

function Removebg(beforePath, afterpath) {
    let path = afterpath;
    let fileSu = beforePath;
    const VhtearKey = "APIKEYMU";//CHAT wa.me/6281238552767
    let formData = {
        image: {
            value: fs.createReadStream(fileSu),
            options: {
                filename: fileSu,
                contentType: 'image/jpeg'
            }
        }
    };
    let options = {
        url: 'https://api.vhtear.com/removebg&apikey=' + VhtearKey,
        method: 'POST',
        formData: formData
    };
    request(options, function(err, resp, body) {
        if (err)
            console.log(err);
        if (!err && resp.statusCode == 200) {
            console.log("Upload success horay!!!");
            const user = JSON.parse(body)
            return user
        }
    });
}

Removebg('origin.jpg','result.png')

//Response json
`{
    "result": {
        "response": 200,
        "creator": "VHtears",
        "create_time": "2020-12-07",
        "image": "https://api.vhtear.com/media/465d39d8e18448b5bb2e6d2c324ede5d.png"
    }
}`
