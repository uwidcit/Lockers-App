import { locker_validate,lockerEdit_validate } from "./validate_locker.js"

async function addLocker(event){
    event.preventDefault()

    let form = event.target
    let fields = event.target.elements

    let data = {
        locker_code: fields['locker_code'].value,
        area:fields['area'].value,
        locker_type: fields['locker_type'].value,
        status: fields['status'].value,
        key: fields['key'].value
    }

    let isValid = locker_validate(data,form)
    if(isValid){
        let elem = document.getElementById('new_locker');
    let instance = M.Modal.getInstance(elem)
    instance.close()

    let result = await sendRequest('/api/locker','POST', data).then((response)=>{
        if (response.status == 201){
            window.location.reload()
            toast("Success");
        }
    }).catch((response)=>{
        toast("Adding locker failed");
        window.location.reload()
    })
}

else{
    let modal = document.getElementById('error_modal');
            let mInstance = M.Modal.getInstance(modal)
            mInstance.open()
}

    
}

async function updateLocker(event){
    event.preventDefault()

    let form = event.target
    let fields = event.target.elements

    let data = {
        locker_code: fields['locker_code'].value,
        area:  fields['area'].value,
        locker_type: fields['locker_type'].value,
        status: fields['status'].value,
        key: fields['key'].value
    }
    let isValid = lockerEdit_validate(data,form)
    if(isValid){
        let elem = document.getElementById('new_locker');
        let instance = M.Modal.getInstance(elem)
        instance.close()

        let result = await sendRequest('/api/locker','PUT', data).then((response)=>{
            if (response.Message){
                toast(response.Message)
            }
            else{
            toast("Success")  
            window.location.reload()
            }
       
    }).catch((error)=>{})
    }
    else{
        let modal = document.getElementById('error_modal');
        let mInstance = M.Modal.getInstance(modal)
        mInstance.open()
    }

    
    

}

async function getAllAreas(){
    let html = `<option value=”” disabled selected>Select a Area Status</option>`
    let result = await sendRequest('/api/area','GET')
    
    
    let data = document.querySelector('#area')
    
    if (result.error){
        html = `<option value="" disabled selected> There are no areas available </option>`
    }
    else{
        for(let r in result){
            html+= `<option value=${result[r].id}> ${result[r].description} </option>`
        }
    }
    data.innerHTML = html
    var elemsBtn = document.querySelectorAll('.dropdown-trigger');
      var instancesBtn = M.Dropdown.init(elemsBtn,{
        hover:true,
        constrainWidth:false
        });
}

function editMode(locker){
    let form = document.getElementById('newLocker')
    console.log(locker)
    form.action = "/locker/"+locker.locker_code+"/update"
    form.removeEventListener('submit',addLocker)
    document.forms['newLocker'].addEventListener('submit',updateLocker)
 
    let id =  document.getElementById('locker_code')
    id.value = locker.locker_code
    id.disabled = true
   
    let type = document.getElementById('locker_type')
    let key = document.getElementById('key')
    key.value = locker.key
   
    let stats = document.getElementById('stats')
    let area = document.getElementById('area')
    let button = document.getElementById('l_submit')

    button.value = "Update Locker"
 
    for (let i = 0; i < 4; i++){
       if(type.options[i].value === locker.locker_type){
         type.selectedIndex = i
       }
   
    }
   
    for(let i =0; i < area.options.length;i++){
     if(area.options[i].value == locker.area){
         area.selectedIndex = i
       }
    }
 
    for (let i = 0; i < 3; i++){
       if(stats.options[i].value === locker.status){
         stats.selectedIndex = i
       } 
 
    }
   let  elem = document.getElementById('new_locker');
    let instance = M.Modal.init(elem,{
        onCloseEnd:()=>{
            let form = document.getElementById('newLocker')
            form.action = "/api/locker"
            let id =  document.getElementById('locker_code')
            id.disabled = false
            let button = document.getElementById('l_submit')
            button.value = "Add Locker"
            form.removeEventListener('submit',updateLocker)
            form.reset()
            document.forms['newLocker'].addEventListener('submit',addLocker)
        }
    })
    instance.open()
   }


