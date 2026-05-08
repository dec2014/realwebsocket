
const chatRoom=document.querySelector('#room_uuid').textContent.replaceAll('"','')
console.log(chatRoom)
let chatSocket=null


const chatLogElemnet=document.querySelector('#chat_log')
const chatMessageElemnet=document.querySelector('#chat_message_input')
const chatSubmitElemnet=document.querySelector('#chat_message_submit')



function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type':'message',
        'message':chatMessageElemnet.value,
        'name':document.querySelector('#user_name').textContent.replaceAll('"',''),
        'agent':document.querySelector('#user_id').textContent.replaceAll('"',''),
    }))
    chatMessageElemnet.value=''
}


function onChatMesssage(data){
    console.log(data)
    const userBubble = `
    <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
        <div>
            <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg shadow-sm">
                <p class="text-sm">
                    ${data.message}
                </p>
            </div>
            <div class="flex justify-end items-center mt-1 space-x-1">
                <span class="text-[10px] text-gray-400 uppercase font-semibold">
                    ${data.created_at} ago
                </span>
            </div>
        </div>
        <div class="flex-shrink-0 h-10 w-10 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold shadow-inner">
            ${data.initials}
        </div>
    </div>
`;

    // This represents a message received from another user (aligned to the left)
    const guestBubble = `
        <div class="flex w-full mt-2 space-x-3 max-w-md">
            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-400 text-white flex items-center justify-center font-bold shadow-inner">
                ${data.initials}
            </div>
            <div>
                <div class="bg-gray-200 text-gray-800 p-3 rounded-r-lg rounded-bl-lg shadow-sm">
                    <p class="text-sm">
                        ${data.message}
                    </p>
                </div>
                <div class="flex justify-start items-center mt-1 space-x-1">
                    <span class="text-[10px] text-gray-500 uppercase font-semibold">
                        ${data.created_at}
                    </span>
                </div>
            </div>
        </div>
    `;


    if (data.type=='chat_message'){
        if (!data.agent){
            chatLogElemnet.innerHTML+=guestBubble

        }else{
            chatLogElemnet.innerHTML+=userBubble
        }
    }

}

chatSocket=new WebSocket(`wss://${window.location.host}/ws/${chatRoom}/`)
    chatSocket.onmessage=function(e){
        console.log('onMessage')
        onChatMesssage(JSON.parse(e.data))

    }
    chatSocket.onclose=function(e){
        console.log('onclose')
    }
    chatSocket.onopen=function(e){
        console.log('onOpen')
    }

    chatSubmitElemnet.onclick=function(e){
    sendMessage()
    return false
}
