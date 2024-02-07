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

    elem = document.getElementById('new_locker');
    instance = M.Modal.getInstance(elem)
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

    
    elem = document.getElementById('new_locker');
    instance = M.Modal.getInstance(elem)
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
var add_list = []
var lockerRow_list = []
var actRent_list = []
var comRent_list = []
var row_id = 0
var rentType_price = new Map()

async function getAllStudents(){
    let result = await sendRequest('/api/student/available','GET').then((result)=>{
        for(r in result){
            student_list.push(result[r])
        }
    })
}
async function getActiveRents(){
    let result = await sendRequest('/api/rent/active','GET')
    initRentTable(result)
}

async function getInactiveRents(){
    let result = await sendRequest('/api/rent/inactive','GET')
    initRentTableC(result)
}

async function getLockers(){
    let result = await sendRequest('/api/locker','GET')
    
    for (r in result){
        locker_list.push(result[r])
    }
    initTable(locker_list)

}

async function getAllRentTypes(){
    let result = await sendRequest('/api/rentType/group','GET').then((result)=>{
        for(r in result){
            rentType_list.push(result[r])

        }
    })
}

async function getAllAdditionalRentTypes(){
    let result = await sendRequest('/api/rentType/addition','GET').then((result)=>{
        for(r in result){
            add_list.push(result[r])
        }
    })
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
    btn = document.querySelector('#options_btn')
    btn.className="dropdown-trigger btn purple darken-4 waves-effect"
    btn.dataset.target ="locker_dropdown1"
    data_dropdown = document.querySelector('#locker_dropdown1')
    html= ``
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
} 

function createRent(studentID,locker_code){
    btn = document.getElementById("rent_form_submit")
    l_code_form = document.getElementById("locker_code_rent")
    l_code_form.value = locker_code
    btn.addEventListener('click',async (event) => {
        event.preventDefault()
        let form = document.getElementById("rentalForm")
        let form2 = document.getElementById("RentTransaction")
        let fields = form.elements
        let fields2 = form2.elements
        let data = {
            student_id: fields['student_id'].value,
            locker_id:  fields['locker_code'].value,
            rentType: fields['rent_type'].value,
            rentMethod: fields['rent_method'].value,
            rent_date_from: fields['rent_date_from'].value,
            rent_date_to: fields['rent_date_to'].value,
            date_returned: fields['date_returned'].value,
            currency:fields2['currency'].value,
            amount:fields2['tL_amount'].value,
            t_date:fields2['transaction_date'].value,
            t_type:fields2['t_type'].value
        }
        elem = document.getElementById('new_Rent');
        instance = M.Modal.getInstance(elem)
        instance.close()
       
        let result = await sendRequest('/api/locker/rent','POST', data).then((response)=>{
            if (response.Message){
                toast(response.Message)
            }
            else{
            toast("Success")  
            window.location.reload()
            }
           
        }).catch((error)=>{
        })
    })
    studentIDBox = document.getElementById("rent_student_id")
    studentIDBox.value = studentID

    rentTypes = document.getElementById("rent_type")
    html = ' <option value=”” disabled selected>Select Rental Method First </option>'
   
   rentTypes.innerHTML = html
   elem = document.getElementById('new_Rent');
   instance = M.Modal.getInstance(elem)
   instance.open()
  }

  function additionalCharge(id){
    form = document.getElementById("additionalForm")
    html = `<input type="hidden" value="${id}" name="rent_id">
    <select id="rType" name="rentType" style="display:inline;" required>
    <option disabled selected>Select Additional Charge </option>
    `
    for(r in add_list){
         html+= `<option value=${add_list[r].id}>${add_list[r].type}: $${add_list[r].price} Period: ${add_list[r].period_from} to ${add_list[r].period_to}</option>`
    }
    html+=`
    </select>
    <div class="input-field col s8 m8 offset-m4" style="display:inline;">

    <div class="col s4 offset-s4">
       <a class="red darken-4 white-text right modal-close waves-light btn">Cancel</a>
    </div>

    <div class="col s4">
     <input type="submit" class="right purple darken-4 waves-light btn" id="l_submit" value="Add Charge">
    </div>
   </div>    `
    form.innerHTML = html 

    form.addEventListener('submit',async (event) => {
        event.preventDefault()
        let form = event.target
        let fields = event.target.elements
    
        let data = {
            rent_id: fields['rent_id'].value,
            rentType:  fields['rentType'].value,  
        }
        elem = document.getElementById('additional_modal');
        instance = M.Modal.getInstance(elem)
        instance.close()
        let result = await sendRequest('/api/rent/additional','POST', data).then((response)=>{
            if (response.Message){
                toast(response.Message)
            }
            else{
            toast("Success")  
            window.location.reload()
            }
        }).catch((response)=>{
             toast("failed");
             window.location.reload()
        })
    })
    

    
    elem = document.getElementById('additional_modal');
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
    btn = document.querySelector('#options_btn')
    btn.className="dropdown-trigger btn purple darken-4 waves-effect"
    btn.dataset.target ="locker_dropdown1"
    data_dropdown = document.querySelector('#locker_dropdown1')
    html= ``
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
    form = document.getElementById("swapKey_form")
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
    elem = document.getElementById('swap_key');
    instance = M.Modal.getInstance(elem)
    instance.open()
}

