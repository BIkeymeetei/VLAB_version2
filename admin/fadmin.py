import streamlit as st
import mysql.connector
import pandas as pd
import paramiko
import docker
import time
import datetime
from datetime import datetime


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

# Function to create a table to store server details if not exists
def create_server_table(cursor):
   cursor.execute("CREATE TABLE IF NOT EXISTS server_details (Hostid VARCHAR(255) PRIMARY KEY, password VARCHAR(255), "
                   "hostname VARCHAR(255), ip_address VARCHAR(15), root_username VARCHAR(255), Host_OS VARCHAR(225))")


# Function to insert server details into the database
def insert_server_details(cursor, Hostid, password, hostname, ip_address, root_username, Host_OS):
    query = "INSERT INTO server_details (Hostid, password, hostname, ip_address, root_username, Host_OS) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (Hostid, password, hostname, ip_address, root_username, Host_OS)
    cursor.execute(query, values)


# Function to get unique hostnames from the database
def get_unique_hostnames(cursor):
    cursor.execute("SELECT DISTINCT Hostid FROM server_details")
    return [row[0] for row in cursor.fetchall()]


# Function to get server details for a specific hostname
def get_server_details_for_hostname(cursor, Hostid):
    query = "SELECT hostname,password, ip_address, root_username, Host_OS FROM server_details WHERE Hostid = %s"
    cursor.execute(query, (Hostid,))
    return cursor.fetchall()


# Function to check if a hostname already exists
def hostname_exists(cursor, Hostid):
    query = "SELECT COUNT(*) FROM server_details WHERE Hostid = %s"
    cursor.execute(query, (Hostid,))
    count = cursor.fetchone()[0]
    return count > 0


###################################################################


###################################################################
###################################################################

# Streamlit app for data entry
def data_entry_page():
    st.title("Data Entry")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Input fields for server details
    Hostid = st.text_input("Hostid:")
    password = st.text_input("Password:", type="password")
    hostname = st.text_input("Hostname:")
    ip_address = st.text_input("IP Address:")
    root_username = st.text_input("Root Username:")
    Host_OS = st.text_input(" HOST OS:")

    # Submit button
    if st.button("Submit"):
        # Validate inputs
        if Hostid and password and hostname and ip_address and root_username and Host_OS:
            # Create the server_details table if not exists
            create_server_table(cursor)

            # Check for duplicate hostname
            if hostname_exists(cursor, Hostid):
                st.warning("HostID already exists. Please choose a different HOST ID.")
            else:
                # Insert server details into the database
                insert_server_details(cursor, Hostid, password, hostname, ip_address, root_username, Host_OS)

                # Commit changes
                db_connection.commit()

                st.success("Server details added successfully.")
        else:
            st.warning("Please enter all details.")

    # Close the database connection
    db_connection.close()

###################################################################
###################################################################
    

###################################################################
###################################################################

# Streamlit app for listing host details
def list_host_details_page():
    st.title("LIST HOST DETAILS")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    try:
        # Display details for all hostnames
        all_server_details = get_all_server_details(cursor)

        for server_detail in all_server_details:
            print (server_detail)
            # Unpack server details
            Hostid, password, hostname, ip_address, root_username , Host_OS = server_detail 

            # Display details for each host
            st.subheader(f"Details for Host ID: {Hostid}")
            details_df = pd.DataFrame({"password":[password], "hostname":[hostname],
                                        "ip-address":[ip_address], "root-username":[root_username],
                                          "Host-OS":[Host_OS]})
            st.table(details_df)

            # Delete button for each host
            delete_button = st.button(f"Delete Host ID: {Hostid}")

            # When the delete button is clicked, delete the host details
            if delete_button:
                delete_host_details(cursor, Hostid)
                st.success(f"Host ID {Hostid} details deleted successfully.")

            st.markdown("---")  # Add a horizontal line to separate details for different hostnames

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        db_connection.close()


###################################################################
###################################################################

###################################################################

# Function to delete host details for a specific host
def delete_host_details(Hostid):
    try:
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        query = "DELETE FROM server_details WHERE Hostid = %s"
        cursor.execute(query, (Hostid,))
        db_connection.commit()

    except Exception as e:
        st.error(f"Error deleting host details: {e}")

    finally:
        # Close the database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()


# Function to get server details for all hostnames
def get_all_server_details(cursor):
    query = "SELECT * FROM server_details"
    cursor.execute(query)
    return cursor.fetchall()

###################################################################


###################################################################
###################################################################

# Streamlit app for updating host details
def update_host_details_page():
    st.title("UPDATE HOST DETAILS")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Get the list of host IDs
    host_ids = get_unique_hostnames(cursor)

    # Dropdown to select a host ID for updating
    selected_host_id = st.selectbox("Select Host ID for Update:", host_ids)

    if selected_host_id:
        # Display current details for the selected host
        current_details = get_server_details_for_hostname(cursor, selected_host_id)
        st.subheader(f"Current Details for Host ID: {selected_host_id}")
        current_details_df = pd.DataFrame({"hostname": [current_details[0][0]], "password": [current_details[0][1]],
                                            "IP Address": [current_details[0][2]], "Root Username": [current_details[0][3]], "Host OS":[current_details[0][4]]})
        st.table(current_details_df)

        # Input fields for updating host details
        updated_hostname = st.text_input("Updated Hostname:", current_details[0][0])
        updated_password = st.text_input("Updated Password:", current_details[0][1], type="password")
        updated_ip_address = st.text_input("Updated IP Address:", current_details[0][2])
        updated_root_username = st.text_input("Updated Root Username:", current_details[0][3])
        updated_host_OS = st.text_input("Updated Host OS:", current_details[0][4])

        # Update button
        if st.button("Update Host Details"):
            # Validate inputs
            if updated_hostname and updated_password and updated_ip_address and updated_root_username and updated_host_OS:
                # Update host details in the database
                update_host_details(cursor, selected_host_id, updated_hostname, updated_password,
                                    updated_ip_address, updated_root_username, updated_host_OS)

                # Commit changes
                db_connection.commit()

                st.success(f"Host ID {selected_host_id} details updated successfully.")
            else:
                st.warning("Please enter all updated details.")

    # Close the database connection
    db_connection.close()


###################################################################
###################################################################

###################################################################

# Function to update host details for a specific host
def update_host_details(cursor, Hostid, updated_hostname, updated_password, updated_ip_address, updated_root_username, updated_host_OS):
    query = "UPDATE server_details SET hostname = %s, password = %s, ip_address = %s, root_username = %s, Host_OS=%s WHERE Hostid = %s"
    values = (updated_hostname, updated_password, updated_ip_address, updated_root_username, updated_host_OS, Hostid)
    cursor.execute(query, values)

###################################################################


###################################################################
###################################################################

