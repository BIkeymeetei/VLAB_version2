import streamlit as st
import mysql.connector
import pandas as pd


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

# Function to create a table to store student details if not exists
def create_student_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS student_details (REGID VARCHAR(255) PRIMARY KEY, STUDENTNAME VARCHAR(255), "
                   "COURSE VARCHAR(255), INSTITUTE VARCHAR(255))")


# Function to insert student details into the database
def insert_student_details(cursor, REGID, STUDENTNAME, COURSE, INSTITUTE):
    query = "INSERT INTO student_details (REGID, STUDENTNAME, COURSE, INSTITUTE) VALUES (%s, %s, %s, %s)"
    values = (REGID, STUDENTNAME, COURSE, INSTITUTE)
    cursor.execute(query, values)   

# Function to get unique STUDENT REG ID from the database
def get_unique_student(cursor):
    cursor.execute("SELECT DISTINCT REGID FROM student_details")
    return [row[0] for row in cursor.fetchall()]

# Function to get student details for a specific STUDENT REG ID
def get_student_details_for_regid(cursor, REGID):
    query = "SELECT STUDENTNAME, COURSE, INSTITUTE FROM student_details WHERE REGID = %s"
    cursor.execute(query, (REGID,))
    return cursor.fetchall()

###################################################################


###################################################################
###################################################################

# Streamlit app for Student data entry
def student_data_entry_page():
    st.title("STUDENT DATA ENTRY")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Input fields for STUDENT details
    REGID = st.text_input("REGISTRATION ID :")
    STUDENTNAME = st.text_input("NAME OF STUDENT :")
    COURSE = st.text_input("COURSE NAME :")
    INSTITUTE = st.text_input("STUDENT INSTITUTE NAME :")

    
    # Submit button
    if st.button("Submit"):
        # Validate inputs
        if REGID and STUDENTNAME and COURSE and INSTITUTE :
            # Create the student_details table if not exists
            create_student_table(cursor)

            # Check for duplicate Student REG ID
            if student_id_exists(cursor, REGID):
                st.warning("This Student REG ID already exists. Please choose a different REG ID.")
            else:
                # Insert student details into the database
                insert_student_details(cursor, REGID, STUDENTNAME, COURSE, INSTITUTE)

                # Commit changes
                db_connection.commit()

                st.success("Student details added successfully.")
        else:
            st.warning("Please enter all details.")

    # Close the database connection
    db_connection.close()


###################################################################
###################################################################


###################################################################

# Function to check if a Student REG ID already exists
def student_id_exists(cursor, REGID):
    query = "SELECT COUNT(*) FROM student_details WHERE REGID = %s"
    cursor.execute(query, (REGID,))
    count = cursor.fetchone()[0]
    return count > 0

###################################################################

###################################################################
###################################################################

# Streamlit app for listing student details
def list_student_details_page():
    st.title("ALL STUDENT DETAILS")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Display details for all student REG ID
    all_student_details = get_all_student_details(cursor)

    for student_detail in all_student_details:
        REGID, STUDENTNAME, COURSE, INSTITUTE = student_detail
        st.subheader(f"Details for STUDENT REGISTRATION ID: {REGID}")
        details_df = pd.DataFrame({"STUDENT NAME":[STUDENTNAME], "COURSE NAME": [COURSE], "INSTITUTE NAME": [INSTITUTE]})
        st.table(details_df)
        st.markdown("---")  # Add a horizontal line to separate details for different hostnames

    # Close the database connection
    db_connection.close()

###################################################################
###################################################################

###################################################################

# Function to get Student details for all STUDENT ID
def get_all_student_details(cursor):
    query = "SELECT REGID, STUDENTNAME, COURSE, INSTITUTE FROM student_details"
    cursor.execute(query)
    return cursor.fetchall()    

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



###################################################################
###################################################################    
    

