# School Analytics System

**A Data-Driven School Management and Academic Performance Analytics Application**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20Application-FF4B4B?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)

## 1. Project Overview

The **School Analytics System** is a lightweight, data-driven school management and academic performance analytics application developed using Python, SQLite, Streamlit, and Pandas.

The application aims to simplify learner records management, subject administration, assessment recording, and academic performance analysis through an interactive dashboard.

It addresses common challenges associated with manual academic record management by introducing a structured digital system for storing, processing, and analyzing educational data.

The project also serves as a practical demonstration of software development, relational database management, data manipulation, and educational data analytics.

### Core Objectives

- Digitize learner registration and academic records.
- Manage school subjects and learner information.
- Record and maintain learner assessments.
- Automate assessment percentage calculations.
- Analyze individual and class academic performance.
- Generate meaningful insights from educational data.
- Support evidence-based academic decision-making.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language and application logic |
| Streamlit | Interactive web application and dashboard |
| SQLite | Relational database management |
| SQL | Database queries and data manipulation |
| Pandas | Data processing and academic analysis |
| Git | Source code management |
| GitHub | Repository hosting and project documentation |

### Technology Architecture

The application follows a modular architecture in which each technology performs a specific responsibility.

- **Python:** Handles application logic, calculations, validation, and data processing.
- **Streamlit:** Provides the interactive user interface.
- **SQLite:** Stores and manages structured academic records.
- **SQL:** Handles database operations and retrieval.
- **Pandas:** Processes and analyzes academic datasets.
- **Git and GitHub:** Support source code management and collaborative development.

## 3. Project Structure

```text
school_analytics/
│
├── app.py
├── database.py
├── school.db
├── requirements.txt
├── README.md
│
├── services/
│   ├── __init__.py
│   ├── learner_service.py
│   ├── subject_service.py
│   └── assessment_service.py
│
├── pages/
│   ├── Learners.py
│   ├── Subjects.py
│   ├── Assessments.py
│   └── Analytics.py
│
└── tests/
    └── test_services.py
```

*Note: The tests directory is a recommended extension if automated tests have not yet been implemented.*

### Directory Responsibilities

| File/Directory | Responsibility |
|---|---|
| `app.py` | Main application entry point and dashboard |
| `database.py` | Database connection, table creation, and schema management |
| `school.db` | Local SQLite database |
| `services/` | Application business logic and reusable functions |
| `pages/` | Individual Streamlit application modules |
| `requirements.txt` | Project dependencies |
| `tests/` | Automated application tests (planned) |
| `README.md` | Project documentation |

## 4. Core Application Features

### 4.1 Learner Management

The learner management module provides functionality for maintaining learner records.

Key capabilities:

- Register new learners.
- Assign unique admission numbers.
- Store learner full names.
- Record class information.
- Retrieve registered learner records.
- Maintain structured learner information.

### 4.2 Subject Management

The subject management module allows users to maintain the list of academic subjects offered by the school.

Key capabilities:

- Add new subjects.
- Retrieve available subjects.
- Prevent duplicate subject names.
- Associate subjects with learner assessments.

### 4.3 Assessment Management

The assessment module handles the recording and processing of learner academic assessments.

Key capabilities:

- Record learner assessments.
- Associate assessments with registered learners.
- Associate assessments with available subjects.
- Store assessment names and dates.
- Record achieved scores and maximum possible scores.
- Validate assessment entries.
- Calculate assessment percentages.

**Assessment percentage calculation:**

```python
percentage = (score / max_score) * 100
```

Example:

```python
score = 36
max_score = 40

percentage = (score / max_score) * 100

print(f"Performance: {percentage}%")
```

Output:

```text
Performance: 90.0%
```

### 4.4 Academic Analytics Dashboard

The analytics module is designed to transform stored assessment records into meaningful academic insights.

Planned analytical capabilities include:

- Overall academic performance summaries.
- Class performance comparisons.
- Subject performance analysis.
- Individual learner performance trends.
- Identification of academic strengths.
- Identification of learners requiring additional academic support.
- Performance comparisons across assessment periods.

## 5. Database Design

The application uses SQLite as its relational database management system.

The initial database design consists of three primary relational tables.

### 5.1 Learners Table

Stores learner registration information.

| Column | Data Type | Description |
|---|---|---|
| learner_id | INTEGER | Primary key |
| admission_no | TEXT | Unique admission number |
| full_name | TEXT | Learner's full name |
| class_name | TEXT | Learner's class |

### 5.2 Subjects Table

Stores information about available academic subjects.

| Column | Data Type | Description |
|---|---|---|
| subject_id | INTEGER | Primary key |
| subject_name | TEXT | Unique subject name |

### 5.3 Assessments Table

