
const crypto = require("crypto-js");

// var key0 = "L#$@XowPu!uZ&c%u";
// var iv0 = "2auvLZzxz7bo#^84";
// var body = "futanari好吗";
// var key = crypto.enc.Latin1.parse(key0);
// var iv = crypto.enc.Latin1.parse(iv0);
// var encrypted = crypto.AES.encrypt(body, key, {
//                     'iv': iv,
//                     'mode': crypto.mode.CBC,
//                     'padding': crypto.pad.ZeroPadding,
//                 }).toString()
// console.log(encrypted)


function encode(body){
    var key0 = "L#$@XowPu!uZ&c%u";
    var iv0 = "2auvLZzxz7bo#^84";
    var key = crypto.enc.Latin1.parse(key0);
    var iv = crypto.enc.Latin1.parse(iv0);
    var encrypted = crypto.AES.encrypt(body, key, {
                        'iv': iv,
                        'mode': crypto.mode.CBC,
                        'padding': crypto.pad.ZeroPadding,
                    }).toString()
    // console.log(encrypted)
    return encrypted;
}

crypto.enc.Latin1