async function addKey(event){
    event.preventDefault()

    let form = event.target
    let fields = event.target.elements

    let data = {
        key_id: fields['key_id'].value,
        key_1_status: fields['key_1'].value,
        key_2_status: fields['key_2'].value
    }

    form.reset()

    let result = await sendRequest('/key/add','POST', data)

    if('error' in result){
        toast("Adding key failed"+result['error']);
      }else{
        toast("Success");
        window.location.href= '/keys';
      }
}

async function getAllKeys(){
    let html = ""
    let result = await sendRequest(window.document.domain +'/key/all','GET')

    data = document.querySelector('#keyTable')

    if (result == []){
        html = ` There are no keys`
    }
    else{
        html += `
        <table>
        <tr> 
            <th>Key ID</th>
            <th>Key 1 Status</th>
            <th>Key 2 Status</th>
        </tr>`  
        for (let d in data){
            html += ` 
            <tr> 
            <td> ${d.key_id}</td>
            <td> ${d.key_1_status}</td>
            <td>${d.key_2_status}</td>
            </tr>`
        }
        html += `</table>`
    }
    data.innerHTML = html
    
}
//Add event listener to object later
