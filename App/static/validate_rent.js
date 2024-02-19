import { is_empty, isNotNumber,is_validDate, is_between } from "./validate_functions.js"

function student_validate(input,form){
    if (is_empty(input)){
        form['student_id'].classList.add('invalid')
        document.getElementById('student_helper').data_error = "Student ID cannot be null"
        return false
    }
    else if (!is_between(input.length,1,20)){
        form['student_id'].classList.add('invalid')
        document.getElementById('student_helper').data_error ='Student ID cannot exceed 18 characters'
        return false
    }
    form['student_id'].classList.add('valid')
    return true
}

function rent_datefrom_validate(input,form,mode){
    let element;
    if (mode === "create"){
        element = document.getElementById('dfrom_helper')
    }
    else if (mode === "edit"){
        element = document.getElementById('u_dfrom_helper')
    }
    else{
        alert("Validate function missing mode")
        return false
    }
    if (is_empty(input)){
        form['rent_date_from'].classList.add('invalid')
        element.dataset.error = "Date From cannot be empty"
        return false
    }

    else if (!is_validDate(input)) {
        form['rent_date_from'].classList.add('invalid')
        element.dataset.error = "Date From: "+input+" is invalid"
        return false
    }

    form['rent_date_from'].classList.add('valid')

    return true
}

function rent_dateto_validate(input,form,mode){
    let element;
    if (mode === "create"){
        element = document.getElementById('dto_helper')
    }
    else if (mode === "edit"){
        element = document.getElementById('u_dto_helper')
    }
    else{
        alert("Validate function missing mode")
        return false
    }
    if (is_empty(input)){
        form['rent_date_to'].classList.add('invalid')
        element.dataset.error = "Date To cannot be empty"
        return false
    }
    
    else if (!is_validDate(input)) {
        form['rent_date_to'].classList.add('invalid')
        element.dataset.error = "Date To: "+input+" is invalid"
        return false
    }

    form['rent_date_to'].classList.add('invalid')
    return true

}

function rent_datereturn_validate(input,form,mode){
     let element;
    if (mode === "create"){
        element = document.getElementById('dreturn_helper')
    }
    else if (mode === "edit"){
        element = document.getElementById('u_dreturn_helper')
    }
    else{
        alert("Validate function missing mode")
        return false
    }
    if (!is_empty(input)){
        if (!is_validDate(input)) {
            form['date_returned'].classList.add('invalid')
            element.dataset.error = "Date Returned: "+input+" is invalid"
         return false
     }
    }
    form['date_returned'].classList.add('valid')
    
     return true
}

function currency_validate(input,form){
    if (is_empty(input)){
        form['currency'].classList.add('invalid')
        document.getElementById('currency_helper').dataset.error = "Currency cannot be empty"
      return false 
    }
    else if (!is_between(input.length,1,3)){
        form['currency'].classList.add('invalid')
        document.getElementById('currency_helper').dataset.error ='Currency can only be 3 characters long'
        return false
    }
    form['currency'].classList.add('valid')
    return true 
}
function amount_validate(input,form){
    if(isNotNumber(input)){
        form['amount'].classList.add('invalid')
        document.getElementById('amount_helper').dataset.error = 'Amount contains letter(s)'
        return false
    }
    else if (is_empty(input)){
        form['amount'].classList.add('invalid')
        document.getElementById('amount_helper').dataset.error = 'Enter an amount'
        return false
    }
    else if(!is_between(input.length,1,15)){
        form['amount'].classList.add('invalid')
        document.getElementById('amount_helper').dataset.error = 'Invalid amount'
        return false
    }
    form['amount'].classList.add('valid')
    return true
}
function transaction_date_validate(input,form){
    if (is_empty(input)){
        form['transaction_date'].classList.add('invalid')
        document.getElementById('transaction_helper').dataset.error ="Transaction Date to cannot be empty"
        return false
    }
    
    else if (!is_validDate(input)) {
        form['transaction_date'].classList.add('invalid')
        document.getElementById('transaction_helper').dataset.error = "Transaction Date: "+input+" is not a valid Date"
        return false
    }
    form['transaction_date'].classList.add('valid')
    return true
}

function rent_method_validate(input,form){
    if (is_empty(input)){
        form['rent_method'].classList.add('dropdown_invalid')
        return false
    }
    else if (!(input === "Fixed" || input === "Rate")){
        form['rent_method'].classList.add('dropdown_invalid')
        return false
    }

    form['rent_method'].classList.remove('dropdown_invalid')
    return true
}

