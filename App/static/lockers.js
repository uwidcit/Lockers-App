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

    form.reset()
    elem = document.getElementById('new_locker');
    instance = M.Modal.getInstance(elem)
    instance.close()

    let result = await sendRequest('/api/locker','POST', data).then((response)=>{
        if (response.status == 201){
            toast("Success");
            locker_list.push(result)
            table = $('#lockerTable').DataTable();
            table.row.add(result).draw()
        }
    }).catch((response)=>{
        toast("Adding locker failed");
    })
}

async function updateLocker(event){
    event.preventDefault()

    let form = event.target
    let fields = event.target.elements
    tData = document.querySelector('#td_'+fields['locker_code'].value)

    let data = {
        locker_code: fields['locker_code'].value,
        area:  fields['area'].value,
        locker_type: fields['locker_type'].value,
        status: fields['status'].value,
        key: fields['key'].value
    }

    
    elem = document.getElementById('new_locker');
    instance = M.Modal.getInstance(elem)
    instance.close()
    form.reset()

    let result = await sendRequest('/api/locker','PUT', data).then(
        (response)=>{
            if(response.status === 200){
             toast("Success");
             table = $('#lockerTable').DataTable();
             table.row(row_id).data(result).draw()
            }
        }
    ).catch((response)=>{
        toast("Updating locker failed");
    })

}
async function getAllLockers(){
    let html = ""
    let result = await sendRequest('/api/locker','GET')
    
    data = document.querySelector('#lockerTable')
    
    if (result.error){
        html = ` <p> There are no lockers </p>`
    }
    else{ 
        for (let d of result){
            html += 
            `<tr class="purple darken-4 white-text" id="td_${d.locker_code}"> 
            <td><a href="/locker/${d.locker_code}"> ${d.locker_code} </a> </td>
            <td>${d.locker_type}</td>
            <td>${d.status}</td>
            <td> <a href="/key/${d.key}">${d.key} <a></td>
            <td><a href="/area/${d.area}">${d.area_description}</a></td>
            <div style=" position: relative;display: inline-flex;">
                    <td>
                        <a class="dropdown-trigger btn-floating purple darken-4 waves-effect" data-target="${d.locker_code}_dropdown1"><i class="large material-icons">list</i></a>
                        <ul id='${d.locker_code}_dropdown1' class='dropdown-content purple darken-4 white-text'>`
                if(d.status === "Free"){
                    html += `<li><a href="/locker/rent/${d.locker_code}/student" class="white-text"><i class="material-icons left white-text">check</i>Rent</a></li>`
                }
                else if (d.status === "Rented"){
                    html += ` <li><a href="#" onclick="loadComments(${d.current_rental.id},1)" class="white-text"><i class="material-icons left white-text">check</i>Note</a></li>
                    <li><a href="#" onclick="releaseMode()" class="white-text"><i class="material-icons left white-text">close</i>Release</a></li>`
                }
    
                else if (d.status == "Not Verified"){
                    html += `<li><a href="#" onclick="loadComments(${d.current_rental.id},1)" class="white-text"><i class="material-icons left white-text">check</i>Note</a></li>
                    <li><a href="/rent/(${d.current_rental.id}/release/verify" class="white-text"><i class="material-icons left white-text">verified_user</i>Verify</a></li>`
                }
                html +=`
                    <li><a href="#edit" onclick="editMode({'locker_code':'${d.locker_code}','locker_type':'${d.locker_type}','area':${d.area},'key':'${d.key}','status':'${d.status}'})" class="white-text"><i class="material-icons left white-text">edit</i>Edit</a></li>
                    <li><a href="#delete" onclick="removeMode({'locker_code':'${d.locker_code}','locker_type':'${d.locker_type}','area':${d.area},'key':'${d.key}','status':'${d.status}'})" class="white-text"><i class="material-icons left white-text">delete</i>Delete</a></li>
                    <li><a href="#delete" onclick="OpenswapKey({})" class="white-text"><i class="material-icons left white-text">swap_horiz</i>Swap</a></li>
                </ul>
                </div>
                </td>
            </tr>`
        }
    }
    data.innerHTML += html
    
}
async function getAllAreas(){
    let html = `<option value=”” disabled selected>Select a Area Status</option>`
    let result = await sendRequest('/api/area','GET')
    
    
    data = document.querySelector('#area')
    
    if (result.error){
        html = `<option value="" disabled selected> There are no areas available </option>`
    }
    else{
        for(r in result){
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
    form = document.getElementById('newLocker')
    form.action = "/locker/"+locker.locker_code+"/update"
    form.removeEventListener('submit',addLocker)
    document.forms['newLocker'].addEventListener('submit',updateLocker)
 
    id =  document.getElementById('locker_code')
    id.value = locker.locker_code
   
    type = document.getElementById('locker_type')
    key = document.getElementById('key')
    key.value = locker.key
   
    stats = document.getElementById('stats')
    area = document.getElementById('area')
    button = document.getElementById('l_submit')

    button.value = "Update Locker"
 
    for (i = 0; i < 4; i++){
       if(type.options[i].value === locker.locker_type){
         type.selectedIndex = i
       }
   
    }
   
    for(i =0; i < area.options.length;i++){
     if(area.options[i].value == locker.area){
         area.selectedIndex = i
       }
    }
 
    for (i = 0; i < 3; i++){
       if(stats.options[i].value === locker.status){
         stats.selectedIndex = i
       } 
 
    }
    elem = document.getElementById('new_locker');
    instance = M.Modal.init(elem,{
        onCloseEnd:()=>{
            form = document.getElementById('newLocker')
            form.action = "/api/locker"
            form.reset()
            button = document.getElementById('l_submit')
            button.value = "Add Locker"
            form.removeEventListener('submit',updateLocker)
            document.forms['newLocker'].addEventListener('submit',addLocker)
        }
    })
    instance.open()
   }

var student_list = []
var locker_list = []
var rentType_list = []
var lockerRow_list = []
var row_id = 0

async function getAllStudents(){
    let result = await sendRequest('/api/student/available','GET').then((result)=>{
        for(r in result){
            student_list.push(result[r])
        }
    })
}
async function getLockers(){
    let result = await sendRequest('/api/locker','GET')
    for (r in result){
        locker_list.push(result[r])
    }
    initTable(locker_list)

}

async function getAllRentTypes(){
    let result = await sendRequest('/api/rentType','GET').then((result)=>{
        for(r in result){
            rentType_list.push(result[r])
        }
    })
}
function initTable(data){
    if ( $.fn.dataTable.isDataTable( '#lockerTable' ) ) {
        table = $('#lockerTable').DataTable();
    }
    else{
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
                enableOptions(table.rows(lockerRow_list).data())
            }
        }
    } );
}
}

