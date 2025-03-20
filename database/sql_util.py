from sqlalchemy import create_engine, MetaData, Table, select, and_
from sqlalchemy.orm import sessionmaker
import pymysql
import pandas as pd
# 创建数据库连接
engine = create_engine('mysql+pymysql://qa:123456@10.10.64.36/QADB')
metadata = MetaData()
# metadata.create_all(engine)
def get_table(table_name):
    return Table(table_name, metadata, autoload_with=engine)

def get_session():
    return  sessionmaker(bind=engine)()

def get_data(session, tableName, columns, conditions=None):
    
    table = get_table(tableName)
    # 确保columns是列表
    if isinstance(columns, str):
        columns = [columns]
    
    # 构建select中的列
    select_columns = [table.c[col] for col in columns]
    
    # 创建查询
    query = select(*select_columns)
    
    # 添加条件
    if conditions:
        if isinstance(conditions, list):
            conditions = [table.c[col] == value for col, value in conditions]
            query = query.where(and_(*conditions))
        else:
            conditions = table.c[conditions[0]] == conditions[1]
            query = query.where(conditions)
    
    return session.execute(query).fetchall()


if __name__ == '__main__':
    pass