# Streamlit app for updating faculty details
def update_faculty_details_page():
    st.title("UPDATE FACULTY DETAILS")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Get the list of host faculty ID
    FACULTY_ID = get_unique_faculty(cursor)

    # Dropdown to select a faculty ID for updating
    selected_FACULTY_ID = st.selectbox("Select FACULTY ID for Update:", FACULTY_ID)

    if selected_FACULTY_ID:
        # Display current details for the selected faculty
        current_details = get_faculty_details_for_FACULTY_ID(cursor, selected_FACULTY_ID)
        st.subheader(f"Current Details for FACULTY ID: {selected_FACULTY_ID}")
        current_details_df = pd.DataFrame({"FACULTY_NAME": [current_details[0][0]], "COURSE": [current_details[0][1]],
                                            "INSTITUTE": [current_details[0][2]]})
        st.table(current_details_df)

        # Input fields for updating faculty details
        updated_FACULTY_NAME = st.text_input("Updated FACULTY NAME:", current_details[0][0])
        updated_COURSE = st.text_input("Updated COURSE:", current_details[0][1])
        updated_INSTITUTE = st.text_input("Updated INSTITUTE:", current_details[0][2])

        # Update button
        if st.button("Update FACULTY Details"):
            # Validate inputs
            if updated_FACULTY_NAME and updated_COURSE and updated_INSTITUTE :
                # Update faculty details in the database
                update_faculty_details(cursor, selected_FACULTY_ID, updated_FACULTY_NAME, updated_COURSE,
                                    updated_INSTITUTE)

                # Commit changes
                db_connection.commit()

                st.success(f"FACULTY ID {selected_FACULTY_ID} details updated successfully.")
            else:
                st.warning("Please enter all updated details.")

    # Close the database connection
    db_connection.close()


###################################################################
###################################################################


###################################################################

# Function to update faculty details for a specific faculty id
def update_faculty_details(cursor, FACULTY_ID, updated_FACULTY_NAME, updated_COURSE, updated_INSTITUTE):
    query = "UPDATE faculty_details SET FACULTY_NAME = %s, COURSE = %s, INSTITUTE = %s WHERE FACULTY_ID = %s"
    values = (updated_FACULTY_NAME, updated_COURSE, updated_INSTITUTE, FACULTY_ID)
    cursor.execute(query, values)


# Function to get FACULTY details for a specific FACULTY REG ID
def get_faculty_details_for_FACULTY_ID(cursor, FACULTY_ID):
    query = "SELECT FACULTY_NAME,COURSE, INSTITUTE FROM faculty_details WHERE FACULTY_ID = %s"
    cursor.execute(query, (FACULTY_ID,))
    return cursor.fetchall()

# Function to get unique FACULTY ID from the database
def get_unique_faculty(cursor):
    cursor.execute("SELECT DISTINCT FACULTY_ID FROM faculty_details")
    return [row[0] for row in cursor.fetchall()]

###################################################################


###################################################################
###################################################################

# Streamlit app for updating student details
def update_student_details_page():
    st.title("UPDATE STUDENT DETAILS")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Get the list of student IDs
    REGID= get_unique_student(cursor)

    # Dropdown to select a student ID for updating
    selected_REGID = st.selectbox("Select STUDENT ID for Update:", REGID)

    if selected_REGID:
        # Display current details for the selected student
        current_details = get_student_details_for_regid(cursor, selected_REGID)
        st.subheader(f"Current Details for STUDENT ID: {selected_REGID}")
        current_details_df = pd.DataFrame({"STUDENTNAME": [current_details[0][0]], "COURSE": [current_details[0][1]],
                                            "INSTITUTE": [current_details[0][2]]})
        st.table(current_details_df)

        # Input fields for updating STUDENT details
        updated_STUDENTNAME = st.text_input("Updated STUDENT NAME:", current_details[0][0])
        updated_COURSE = st.text_input("Updated COURSE:", current_details[0][1])
        updated_INSTITUTE = st.text_input("Updated INSTITUTE:", current_details[0][2])

        # Update button
        if st.button("Update STUDENT Details"):
            # Validate inputs
            if updated_STUDENTNAME and updated_COURSE and updated_INSTITUTE :
                # Update student details in the database
                update_student_details(cursor, selected_REGID, updated_STUDENTNAME, updated_COURSE,
                                    updated_INSTITUTE)

                # Commit changes
                db_connection.commit()

                st.success(f"STUDENT ID {selected_REGID} details updated successfully.")
            else:
                st.warning("Please enter all updated details.")

    # Close the database connection
    db_connection.close()



###################################################################
###################################################################


###################################################################

## Function to update student details for a specific Student id
def update_student_details(cursor, REGID, updated_STUDENTNAME, updated_COURSE, updated_INSTITUTE):
    query = "UPDATE student_details SET STUDENTNAME = %s, COURSE = %s, INSTITUTE = %s WHERE REGID = %s"
    values = (updated_STUDENTNAME, updated_COURSE, updated_INSTITUTE, REGID)
    cursor.execute(query, values)


# Function to get student details for a specific STUDENT REG ID
def get_student_details_for_regid(cursor, REGID):
    query = "SELECT STUDENTNAME,COURSE, INSTITUTE FROM student_details WHERE REGID = %s"
    cursor.execute(query, (REGID,))
    return cursor.fetchall()

# Function to get unique STUDENT REG ID from the database
def get_unique_student(cursor):
    cursor.execute("SELECT DISTINCT REGID FROM student_details")
    return [row[0] for row in cursor.fetchall()]


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

        # Delete button for each faculty ID
        delete_button = st.button(f"Delete FACULTY ID: {FACULTY_ID}")

        # When the delete button is clicked, delete the faculty details
        if delete_button:
            delete_faculty_details(FACULTY_ID)
            st.success(f"FACULTY ID {FACULTY_ID} details deleted successfully.")


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




# Function to delete Faculty details for a specific faculty ID
def delete_faculty_details(FACULTY_ID):
    try:
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        query = "DELETE FROM faculty_details WHERE FACULTY_ID = %s"
        cursor.execute(query, (FACULTY_ID,))
        db_connection.commit()

    except Exception as e:
        st.error(f"Error deleting FACULTY ID details: {e}")

    finally:
        # Close the database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()



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
        REGID, STUDENTNAME,COURSE, INSTITUTE = student_detail
        st.subheader(f"Details for STUDENT REGISTRATION ID: {REGID}")
        details_df = pd.DataFrame({"STUDENT NAME":[STUDENTNAME], "BRANCH NAME": [COURSE], "INSTITUTE NAME": [INSTITUTE]})
        st.table(details_df)

        # Delete button for each faculty ID
        delete_button = st.button(f"Delete STUDENT ID: {REGID}")

        # When the delete button is clicked, delete the STUDENT details
        if delete_button:
            delete_student_details(REGID)
            st.success(f"STUDENT ID {REGID} details deleted successfully.")


        st.markdown("---")  # Add a horizontal line to separate details for different hostnames

    # Close the database connection
    db_connection.close()


###################################################################
###################################################################



###################################################################


# Function to delete student details for a specific student ID
def delete_student_details(REGID):
    try:
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        query = "DELETE FROM student_details WHERE REGID = %s"
        cursor.execute(query, (REGID,))
        db_connection.commit()

    except Exception as e:
        st.error(f"Error deleting STUDENT ID details: {e}")

    finally:
        # Close the database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()