function openSwapRent(old_locker_code,new_locker_code){
    ol_code_form = document.getElementById("old_locker_code")
    ol_code_form.value = old_locker_code
    nl_code_form = document.getElementById("new_locker_code")
    nl_code_form.value = new_locker_code

    u_rentTypes = document.getElementById("s_rent_type")
    html = ' <option disabled selected>Select Rental Type </option>'
    u_rentTypes.innerHTML = html

    btn = document.getElementById('s_rent_form_submit')
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
        elem = document.getElementById('swap_Rent');
        instance = M.Modal.getInstance(elem)
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
    elem = document.getElementById('swap_Rent');
    instance = M.Modal.getInstance(elem)
    instance.open()

}

function initRentTable(data){
    let table = new DataTable('#rentTable',{
        "responsive":true,
        select:"multi",
        data:data,
        "columns":[
            {"data":"id"},
            {"data":"student_id"},
            {"data":"locker_code"},
            {"data":"rent_types"},
            {"data":"rent_date_from"},
            {"data":"rent_date_to"},
            {"data":"amount_owed"},
            {"data":"status"},
        ]
    })
    table.on( 'select', function ( e, dt, type, indexes ) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data();
            row_id = indexes
            if (actRent_list.length < 1){
                actRent_list.push(indexes[0])
            }
            else{
                p = actRent_list.shift()
                table.rows(p).deselect()
                actRent_list.push(indexes[0])
            }
        }
        rentOptions(data[0])
    } );

    table.on( 'deselect', function ( e, dt, type, indexes ) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data();
            actRent_list.shift()
    }});
}

function initRentTableC(data){
    let table = new DataTable('#rentTable_complete',{
        "responsive":true,
        select:"multi",
        data:data,
        "columns":[
            {"data":"id"},
            {"data":"student_id"},
            {"data":"key"},
            {"data":"locker_code"},
            {"data":"rent_types"},
            {"data":"rent_date_from"},
            {"data":"rent_date_to"},
            {"data":"status"},
        ]
    })

    table.on( 'select', function ( e, dt, type, indexes ) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data();
            row_id = indexes
            if (comRent_list.length < 1){
                comRent_list.push(indexes[0])
            }
            else{
                p = comRent_list.shift()
                table.rows(p).deselect()
                comRent_list.push(indexes[0])
            }
        }
        enableRentDetails(data[0].id)
    } );

    table.on( 'deselect', function ( e, dt, type, indexes ) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data();
            comRent_list.shift()
            disableRentDetails()
    }});
}

