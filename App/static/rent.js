import { rentValidate,rentEditValidate,additionalChargeValidate} from "./validate_rent.js"
import { lockerRow_list,addLocker } from "./lockers.js"
var rentType_list = []
var add_list = []
var actRent_list = []
var comRent_list = []
var student_list = []
var row_id = 0
var rentType_price = new Map()

async function getAllStudents(){
    let result = await sendRequest('/api/student/available','GET').then((result)=>{
        for(let r in result){
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

async function getAllRentTypes(){
    let result = await sendRequest('/api/rentType/group','GET').then((result)=>{
        for(let r in result){
            rentType_list.push(result[r])

        }
    })
}

async function getAllAdditionalRentTypes(){
    let result = await sendRequest('/api/rentType/addition','GET').then((result)=>{
        for(let r in result){
            add_list.push(result[r])
        }
    })
}

async function rentInit(locker_code){
    const lock = locker_code
    let elem = document.querySelector('#rent_modal')
    let table = null
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

    let instance = M.Modal.getInstance(elem)
    instance.open()
} 

function createRent(studentID,locker_code){
    let btn = document.getElementById("rent_form_submit")
    let l_code_form = document.getElementById("locker_code_rent")
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
        let elem = document.getElementById('new_Rent');
        let instance = M.Modal.getInstance(elem)
        let isValid = rentValidate(data,fields,fields2)
       if (isValid){
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
       }
       else{
            let modal = document.getElementById('error_modal');
            let mInstance = M.Modal.getInstance(modal)
            mInstance.open()
       }
        
    })
    let studentIDBox = document.getElementById("rent_student_id")
    studentIDBox.value = studentID

    let rentTypes = document.getElementById("rent_type")
    let html = ' <option value=”” disabled selected>Select Rental Method First </option>'
   
   rentTypes.innerHTML = html
   let elem = document.getElementById('new_Rent');
   let instance = M.Modal.getInstance(elem)
   instance.open()
  }

  function additionalCharge(id){
    let form = document.getElementById("additionalForm")
    let html = `<input type="hidden" value="${id}" name="rent_id">
    <select id="rType" name="rentType" style="display:inline;" required>
    <option disabled selected>Select Additional Charge </option>
    `
    for(let r in add_list){
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
        let isValid = additionalChargeValidate(data,form)

        if(isValid){
             let elem = document.getElementById('additional_modal');
        let instance = M.Modal.getInstance(elem)
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
        }
        else{
            let modal = document.getElementById('error_modal');
            let mInstance = M.Modal.getInstance(modal)
            mInstance.open()
        }

       
    })
    

    
    let elem1 = document.getElementById('additional_modal');
    let instance1 = M.Modal.getInstance(elem1)
    instance1.open()

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
                let p = actRent_list.shift()
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
    let btn = document.querySelector('#crent_details_btn')
    btn.className="btn purple darken-4 waves-effect"
    btn.href = '/rent/'+id
}

function disableRentDetails(){
    let btn = document.querySelector('#crent_details_btn')
    btn.className="btn disabled center-align"
    btn.href = '#'
}


function rentOptions(d){
    let btn = document.querySelector('#rent_options_btn')
    btn.className="dropdown-trigger btn purple darken-4 waves-effect"
    btn.dataset.target ="rent_dropdown1"
    let data_dropdown = document.querySelector('#rent_dropdown1')
    let html = ``
    
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
    let form = document.getElementById('editRentalForm')
    form.action = "/rent/"+rent.id+"/update"
    form.removeEventListener('submit',addLocker)
    //document.forms['editRentalForm'].addEventListener('submit','')

    let u_rent_method = document.getElementById('u_rent_method')
    let temp_rm = '';
    if (rent.rent_method === 'Period'){
        temp_rm = 'Fixed'
    }
    else{
        temp_rm = rent.rent_method
    }

    let u_rentTypes = document.getElementById("u_rent_type")
    let html = ' <option disabled selected>Select Rental Type </option>'
    if(temp_rm === "Rate"){
        for (let r in rentType_list[0]){
            html+= `<option value=${rentType_list[0][r].id}>${rentType_list[0][r].type}: $${rentType_list[0][r].price} Period: ${rentType_list[0][r].period_from} to ${rentType_list[0][r].period_to}</option>`
       }
    }
    else{
        for (let r in rentType_list[1]){
            if(rentType_list[1][r].type.toLowerCase().includes(rent.rent_types.substring(rent.rent_types.indexOf(' ')+1).toLowerCase())){
            html+= `<option value=${rentType_list[1][r].id}>${rentType_list[1][r].type}: $${rentType_list[1][r].price} Period: ${rentType_list[1][r].period_from} to ${rentType_list[1][r].period_to}</option>`
        }
    }}
    u_rentTypes.innerHTML = html
    
   
    for(let i=0; i<u_rent_method.options.length;i++){
        if(u_rent_method.options[i].value === temp_rm){
            u_rent_method.selectedIndex = i
        }
    }
    for(let i=0; i<u_rentTypes.options.length;i++){
        if(u_rentTypes.options[i].value == rent.rent_type){    
              u_rentTypes.selectedIndex = i
        }
    }

    let u_rent_date_from = document.getElementById('u_r_date_from')
    let u_rent_date_to = document.getElementById('u_r_date_to')
    let u_add_fee = document.getElementById('u_add_fee')
    let u_late_fee = document.getElementById('u_late_fee')

    u_rent_date_from.value = rent.rent_date_from
    u_rent_date_to.value = rent.rent_date_to
    u_add_fee.value = rent.additional_fees
    u_late_fee.value = rent.late_fees

    if(rent.date_returned){
        let u_date_return = document.getElementById('u_date_return')
        u_date_return.value = rent.date_returned
    }
    let btn = document.getElementById('update_rent_form_submit')
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
        let isValid = rentEditValidate(data,form)
        if (isValid){
            let elem = document.getElementById('edit_rent');
            let instance = M.Modal.getInstance(elem)
            instance.close()
       
            let result = await sendRequest('/api/rent/'+rent.id+'/update','POST', data).then((response)=>{
                toast("Success")
                window.location.reload()
            }).catch((response)=>{
                toast("Rental failed");
                window.location.reload()
            })
        }
        else{
            let modal = document.getElementById('error_modal');
            let mInstance = M.Modal.getInstance(modal)
            mInstance.open()
        }
        
    })
  
    let elem = document.getElementById('edit_rent');
    let instance = M.Modal.getInstance(elem)
    instance.open()
}


