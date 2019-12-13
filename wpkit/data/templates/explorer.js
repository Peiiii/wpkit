explorerjs = function () {
    var QWindow = winjs.QWindow;
    var getDir = panjs.getDir;
    var getFile = panjs.getFile;
    var newFile = panjs.newFile;
    var newDir = panjs.newDir;
    var Editor = edjs.Editor;
    var T = wpjs.T;
    var genUid = wpjs.genUid;

    class Explorer {
        constructor(el) {
            if ($.isPlainObject(el)) {
                this.el = el.el;
            } else {
                this.el = el;
            }
            this.init();
        }

        init() {
            this.uclass = 'explorer-' + genUid();
            this.uid = this.uclass;
            this.window = new QWindow({
                el: this.el, title: 'Explorer'
            });
            this.window.fill(this.source().template);
            this.viewbox = $('#' + this.uid);
            this.vm = this.init_vm();
            this.window.show();
        }

        init_vm() {

            var vm= new Vue({
                el: `#${this.uid}`,
                delimiters: ['<%', '%>'],
                data: {
                    items: getDir('./', './'),
                    location: "./",
                    root_path: './',
                    loc_history: ['./'],
                    window:null
                },
                methods: {
                    log: function (text) {
                        text = text || 'expolorer info....';
                        console.log(text);
                    },
                    forward: function (name) {
                        this.loc_history.push(this.location + '/' + name);
                        this.refresh();
                    },
                    backward: function () {
                        if (this.loc_history.length <= 1) {
                            return false;
                        }
                        this.loc_history.pop();
                        this.refresh();
                    },
                    goTo:function(path){
                        this.loc_history.push(path);this.refresh();
                    },
                    goHome:function(){
                        this.goTo(this.loc_history[0]);
                    },
                    refresh: function () {
                        var loc = this.loc_history.slice(-1)[0];
                        this.items = getDir(this.root_path, loc);
                        this.location = loc;
                    },
                    dialog:function(e){
                        console.log('window:',this.window);
                        // this.window.dialog();
                        this.window.input((text)=>{
                            console.log('get text:',text);
                        });
                        console.log('dialog sent...');
                    },
                    input:function(msg,callback){
                      this.window.input(msg,(text)=>{
                            callback(text);
                      })
                    },
                    tryNewFile: function (e) {
                        var self=this;
                        this.input('What is the file name?',function (fn) {
                            newFile(self.location,fn);self.refresh();
                        })
                    },
                    tryNewDir: function (e) {
                        var self=this;
                        this.input('What is the directory name?',function (dn) {
                            newDir(self.location,dn);self.refresh();
                        })
                    },
                    trySaveFile: function (e) {

                    },
                    tryDeleteFile: function (e) {

                    },
                    tryDeleteDir: function (e) {

                    },
                    updateView: function (e) {
                        console.log(e.target);
                        var obj = $(e.target).parent('.flist-item');
                        var name = obj.attr('itemname');
                        var type = obj.attr('itemtype');
                        switch (type) {
                            case T.DIR:
                                this.forward(name);
                                break;
                            case T.FILE:
                                var content = getFile(this.location, name);
                                var ed=new Editor();
                                ed.add_content(content);
                                ed.show();
                                break;
                            default:
                                null;
                                break;
                        }

                    }
                }
            });
            vm.$data.window=this.window;
            console.log('window init:',vm.$window)
            return vm;
        }

        source() {
            return {
                template: `<div class="w-100 h-100 explorer" id="${this.uid}">
        <div class="text-info head">
            <span class="label-primary menu-item" @click="goHome">Home</span><span @click="backward" class="label-public menu-item">Back</span>
            <span class="label-primary menu-item" @click="tryNewFile">New File</span><span class="label-public menu-item" @click="tryNewDir">New Dir</span>
            <span @click="refresh" class="label-primary menu-item">Refresh</span>
        </div>
        <div class="body">
            <div class="flist-item" v-bind:itemname="fileitem.name" v-bind:itemtype="fileitem.type"
                 v-for="fileitem in items">
                <label @click="updateView"><%fileitem.name%></label>
                <label><%fileitem.type%></label>
            </div>
        </div>
    </div>
    <style>
        #${this.uid} {
            display: flex;
            flex-flow: column;
        }
        #${this.uid} .head {
            flex: 0 1 40px;
            width: 100%;
            background-color: white;color: orange;
            border-bottom: black dotted 2px;
        }
        #${this.uid} .head .menu-item{
            margin:auto 3px auto 3px;
            padding: auto 3px auto 3px !important;
            border: solid gray 2px;
        }
        #${this.uid} .flist-item{
            border-bottom: dotted 2px black;
        }
        #${this.uid} .body {
            flex: 1 0 auto;
            max-height: calc(90% - 40px);
            /*height: 300px;*/
            width: 100%;
            background-color: white;
            color: orange;
            overflow: auto;
        }

    </style>`,
                style: ``
            }
        }

    }

    return {
        Explorer: Explorer
    }
}();