# Function to get Student details for all STUDENT ID
def get_all_student_details(cursor):
    query = "SELECT REGID, STUDENTNAME, COURSE, INSTITUTE FROM student_details"
    cursor.execute(query)
    return cursor.fetchall()    


###################################################################


###################################################################


# Function to create a table to store course details if not exists
def create_course_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS course_details ("
                   "course_id INT AUTO_INCREMENT PRIMARY KEY, "
                   "course_name VARCHAR(255))"
                   )

# Function to create a table to store subjects for each course if not exists
def create_subject_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS subject_details ("
                   "subject_id INT AUTO_INCREMENT PRIMARY KEY, "
                   "course_id INT, "
                   "subject_name VARCHAR(255), "
                   "FOREIGN KEY (course_id) REFERENCES course_details(course_id))"
                   )

# Function to insert course details into the database
def insert_course_details(cursor, course_name):
    query = "INSERT INTO course_details (course_name) VALUES (%s)"
    values = (course_name,)
    cursor.execute(query, values)
    return cursor.lastrowid  # Return the ID of the newly inserted course

# Function to insert subject details into the database
def insert_subject_details(cursor, course_id, subject_names_list):
    query = "INSERT INTO subject_details (course_id, subject_name) VALUES (%s, %s)"
    values = [(course_id, subject_name) for subject_name in subject_names_list]
    cursor.executemany(query, values)
    cursor.fetchall()  # Fetch the results to avoid "Unread result found" error


###################################################################


###################################################################
###################################################################


# Streamlit app for course data entry
def course_data_entry_page():
    st.title("ENTER NEW COURSE NAME FOR ME DEGREE")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Input fields for course details
    course_name = st.text_input("Course Name:")

    # Submit button
    if st.button("Submit"):
        # Validate inputs
        if course_name:
            # Create the course_details table if not exists
            create_course_table(cursor)

            # Insert course details into the database and get the course ID
            course_id = insert_course_details(cursor, course_name)

            # Create the subject_details table if not exists
           # create_subject_table(cursor)

            # Insert subject details into the database
           # insert_subject_details(cursor, course_id, "Subject1")

            # Commit changes
            db_connection.commit()

            st.success("Course details added successfully.")
        else:
            st.warning("Please enter the course name.")

    # Display details for all courses
    all_courses = get_all_courses(cursor)
    if all_courses:
        st.subheader("Course Available for ME degree in SOIS")
        course_details_df = pd.DataFrame({"Course Name": all_courses})
        st.table(course_details_df)
    else:
        st.info("No courses available.")

    # Close the database connection
    db_connection.close()


###################################################################
###################################################################


###################################################################

# Function to get all course names
def get_all_courses(cursor):
    cursor.execute("SELECT course_name FROM course_details")
    result = [row[0] for row in cursor.fetchall()]
    return result

###################################################################



###################################################################
###################################################################

# Streamlit app for subject data entry
def subject_data_entry_page():
    st.title("Subject Data Entry")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Input fields for subject details
    course_name = st.selectbox("Select Course:", get_all_courses(cursor))
    subject_names = st.text_area("Enter Subject Names (separated by commas):")

    # Submit button
    if st.button("Submit"):
        # Validate inputs
        if course_name and subject_names:
            # Get the course_id for the selected course
            course_id = get_course_id(cursor, course_name)

            # Create the subject_details table if not exists
            create_subject_table(cursor)

            # Split the entered subject names into a list
            subject_names_list = [subject.strip() for subject in subject_names.split(',')]

            # Insert subject details into the database
            insert_subject_details(cursor, course_id, subject_names_list)

            # Commit changes
            db_connection.commit()

            st.success("Subject details added successfully.")
        else:
            st.warning("Please select a course and enter at least one subject name.")

    # Close the database connection
    db_connection.close()


###################################################################
###################################################################


###################################################################

# Function to get all course names
def get_all_courses(cursor):
    cursor.execute("SELECT course_name FROM course_details")
    result = [row[0] for row in cursor.fetchall()]
    return result

# Function to get course_id for a given course name
def get_course_id(cursor, course_name):
    cursor.execute("SELECT course_id FROM course_details WHERE course_name = %s", (course_name,))
    result = cursor.fetchone()
    return result[0] if result else None

###################################################################


###################################################################
###################################################################

# Streamlit app for listing subject details
def list_subject_details_page():
    st.title("List Subject Details")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Get all courses
    all_courses = get_all_courses(cursor)

    # Display subject details for each course
    for course_name in all_courses:
        st.subheader(f"Subject Details for Course: {course_name}")

        # Get the course_id for the selected course
        course_id = get_course_id(cursor, course_name)

        # Get subject details for the course
        subject_details = get_subject_details_for_course(cursor, course_id)

        if subject_details:
            subject_details_df = pd.DataFrame({"Subject Name": subject_details})
            st.table(subject_details_df)
        else:
            st.info(f"No subjects available for {course_name}.")

        st.markdown("---")  # Add a horizontal line to separate details for different courses

    # Close the database connection
    db_connection.close()

###################################################################
###################################################################


###################################################################

# Function to get subject details for a specific course
def get_subject_details_for_course(cursor, course_id):
    query = "SELECT subject_name FROM subject_details WHERE course_id = %s"
    cursor.execute(query, (course_id,))
    return [row[0] for row in cursor.fetchall()]

###################################################################

###################################################################
###################################################################
    

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
                    if end_datetime is not None and end_datetime <= current_datetime:
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