function enableOptions(d){
    btn = document.querySelector('#options_btn')
    btn.className="dropdown-trigger btn purple darken-4 waves-effect"
    btn.dataset.target ="locker_dropdown1"
    data_dropdown = document.querySelector('#locker_dropdown1')
    html= ``
    if(d.status === "Free"){
        html += `<li><a href="#" onclick="rentInit('${d.locker_code}')" class="white-text"><i class="material-icons left white-text">check</i>Rent</a></li>`
    }
    else if (d.status === "Rented"){
        html += ` <li><a href="#" onclick="loadComments(${d.current_rental.id},1)" class="white-text"><i class="material-icons left white-text">check</i>Note</a></li>
        <li><a href="#" onclick="releaseMode({'amount_owed':${d.current_rental.amount_owed}, 'id':${d.current_rental.id},'locker_id':'${d.current_rental.locker_id}'})" class="white-text"><i class="material-icons left white-text">close</i>Release</a></li>`
    }

    else if (d.status == "Not Verified"){
        html += `<li><a href="#" onclick="loadComments(${d.current_rental.id},1)" class="white-text"><i class="material-icons left white-text">check</i>Note</a></li>
        <li><a href="/rent/${d.current_rental.id}/release/verify" class="white-text"><i class="material-icons left white-text">verified_user</i>Verify</a></li>`
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
    btn = document.querySelector('#options_btn')
    btn.className ="btn disabled center-align"
    btn.dataset.target ="#locker_dropdown1"
    data_dropdown = document.querySelector('#locker_dropdown1')
    data_dropdown.innerHTML = ''
}

function disableStudent(){
    btn = document.querySelector('#studentConfirm_btn')
    btn.className ="btn disabled center-align"
    btn.removeEventListener('click', ()=> {

    })
}

function passStudent (locker_code,student){
    const lock = locker_code
    student_id = student['student_id']
    btn = document.querySelector('#studentConfirm_btn')
    btn.className="btn purple darken-4 waves-effect"
    btn.addEventListener('click',(()=>{
        elem = document.querySelector('#rent_modal')
        instance = M.Modal.getInstance(elem)
        instance.close()
        createRent(student_id,lock)
    }))
}

async function rentInit(locker_code){
    const lock = locker_code
    await getAllStudents().then(()=>{
        elem = document.querySelector('#rent_modal')
        if ( $.fn.dataTable.isDataTable( '#studentTable' ) ) {
            table = $('#studentTable').DataTable();
        }
        else{
        table = new DataTable('#studentTable',{
        "responsive":true,
        select:true,
        data:student_list,
        "columns":[
            {"data":"student_id"},
            {"data":"first_name"},
            {"data":"last_name"},
            {"data":"faculty"},
            {"data":"email"},
            {"data": "phone_number"},
            {"data":"rentStanding"},
        ]
    })}
        
    table.on( 'select', function ( e, dt, type, indexes) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data();
            passStudent(lock,data[0])
        }
    } );

    table.on( 'deselect', function ( e, dt, type, indexes ) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data();
            disableStudent()
        }
    } );

    instance = M.Modal.getInstance(elem)
    instance.open()
    }) 
}

