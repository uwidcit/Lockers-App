import { is_empty,is_between } from "./validate_functions.js"

function locker_code_validate(input,form){
    if (is_empty(input)){
        form['locker_code'].classList.add('invalid')
        document.getElementById('newLockerID_helper').dataset.error ="Locker ID cannot be empty"
        return false
    }
    else if (!is_between(input.length,1,25)){
        form['locker_code'].classList.add('invalid')
        document.getElementById('newLocker_helper').dataset.error ="Locker ID cannot exceed 25 characters"
        return false
    }
    form['locker_type'].classList.remove('invalid')
    return true
}

function locker_type_validate(input,form){
    if (is_empty(input)){
        form['locker_type'].classList.add('dropdown_invalid')
        return false
    }
    else if (!is_between(input.length,1,25)){
        form['locker_type'].classList.add('dropdown_invalid')
        return false
    }
    form['locker_type'].classList.remove('dropdown_invalid')
    return true
}

function status_validate(input,form){
    if (is_empty(input)){
        form['area'].classList.add('dropdown_invalid')
        return false
    }
    else if (!is_between(input.length,1,25)){
        form['area'].classList.add('dropdown_invalid')
        return false
    }
    form['area'].classList.remove('dropdown_invalid')
    return true
}

function key_validate(input,form){
    if (!is_empty(input)){
        if (!is_between(input.length,1,10)){
            form['key'].classList.add('invalid')
            document.getElementById('newKey_helper').dataset.error ="Key ID to long"
            return false
        }
    }
    form['key'].classList.remove('invalid')
    return true
}

function area_validate(input,form){
    if (is_empty(input)){
        form['area'].classList.add('dropdown_invalid')
        return false
    }
    else if (!is_between(input.length,1,25)){
        form['area'].classList.add('dropdown_invalid')
        return false
    }
    return true
}

function locker_validate(data,form){
    let test_locker_code = locker_code_validate(data["locker_code"],form),
        test_area = area_validate(data["area"],form),
        test_locker_type = locker_type_validate(data["locker_type"],form),
        test_status = status_validate(data["status"],form),
        test_key = key_validate(data["key"],form)

        return test_locker_code && test_locker_type
        && test_area && test_status && test_key
}

function lockerEdit_validate(data,form){
    let test_locker_code = locker_code_validate(data["locker_code"],form,),
        test_area = area_validate(data["area"],form),
        test_locker_type = locker_type_validate(data["locker_type"],form),
        test_status = status_validate(data["status"],form),
        test_key = key_validate(data["key"],form,"edit")

        return test_locker_code && test_locker_type
        && test_area && test_status && test_key
}



export {locker_validate,lockerEdit_validate}

