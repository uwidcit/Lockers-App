async function addLocker(event){
    event.preventDefault()

    let form = event.target
    let fields = event.target.elements

    let data = {
        locker_code: fields['locker_code'].value,
        area:  fields['area'].value,
        locker_type: fields['locker_type'].value,
        status: fields['status'].value,
        key_id: fields['key_id'].value
    }

    form.reset()

    let result = await sendRequest('/locker/add','POST', data)

    if('error' in result){
        toast("Adding locker failed"+result['error']);
      }else{
        toast("Success");
        window.location.href= '/locker';
      }
}
async function getAllLockers(){
    let html = ""
    let result = await sendRequest('/lockers/get/all','GET')
    
    data = document.querySelector('#lockerTable')
    
    
    if (result.error){
        html = ` <p> There are no lockers </p>`
    }
    else{
        html += `
        <table>
        <tr> 
            <th>Locker Code</th>
            <th>Key ID </th>
            <th>Area</th>
            <th>Locker Type</th>
            <th>Status</th>
        </tr>`  
        for (let d of result.data){
            html += ` 
            <tr> 
            <td> ${d.locker_id}</td>
            <td> ${d.key_id}</td>
            <td>${d.area}</td>
            <td>${d.locker_type}</td>
            <td>${d.status}</td>
            </tr>`
        }
        html += `</table>`
    }
    data.innerHTML = html
    
}
//Add event listener to object later
document.addEventListener('DOMContentLoaded',getAllLockers)
document.forms['newLocker'].addEventListener('submit',addLocker)