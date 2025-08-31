# HR Enrollees ETL Pipeline

## About This Project

This project implements a comprehensive ETL (Extract, Transform, Load) pipeline for processing HR enrollees data from multiple heterogeneous data sources. The pipeline automates the process of collecting, cleaning, and consolidating employee enrollment data for analytics and reporting purposes.

The system is designed to handle real-world data challenges including missing values, duplicate records, and inconsistent data formats across different sources.

## Data Sources

Our ETL pipeline processes data from 6 different sources:

### 1. **Google Sheets** - Primary Enrollees Data
- **Source**: Google Sheets API (Sheet ID: 1VCkHwBjJGRJ21asd9pxW4_0z2PWuKhbLR3gUHm-p4GI)
- **Content**: Basic enrollee information (enrollee_id, full_name, city, gender)
- **Records**: ~19,158 entries

### 2. **Excel File** - Education Data
- **Source**: `enrollies_education.xlsx` (auto-downloaded if not present)
- **Content**: Educational background (enrollee_id, enrolled_university, education_level, major_discipline)
- **Records**: ~19,158 entries

### 3. **CSV File** - Work Experience Data  
- **Source**: `work_experience.csv` (auto-downloaded if not present)
- **Content**: Professional experience (enrollee_id, relevant_experience, experience, company_size, company_type, last_new_job)
- **Records**: ~19,158 entries

### 4. **MySQL Database** - Training & Employment Data
- **Source**: Remote MySQL server (112.213.86.31:3360/company_course)
- **Tables**: 
  - `training_hours`: Training completion data
  - `employment`: Employment status and targets
- **Records**: ~19,158 entries each

### 5. **Web Table** - City Development Index
- **Source**: HTML table from https://sca-programming-school.github.io/city_development_index/
- **Content**: City development metrics for location-based analytics
- **Records**: 123 cities

## ETL Process Description

### EXTRACT Phase

**Decision Rationale**: We chose to support multiple data source types to demonstrate real-world ETL scenarios where data comes from various systems.

1. **Google Sheets**: Direct API access using pandas read_excel with export URL
2. **File Downloads**: Automatic download mechanism to ensure latest data availability
3. **Database Connection**: SQLAlchemy engine for robust MySQL connectivity
4. **Web Scraping**: pandas read_html for structured web table extraction

### TRANSFORM Phase

#### Data Cleaning Decisions:

**1. Duplicate Removal**
```python
df = df.drop_duplicates()
```
**Why**: Data from multiple sources often contains duplicate records. We remove duplicates to ensure data integrity and prevent skewed analytics.

**2. Missing Value Handling**
```python
df = df.fillna({'column': 'Unknown'})
```
**Why**: We chose "Unknown" over dropping records because:
- Preserves sample size for statistical analysis
- Maintains referential integrity across related tables
- Provides explicit indication of missing data for business users

**3. Data Type Optimization**
```python
df['column'] = df['column'].astype('category')
```
**Why**: 
- **Memory Efficiency**: Category dtype reduces memory usage by 70-80% for repetitive string data
- **Performance**: Faster operations on categorical data
- **Analytics**: Better support for groupby operations and statistical analysis

**4. String Optimization**
```python
df['full_name'] = df['full_name'].astype('string')
```
**Why**: Pandas string dtype is more memory-efficient and provides better string operations than object dtype.

### LOAD Phase

**SQLite Database Selection**
- **Portability**: Single file database, easy to share and deploy
- **No Dependencies**: No server setup required
- **Performance**: Sufficient for analytical workloads up to millions of records
- **Compatibility**: Widely supported across platforms and tools

## Installation & Usage

### Prerequisites
```bash
pip install pandas pymysql sqlalchemy requests openpyxl lxml
```

### Configuration
Update the download URLs in `etl.py`:
```python
# Line 21
excel_url = "YOUR_EXCEL_FILE_URL"
# Line 30  
csv_url = "YOUR_CSV_FILE_URL"
```

### Running the Pipeline
```bash
python etl.py
```

### Output
The pipeline creates `hr_enrollies_data.db` with 6 tables:
- `enrollies_data` - Basic enrollee information
- `enrollies_education` - Educational background
- `work_experience` - Professional experience  
- `training_hours` - Training completion data
- `employment` - Employment status
- `city_development_index` - City metrics

## Scheduling Instructions

### Option 1: Windows Task Scheduler

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`

2. **Create Basic Task**
   - Right-click "Task Scheduler Library" → "Create Basic Task"
   - Name: "HR ETL Pipeline"
   - Description: "Daily HR data processing"

3. **Set Trigger**
   - Choose "Daily"
   - Set start date and time (recommended: early morning, e.g., 6:00 AM)
   - Recur every 1 day

4. **Set Action**
   - Choose "Start a program"
   - Program: `python.exe` (full path, e.g., `C:\Python39\python.exe`)
   - Arguments: `etl.py`
   - Start in: Your project directory path

5. **Configure Conditions**
   - Uncheck "Start the task only if the computer is on AC power"
   - Check "Wake the computer to run this task"