function disableStudent(){
    let btn = document.querySelector('#studentConfirm_btn')
    btn.className ="btn disabled center-align"
    btn.removeEventListener('click', ()=> {

    })
}

function passStudent (locker_code,student){
    const lock = locker_code
    let student_id = student['student_id']
    let btn = document.querySelector('#studentConfirm_btn')
    btn.className="btn purple darken-4 waves-effect"
    btn.addEventListener('click',(()=>{
        let elem = document.querySelector('#rent_modal')
        let instance = M.Modal.getInstance(elem)
        instance.close()
        createRent(student_id,lock)
    }))
}

document.addEventListener('DOMContentLoaded',getAllRentTypes)
document.addEventListener('DOMContentLoaded',getAllAdditionalRentTypes)
document.addEventListener('DOMContentLoaded',getActiveRents)
document.addEventListener('DOMContentLoaded',getInactiveRents)
document.addEventListener('DOMContentLoaded',getAllStudents)

document.getElementById('rent_method').addEventListener('change',(event)=>{
    let table = $('#lockerTable').DataTable();
    var data = table.rows( lockerRow_list[0]).data();
    let rentTypes = document.getElementById("rent_type")
    let html = ' <option disabled selected>Select Rental Type </option>'
    
    if(event.target.value === "Rate"){
        for (let r in rentType_list[0]){
            html+= `<option value=${rentType_list[0][r].id}>${rentType_list[0][r].type}: $${rentType_list[0][r].price} Period: ${rentType_list[0][r].period_from} to ${rentType_list[0][r].period_to}</option>`
            rentType_price.set(rentType_list[0][r].id,rentType_list[0][r])
       }
    }
    else{
        for (let r in rentType_list[1]){
            if(rentType_list[1][r].type.toLowerCase().includes(data[0].locker_type.toLowerCase())){
            html+= `<option value=${rentType_list[1][r].id}>${rentType_list[1][r].type}: $${rentType_list[1][r].price} Period: ${rentType_list[1][r].period_from} to ${rentType_list[1][r].period_to}</option>`
        }
        rentType_price.set(rentType_list[1][r].id,rentType_list[1][r])
    }
    }

    rentTypes.innerHTML = html
})

document.getElementById('u_rent_method').addEventListener('change',(event)=>{
    let table = $('#rentTable').DataTable();
    var data = table.rows(actRent_list[0]).data();
    let rentTypes = document.getElementById("u_rent_type")
    html = ' <option  disabled selected>Select Rental Type </option>'
    
    if(event.target.value === "Rate"){
        for (let r in rentType_list[0]){
            html+= `<option value=${rentType_list[0][r].id}>${rentType_list[0][r].type}: $${rentType_list[0][r].price} Period: ${rentType_list[0][r].period_from} to ${rentType_list[0][r].period_to}</option>`
       }
    }
    else{
        for (let r in rentType_list[1]){
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
        for (let r in rentType_list[0]){
            html+= `<option value=${rentType_list[0][r].id}>${rentType_list[0][r].type}: $${rentType_list[0][r].price} Period: ${rentType_list[0][r].period_from} to ${rentType_list[0][r].period_to}</option>`
       }
    }
    else{
        for (let r in rentType_list[1]){
            if(rentType_list[1][r].type.toLowerCase().includes(data.locker_type.toLowerCase())){
            html+= `<option value=${rentType_list[1][r].id}>${rentType_list[1][r].type}: $${rentType_list[1][r].price} Period: ${rentType_list[1][r].period_from} to ${rentType_list[1][r].period_to}</option>`
        }
    }
    }

    rentTypes.innerHTML = html
})

document.getElementById("rent_type").addEventListener("change",(event)=>{
    let amount = document.getElementById("tL_amount")
    let id = parseInt(event.target.value)
    let rentType = rentType_price.get(id)
    amount.value = rentType.price
})

window.rentInit = rentInit
window.additionalCharge = additionalCharge
window.editRent = editRent