function enableRentDetails(id){
    btn = document.querySelector('#crent_details_btn')
    btn.className="btn purple darken-4 waves-effect"
    btn.href = '/rent/'+id
}

function disableRentDetails(){
    btn = document.querySelector('#crent_details_btn')
    btn.className="btn disabled center-align"
    btn.href = '#'
}


function rentOptions(d){
    btn = document.querySelector('#rent_options_btn')
    btn.className="dropdown-trigger btn purple darken-4 waves-effect"
    btn.dataset.target ="rent_dropdown1"
    data_dropdown = document.querySelector('#rent_dropdown1')
    html = ``
    
    if (d.status !== "Returned"){
        if(d.amount_owed !==0) {
            html += ` <li><a href="#" onclick="loadComments(${d.id},1)" class="white-text"><i class="material-icons left white-text">check</i>Note</a></li>
        <li><a href="/rent/${d.id}" class="white-text" > <i class="material-icons left white-text">list</i>Rent Details</a></li>
        <li><a href="#" onclick="editRent({'id':${d.id},'rent_method':'${d.rent_method}','rent_type':${d.rent_type},'rent_date_from':'${d.rent_date_from}','rent_date_to':'${d.rent_date_to}','date_return':'${d.date_returned}','late_fees':${d.late_fees},'additional_fees':${d.additional_fees},'rent_types':'${d.rent_types}'})" class="white-text"><i class="material-icons left white-text">edit</i>Edit</a></li>
        <li><a href="#" onclick="releaseMode({'amount_owed':${d.amount_owed}, 'id':${d.id},'locker_id':'${d.locker_id}'})" class="white-text"><i class="material-icons left white-text">attach_money</i>Open Transaction Log</a></li>
        <li><a href="#" onclick="additionalCharge(${d.id})" class="white-text"><i class="material-icons left white-text">add_circle_outline</i>Add Charge</a></li>
        `
        }
        else{
            html += ` <li><a href="#" onclick="loadComments(${d.id},1)" class="white-text"><i class="material-icons left white-text">check</i>Note</a></li>
            <li><a href="/rent/${d.id}" class="white-text" > <i class="material-icons left white-text">list</i>Rent Details</a></li>
            <li><a href="#" onclick="editRent({'id':${d.id},'rent_method':'${d.rent_method}','rent_type':${d.rent_type},'rent_date_from':'${d.rent_date_from}','rent_date_to':'${d.rent_date_to}','date_return':'${d.date_returned}','late_fees':${d.late_fees},'additional_fees':${d.additional_fees},'rent_types':'${d.rent_types}'})" class="white-text"><i class="material-icons left white-text">edit</i>Edit</a></li>
        <li><a href="#" onclick="releaseMode({'amount_owed':${d.amount_owed}, 'id':${d.id},'locker_id':'${d.locker_id}'})" class="white-text"><i class="material-icons left white-text">close</i>Release</a></li>
        <li><a href="#" onclick="additionalCharge(${d.id})" class="white-text"><i class="material-icons left white-text">add_circle_outline</i>Add Charge</a></li>
        `
        }
        
    }

    else if (d.status === "Returned"){
        html += `<li><a href="#" onclick="loadComments(${d.id},1)" class="white-text"><i class="material-icons left white-text">check</i>Note</a></li>
        <li><a href="/rent/${d.id}" class="white-text" > <i class="material-icons left white-text">list</i>Rent Details</a></li>
        <li><a href="/rent/${d.id}/release/verify" class="white-text"><i class="material-icons left white-text">verified_user</i>Verify</a></li>`
    }
    data_dropdown.innerHTML = html
    var elemsBtn = document.querySelectorAll('.dropdown-trigger');
      var instancesBtn = M.Dropdown.init(elemsBtn,{
        hover:true,
        constrainWidth:false
    });
}