## Function to create a table for tools requests if not exists
def create_tools_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tools (
            TOOLID INT AUTO_INCREMENT PRIMARY KEY, 
            OS VARCHAR(255),
            PACKAGES VARCHAR(255),
            HOST_PORT VARCHAR(255),
            CONTAINER_PORT VARCHAR(255),
            USERNAME VARCHAR(255),
            PASSWORD_KEY VARCHAR(255),
            PASSWORD_VALUE VARCHAR(255),       
            DOCKER_IMAGE_NAME VARCHAR(255),
            SOURCE_VOLUME VARCHAR(255),
            CONTAINER_VOLUME VARCHAR(255)
        )
    """)
# Function to insert server details into the database
def insert_tools(cursor, TOOLID, OS, PACKAGES, HOST_PORT, CONTAINER_PORT, USERNAME, PASSWORD_KEY,
                  PASSWORD_VALUE, DOCKER_IMAGE_NAME,SOURCE_VOLUME,CONTAINER_VOLUME):
    query = "INSERT INTO tools (TOOLID, OS, PACKAGES, HOST_PORT, CONTAINER_PORT, USERNAME, PASSWORD_KEY, PASSWORD_VALUE, DOCKER_IMAGE_NAME, SOURCE_VOLUME,CONTAINER_VOLUME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (TOOLID, OS, PACKAGES, HOST_PORT, CONTAINER_PORT, USERNAME, PASSWORD_KEY, PASSWORD_VALUE, DOCKER_IMAGE_NAME,SOURCE_VOLUME,CONTAINER_VOLUME)
    cursor.execute(query, values)

# Function to get unique hostnames from the database
def get_unique_toolid(cursor):
    cursor.execute("SELECT DISTINCT TOOLID FROM tools")
    return [row[0] for row in cursor.fetchall()]

# Function to get server details for a specific hostname
def get_tools_for_toolid(cursor, TOOLID):
    query = "SELECT OS, PACKAGES, HOST_PORT, CONTAINER_PORT, USERNAME, PASSWORD_KEY, PASSWORD_VALUE, DOCKER_IMAGE_NAME,SOURCE_VOLUME,CONTAINER_VOLUME FROM tools WHERE TOOLID = %s"
    cursor.execute(query, (TOOLID,))
    return cursor.fetchall()


###################################################################


###################################################################
###################################################################

## Streamlit app for data entry
def tool_data_entry_page():
    st.title("TOOLS Data Entry")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Input fields for server details
    TOOLID = st.text_input("TOOLID:")
    OS = st.text_input("OS NAME:")
    PACKAGES = st.text_input("PACKAGES (comma-separated):")
    HOST_PORT = st.text_input("HOST PORT:")
    CONTAINER_PORT = st.text_input("CONTAINER PORT:")
    USERNAME = st.text_input("USERNAME:")
    PASSWORD_KEY = st.text_input("PASSWORD_KEY:")
    PASSWORD_VALUE = st.text_input("PASSWORD_VALUE:", type="password")
    DOCKER_IMAGE_NAME = st.text_input("DOCKER IMAGE NAME:")
    SOURCE_VOLUME = st.text_input("Source Volume")
    CONTAINER_VOLUME = st.text_input("Container Volume")
    
    # Submit button
    if st.button("Submit"):
        # Validate inputs
        if TOOLID and OS and PACKAGES and HOST_PORT and CONTAINER_PORT and USERNAME and PASSWORD_KEY and PASSWORD_VALUE and DOCKER_IMAGE_NAME and SOURCE_VOLUME and CONTAINER_VOLUME:
            # Create the tools table if not exists
            create_tools_table(cursor)

            # Check for duplicate TOOL ID
            if toolid_exists(cursor, TOOLID):
                st.warning("TOOL ID already exists. Please choose a different TOOL ID.")
            else:
                # Insert TOOL details into the database
                insert_tools(cursor, TOOLID, OS, PACKAGES, HOST_PORT, CONTAINER_PORT, USERNAME, PASSWORD_KEY, PASSWORD_VALUE, DOCKER_IMAGE_NAME,SOURCE_VOLUME,CONTAINER_VOLUME)

                # Commit changes
                db_connection.commit()

                st.success("TOOLS added successfully.")
        else:
            st.warning("Please enter all details.")

    # Close the database connection
    db_connection.close()


###################################################################
###################################################################


###################################################################

# Function to check if a hostname already exists
def toolid_exists(cursor, TOOLID):
    query = "SELECT COUNT(*) FROM tools WHERE TOOLID = %s"
    cursor.execute(query, (TOOLID,))
    count = cursor.fetchone()[0]
    return count > 0

###################################################################


###################################################################
###################################################################

#  Streamlit app for listing host details
def list_tool_page():
    st.title("LIST TOOLS DETAILS")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Display details for all hostnames
    all_tools = get_all_tools(cursor)

    for tools in all_tools:
        TOOLID, OS, PACKAGES, HOST_PORT, CONTAINER_PORT, USERNAME, PASSWORD_KEY, PASSWORD_VALUE, DOCKER_IMAGE_NAME, SOURCE_VOLUME, CONTAINER_VOLUME = tools
        st.subheader(f"Details for TOOL ID: {TOOLID}")
        details_df = pd.DataFrame({"OS TYPE": [OS], "PACKAGES": [PACKAGES], "HOST PORT": [HOST_PORT],
                                   "CONTAINER PORT": [CONTAINER_PORT],"USERNAME": [USERNAME],
                                   "PASSWORD KEY": [PASSWORD_KEY],"PASSWORD VALUE": [PASSWORD_VALUE],
                                   "DOCKER IMAGE NAME": [DOCKER_IMAGE_NAME],"Source Volume":[SOURCE_VOLUME],"Container Volume":[CONTAINER_VOLUME]})
        st.table(details_df)

        # Delete button for each host
        delete_button = st.button(f"Delete TOOL ID: {TOOLID}")

        # When the delete button is clicked, delete the host details
        if delete_button:
            delete_toolid_details(TOOLID)
            st.success(f"TOOL ID {TOOLID} details deleted successfully.")

        st.markdown("---")  # Add a horizontal line to separate details for different hostnames

    # Close the database connection
    db_connection.close()



###################################################################
###################################################################


###################################################################

## Function to delete host details for a specific host
def delete_toolid_details(TOOLID):
    try:
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        query = "DELETE FROM tools WHERE TOOLID = %s"
        cursor.execute(query, (TOOLID,))
        db_connection.commit()

    except Exception as e:
        st.error(f"Error deleting TOOL details: {e}")

    finally:
        # Close the database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()


# Function to get server details for all hostnames
def get_all_tools(cursor):
    query = "SELECT TOOLID, OS, PACKAGES, HOST_PORT, CONTAINER_PORT, USERNAME, PASSWORD_KEY, PASSWORD_VALUE, DOCKER_IMAGE_NAME ,SOURCE_VOLUME,CONTAINER_VOLUME FROM tools"
    cursor.execute(query)
    return cursor.fetchall()

###################################################################


###################################################################
###################################################################

# Streamlit app for updating host details
def update_tools_page():
    st.title("UPDATE TOOL DETAILS")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Get the list of host IDs
    tool_ids = get_unique_toolid(cursor)

    # Dropdown to select a host ID for updating
    selected_tool_id = st.selectbox("Select TOOL ID for Update:", tool_ids)

    if selected_tool_id:
        # Display current details for the selected host
        current_details = get_tools_for_toolid(cursor, selected_tool_id)
        st.subheader(f"Current Details for TOOLID: {selected_tool_id}")
        current_details_df = pd.DataFrame({"OS": [current_details[0][0]], "PACKAGES": [current_details[0][1]],
                                            "HOST_PORT": [current_details[0][2]], "CONTAINER_PORT": [current_details[0][3]],
                                            "USERNAME": [current_details[0][4]],"PASSWORD_KEY": [current_details[0][5]],"PASSWORD_VALUE": [current_details[0][6]],
                                            "DOCKER_IMAGE_NAME": [current_details[0][7]], "SOURCE_VOLUME":[current_details[0][8]],
                                            "CONTAINER_VOLUME":[current_details[0][9]]})
        st.table(current_details_df)

        # Input fields for updating host details
        updated_OS = st.text_input("Updated Type OS:", current_details[0][0])
        updated_PACKAGES = st.text_input("Updated PACKAGE:", current_details[0][1] )
        updated_HOST_PORT = st.text_input("Updated HOST PORT:", current_details[0][2])
        updated_CONTAINER_PORT = st.text_input("Updated CONTAINER PORT:", current_details[0][3])
        updated_USERNAME = st.text_input("Updated USERNAME:", current_details[0][4])
        updated_PASSWORD_key = st.text_input("Updated PASSWORD KEY:", current_details[0][5])
        updated_PASSWORD_VALUE = st.text_input("Updated PASSWORD VALUE:", current_details[0][6],type="password")
        updated_DOCKER_IMAGE_NAME = st.text_input("Updated DOCKER IMAGE NAME:", current_details[0][7])
        update_SOURCE_VOLUME = st.text_input("Updated SOURCE VOLUME:", current_details[0][8])
        update_CONTAINER_VOLUME = st.text_input("Updated CONTAINER VOLUME:",current_details[0][9])

        # Update button
        if st.button("Update TOOL Details"):
            # Validate inputs
            if updated_OS and updated_PACKAGES and updated_HOST_PORT and updated_CONTAINER_PORT and updated_USERNAME and updated_PASSWORD_key and updated_PASSWORD_VALUE and updated_DOCKER_IMAGE_NAME and update_SOURCE_VOLUME and update_CONTAINER_VOLUME:
                # Update host details in the database
                update_tool_details(cursor, selected_tool_id, updated_OS, updated_PACKAGES,
                                    updated_HOST_PORT, updated_CONTAINER_PORT, updated_USERNAME, updated_PASSWORD_key, updated_PASSWORD_VALUE, updated_DOCKER_IMAGE_NAME, update_SOURCE_VOLUME, update_CONTAINER_VOLUME)

                # Commit changes
                db_connection.commit()

                st.success(f"TOOL ID {selected_tool_id} details updated successfully.")
            else:
                st.warning("Please enter all updated details.")

    # Close the database connection
    db_connection.close()

###################################################################
###################################################################


###################################################################

# Function to update host details for a specific host
def update_tool_details(cursor, TOOLID,updated_OS, updated_PACKAGES,updated_HOST_PORT, updated_CONTAINER_PORT, updated_USERNAME, updated_PASSWORD_key, updated_PASSWORD_VALUE, updated_DOCKER_IMAGE_NAME, update_SOURCE_VOLUME, update_CONTAINER_VOLUME):
    query = "UPDATE tools SET OS = %s, PACKAGES = %s, HOST_PORT = %s, CONTAINER_PORT = %s, USERNAME = %s, PASSWORD_KEY = %s, PASSWORD_VALUE = %s, DOCKER_IMAGE_NAME = %s , SOURCE_VOLUME = %s, CONTAINER_VOLUME = %s WHERE TOOLID = %s"
    values = (updated_OS, updated_PACKAGES, updated_HOST_PORT, updated_CONTAINER_PORT,updated_USERNAME ,updated_PASSWORD_key, updated_PASSWORD_VALUE,updated_DOCKER_IMAGE_NAME ,update_SOURCE_VOLUME, update_CONTAINER_VOLUME, TOOLID)
    cursor.execute(query, values)


###################################################################


###################################################################


###################################################################

    
# Function to check if the HOST IP ADDRESS is active
def check_host_activity(ip_address, root_username, password):
    try:
        # Connect to the server using paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=root_username, password=password)

        # Close the SSH connection
        ssh.close()

        return True  # Host is active

    except Exception as e:
        return False  # Host is not active

###################################################################

###################################################################
###################################################################

# Streamlit app for listing host details
def connected_host_details_page():
    st.title("LIST CONNECTED HOST DETAILS")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Display details for all hostnames
    all_server_details = get_all_server_details(cursor)
    
    # Get connected hosts from the host preparing page
    connected_hosts = connecting_host_page()

    for server_detail in all_server_details:
        Hostid, hostname, password, ip_address, root_username, Host_OS = server_detail
        st.subheader(f"Details for Host ID: {Hostid}")

        # Check if the host is active
        is_active = ip_address in connected_hosts
        status = "Active" if is_active else "Not Active"

        details_df = pd.DataFrame({
            "Hostname": [hostname],
            "Password": [password],
            "IP Address": [ip_address],
            "Root Username": [root_username],
            "Host OS": [Host_OS],
            "Status": [status]
        })
        st.table(details_df)

        st.markdown("---")  # Add a horizontal line to separate details for different hostnames

    # Close the database connection
    db_connection.close()
import subprocess  # Import subprocess module for executing local commands in Windows

# Function to connect to host and retrieve system details
def connecting_host_page():
    system_details_data = []
    failed_servers = []  # List to store failed IP addresses
    connected_hosts = []  # List to store connected IP addresses

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Fetch server details from the table
    sql = "SELECT Hostid, ip_address, root_username, password, Host_OS FROM server_details"
    cursor.execute(sql)
    servers = cursor.fetchall()

    # Create a multiselect list with host IDs and corresponding IP addresses
    selected_host_ids = st.multiselect("Select Host IDs:", [f"{host_id} - {ip_address}" for host_id, ip_address, _, _, _ in servers])

    # Loop through selected hosts
    for selected_id in selected_host_ids:
        # Extract the selected host ID and IP address
        selected_host_id, selected_ip_address = selected_id.split(" - ")

        # Find the corresponding username, password, and OS from the database
        selected_servers = [server for server in servers if str(server[0]) == selected_host_id]

        if selected_servers:
            host_id, ip_address, root_username, password, host_os = selected_servers[0]

            # Connect to the server using paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            system_details_output = ""  # Initialize system_details_output

            try:
                # Attempt to connect to the server
                ssh.connect(ip_address, username=root_username, password=password)
                

                # Execute commands based on the host's operating system
                if host_os.lower() == "linux":
                    # Execute Linux commands
                    
                    system_details_output = execute_linux_commands(ssh)
                elif host_os.lower() == "windows":
                    # Execute Windows commands
                    
                    system_details_output = execute_windows_commands(ssh)

                # Determine the status based on the success of commands execution
                status = "Success" if system_details_output else "Failed"

                # Accumulate data for multiple servers
                system_details_data.append({
                    "IP Address": ip_address,
                    "System Details": system_details_output,
                    "Status": status
                })

                # If successful, add the IP address to the list of connected hosts
                connected_hosts.append(ip_address)

            except Exception as e:
                # Error connecting to the host, add IP address to failed servers
                failed_servers.append(ip_address)
                st.error(f"Error connecting to {selected_ip_address}: {str(e)}")

            finally:
                # Close the SSH connection
                ssh.close()

    # Display accumulated system details in a DataFrame
    #details_df = pd.DataFrame(system_details_data)
    #st.dataframe(details_df)


    # Display IP addresses of failed servers
    if failed_servers:
        st.warning("Failed to establish connection with the following IP addresses:")
        st.write(failed_servers)
   

    # Return the list of connected hosts
    return connected_hosts

# Function to execute Linux commands and retrieve system details
def execute_linux_commands(ssh):
    # Initialize system_details_output
    system_details_output = ""

    # Configure user permissions for Docker (before Docker installation)
    user_permissions_commands = [
        "sudo usermod -aG docker $USER",        # Add user to "docker" group
        "sudo chmod 666 /var/run/docker.sock"    # Check Docker Daemon Socket Permissions
    ]

    for cmd in user_permissions_commands:
        _, stdout, stderr = ssh.exec_command(cmd)
        # You can check the output or handle errors if needed

    # Install Docker
    install_docker_command = "curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh"
    ssh.exec_command(install_docker_command)
    # Wait for the installation to complete
    ssh.exec_command("wait")

    # Get system details after Docker installation
    system_details_command = "uname -a && docker --version"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(system_details_command)
    system_details_output = ssh_stdout.read().decode()

    return system_details_output

# Function to execute Windows commands and retrieve system details
def execute_windows_commands(ssh):
    # Initialize system_details_output
    system_details_output = ""

    # Execute command to retrieve IP address in Windows
    ipconfig_command = "ipconfig"
    stdin, stdout, stderr = ssh.exec_command(ipconfig_command)
    system_details_output = stdout.read().decode()

    # Print output and error messages for debugging
    print("Output:", system_details_output)
    print("Error:", stderr.read().decode())

    return system_details_output

# Function to get server details for all hostnames
def get_all_server_details(cursor):
    query = "SELECT Hostid, hostname, password, ip_address, root_username, Host_OS FROM server_details"
    cursor.execute(query)
    return cursor.fetchall()


###################################################################
###################################################################



###################################################################




###################################################################
###################################################################

# Streamlit app for creating environment
def create_environment_page():
    st.title("CREATE ENVIRONMENT")

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Fetch Faculty Request details from faculty_requests table
    faculty_requests = get_pending_faculty_requests(cursor)

    # Create a list of entries for the dropdown
    dropdown_options = [f"{course_name} - {subject} - ID: {request_id}" for request_id, course_name, subject, *_ in faculty_requests]

    # Display a dropdown to select Faculty Request
    selected_faculty_request = st.selectbox("Select Faculty Request:", dropdown_options)

    # Extract details from the selected entry
    parts = selected_faculty_request.split(" - ")
    selected_course_name = parts[0]
    selected_subject = parts[1]
    selected_faculty_request_id = parts[2].split(":")[1].strip()

    # Fetch OS type and required tools based on the selected Faculty Request ID
    os_type, required_tools = get_os_and_tools_for_faculty_request(cursor, selected_faculty_request_id)

    # Display OS type and required tools
    st.text(f"Course Name: {selected_course_name}")
    st.text(f"Subject: {selected_subject}")
    st.text(f"OS Type: {os_type}")
    st.text(f"Required Tools: {', '.join(required_tools)}")

    # Fetch matching tool details based on OS type and required tools
    matching_tool = get_matching_tool(cursor, os_type, required_tools)

    print("Matching Tool Details:", matching_tool)

    # Display matching tool ID
    if matching_tool:
        TOOLID, _, _, _, _, _, _, _, docker_image_name,_,_  = matching_tool

        print("Docker Image Name:", docker_image_name)


        # Display matching tool ID
        st.text(f"Matching Tool ID: {TOOLID}")

        # Display details of the matching tool ID
        if docker_image_name:
            st.text(f"Docker Image Name: {docker_image_name}")
        

            # Fetch NUM_SYS_REQ from faculty_requests for the selected Faculty Request ID
            num_sys_req = get_num_sys_req_for_faculty_request(cursor, selected_faculty_request_id)
            st.text(f"System Requested by Faculty (NUM_SYS_REQ): {num_sys_req}")

            # Fetch IP addresses and hostnames from host_details where the count of IP addresses is equal to NUM_SYS_REQ
            ip_addresses, hostnames = get_ip_addresses_for_num_sys_req(cursor, num_sys_req)

            # Display IP addresses and hostnames
            st.text("IP Addresses:")
            st.text(', '.join(ip_addresses))

            st.text("Hostnames:")
            st.text(', '.join(hostnames))

            # Button to create environment
            create_env_button = st.button("Create Environment")

            if create_env_button:
                for ip_address in ip_addresses:
                    # Establish SSH connection and execute commands
                    establish_ssh_connection_and_create_container(
                        ip_address, TOOLID, 
                        selected_course_name, selected_subject, selected_faculty_request_id
                    )

            
        else:
            st.warning("No details found for the matching tool ID.")
    else:
        st.warning("No matching tool found for the specified OS type and required tools.")

    # Close the database connection
    db_connection.close()

###################################################################
###################################################################


###################################################################

import random
# Function to establish SSH connection and create Docker container
def establish_ssh_connection_and_create_container(
    ip_address, selected_tool_id, 
    course_name, subject, faculty_request_id
):
    try:
        # Connect to the database to fetch SSH and Docker details
        db_connection = connect_to_database()
        cursor = db_connection.cursor()


        # Record start time
        start_time = time.time()

        # Fetch SSH and root password details from server_details table
        ssh_query = "SELECT root_username, password FROM server_details WHERE ip_address = %s"
        cursor.execute(ssh_query, (ip_address,))
        ssh_result = cursor.fetchone()

        if ssh_result:
            root_username, root_password = ssh_result

            # Connect to the server using paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_address, username=root_username, password=root_password)

            # Commands for setting up Docker permissions
            user_permissions_commands = [
                f"echo {root_password} | sudo -S usermod -aG docker $USER",        # Add user to "docker" group
                f"echo {root_password} | sudo -S chmod 666 /var/run/docker.sock"    # Check Docker Daemon Socket Permissions
            ]

            for cmd in user_permissions_commands:
                _, stdout, stderr = ssh.exec_command(cmd)
                # Read and print the output
                output = stdout.read().decode()
                print(output)
                # Read and print the error (if any)
                error = stderr.read().decode()
                print(error)
                # You can check the output or handle errors if needed

            # Before executing the SQL query
            print("TOOLID to fetch Docker image:", selected_tool_id)    

            # Fetch Docker details from tools table based on matching tool_id
            docker_query = "SELECT OS, PACKAGES, HOST_PORT, CONTAINER_PORT, USERNAME, PASSWORD_KEY, PASSWORD_VALUE, DOCKER_IMAGE_NAME , SOURCE_VOLUME, CONTAINER_VOLUME FROM tools WHERE TOOLID = %s"
            cursor.execute(docker_query, (selected_tool_id,))
            docker_result = cursor.fetchone()

            if docker_result:
                os_type, packages, host_port, container_port, docker_username, password_key, password_value, docker_image_name , source_volume, container_volume = docker_result

                # Print the Docker image name fetched from the database
                print("Docker Image Name from Database:", docker_image_name)

                # Generate a unique container name (e.g., using timestamp)
                container_name = f"MSIS_container_{int(time.time())}"

                # Choose a unique port for each container (e.g., using timestamp)
                unique_port = 1000 + int(time.time()) % 5000

                # Generate a random 4-digit number
                random_number = random.randint(1000, 9999)

                #unique name for source volume name()
                source_volume_loc =  f"{source_volume}{random_number}"

                # Print the Docker image name before running the Docker command
                print("Docker Image Name:", docker_image_name)

                # Print the Docker image password before running the Docker command
                print("Docker Image password Key:", password_key)

                # Print the Docker image password before running the Docker command
                print("Docker Image password Value:", password_value)


                # Command to run Docker container
                docker_command = f"docker run --name {container_name} -d -it -p {unique_port}:{container_port} -v {source_volume_loc}:{container_volume} -e {password_key}={password_value} {docker_image_name}"
                                

                # Print the Docker run command before executing it
                print("Docker Run Command:", docker_command)

                _, stdout, stderr = ssh.exec_command(docker_command)
                # Read and print the output
                docker_output = stdout.read().decode()
                print(docker_output)
                # Read and print the error (if any)
                docker_error = stderr.read().decode()
                print(docker_error)

                #Record End Time
                end_time = time.time()

                # Calculate duration
                duration = end_time - start_time

                # Output duration
                print("Execution Time:", duration, "seconds")




                st.success(f"Docker container created on {ip_address} with ID: {docker_output}")

                # Call insert_container_details to insert container details into the database
                insert_container_details(db_connection, cursor, ip_address, f"http://{ip_address}:{unique_port}", docker_image_name, packages, password_value, course_name, subject, faculty_request_id,source_volume_loc, docker_output)
                


            else:
                st.error(f"No Docker details found for {ip_address}. Please check tools table.")

        else:
            st.error(f"No SSH details found for {ip_address}.")

    except Exception as e:
        st.error(f"Error establishing SSH connection and creating Docker container on {ip_address}: {str(e)}")

        

        
        
 
         
        


    finally:
        # Close the SSH connection and database connection
        ssh.close()
        db_connection.close()





def get_ip_addresses_for_num_sys_req(cursor, num_sys_req):
    try:
        # Fetch all IP addresses and hostnames from server_details
        query_all = "SELECT ip_address, hostname FROM server_details"
        cursor.execute(query_all)
        all_results = cursor.fetchall()
        
        # If there are no results, return empty lists
        if not all_results:
            return [], []

        # If the number of system requirements is greater than available entries,
        # repeat the IP addresses and hostnames until the requirement is fulfilled
        repeated_results = []
        while len(repeated_results) < num_sys_req:
            repeated_results.extend(all_results)

        # Extract IP addresses and hostnames based on the number of system requirements
        ip_addresses = [row[0] for row in repeated_results[:num_sys_req]]
        hostnames = [row[1] for row in repeated_results[:num_sys_req]]

        return ip_addresses, hostnames

    except Exception as e:
        st.error(f"Error fetching IP addresses: {e}")
        return [], []







# Function to get NUM_SYS_REQ for the selected Faculty Request ID
def get_num_sys_req_for_faculty_request(cursor, faculty_request_id):
    query = "SELECT NUM_SYS_REQ FROM faculty_requests WHERE REQUEST_ID = %s"
    cursor.execute(query, (faculty_request_id,))
    result = cursor.fetchone()
    return result[0] if result else None



# Function to get details of the matching tool ID
def get_tool_details(cursor, tool_id):
    query = "SELECT TOOLID, OS, PACKAGES, HOST_PORT, CONTAINER_PORT, USERNAME, PASSWORD_KEY, PASSWORD_VALUE, DOCKER_IMAGE_NAME FROM tools WHERE TOOLID = %s"
    cursor.execute(query, (tool_id,))
    return cursor.fetchone()   

# Function to get matching tool details based on OS type and required tools
def get_matching_tool(cursor, os_type, required_tools):
    query = "SELECT TOOLID FROM tools WHERE OS = %s AND PACKAGES = %s"
    cursor.execute(query, (os_type, ', '.join(required_tools)))
    result = cursor.fetchone()

    if result:
        tool_id = result[0]
        tool_query = "SELECT * FROM tools WHERE TOOLID = %s"
        cursor.execute(tool_query, (tool_id,))
        return cursor.fetchone()
    else:
        return None 


# Function to get matching tool ID based on OS type and required tools
def get_matching_tool_id(cursor, os_type, required_tools):
    query = "SELECT TOOLID FROM tools WHERE OS = %s AND PACKAGES = %s"
    cursor.execute(query, (os_type, ', '.join(required_tools)))
    result = cursor.fetchone()

    # If the result is found, return the matching tool ID, else return None
    if result:
        return result[0]
    else:
        return None


# Function to get OS type and required tools for a Faculty Request ID
def get_os_and_tools_for_faculty_request(cursor, faculty_request_id):
    query = "SELECT OS_TYPE, REQUIRED_TOOLS FROM faculty_requests WHERE REQUEST_ID = %s"
    cursor.execute(query, (faculty_request_id,))
    result = cursor.fetchone()

    # If the result is found, unpack the values, else return None
    if result:
        os_type, required_tools_str = result
        required_tools = required_tools_str.split(', ') if required_tools_str else []
        return os_type, required_tools
    else:
        return None, []

# Function to get Faculty Request IDs from faculty_requests table
def get_faculty_request_ids(cursor):
    query = "SELECT REQUEST_ID FROM faculty_requests"
    cursor.execute(query)
    faculty_request_ids = [row[0] for row in cursor.fetchall()]
    return faculty_request_ids

# Function to get pending faculty requests
def get_pending_faculty_requests(cursor):
    try:
        # Fetch faculty requests where the request ID is not present in the CONTAINER_DETAILS table
        query = """
            SELECT REQUEST_ID, Course_name, Subject, Faculty_ID, NUM_SYS_REQ, 
               OS_TYPE, REQUIRED_TOOLS, 
               CONCAT(START_DATE, ' ', START_TIME) AS START_DATETIME, 
               CONCAT(END_DATE, ' ', END_TIME) AS END_DATETIME, 
               REQUEST_DATETIME 
        FROM faculty_requests 
            WHERE REQUEST_ID NOT IN (SELECT FACULTY_REQUEST_ID FROM CONTAINER_DETAILS)
            """
        cursor.execute(query)
        return cursor.fetchall()

    except Exception as e:
        st.error(f"Error fetching pending faculty requests: {e}")
        return []

###################################################################




###################################################################
###################################################################


###################################################################
###################################################################



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
        container_df = pd.DataFrame(container_details, columns=["IP Address", "URL", "Docker Image Name", "Package", "Password", "Course", "subject", "Faculty request ID","Source volume location", "CONTAINER ID"])
        # Format the 'URL' column as a hyperlink
        container_df['URL'] = container_df.apply(lambda row: f'<a href="{row["URL"]}" target="_blank">{row["URL"]}</a>', axis=1)

        # Display the table with HTML in the 'URL' column
        st.write(container_df.to_html(escape=False), unsafe_allow_html=True)
    
    else:
        st.warning("No container details found.")

    # Close the database connection
    db_connection.close()

    # Section for stopping Docker container
    st.header("Stop Docker Container")
    faculty_request_id = st.text_input("Enter Faculty Request ID:")
    stop_button = st.button("Stop Container")

    if stop_button:
        stop_containers_by_faculty_id(faculty_request_id)

    # Section for deleting container details
    st.header("Delete Container Details")
    faculty_request_id_delete = st.text_input("Enter Faculty Request ID:", key="delete_input")
    delete_button = st.button("Delete Container Details", key="delete_button")

    if delete_button:
        delete_container_details_by_faculty_id(faculty_request_id_delete)
    






###################################################################
###################################################################
###################################################################

# Create the 'CONTAINER_DETAILS' table if it doesn't exist
def create_container_details_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CONTAINER_DETAILS (
            IP_ADDRESS VARCHAR(15) ,
            CONTAINER_ID VARCHAR(255),
            URL VARCHAR(255),
            DOCKER_IMAGE_NAME VARCHAR(255),
            PACKAGE VARCHAR(255),
            PASSWORD VARCHAR(255),
            COURSE VARCHAR(255),
            SUBJECT VARCHAR(255),
            SOURCE_VOLUME_LOCATION  VARCHAR(255),
            FACULTY_REQUEST_ID INT
        )
    """)