var locker_list = []
var lockerRow_list = []
var row_id = 0


async function getLockers(){
    let result = await sendRequest('/api/locker','GET')
    
    for (let r in result){
        locker_list.push(result[r])
    }
    initTable(locker_list)

}



function initTable(data){
    let table = new DataTable('#lockerTable',{
        "responsive":true,
        select:"multi",
        
        data:data,
        "columns":[
            {"data":"locker_code"},
            {"data":"locker_type"},
            {"data":"status"},
            {"data":"key"},
            {"data":"area_description"},
        ]
    })
     table.on( 'select', function ( e, dt, type, indexes ) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data();
            row_id = indexes
            if (lockerRow_list.length < 2){
                lockerRow_list.push(indexes[0])
                if(lockerRow_list.length == 2){
                    enableOptionsSwap(table.rows(lockerRow_list).data())
                }
                else{
                    enableOptions(data[0])
                }
            }
            else{
                p = lockerRow_list.shift()
                table.rows(p).deselect()
                lockerRow_list.push(indexes[0])
                enableOptionsSwap(table.rows(lockerRow_list).data())
            }
        }
    } );

    table.on( 'deselect', function ( e, dt, type, indexes ) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data();
            if (lockerRow_list.length == 1){
                if(lockerRow_list[0] == indexes[0]){
                    lockerRow_list.shift()
                    disableOptions()
                }
            }
            else{
                if (lockerRow_list[0] === indexes[0]){
                    lockerRow_list.shift()
                }
                else if(lockerRow_list[1] == indexes[0]){
                    lockerRow_list.pop()
                }
                enableOptions(table.rows(lockerRow_list).data()[0])
            }
        }
    } );
}

function enableOptions(d){
    let btn = document.querySelector('#options_btn')
    btn.className="dropdown-trigger btn purple darken-4 waves-effect"
    btn.dataset.target ="locker_dropdown1"
    let data_dropdown = document.querySelector('#locker_dropdown1')
    let html= ``
    if(d.status === "Free"){
        html += `<li><a href="#" onclick="rentInit('${d.locker_code}')" class="white-text"><i class="material-icons left white-text">check</i>Rent</a></li>`
    }
    html +=`
        <li><a href="#edit" onclick="editMode({'locker_code':'${d.locker_code}','locker_type':'${d.locker_type}','area':${d.area},'key':'${d.key}','status':'${d.status}'})" class="white-text"><i class="material-icons left white-text">edit</i>Edit</a></li>
        <li><a href="#delete" onclick="removeMode({'locker_code':'${d.locker_code}','locker_type':'${d.locker_type}','area':${d.area},'key':'${d.key}','status':'${d.status}'})" class="white-text"><i class="material-icons left white-text">delete</i>Delete</a></li>`
    data_dropdown.innerHTML = html
      var elemsBtn = document.querySelectorAll('.dropdown-trigger');
      var instancesBtn = M.Dropdown.init(elemsBtn,{
        hover:true,
        constrainWidth:false
        });
}

function disableOptions(){
    let btn = document.querySelector('#options_btn')
    btn.className ="btn disabled center-align"
    btn.dataset.target ="#locker_dropdown1"
    let data_dropdown = document.querySelector('#locker_dropdown1')
    data_dropdown.innerHTML = ''
}

  async function swapKey(event){
    event.preventDefault()

    let form = event.target
    let fields = event.target.elements

    let data = {
        locker_code1: fields['locker_code1'].value,
        locker_code2: fields['locker_code2'].value,
    }
    
    elem = document.getElementById('swap_key');
    instance = M.Modal.getInstance(elem)
    instance.close()

    let result = await sendRequest('/api/locker/swap','PUT', data).then((response)=>{
        if (response.Message){
            toast(response.Message)
        }
        else{
        toast("Success")  
        window.location.reload()
        }
    }).catch((response)=>{
        toast("Updating locker failed");
        window.location.reload()
    })
}

