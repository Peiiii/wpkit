panjs = function () {
    var postJson=wpjs.postJson;
    var getDir = function (location, dirname) {
        var cmd = {cmd: {op: "getDir", params: {location: location, dirname: dirname}}};
        console.log(cmd);
        var res = postJson('/pan/cmd', cmd).responseJSON;
        console.log(res);
        return res;
    };
    var getFile = function (location, filename) {
        var cmd = {cmd: {op: "getFile", params: {location: location, filename: filename}}};
        console.log(cmd);
        var res = postJson('/pan/cmd', cmd).responseJSON;
        console.log(res);
        return res;
    };

    var newDir = function (location, dirname) {
        var cmd = {cmd: {op: "newDir", params: {location: location, dirname: dirname}}};
        console.log(cmd);
        var res = postJson('/pan/cmd', cmd).responseJSON;
        console.log(res);
        return res;
    };
    var newFile = function (location, filename) {
        var cmd = {cmd: {op: "newFile", params: {location: location, filename: filename}}};
        console.log(cmd);
        var res = postJson('/pan/cmd', cmd).responseJSON;
        console.log(res);
        return res;
    };
    var saveFile = function (location, filename,content) {
        var cmd = {cmd: {op: "saveFile", params: {location: location, filename: filename,content:content}}};
        console.log(cmd);
        var res = postJson('/pan/cmd', cmd).responseJSON;
        console.log(res);
        return res;
    };
    var deleteFile = function (location, name) {
        var cmd = {cmd: {op: "delete", params: {location: location, name: name}}};
        console.log(cmd);
        var res = postJson('/pan/cmd', cmd).responseJSON;
        console.log(res);
        return res;
    };
    var deleteDir = function (location, name) {
        var cmd = {cmd: {op: "delete", params: {location: location, name: name}}};
        console.log(cmd);
        var res = postJson('/pan/cmd', cmd).responseJSON;
        console.log(res);
        return res;
    };
    return {
        getDir:getDir,
        getFile:getFile,
        newDir:newDir,
        newFile:newFile,
        saveFile:saveFile,
        deleteDir:deleteDir,
        deleteFile:deleteFile
    }
}();