import streamlit as st
import mysql.connector
import pandas as pd
import datetime

###################################################################

# Function to connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="mysql",
        user="Bikey",
        password="Lifegood@7776",
        database="admin"
    )

###################################################################


###################################################################

# Function to create a table to store FACULTY details if not exists
def create_faculty_table(cursor):
   cursor.execute("CREATE TABLE IF NOT EXISTS faculty_details (FACULTY_ID VARCHAR(255) PRIMARY KEY, FACULTY_NAME VARCHAR(255), COURSE VARCHAR(255), "
                   "INSTITUTE VARCHAR(255))")


# Function to insert FACULTY details into the database
def insert_faculty_details(cursor, FACULTY_ID, FACULTY_NAME, COURSE, INSTITUTE):
    query = "INSERT INTO faculty_details (FACULTY_ID, FACULTY_NAME, COURSE, INSTITUTE) VALUES (%s, %s, %s, %s)"
    values = (FACULTY_ID, FACULTY_NAME, COURSE, INSTITUTE)
    cursor.execute(query, values)   


# Function to get unique FACULTY REG ID from the database
def get_unique_faculty(cursor):
    cursor.execute("SELECT DISTINCT FACULTY_ID FROM faculty_details")
    return [row[0] for row in cursor.fetchall()]


# Function to get FACULTY details for a specific FACULTY REG ID
def get_faculty_details_for_FACULTY_ID(cursor, FACULTY_ID):
    query = "SELECT FACULTY_NAME,COURSE, INSTITUTE FROM faculty_details WHERE FACULTY_ID = %s"
    cursor.execute(query, (FACULTY_ID,))
    return cursor.fetchall()

###################################################################


###################################################################
###################################################################

# Streamlit app for FACULTY data entry
def faculty_data_entry_page():
    st.title("FACULTY DATA ENTRY")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Input fields for FACULTY details
    FACULTY_ID = st.text_input("REGISTRATION ID :")
    FACULTY_NAME = st.text_input("NAME OF FACULTY :")
    COURSE = st.text_input("COURSE NAME :")
    INSTITUTE = st.text_input("FACULTY INSTITUTE NAME :")



    # Submit button
    if st.button("Submit"):
        # Validate inputs
        if FACULTY_ID and FACULTY_NAME and COURSE and INSTITUTE :
            # Create the faculty_details table if not exists
            create_faculty_table(cursor)

            # Check for duplicate FACULTY REG ID
            if FACULTY_id_exists(cursor, FACULTY_ID):
                st.warning("This  Faculty ID already exists. Please choose a different Faculty ID.")
            else:
                # Insert FACULTY details into the database
                insert_faculty_details(cursor, FACULTY_ID, FACULTY_NAME, COURSE, INSTITUTE)

                # Commit changes
                db_connection.commit()

                st.success("FACULTY details added successfully.")
        else:
            st.warning("Please enter all details.")

    # Close the database connection
    db_connection.close()

###################################################################
###################################################################


###################################################################

# Function to check if a FACULTY REG ID already exists
def FACULTY_id_exists(cursor, FACULTY_ID):
    query = "SELECT COUNT(*) FROM faculty_details WHERE FACULTY_ID = %s"
    cursor.execute(query, (FACULTY_ID,))
    count = cursor.fetchone()[0]
    return count > 0


###################################################################


###################################################################
###################################################################

# Streamlit app for listing FACULTY details
def list_faculty_details_page():
    st.title("ALL FACULTY DETAILS")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Display details for all FACULTY REG ID
    all_faculty_details = get_all_faculty_details(cursor)

    for FACULTY_detail in all_faculty_details:
        FACULTY_ID, FACULTY_NAME,COURSE, INSTITUTE = FACULTY_detail
        st.subheader(f"Details for FACULTY ID: {FACULTY_ID}")
        details_df = pd.DataFrame({"FACULTY NAME":[FACULTY_NAME], "COURSE NAME": [COURSE], "INSTITUTE NAME": [INSTITUTE]})
        st.table(details_df)
        st.markdown("---")  # Add a horizontal line to separate details for different hostnames

    # Close the database connection
    db_connection.close()