function editRent(rent){
    form = document.getElementById('editRentalForm')
    form.action = "/rent/"+rent.id+"/update"
    form.removeEventListener('submit',addLocker)
    //document.forms['editRentalForm'].addEventListener('submit','')

    u_rent_method = document.getElementById('u_rent_method')
    temp_rm = '';
    if (rent.rent_method === 'Period'){
        temp_rm = 'Fixed'
    }
    else{
        temp_rm = rent.rent_method
    }

    u_rentTypes = document.getElementById("u_rent_type")
    html = ' <option disabled selected>Select Rental Type </option>'
    if(temp_rm === "Rate"){
        for (r in rentType_list[0]){
            html+= `<option value=${rentType_list[0][r].id}>${rentType_list[0][r].type}: $${rentType_list[0][r].price} Period: ${rentType_list[0][r].period_from} to ${rentType_list[0][r].period_to}</option>`
       }
    }
    else{
        for (r in rentType_list[1]){
            if(rentType_list[1][r].type.toLowerCase().includes(rent.rent_types.substring(rent.rent_types.indexOf(' ')+1).toLowerCase())){
            html+= `<option value=${rentType_list[1][r].id}>${rentType_list[1][r].type}: $${rentType_list[1][r].price} Period: ${rentType_list[1][r].period_from} to ${rentType_list[1][r].period_to}</option>`
        }
    }}
    u_rentTypes.innerHTML = html
    
   
    for(i=0; i<u_rent_method.options.length;i++){
        if(u_rent_method.options[i].value === temp_rm){
            u_rent_method.selectedIndex = i
        }
    }
    for(i=0; i<u_rentTypes.options.length;i++){
        if(u_rentTypes.options[i].value == rent.rent_type){    
              u_rentTypes.selectedIndex = i
        }
    }

    u_rent_date_from = document.getElementById('u_r_date_from')
    u_rent_date_to = document.getElementById('u_r_date_to')
    u_add_fee = document.getElementById('u_add_fee')
    u_late_fee = document.getElementById('u_late_fee')

    u_rent_date_from.value = rent.rent_date_from
    u_rent_date_to.value = rent.rent_date_to
    u_add_fee.value = rent.additional_fees
    u_late_fee.value = rent.late_fees

    if(rent.date_returned){
        u_date_return = document.getElementById('u_date_return')
        u_date_return.value = rent.date_returned
    }
    btn = document.getElementById('update_rent_form_submit')
    btn.addEventListener('click',async (event) => {
        let form = document.getElementById("editRentalForm")
        let fields = form.elements
        let data = {
            rentType: fields['rent_type'].value,
            rentMethod: fields['rent_method'].value,
            rent_date_from: fields['rent_date_from'].value,
            rent_date_to: fields['rent_date_to'].value,
            date_returned: fields['date_returned'].value,
            late_fees: fields['u_late_fee'].value,
            additional_fees: fields['u_add_fee'].value,
        }
        elem = document.getElementById('edit_rent');
        instance = M.Modal.getInstance(elem)
        instance.close()
       
        let result = await sendRequest('/api/rent/'+rent.id+'/update','POST', data).then((response)=>{
            toast("Success")
            window.location.reload()
        }).catch((response)=>{
             toast("Rental failed");
             window.location.reload()
        })
    })
  
    elem = document.getElementById('edit_rent');
    instance = M.Modal.getInstance(elem)
    instance.open()
}

//Add event listener to object later
document.addEventListener('DOMContentLoaded',getLockers)
document.addEventListener('DOMContentLoaded',getAllAreas)
document.addEventListener('DOMContentLoaded',getAllRentTypes)
document.addEventListener('DOMContentLoaded',getAllAdditionalRentTypes)
document.addEventListener('DOMContentLoaded',getAllStudents)
document.addEventListener('DOMContentLoaded',getActiveRents)
document.addEventListener('DOMContentLoaded',getInactiveRents)
document.getElementById('newLocker').addEventListener('submit',addLocker)
document.getElementById('swapKey_form').addEventListener('submit',swapKey)

