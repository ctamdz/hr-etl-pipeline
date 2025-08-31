import pandas as pd
import sqlite3
import pymysql
from sqlalchemy import create_engine
import requests
import os

# EXTRACT - Đọc dữ liệu từ các nguồn

# 1. Đọc dữ liệu từ Google Sheets
google_sheet_id = '1VCkHwBjJGRJ21asd9pxW4_0z2PWuKhbLR3gUHm-p4GI'
url = 'https://docs.google.com/spreadsheets/d/' + google_sheet_id + '/export?format=xlsx'
df_enrollies_data = pd.read_excel(url)

# 2. Đọc file Excel - tự động tải nếu cần
excel_filename = 'enrollies_education.xlsx'
if not os.path.exists(excel_filename):
    # Thay URL này bằng link download thật
    excel_url = "https://example.com/enrollies_education.xlsx"  
    print(f"Tải {excel_filename}...")
    response = requests.get(excel_url)
    with open(excel_filename, 'wb') as f:
        f.write(response.content)

df_enrollies_education = pd.read_excel(excel_filename)

# 3. Đọc file CSV - tự động tải nếu cần  
csv_filename = 'work_experience.csv'
if not os.path.exists(csv_filename):
    # Thay URL này bằng link download thật
    csv_url = "https://example.com/work_experience.csv"
    print(f"Tải {csv_filename}...")
    response = requests.get(csv_url)
    with open(csv_filename, 'wb') as f:
        f.write(response.content)

df_work_experience = pd.read_csv(csv_filename)

# 4. Đọc từ MySQL database
engine = create_engine('mysql+pymysql://etl_practice:550814@112.213.86.31:3360/company_course')
df_training_hours = pd.read_sql_table('training_hours', con=engine)
df_employment = pd.read_sql_table('employment', con=engine)

# 5. Đọc từ web table
tables = pd.read_html('https://sca-programming-school.github.io/city_development_index/index.html')
df_city_development_index = tables[0]

# TRANSFORM - Làm sạch dữ liệu

# Xử lý enrollies_data
df_enrollies_data = df_enrollies_data.drop_duplicates()
df_enrollies_data = df_enrollies_data.fillna({'gender': 'Unknown'})
df_enrollies_data['full_name'] = df_enrollies_data['full_name'].astype('string')
df_enrollies_data['city'] = df_enrollies_data['city'].astype('category')
df_enrollies_data['gender'] = df_enrollies_data['gender'].astype('category')

# Xử lý enrollies_education
df_enrollies_education = df_enrollies_education.drop_duplicates()
df_enrollies_education = df_enrollies_education.fillna({
    'enrolled_university': 'Unknown',
    'education_level': 'Unknown', 
    'major_discipline': 'Unknown'
})
df_enrollies_education['enrolled_university'] = df_enrollies_education['enrolled_university'].astype('category')
df_enrollies_education['education_level'] = df_enrollies_education['education_level'].astype('category')
df_enrollies_education['major_discipline'] = df_enrollies_education['major_discipline'].astype('category')

# Xử lý work_experience
df_work_experience = df_work_experience.drop_duplicates()
df_work_experience = df_work_experience.fillna({
    'experience': 'Unknown',
    'company_size': 'Unknown',
    'company_type': 'Unknown',
    'last_new_job': 'Unknown'
})
df_work_experience['relevent_experience'] = df_work_experience['relevent_experience'].astype('category')
df_work_experience['experience'] = df_work_experience['experience'].astype('category')
df_work_experience['company_size'] = df_work_experience['company_size'].astype('category')
df_work_experience['company_type'] = df_work_experience['company_type'].astype('category')
df_work_experience['last_new_job'] = df_work_experience['last_new_job'].astype('category')

# Xử lý training_hours
df_training_hours = df_training_hours.drop_duplicates()

# LOAD - Lưu vào SQLite database
conn = sqlite3.connect('hr_enrollies_data.db')

df_enrollies_data.to_sql('enrollies_data', conn, if_exists='replace', index=False)
df_enrollies_education.to_sql('enrollies_education', conn, if_exists='replace', index=False)
df_work_experience.to_sql('work_experience', conn, if_exists='replace', index=False)
df_training_hours.to_sql('training_hours', conn, if_exists='replace', index=False)
df_employment.to_sql('employment', conn, if_exists='replace', index=False)
df_city_development_index.to_sql('city_development_index', conn, if_exists='replace', index=False)

conn.close()

print("ETL hoàn thành!")