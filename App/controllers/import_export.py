from datetime import datetime
import pandas as pd
import io
from App.models import *
from sqlalchemy import Sequence
from App.models.rentTypes import Types as RType
from App.controllers import (
    new_masterkey,
    new_key,
    restore_keyHistory,
    restore_area,
    add_new_student,
    restore_locker,
    import_verified_rent,
    init_amount_owed,
    restore_rentType,
    create_comment,
    restore_transaction
)

model_list = [
    Student,
    Rent,
    Locker,
    Area,
    MasterKey,
    Key,
    TransactionLog,
    KeyHistory,
    Notes,
    RentTypes
]

def export_all():
    buffer = io.BytesIO()
    data_frame = {}
    data_f = []
    d_head= []

    for m in model_list:
        query_list = [r.toJSON() for r in m.query.all()]
        data_frame[m.__tablename__] = query_list

    for d in data_frame:
        data_f.append(pd.DataFrame(data_frame[d]))
        d_head.append(d)
    
    with pd.ExcelWriter(buffer, engine='xlsxwriter',mode="w") as writer:
        index = 0
        for i in range(0,len(data_f)):
            data_f[i].to_excel(writer, sheet_name=d_head[index], startrow=1, header=False, index=False)
            workbook = writer.book
            worksheet = writer.sheets[d_head[index]]
            (max_row, max_col) = data_f[i].shape
            column_settings = []
            for header in data_f[i].columns:
                column_settings.append({'header': header})
            worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
            index = index+1
    buffer.seek(0)
    return buffer

def import_all(uploaded_file):
    import_masterkey(uploaded_file)
    import_key(uploaded_file)
    import_area(uploaded_file)
    import_student(uploaded_file)
    import_locker(uploaded_file)
    import_keyHistory(uploaded_file)
    import_rentTypes(uploaded_file)
    import_rent(uploaded_file)
    import_notes(uploaded_file)
    import_transactionLog(uploaded_file)
    
def import_masterkey(uploaded_file):
    reader = pd.read_excel(uploaded_file,"masterkey")
    masterkey_json = reader.to_dict('records')
    for m in masterkey_json:
        new_masterkey(m['masterkey_id'],m['series'],m['key_type'],datetime.strptime(m['date_added'],'%Y-%m-%d'))
    return True
    

def import_key(uploaded_file):
    reader = pd.read_excel(uploaded_file,"locker_keys_table")
    key_json = reader.to_dict('records')
    for k in key_json:
        new_key(k['key_id'],k['masterkey_id'],k['key_status'],datetime.strptime(k['date_added'],'%Y-%m-%d'))
    return True

def import_area(uploaded_file):
    reader = pd.read_excel(uploaded_file,"area")
    area_json = reader.to_dict('records')
    for a in area_json:
        restore_area(a['id'],a["description"], a['longitude'], a['latitude'])
    
    seq = Sequence(name='area_id_seq')
    key = db.session.execute(seq)
    
    while (key < area_json[len(area_json)-1]['id']):
        key = db.session.execute(seq)
    
    return True

def import_student(uploaded_file):
    reader = pd.read_excel(uploaded_file,"student")
    student_json = reader.to_dict('records')
    for s in student_json:
        if len(str(s['faculty'])) > 3:
            s['faculty'] = str(s['faculty'])[0:2].upper()
        add_new_student(s['student_id'], s['first_name'], s['last_name'], s['faculty'], s['phone_number'],s['email'])
    return True


def import_locker(uploaded_file):
    reader = pd.read_excel(uploaded_file,"locker")
    
    locker_json = reader.to_dict('records')
    for l in locker_json:
        if l['status'] == 'Rented':
            restore_locker(l['locker_code'], l['locker_type'],'Free',l['area'])
        else:
            restore_locker(l['locker_code'], l['locker_type'],l['status'],l['area'])
       
    return True

def import_keyHistory(uploaded_file):
    reader = pd.read_excel(uploaded_file,"key_history")
    seq = Sequence(name='key_history_id_seq')
    keyH_json = reader.to_dict('records')
    for kh in keyH_json:
        k = restore_keyHistory(kh['id'],kh['key_id'], kh['locker_id'],kh['date_moved'])
    key = db.session.execute(seq)
    
    while (key < keyH_json[len(keyH_json)-1]['id']):
        key = db.session.execute(seq)

    return True

def import_rentTypes(uploaded_file):
    reader = pd.read_excel(uploaded_file,"rental_types")
    rentTypes_json = reader.to_dict('records')
    for rT in rentTypes_json:
        for r in RType.__members__:
            if (rT['type'] == RType[r].value):
                 rT['type'] = RType[r].name
        restore_rentType(rT['id'],datetime.strptime(rT['period_from'],'%Y-%m-%d'),datetime.strptime(rT['period_to'],'%Y-%m-%d'),rT['type'],rT['price'])
    seq = Sequence(name='rental_types_id_seq')
    key = db.session.execute(seq)
    
    while (key < rentTypes_json[len(rentTypes_json)-1]['id']):
        key = db.session.execute(seq)
    
    return True

def import_rent(uploaded_file):
    reader = pd.read_excel(uploaded_file,"rent")
    rent_json = reader.to_dict('records')
    r_dfrom= None
    r_dto= None
    d_return = None
    for r in rent_json:
        try:
            r_dfrom = datetime.strptime(r['rent_date_to'],'%Y-%m-%d %H:%M:%S')
            r_dto = datetime.strptime(r['rent_date_from'],'%Y-%m-%d %H:%M:%S')
            d_return = datetime.strptime(r['date_returned'],'%Y-%m-%d %H:%M:%S')
        except:
            d_return = None
        amount_owed = init_amount_owed(r['rent_type'],r_dfrom,r_dto)
        import_verified_rent(r['id'],r['student_id'],r['keyHistory_id'], r['rent_type'],r_dfrom,r_dto,amount_owed,r['status'],d_return,r['rent_method'],r['additional_fees'], r['late_fees'])
    seq = Sequence(name='rent_id_seq')
    key = db.session.execute(seq)
    
    while (key < rent_json[len(rent_json)-1]['id']):
        key = db.session.execute(seq)
        return True

def import_notes(uploaded_file):
    reader = pd.read_excel(uploaded_file,"notes")
    notes_json = reader.to_dict('records')
    for n in notes_json:
        if type(n['date_created']) is not datetime:
            d_cre = datetime.strptime(n['date_created'],'%Y-%m-%d')
        else:
            d_cre = n['date_created']
        create_comment(n['rent_id'],n['comment'],d_cre)
        return True
    return True

def import_transactionLog(uploaded_file):
    reader = pd.read_excel(uploaded_file,"transaction_log")
    tLog_json = reader.to_dict('records')
    for tL in tLog_json:
        try:
            tL['transaction_date'] = datetime.strptime(tL['transaction_date'],'%Y-%m-%d')
        except:
            print('Invalid date conversation')
        restore_transaction(tL['id'],tL['rent_id'], tL['currency'],tL['transaction_date'], tL['amount'], tL['description'], tL['type'], tL['receipt_number'])
    seq = Sequence(name='transaction_log_id_seq')
    key = db.session.execute(seq)
    
    while (key < tLog_json[len(tLog_json)-1]['id']):
        key = db.session.execute(seq)

    return True

        