document.getElementById('rent_method').addEventListener('change',(event)=>{
    table = $('#lockerTable').DataTable();
    var data = table.rows( lockerRow_list[0]).data();
    rentTypes = document.getElementById("rent_type")
    html = ' <option disabled selected>Select Rental Type </option>'
    
    if(event.target.value === "Rate"){
        for (r in rentType_list[0]){
            html+= `<option value=${rentType_list[0][r].id}>${rentType_list[0][r].type}: $${rentType_list[0][r].price} Period: ${rentType_list[0][r].period_from} to ${rentType_list[0][r].period_to}</option>`
            rentType_price.set(rentType_list[0][r].id,rentType_list[0][r])
       }
    }
    else{
        for (r in rentType_list[1]){
            if(rentType_list[1][r].type.toLowerCase().includes(data[0].locker_type.toLowerCase())){
            html+= `<option value=${rentType_list[1][r].id}>${rentType_list[1][r].type}: $${rentType_list[1][r].price} Period: ${rentType_list[1][r].period_from} to ${rentType_list[1][r].period_to}</option>`
        }
        rentType_price.set(rentType_list[1][r].id,rentType_list[1][r])
    }
    }

    rentTypes.innerHTML = html
})

document.getElementById('u_rent_method').addEventListener('change',(event)=>{
    table = $('#rentTable').DataTable();
    var data = table.rows(actRent_list[0]).data();
    rentTypes = document.getElementById("u_rent_type")
    html = ' <option  disabled selected>Select Rental Type </option>'
    
    if(event.target.value === "Rate"){
        for (r in rentType_list[0]){
            html+= `<option value=${rentType_list[0][r].id}>${rentType_list[0][r].type}: $${rentType_list[0][r].price} Period: ${rentType_list[0][r].period_from} to ${rentType_list[0][r].period_to}</option>`
       }
    }
    else{
        for (r in rentType_list[1]){
            console.log(data[0].rent_size)
            if(rentType_list[1][r].type.toLowerCase().includes(data[0].rent_size.toLowerCase())){
            html+= `<option value=${rentType_list[1][r].id}>${rentType_list[1][r].type}: $${rentType_list[1][r].price} Period: ${rentType_list[1][r].period_from} to ${rentType_list[1][r].period_to}</option>`
        }
    }
    }

    rentTypes.innerHTML = html
})

document.getElementById('s_rent_method').addEventListener('change',(event)=>{
    table = $('#lockerTable').DataTable();
    var temp = table.rows( lockerRow_list[0]).data()[0];
    var data;
    if (temp.status === "Rented"){
        data = table.rows( lockerRow_list[1]).data()[0];
    }
    else{
        data = table.rows( lockerRow_list[0]).data()[0];
    }

    rentTypes = document.getElementById("s_rent_type")
    html = ' <option disabled selected>Select Rental Type </option>'
    
    if(event.target.value === "Rate"){
        for (r in rentType_list[0]){
            html+= `<option value=${rentType_list[0][r].id}>${rentType_list[0][r].type}: $${rentType_list[0][r].price} Period: ${rentType_list[0][r].period_from} to ${rentType_list[0][r].period_to}</option>`
       }
    }
    else{
        for (r in rentType_list[1]){
            if(rentType_list[1][r].type.toLowerCase().includes(data.locker_type.toLowerCase())){
            html+= `<option value=${rentType_list[1][r].id}>${rentType_list[1][r].type}: $${rentType_list[1][r].price} Period: ${rentType_list[1][r].period_from} to ${rentType_list[1][r].period_to}</option>`
        }
    }
    }

    rentTypes.innerHTML = html
})

document.getElementById("rent_type").addEventListener("change",(event)=>{
    amount = document.getElementById("tL_amount")
    id = parseInt(event.target.value)
    rentType = rentType_price.get(id)
    console.log(rentType)
    amount.value = rentType.price
})



