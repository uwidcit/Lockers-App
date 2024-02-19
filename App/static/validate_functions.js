const is_empty = result => result === '' ? true : false
const is_between = (result,min,max) => result < min || result > max ? false:  true
const isNotNumber = result => /\D/g.test(result)
const is_validDate = date => {
    let test_date = new Date(date)
    if (isNaN(test_date))
        return false
    return true
}


export {is_empty,is_between,isNotNumber,is_validDate}