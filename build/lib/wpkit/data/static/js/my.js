// class App{
//     constructor(el){
//         this.email=el.find('.email-input');
//         this.password=el.find('.password-input');
//         this.submit=el.find('.btn-submit');
//         this.msg=el.find('.msg-box');
//     }
//     bind(){
//         var app=this;
//         this.submit.click(()=>{
//             var data={
//                 user_email:app.email.val(),
//                 user_password:app.password.val()
//             };
//
//         })
//     }
//     postJson(url,data){
//         return $.post({url:url,data:JSON.stringify(data),async:false}).responseJSON;
//     }
//
// }
console.log('my.js loaded.')
function postJson(url, data) {
    return $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: url,
        data: JSON.stringify(data),
        async: false,
        dataType: "json"
    });
}