from datetime import datetime
from database import db
import enum
import pandas as pd
import io
import uuid
from models import *

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
    writer.close()
    return buffer