function enableOptionsSwap(d){
    let btn = document.querySelector('#options_btn')
    btn.className="dropdown-trigger btn purple darken-4 waves-effect"
    btn.dataset.target ="locker_dropdown1"
    let data_dropdown = document.querySelector('#locker_dropdown1')
    let html= ``
    if(d[0].status === "Free" && d[1].status === "Free"){
        html += `<li><a href="#" onclick="OpenSwapKey('${d[0].locker_code}','${d[1].locker_code}')" class="white-text"><i class="material-icons left white-text">swap_horiz</i>Swap Keys</a></li>`
    }
    else if((d[0].status === "Rented" && d[1].status === "Free") || (d[0].status === "Free" && d[1].status === "Rented")){   
        html += `<li><a href="#" class="white-text" onclick="openSwapRent('${d[0].locker_code}','${d[1].locker_code}')"><i class="material-icons left white-text">swap_horiz</i>Swap Rent</a></li>`
    }
    else{
        html += `<li><a href="#" class="white-text">Cannot modify locker(s) while rented</a></li>`
    }
    data_dropdown.innerHTML = html
      var elemsBtn = document.querySelectorAll('.dropdown-trigger');
      var instancesBtn = M.Dropdown.init(elemsBtn,{
        hover:true,
        constrainWidth:false
        });
}

function OpenSwapKey(locker1, locker2){
    let form = document.getElementById("swapKey_form")
    form.innerHTML = `<p> Do you want to swap ${locker1} with ${locker2} <p>
    <input type = "hidden" value = '${locker1}' name = locker_code1>
    <input type = "hidden" value = '${locker2}' name = locker_code2>
    <div class="input-field col s8 m8 offset-m4" style="display:inline;">
        <div class="col s4 offset-s4">
        <a class="red darken-4 white-text right modal-close waves-light btn">Cancel</a>
        </div>
        <div class="col s4">
        <input type="submit" class="right purple darken-4 waves-light btn" value="Assign">
        </div>
    </div>`
    let elem = document.getElementById('swap_key');
    let instance = M.Modal.getInstance(elem)
    instance.open()
}

function openSwapRent(old_locker_code,new_locker_code){
    let ol_code_form = document.getElementById("old_locker_code")
    ol_code_form.value = old_locker_code
    let nl_code_form = document.getElementById("new_locker_code")
    nl_code_form.value = new_locker_code

    let u_rentTypes = document.getElementById("s_rent_type")
    let html = ' <option disabled selected>Select Rental Type </option>'
    u_rentTypes.innerHTML = html

    let btn = document.getElementById('s_rent_form_submit')
    btn.addEventListener('click',async (event) => {
        let form = document.getElementById("swaprentForm")
        let fields = form.elements
        let data = {
            rentType: fields['rent_type'].value,
            rentMethod: fields['rent_method'].value,
            rent_date_from: fields['s_rent_date_from'].value,
            rent_date_to: fields['s_rent_date_to'].value,
            date_returned: fields['s_date_returned'].value,
            rented_locker_id: fields['old_locker_code'].value,
            locker_id: fields['new_locker_code'].value,
        }
        let elem = document.getElementById('swap_Rent');
        let instance = M.Modal.getInstance(elem)
        instance.close()
       
        let result = await sendRequest('/api/rent/swap','POST', data).then((response)=>{
            if (response.Message){
                toast(response.Message)
            }
            else{
            toast("Success")  
            window.location.reload()
            }
        }).catch((response)=>{
             
        })
    })
    let elem = document.getElementById('swap_Rent');
    let instance = M.Modal.getInstance(elem)
    instance.open()

}

//Add event listener to object later
document.addEventListener('DOMContentLoaded',getLockers)
document.addEventListener('DOMContentLoaded',getAllAreas)
document.getElementById('newLocker').addEventListener('submit',addLocker)
document.getElementById('swapKey_form').addEventListener('submit',swapKey)

export {lockerRow_list, addLocker}
window.editMode = editMode
window.OpenSwapKey = OpenSwapKey
window.openSwapRent = openSwapRent