function rent_type_validate(input,form){
    if (is_empty(input)){
        form['rent_type'].classList.add('dropdown_invalid')
        return false
    }
    else if (isNotNumber(input)){
        form['rent_type'].classList.add('dropdown_invalid')
        return false
    }
    form['rent_type'].classList.remove('dropdown_invalid')

    return true
}

function validate_transactionType(input,form){
    if(is_empty(input)){
        form['t_type'].classList.add('dropdown_invalid')
        return false
    }
    else if(!(input === "credit" || input === "debit")){
        form['t_type'].classList.add('dropdown_invalid')
        return false
    }
    return true
}


function additional_fees_validate(input,form){
    if(isNotNumber(input)){
        form['u_add_fee'].classList.add('invalid')
        document.getElementById('u_addfee_helper').dataset.error = 'Amount contains letter(s)'
        return false
    }
    else if (is_empty(input)){
        form['u_add_fee'].classList.add('invalid')
        document.getElementById('u_addfee_helper').dataset.error = 'Enter an amount'
        return false
    }
    else if(!is_between(input.length,1,15)){
        form['u_add_fee'].classList.add('invalid')
        document.getElementById('u_addfee_helper').dataset.error = 'Invalid amount'
        return false
    }
    form['u_add_fee'].classList.add('valid')
    return true
}

function late_fees_validate(input,form){
    if(isNotNumber(input)){
        form['u_late_fee'].classList.add('invalid')
        document.getElementById('u_latefee_helper').dataset.error = 'Amount contains letter(s)'
        return false
    }
    else if (is_empty(input)){
        form['u_late_fee'].classList.add('invalid')
        document.getElementById('u_latefee_helper').dataset.error = 'Enter an amount'
        return false
    }
    else if(!is_between(input.length,1,15)){
        form['u_late_fee'].classList.add('invalid')
        document.getElementById('u_latefee_helper').dataset.error = 'Invalid amount'
        return false
    }
    form['u_late_fee'].classList.add('valid')
    return true
}

function additionalChargesValidate(input,form){
    if (is_empty(input)){
        form['rentType'].classList.add('dropdown_invalid')
        return false
    }
    else if (isNotNumber(input)){
        form['rentType'].classList.add('dropdown_invalid')
        return false
    }
    form['rentType'].classList.remove('dropdown_invalid')

    return true
}

function rentIDValidate(input,form){
    if (is_empty(input)){
        return false
    }
    else if (isNotNumber(input)){
        return false
    }
    return true
}


function rentValidate(data,form,form_transaction){
    let test_student = student_validate(data["student_id"],form),
        test_rentMethod = rent_method_validate(data["rentMethod"],form),
        test_rentType = rent_type_validate(data["rentType"],form),
        test_rentFrom = rent_datefrom_validate(data["rent_date_from"],form,"create"),
        test_rentTo = rent_dateto_validate(data["rent_date_to"],form,"create"),
        test_date_return = rent_datereturn_validate(data["date_returned"],form,"create"),
        test_currency = currency_validate(data["currency"],form_transaction),
        test_amount = amount_validate(data["amount"],form_transaction),
        test_transactionDate = transaction_date_validate(data["t_date"],form_transaction),
        test_trasactionType = validate_transactionType(data["t_type"],form_transaction)

        return test_student && test_rentMethod && test_rentType && test_rentFrom && test_rentTo &&
        test_date_return && test_currency && test_amount && test_transactionDate && test_trasactionType
}

function rentEditValidate(data,form){
        let test_rentMethod = rent_method_validate(data["rentMethod"],form),
        test_rentType = rent_type_validate(data["rentType"], form),
        test_rentFrom = rent_datefrom_validate(data["rent_date_from"],form,"edit"),
        test_rentTo = rent_dateto_validate(data["rent_date_to"],form,"edit"),
        test_date_return = rent_datereturn_validate(data["date_returned"],form,"edit"),
        test_additional_fees = additional_fees_validate(data["additional_fees"],form),
        test_late_fees = late_fees_validate(data["late_fees"],form)

        return test_rentMethod && test_rentType && test_rentFrom && test_rentTo
        && test_date_return && test_additional_fees && test_late_fees
}

function additionalChargeValidate(data,form){
    let test_rentID = rentIDValidate(data["rent_id"],form),
        test_rentType = additionalChargesValidate(data["rentType"],form)

        return test_rentID && test_rentType
}

export {rentValidate,rentEditValidate,additionalChargeValidate};