# Streamlit app for displaying student Lab Environment details based on course and subject
def environment_for_student_page():
    st.title("LAB ENVIRONMENT FOR STUDENT")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Input fields for selecting a course and subject
    course_name = st.selectbox("Select your Course:", get_all_courses(cursor))
    subjects = get_subjects_for_course(cursor, course_name)
    subject = st.selectbox("Select which Subject:", subjects) if subjects else None

    # Dropdown for selecting faculty id from faculty_details table
    #faculty_id = get_all_faculty_id(cursor)
    #selected_faculty_id = st.selectbox("Select Faculty ID:", faculty_id) if faculty_id else None

    # Display faculty name based on selected faculty ID
    #faculty_name = get_faculty_name_for_id(cursor, selected_faculty_id) if selected_faculty_id else None
    #st.text(f"Faculty Name: {faculty_name}")

    # Display student details for the selected course and subject
    if course_name and subject:
        st.subheader(f"Environment Details for Course: {course_name} and Subject: {subject}")
        student_details = get_student_details_for_course_and_subject(cursor, course_name, subject)
        total_students = len(student_details)  # Get the total number of students

        # Display total number of students
        st.info(f"Total Number of Students for {subject}: {total_students}")

        if student_details:
            # Create a DataFrame with course and subject columns
            details_df = pd.DataFrame({"REGID": [row[0] for row in student_details],
                                       "STUDENTNAME": [row[1] for row in student_details],
                                       "INSTITUTE": [row[2] for row in student_details],
                                       "COURSE": [course_name] * total_students,
                                       "SUBJECT": [subject] * total_students})
            
            
           
            


            # Add a new column "URL" and fetch values from container_details table
            details_df["URL"] = get_url_from_container_details(cursor, course_name, subject, total_students)
            # Add a new column "Password" and fetch values from container_details table based on matching URLs
            details_df["Password"] = get_password_from_container_details(cursor, details_df["URL"])

            # Add a new column "Package/Tool" and fetch values from container_details table based on matching URLs
            details_df["Package/Tool"] = get_package_tool_from_container_details(cursor, details_df["URL"])

            # Display the DataFrame with checkboxes and format "URL" as hyperlinks
            details_df["URL"] = details_df["URL"].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

            # Reorder columns to place "Package/Tool" next to "Subject"
            details_df = details_df[["REGID", "STUDENTNAME", "INSTITUTE", "COURSE", "SUBJECT", "Package/Tool", "URL", "Password"]]
            
            st.write(details_df.to_markdown(index=False), unsafe_allow_html=True)

    else:
        st.info("No student details available for the selected course and subject.")

    # Close the database connection
    db_connection.close()


###################################################################
###################################################################


###################################################################



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

# Function to get URL from container_details table
def get_url_from_container_details(cursor, course_name, subject, total_students):
    query = "SELECT URL FROM CONTAINER_DETAILS WHERE COURSE = %s AND SUBJECT = %s LIMIT %s"
    cursor.execute(query, (course_name, subject, total_students))
    return [row[0] for row in cursor.fetchall()]




# Function to get Password from container_details table based on matching URLs
def get_password_from_container_details(cursor, urls):
    # Construct the SQL query dynamically
    query = f"SELECT PASSWORD FROM CONTAINER_DETAILS WHERE URL IN ({', '.join(['%s'] * len(urls))})"
    cursor.execute(query, tuple(urls))
    return [row[0] for row in cursor.fetchall()]


# Function to get Package/Tool from container_details table based on matching URLs
def get_package_tool_from_container_details(cursor, urls):
    # Construct the SQL query dynamically
    query = f"SELECT PACKAGE FROM CONTAINER_DETAILS WHERE URL IN ({', '.join(['%s'] * len(urls))})"
    cursor.execute(query, tuple(urls))
    return [row[0] for row in cursor.fetchall()]


###################################################################



# Main Streamlit app to switch between student data entry and All student detail pages
def main():
    page = st.sidebar.radio("Select Page:", ["STUDENT DATA ENTRY", "ALL STUDENT DETAILS", "ENVIRONMENT FOR STUDENT"]) # "ENVIRONMENT DETAIL",

    if page == "STUDENT DATA ENTRY":
        student_data_entry_page()
    elif page == "ALL STUDENT DETAILS":
        list_student_details_page()
    elif page == "ENVIRONMENT DETAIL":
        container_detail_page()
    elif page == "ENVIRONMENT FOR STUDENT":
        environment_for_student_page()       

if __name__ == "__main__":
    main()