###################################################################
###################################################################

###################################################################


# Function to get FACULTY details for all FACULTY ID
def get_all_faculty_details(cursor):
    query = "SELECT FACULTY_ID, FACULTY_NAME, COURSE, INSTITUTE FROM faculty_details"
    cursor.execute(query)
    return cursor.fetchall()    

###################################################################

###################################################################
###################################################################

# Streamlit app for displaying student details based on course
def student_details_by_course_page():
    st.title("Student Details by Course")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Input fields for selecting a course
    course_name = st.selectbox("Select Course:", get_all_courses(cursor))

    # Display student details for the selected course
    if course_name:
        st.subheader(f"Student Details for Course: {course_name}")
        student_details = get_student_details_for_course(cursor, course_name)
        if student_details:
            details_df = pd.DataFrame({"REGID": [row[0] for row in student_details],
                                       "STUDENTNAME": [row[1] for row in student_details],
                                       "COURSE": [row[2] for row in student_details],
                                       "INSTITUTE": [row[3] for row in student_details]})
            st.table(details_df)
        else:
            st.info("No student details available for the selected course.")

    # Close the database connection
    db_connection.close()

###################################################################
###################################################################


###################################################################

# Function to get student details for a specific course
def get_student_details_for_course(cursor, course_name):
    query = "SELECT REGID, STUDENTNAME, COURSE, INSTITUTE FROM student_details WHERE COURSE = %s"
    cursor.execute(query, (course_name,))
    return cursor.fetchall()

# Function to get all course names
def get_all_courses(cursor):
    cursor.execute("SELECT course_name FROM course_details")
    result = [row[0] for row in cursor.fetchall()]
    return result

###################################################################

###################################################################
###################################################################
from datetime import datetime

# Streamlit app for displaying student details based on course and subject
def student_details_by_course_subject_page():
    st.title("Student Details by Course and Subject")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Input fields for selecting a course and subject
    course_name = st.selectbox("Select Course:", get_all_courses(cursor))
    subjects = get_subjects_for_course(cursor, course_name)
    subject = st.selectbox("Select Subject:", subjects) if subjects else None

    # Dropdown for selecting faculty id from faculty_details table
    faculty_id = get_all_faculty_id(cursor)
    selected_faculty_id = st.selectbox("Select Faculty ID:", faculty_id) if faculty_id else None


    # Display faculty name based on selected faculty ID
    faculty_name = get_faculty_name_for_id(cursor, selected_faculty_id) if selected_faculty_id else None
    st.text(f"Faculty Name: {faculty_name}")


    # Display student details for the selected course and subject
    if course_name and subject:
        st.subheader(f"Student Details for Course: {course_name} and Subject: {subject}")
        student_details = get_student_details_for_course_and_subject(cursor, course_name, subject)
        total_students = len(student_details)  # Get the total number of students

        # Display total number of students
        st.info(f"Total Number of Students for {subject}: {total_students}")

        if student_details:
            details_df = pd.DataFrame({"REGID": [row[0] for row in student_details],
                                       "STUDENTNAME": [row[1] for row in student_details],
                                       "INSTITUTE": [row[2] for row in student_details],})

            # Display the DataFrame with checkboxes
            st.dataframe(details_df)

            # Form for faculty requests
            st.subheader("Faculty Requirement Request Form")

            # Fetch OS types from the "tools" table
            os_types = get_all_os_types(cursor)
            os_type = st.selectbox("Type of OS:", os_types)

            # Fetch tools/packages based on the selected OS
            available_tools = get_tools_for_os(cursor, os_type)
            required_tools_options = [tool[0] for tool in available_tools] if available_tools else []
            required_tools = st.multiselect("Required Tools:", required_tools_options)
            
            # Allow users to input date range for the "Duration" field
            st.subheader("Duration")
            start_date = st.date_input("From Date:")
            start_time = st.time_input("Start Time:")
            end_date = st.date_input("To Date:")
            end_time = st.time_input("End Time:")

            # Combine date and time for start and end
            start_datetime = datetime.combine(start_date, start_time)
            end_datetime = datetime.combine(end_date, end_time)

            # Submit button for faculty requests
            if st.button("Submit Faculty Request"):
                if course_name and subject and selected_faculty_id and total_students and os_type and required_tools and start_datetime and end_datetime:
                    # Create the faculty_request table if not exists
                    create_faculty_request_table(cursor)

                    # Convert datetime to date and time components
                    start_date = start_datetime.date()
                    start_time = start_datetime.time()
                    end_date = end_datetime.date()
                    end_time = end_datetime.time()

                    # Insert faculty request into the database
                    insert_faculty_request(cursor, course_name, subject, selected_faculty_id, total_students, os_type, required_tools, start_date, start_time, end_date, end_time)
                    
                    # Commit changes
                    db_connection.commit()
                    st.success("Faculty requirement request submitted successfully.")
                else:
                    st.warning("Please fill in all the required fields.")

    else:
        st.info("No student details available for the selected course and subject.")

    # Close the database connection
    db_connection.close()