Stores learner assessment records.

| Column | Data Type | Description |
|---|---|---|
| assessment_id | INTEGER | Primary key |
| learner_id | INTEGER | Foreign key referencing learners |
| subject_id | INTEGER | Foreign key referencing subjects |
| assessment_name | TEXT | Assessment title |
| score | REAL | Learner's achieved score |
| max_score | REAL | Maximum possible score |
| date_taken | TEXT | Assessment date |

### 5.4 Database Relationships

The database uses relational constraints to maintain consistency between records.

- One learner can have multiple assessment records.
- One subject can appear in multiple assessment records.
- Each assessment belongs to one learner and one subject.

```text
LEARNERS
   |
   | 1
   |
   | Many
ASSESSMENTS
   |
   | Many
   |
   | 1
SUBJECTS
```

### 5.5 Data Integrity

The database and application are designed to enforce the following rules:

- Admission numbers must be unique.
- Subject names must be unique.
- Required fields cannot be empty.
- Assessment scores cannot be negative.
- Maximum assessment scores must be positive.
- Achieved scores cannot exceed maximum scores.
- Assessment records must reference valid learners and subjects.

Foreign key enforcement should be enabled on each SQLite connection.

Example:

```python
import sqlite3

def get_connection():
    conn = sqlite3.connect("school.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
```

## 6. Technical Skills Demonstrated

The project provides practical exposure to software development, database engineering, data processing, and educational data analytics.

### 6.1 Python Programming

Skills applied:

- Variables and data types.
- Functions and reusable code.
- Conditional statements and loops.
- Exception handling.
- Modular programming.
- Input validation.
- Application logic implementation.

### 6.2 Database Management and SQL

Skills applied:

- Relational database design.
- SQLite database creation and management.
- Primary and foreign key relationships.
- CRUD operations (Create, Read, Update, Delete).
- SQL queries and data retrieval.
- Database constraints.
- Data integrity management.

### 6.3 Data Analysis and Processing

Skills applied:

- Data manipulation using Pandas.
- Data filtering and aggregation.
- Calculating academic performance percentages.
- Computing learner and subject performance summaries.
- Analyzing structured educational datasets.
- Preparing data for visualization.

### 6.4 Web Application Development

Skills applied:

- Developing interactive applications using Streamlit.
- Creating data-entry forms.
- Building dashboard interfaces.
- Handling user input.
- Connecting Python applications to SQLite.
- Organizing multi-page applications.

### 6.5 Data Visualization and Reporting

Skills targeted:

- Presenting academic performance indicators.
- Comparing class and subject performance.
- Visualizing individual learner performance trends.
- Creating interactive analytical dashboards.
- Preparing structured academic reports.

### 6.6 Software Engineering Practices

Skills applied or targeted:

- Modular application architecture.
- Separation of concerns.
- Reusable service functions.
- Input validation and exception handling.
- Version control using Git.
- Project documentation using Markdown.
- Automated testing using pytest (planned).

### 6.7 Problem-Solving and Educational Technology

The project applies software engineering concepts to an educational environment through:

- Digitization of manual learner record management.
- Automation of assessment calculations.
- Structured academic data storage.
- Educational data analysis.
- Technology-supported academic decision-making.

## 7. Application Architecture and Development Workflow

The application follows a modular architecture that separates presentation, business logic, and database operations.

### Application Workflow

1. Users interact with the application through Streamlit.
2. Streamlit captures and validates user input.
3. Service modules process application requests.
4. The database module handles SQLite operations.
5. SQLite stores and retrieves academic records.
6. Pandas processes retrieved data for analysis.
7. Streamlit presents the resulting information through dashboards.

### Architectural Principles

**Separation of concerns:** Database operations, business logic, and presentation are maintained in separate modules.

**Reusability:** Common operations are implemented as reusable functions.

**Maintainability:** The modular structure makes it easier to modify individual application components.

**Scalability:** The architecture provides a foundation for future features such as reporting, authentication, and deployment.

## 8. Data Validation and Application Reliability

The application incorporates validation mechanisms to protect the accuracy and consistency of academic records.

Examples include:

| Validation Rule | Expected Behaviour |
|---|---|
| Duplicate admission number | Reject registration |
| Duplicate subject name | Reject subject entry |
| Empty required fields | Prevent submission |
| Negative assessment score | Reject assessment |
| Zero maximum score | Reject assessment |
| Score greater than maximum score | Reject assessment |
| Invalid learner reference | Reject assessment |
| Invalid subject reference | Reject assessment |

Application-level validation should be complemented by database-level constraints wherever possible.

## 9. Installation and Setup

### Prerequisites

Ensure that the following tools are installed:

- Python 3.10 or later.
- Git.
- Visual Studio Code or another code editor.
- A terminal or command-line interface.