# Function to insert container details into the CONTAINER_DETAILS table
def insert_container_details(db_connection, cursor, ip_address, url, docker_image_name, packages, password_value, course_name, subject, faculty_request_id, source_volume_loc, docker_output):
    try:
        query = """
            INSERT INTO CONTAINER_DETAILS 
            (IP_ADDRESS, URL, DOCKER_IMAGE_NAME, PACKAGE, PASSWORD, COURSE,SUBJECT, FACULTY_REQUEST_ID, SOURCE_VOLUME_LOCATION, CONTAINER_ID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with cursor as cursor:
            cursor.execute(query, (ip_address, url, docker_image_name, packages, password_value, course_name, subject, faculty_request_id, source_volume_loc, docker_output))
            db_connection.commit()
        st.success("Container details inserted successfully.")
    except Exception as e:
        db_connection.rollback()
        st.error(f"Error inserting container details: {e}")


# Function to get container details from the containers table
def get_container_details(cursor):
    try:
        # Fetch container details from the containers table
        query = "SELECT IP_ADDRESS, URL, DOCKER_IMAGE_NAME, PACKAGE, PASSWORD, COURSE, SUBJECT, FACULTY_REQUEST_ID ,SOURCE_VOLUME_LOCATION , CONTAINER_ID FROM CONTAINER_DETAILS ORDER BY FACULTY_REQUEST_ID DESC"
        cursor.execute(query)
        container_details = cursor.fetchall()

        # Return the container details
        return container_details

    except Exception as e:
        st.error(f"Error fetching container details: {e}")
        return []


import subprocess


# Function to stop Docker containers based on faculty request ID
def stop_containers_by_faculty_id(faculty_request_id):
    try:
        # Connect to the database to fetch container details
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        # Fetch SSH and root password details from server_details table
        ssh_query = "SELECT ip_address, root_username, password FROM server_details"
        cursor.execute(ssh_query)
        ssh_results = cursor.fetchall()

        for ip_address, root_username, root_password in ssh_results:
            # Connect to the server using paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_address, username=root_username, password=root_password)

            # Fetch container ID based on faculty request ID
            query = "SELECT CONTAINER_ID FROM CONTAINER_DETAILS WHERE FACULTY_REQUEST_ID = %s"
            cursor.execute(query, (faculty_request_id,))
            container_ids = cursor.fetchall()

            for container_id_row in container_ids:
                container_id = container_id_row[0].strip()  # Remove leading/trailing whitespace and newline characters

                # Command to stop Docker container
                stop_command = f"docker stop {container_id}"

                # Execute the command
                _, stdout, stderr = ssh.exec_command(stop_command)
                # Read and print the output
                output = stdout.read().decode()
                print(output)
                # Read and print the error (if any)
                error = stderr.read().decode()
                print(error)

            ssh.close()
            
        st.success(f"All Docker containers with Faculty Request ID {faculty_request_id} stopped successfully.")
        
    except Exception as e:
        st.error(f"Error stopping Docker containers: {str(e)}")

    finally:
        # Close the database connection
        db_connection.close()




# Function to delete container details based on faculty request ID
def delete_container_details_by_faculty_id(faculty_request_id):
    try:
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        # Delete container details based on faculty request ID from CONTAINER_DETAILS table
        delete_container_query = "DELETE FROM CONTAINER_DETAILS WHERE FACULTY_REQUEST_ID = %s"
        cursor.execute(delete_container_query, (faculty_request_id,))
        db_connection.commit()

        # Delete faculty request based on faculty request ID from faculty_requests table
        delete_faculty_query = "DELETE FROM faculty_requests WHERE REQUEST_ID = %s"
        cursor.execute(delete_faculty_query, (faculty_request_id,))
        db_connection.commit()

        st.success(f"Container details and Faculty Request with ID {faculty_request_id} deleted successfully.")
        
    except Exception as e:
        st.error(f"Error deleting container details and Faculty Request: {str(e)}")

    finally:
        # Close the database connection
        db_connection.close()



###################################################################

###################################################################



# Main Streamlit app to switch between  pages
def main():
    page = st.sidebar.radio("Select Page:", ["Data Entry", "LIST HOST DETAILS","UPDATE HOST DETAILS",
                                             "ALL FACULTY DETAILS","UPDATE FACULTY DETAILS","ALL STUDENT DETAILS",
                                             "UPDATE STUDENT DETAILS","Course Data Entry", "Subject Data Entry", 
                                             "List Subject Details","FACULTY REQUESTS",
                                             "TOOL Data Entry", "LIST TOOL DETAILS","UPDATE TOOLS DETAILS","HOST PREPARING",
                                             "CREATE ENVIRONMENT","ENVIRONMENT DETAIL"])

    if page == "Data Entry":
        data_entry_page()
    elif page == "LIST HOST DETAILS":
        list_host_details_page()
    elif page == "UPDATE HOST DETAILS":
        update_host_details_page()    
    elif page == "ALL FACULTY DETAILS":
        list_faculty_details_page()  
    elif page == "UPDATE FACULTY DETAILS" :
        update_faculty_details_page ()   
    elif page == "ALL STUDENT DETAILS":
        list_student_details_page() 
    elif page == "UPDATE STUDENT DETAILS" :
        update_student_details_page()
    elif page == "Course Data Entry":
        course_data_entry_page()
    elif page == "Subject Data Entry":
        subject_data_entry_page()
    elif page == "List Subject Details":
        list_subject_details_page()           
    elif page == "FACULTY REQUESTS":
        faculty_requests_page()
    elif page == "TOOL Data Entry":
        tool_data_entry_page()
    elif page == "LIST TOOL DETAILS":
        list_tool_page()
    elif page == "UPDATE TOOLS DETAILS":
        update_tools_page()
    elif page == "HOST PREPARING":
        connected_host_details_page()
    elif page == "HOST PREPARING33":
        connecting_host_page() 
    elif page == "CREATE ENVIRONMENT":
        create_environment_page()
    elif page == "ENVIRONMENT DETAIL":
        container_detail_page()
           

if __name__ == "__main__":
    main()