###################################################################
###################################################################


###################################################################

## Function to create a table for faculty requirement requests if not exists
def create_faculty_request_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS faculty_requests ("
                   "REQUEST_ID INT AUTO_INCREMENT PRIMARY KEY, "
                   "Course_name VARCHAR(255),"
                   "Subject VARCHAR(255),"
                   "Faculty_ID VARCHAR(255),"
                   "NUM_SYS_REQ INT,"
                   "OS_TYPE VARCHAR(255), "
                   "REQUIRED_TOOLS VARCHAR(255), "
                   "START_DATE DATE, "
                   "START_TIME TIME, "
                   "END_DATE DATE, "
                   "END_TIME TIME, "
                   "REQUEST_DATETIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

# Function to insert faculty requirement request into the database
def insert_faculty_request(cursor, course_name, subject, selected_faculty_id, total_students, os_type, required_tools, start_date, start_time, end_date, end_time):
    # Convert the list of tools to a comma-separated string
    tools_str = ', '.join(required_tools) if required_tools else None
    
    query = "INSERT INTO faculty_requests (Course_name, Subject, Faculty_ID, NUM_SYS_REQ, OS_TYPE, REQUIRED_TOOLS, START_DATE, START_TIME, END_DATE, END_TIME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (course_name, subject, selected_faculty_id, total_students, os_type, tools_str, start_date, start_time, end_date, end_time)
    cursor.execute(query, values)





# Function to get student details for a specific course and subject
def get_student_details_for_course_and_subject(cursor, course_name, subject):
    query = "SELECT REGID, STUDENTNAME, INSTITUTE FROM student_details WHERE COURSE = %s AND REGID IN (SELECT REGID FROM subject_details WHERE SUBJECT_NAME = %s)"
    cursor.execute(query, (course_name, subject))
    return cursor.fetchall()


# Function to get subjects for a specific course
def get_subjects_for_course(cursor, course_name):
    query = "SELECT SUBJECT_NAME FROM subject_details WHERE COURSE_ID = (SELECT COURSE_ID FROM course_details WHERE course_name = %s)"
    cursor.execute(query, (course_name,))
    result = [row[0] for row in cursor.fetchall()]
    return result


# Function to get all course names
def get_all_courses(cursor):
    cursor.execute("SELECT course_name FROM course_details")
    result = [row[0] for row in cursor.fetchall()]
    return result
# Function to get OS from Tool
def get_all_os_types(cursor):
    cursor.execute("SELECT DISTINCT OS FROM tools")
    return [row[0] for row in cursor.fetchall()]

# Function to get tools/packages for a specific OS
def get_tools_for_os(cursor, os_type):
    query = "SELECT PACKAGES FROM tools WHERE OS = %s"
    cursor.execute(query, (os_type,))
    return cursor.fetchall()

# Function to get all faculty names
def get_all_faculty(cursor):
    cursor.execute("SELECT FACULTY_NAME FROM faculty_details")
    result = [row[0] for row in cursor.fetchall()]
    return result

# Function to get all faculty ID
def get_all_faculty_id(cursor):
    cursor.execute("SELECT FACULTY_ID FROM faculty_details")
    result = [row[0] for row in cursor.fetchall()]
    return result

# Function to get faculty name for a specific faculty ID
def get_faculty_name_for_id(cursor, faculty_id):
    query = "SELECT FACULTY_NAME FROM faculty_details WHERE FACULTY_ID = %s"
    cursor.execute(query, (faculty_id,))
    result = cursor.fetchone()
    return result[0] if result else None

###################################################################

###################################################################
###################################################################

# Streamlit app for displaying faculty requests with status
# Streamlit app for displaying faculty requests with status
def faculty_requests_page():
    st.title("Faculty Requests List")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Button to manually refresh faculty requests
    refresh_button = st.button("Refresh Faculty Requests")

    # Display faculty requests with status
    if refresh_button:
        faculty_requests = get_faculty_requests(cursor)
        if faculty_requests:
            # Get current date and time
            current_datetime = datetime.today()

            # Create a list to store status for each request
            status_list = []

            for row in faculty_requests:
                faculty_request_id = row[0]
                end_datetime = row[9]

                # Check if FACULTY_REQUEST_ID is present in CONTAINER_DETAILS
                if is_request_id_present(cursor, faculty_request_id):
                    # Check if END DATETIME is equal to or past the current datetime
                    if end_datetime is not None and end_datetime >= current_datetime:
                        status = "Completed"
                    else:
                        status = "Success"
                else:
                    status = "Pending"

                status_list.append(status)

            # Add a new column "Status" to the DataFrame
            faculty_requests_df = pd.DataFrame({
                "REQUEST ID": [row[0] for row in faculty_requests],
                "COURSE NAME": [row[1] for row in faculty_requests],
                "SUBJECT": [row[2] for row in faculty_requests],
                "Faculty_ID": [row[3] for row in faculty_requests],
                "NUM SYS REQ": [row[4] for row in faculty_requests],
                "TYPE OF OS": [row[5] for row in faculty_requests],
                "REQUIRED TOOLS": [row[6] for row in faculty_requests],
                "START DATE AND TIME": [row[7] for row in faculty_requests],
                "END DATE AND TIME": [row[8] for row in faculty_requests],
                "REQUEST DATETIME": [row[9] for row in faculty_requests],
                "Status": status_list  # New column "Status"
            })

            # Apply background colors based on the "Status" column
            try:
                colors = {"Pending": "background-color: red", "Success": "background-color: green", "Completed": "background-color: violet", "Expired": "background-color: yellow"}
                faculty_requests_df_styled = faculty_requests_df.style.applymap(lambda value: apply_color(value, colors))
                st.table(faculty_requests_df_styled)
            except KeyError as e:
                st.error(f"Error applying background colors: {e}")
        else:
            st.info("No faculty requests available.")

    # Close the database connection
    db_connection.close()




###################################################################
###################################################################


###################################################################

# Function to get faculty requests in descending order of date and time
def get_faculty_requests(cursor):
    query = """
        SELECT REQUEST_ID, Course_name, Subject, Faculty_ID, NUM_SYS_REQ, 
               OS_TYPE, REQUIRED_TOOLS, 
               CONCAT(START_DATE, ' ', START_TIME) AS START_DATETIME, 
               CONCAT(END_DATE, ' ', END_TIME) AS END_DATETIME, 
               REQUEST_DATETIME 
        FROM faculty_requests 
        ORDER BY REQUEST_DATETIME DESC
    """
    cursor.execute(query)
    return cursor.fetchall()




# Function to check if FACULTY_REQUEST_ID is present in CONTAINER_DETAILS
def is_request_id_present(cursor, faculty_request_id):
    query = "SELECT COUNT(*) FROM CONTAINER_DETAILS WHERE FACULTY_REQUEST_ID = %s"
    cursor.execute(query, (faculty_request_id,))
    count = cursor.fetchone()[0]
    return count > 0

# Function to apply background colors based on the "Status" column
def apply_color(value, colors):
    try:
        return colors.get(value, "background-color: none")
    except Exception as e:
        st.error(f"Error applying background color: {e}")
        return "background-color: none"



###################################################################


###################################################################
###################################################################

### Streamlit app for Container Details
def container_detail_page():
    st.title("ENVIRONMENT DETAIL")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Create the 'CONTAINER_DETAILS' table if it doesn't exist
    create_container_details_table(cursor)

    # Fetch container details from the CONTAINER_DETAILS table
    container_details = get_container_details(cursor)

    # Display a table with container details
    if container_details:
        container_df = pd.DataFrame(container_details, columns=["IP Address", "URL", "Docker Image Name", "Package", "Password", "Course", "subject", "Faculty request ID"])
        # Format the 'URL' column as a hyperlink
        container_df['URL'] = container_df.apply(lambda row: f'<a href="{row["URL"]}" target="_blank">{row["URL"]}</a>', axis=1)

        # Display the table with HTML in the 'URL' column
        st.write(container_df.to_html(escape=False), unsafe_allow_html=True)
    
    else:
        st.warning("No container details found.")

    # Close the database connection
    db_connection.close()





###################################################################
###################################################################


###################################################################

# Create the 'CONTAINER_DETAILS' table if it doesn't exist
def create_container_details_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CONTAINER_DETAILS (
            IP_ADDRESS VARCHAR(15) ,
            URL VARCHAR(255),
            DOCKER_IMAGE_NAME VARCHAR(255),
            PACKAGE VARCHAR(255),
            PASSWORD VARCHAR(255),
            COURSE VARCHAR(255),
            SUBJECT VARCHAR(255),
            FACULTY_REQUEST_ID INT
        )
    """)


# Function to insert container details into the CONTAINER_DETAILS table
def insert_container_details(db_connection, cursor, ip_address, url, docker_image_name, packages, password_value, course_name, subject, faculty_request_id):
    try:
        query = """
            INSERT INTO CONTAINER_DETAILS 
            (IP_ADDRESS, URL, DOCKER_IMAGE_NAME, PACKAGE, PASSWORD, COURSE,SUBJECT, FACULTY_REQUEST_ID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        with cursor as cursor:
            cursor.execute(query, (ip_address, url, docker_image_name, packages, password_value, course_name, subject, faculty_request_id))
            db_connection.commit()
        st.success("Container details inserted successfully.")
    except Exception as e:
        db_connection.rollback()
        st.error(f"Error inserting container details: {e}")


# Function to get container details from the containers table
def get_container_details(cursor):
    try:
        # Fetch container details from the containers table
        query = "SELECT IP_ADDRESS, URL, DOCKER_IMAGE_NAME, PACKAGE, PASSWORD, COURSE, SUBJECT, FACULTY_REQUEST_ID FROM CONTAINER_DETAILS ORDER BY FACULTY_REQUEST_ID DESC"
        cursor.execute(query)
        container_details = cursor.fetchall()

        # Return the container details
        return container_details

    except Exception as e:
        st.error(f"Error fetching container details: {e}")
        return []



###################################################################



# Main Streamlit app to switch between FACULTY data entry and All FACULTY detail pages
def main():
    page = st.sidebar.radio("Select Page:", ["FACULTY DATA ENTRY", "ALL FACULTY DETAILS", "STUDENT AS PER COURSE",
                                             "FACULTY RESQUEST FOR STUDENT","FACULTY REQUESTS LIST","ENVIRONMENT DETAIL"])

    if page == "FACULTY DATA ENTRY":
        faculty_data_entry_page()
    elif page == "ALL FACULTY DETAILS":
        list_faculty_details_page()
    elif page == "STUDENT AS PER COURSE":
        student_details_by_course_page()
    elif page == "FACULTY RESQUEST FOR STUDENT" :
        student_details_by_course_subject_page()
    elif page == "FACULTY REQUESTS LIST":
        faculty_requests_page()  
    elif page == "ENVIRONMENT DETAIL":
        container_detail_page()      
    

if __name__ == "__main__":
    main()