### Step 1: Clone the Repository

```bash
git clone <repository-url>
```

Navigate into the project directory:

```bash
cd school_analytics
```

Replace `<repository-url>` with the actual GitHub repository URL.

### Step 2: Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Linux/macOS:

```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

Windows Git Bash:

```bash
source venv/Scripts/activate
```

Windows Command Prompt:

```cmd
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

If the requirements file has not yet been created:

```bash
pip install streamlit pandas
```

SQLite is included in Python's standard library.

### Step 5: Initialize the Database

```bash
python database.py
```

This should create the database and initialize the required tables if the database initialization logic is implemented in `database.py`.

### Step 6: Run the Application

```bash
streamlit run app.py
```

Open the local application URL displayed in your terminal.

Default address:

```text
http://localhost:8501
```

## 10. Development and Testing

The application should be tested to ensure that its database operations, calculations, and user interactions behave as expected.

### Recommended Testing Areas

**Learner Management**
- Test learner registration.
- Test duplicate admission numbers.
- Test retrieval of learner records.

**Subject Management**
- Test subject registration.
- Test duplicate subject prevention.
- Test subject retrieval.

**Assessment Management**
- Test valid assessment registration.
- Test assessment percentage calculations.
- Test invalid scores.
- Test invalid learner and subject references.

### Recommended Testing Framework

`pytest` can be introduced for automated testing.

Install:

```bash
pip install pytest
```

Run tests:

```bash
pytest
```

*Automated testing is a recommended development milestone and should only be described as implemented after test cases have been written and executed.*

## 11. Future Development Roadmap

The project will evolve from a basic school records management application into a more comprehensive academic analytics platform.

| Phase | Planned Development |
|---|---|
| Phase 1 | Learner registration and management |
| Phase 2 | Subject management |
| Phase 3 | Assessment recording and validation |
| Phase 4 | Academic analytics dashboard |
| Phase 5 | Individual learner performance reports |
| Phase 6 | PDF and Excel report generation |
| Phase 7 | User authentication and role-based access |
| Phase 8 | Automated testing and application optimization |
| Phase 9 | Cloud deployment and database backups |
| Phase 10 | Advanced educational data analytics and machine learning |

### Future Data Science Integration

A major direction for the project is integrating data science techniques into educational analytics.

Potential applications include:

**Descriptive Analytics**
- Calculate average learner performance.
- Compare class and subject performance.
- Summarize academic assessment records.

**Diagnostic Analytics**
- Identify subjects where learners experience difficulties.
- Investigate patterns in academic performance.
- Identify areas requiring targeted academic intervention.

**Predictive Analytics**
- Explore historical assessment trends.
- Investigate whether previous performance patterns can help identify learners who may need additional academic support.

**Prescriptive Analytics**
- Generate evidence-based recommendations for academic interventions.
- Support teachers in planning targeted learning activities.

Any predictive functionality will require sufficient, representative data and appropriate model evaluation. Predictions should support, not replace, professional teacher judgement.

## 12. Security, Privacy and Data Protection

Since the application handles educational records, future production deployment must consider data protection and responsible information management.

Planned improvements include:

- User authentication.
- Role-based access control.
- Secure handling of learner information.
- Database backup and recovery mechanisms.
- Protection against unauthorized access.
- Appropriate data retention policies.

Real learner information should not be committed to a public GitHub repository.

The local database file should be excluded from version control when it contains personal or confidential information.

Recommended `.gitignore` entries:

```gitignore
venv/
__pycache__/
*.pyc
.env
school.db
.pytest_cache/
.streamlit/secrets.toml
```

## 13. Contributing

Contributions, suggestions, and improvements are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Test your changes.
5. Commit your work.
6. Submit a pull request.

Example:

```bash
git checkout -b feature/academic-analytics
```

Commit changes:

```bash
git add .
git commit -m "Add academic analytics functionality"
```

Push your branch:

```bash
git push origin feature/academic-analytics
```

## 14. License

This project is currently under active development.

Licensing terms will be established before public distribution.

## 15. Project Information

| Attribute | Details |
|---|---|
| Project | School Analytics System |
| Category | Educational Technology / Data Analytics |
| Programming Language | Python |
| Database | SQLite |
| User Interface | Streamlit |
| Data Processing | Pandas |
| Version Control | Git and GitHub |
| Development Status | Active Development |

## 16. Author and Project Vision

**School Analytics System** is a practical software development project exploring the intersection of education, software engineering, and data analytics.

Its long-term vision is to demonstrate how accessible technologies can simplify school administration, improve academic data management, and support evidence-based teaching and learning.

**Built with Python, SQLite, Streamlit.**

---

*Learn. Build. Test. Improve.*