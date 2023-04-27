document.querySelector('#chat-message-submit').onclick = function(e) {
        let name = 'Alex Jite'

        let fragment = `<a href="#" class="message list-group-item list-group-item-action">
                           <div class="d-flex align-items-start">
                               <img class="img-xs rounded-circle"
                                    src="" height="40"
                                    class="img-xs rounded-circle mr-1" width="40">
                               <div class="flex-grow-1 ml-3">
                                   ${name}
                                   <div class="small"><span class="fas fa-circle chat-online"></span>
                                       <span class="onlyline">Hello</span>
                                   </div>
                               </div>
                           </div>
                       </a>`

        const subject = document.querySelector("#subject");
        subject.insertAdjacentHTML("afterbegin", fragment);
};


//document.querySelector('#chat-message-submit').onclick = function(e) {
    //const messageInputDom = document.querySelector('#chat-message-input');
    //const message = messageInputDom.value;
    //chatSocket1.send(JSON.stringify({
    //    'user_id': user_id
    //}));
    //messageInputDom.value = '';
//};

//document.querySelector('#chat-message').onclick = function(e) {
//    clearInterval(interval);
//};