function createRent(studentID,locker_code){
    form = document.getElementById("rentalForm")
    l_code_form = document.getElementById("locker_code_rent")
    l_code_form.value = locker_code
    form.addEventListener('submit',async (event) => {
        event.preventDefault()
        let form = event.target
        let fields = event.target.elements
    
        let data = {
            student_id: fields['student_id'].value,
            locker_id:  fields['locker_code'].value,
            rentType: fields['rent_type'].value,
            rent_date_from: fields['rent_date_from'].value,
            rent_date_to: fields['rent_date_to'].value   
        }
        elem = document.getElementById('new_Rent');
        instance = M.Modal.getInstance(elem)
        form.reset()
        let result = await sendRequest('/api/locker/rent','POST', data).then((response)=>{
            toast("Success");
        }).catch((response)=>{
             toast("Rental failed");
        })
    })
    studentIDBox = document.getElementById("rent_student_id")
    studentIDBox.value = studentID

    rentTypes = document.getElementById("rent_type")
    html = ' <option value=”” disabled selected>Select Rental Plan</option>'
    for (r in rentType_list){
        html+= `<option value=${rentType_list[r].id}>${rentType_list[r].type}: $${rentType_list[r].price} Period: ${rentType_list[r].period_from} to ${rentType_list[r].period_to}</option>`
    }
   rentTypes.innerHTML = html
   elem = document.getElementById('new_Rent');
   instance = M.Modal.getInstance(elem)
   instance.open()
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
    form.reset()

    let result = await sendRequest('/api/locker/swap','PUT', data).then((response)=>{
        toast("Success");
        getLockers()
    }).catch((response)=>{
        toast("Updating locker failed");
    })
}

function enableOptionsSwap(d){
    console.log(d)
    btn = document.querySelector('#options_btn')
    btn.className="dropdown-trigger btn purple darken-4 waves-effect"
    btn.dataset.target ="locker_dropdown1"
    data_dropdown = document.querySelector('#locker_dropdown1')
    html= ``
    if(d[0].status === "Free" && d[1].status === "Free"){
        html += `<li><a href="#" onclick="OpenSwapKey('${d[0].locker_code}','${d[1].locker_code}')" class="white-text"><i class="material-icons left white-text">swap_horiz</i>Swap</a></li>`
    }
    else{
        html += `<li><a href="#" class="white-text">Can't edit locker while rented</a></li>`
    }
    data_dropdown.innerHTML = html
      var elemsBtn = document.querySelectorAll('.dropdown-trigger');
      var instancesBtn = M.Dropdown.init(elemsBtn,{
        hover:true,
        constrainWidth:false
        });
}

function OpenSwapKey(locker1, locker2){
    form = document.getElementById("swapKey_form")
    form.innerHTML = `<p> Do you want to swap ${locker1} with ${locker2} <p>
    <input type = "hidden" value = ${locker1} name = locker_code1>
    <input type = "hidden" value = ${locker2} name = locker_code2>
    <div class="input-field col s8 m8 offset-m4" style="display:inline;">
        <div class="col s4 offset-s4">
        <a class="red darken-4 white-text right modal-close waves-light btn">Cancel</a>
        </div>
        <div class="col s4">
        <input type="submit" class="right purple darken-4 waves-light btn" value="Assign">
        </div>
    </div>`
    elem = document.getElementById('swap_key');
    instance = M.Modal.getInstance(elem)
    instance.open()
  }

//Add event listener to object later
document.addEventListener('DOMContentLoaded',getLockers)
document.addEventListener('DOMContentLoaded',getAllAreas)
document.addEventListener('DOMContentLoaded',getAllRentTypes)
document.addEventListener('DOMContentLoaded',getAllStudents)
document.getElementById('newLocker').addEventListener('submit',addLocker)
document.getElementById('swapKey_form').addEventListener('submit',swapKey)
