from bash import bash
import requests
import os

def main():
    #base url path for all get requests_
    BASE_URL = "https://canvas.instructure.com/api/v1"

    #retrieve canvas access key
    with open("canvasAccessKey.txt", "r") as file:
        for line in file:
            access_token = line

    #params used for all get requets
    PARAMS = {
        'access_token': access_token,
        'per_page': "200"}

    #get courses
    URL = BASE_URL + "/courses"
    r = requests.get(URL, PARAMS)
    courses = r.json()

    #display courses
    for x in range (0, len(courses)):
        try:
            print("[", x, "] ", courses[x]["name"], sep="")
        except:
            continue

    #revcieve course index from user
    bad_input = True
    while (bad_input):
        try:
            course_index = int(input("\nPlease select a course: "))
            if (course_index > -1 and course_index < len(courses)):
                bad_input = False
            else:
                print("\nIndex out of range\n")
        except:
            print("\nNot a number\n")

    #establish course id for session
    course_id = str(courses[course_index]["id"])

    #create folder for course
    course_dir = courses[course_index]["name"].replace(" ", "_")
    try:
        os.mkdir(course_dir)
    except:
        pass

    #get assignments
    URL = BASE_URL + "/courses/" + course_id + "/assignments"
    r = requests.get(URL, PARAMS)
    assignments = r.json()

    #display assignments
    for x in range (0, len(assignments)):
        print("[", x, "] ", assignments[x]["name"], sep="")

    #recieve assignment index from user
    bad_input = True
    while (bad_input):
        try:
            assignment_index = int(input("\nPlease select an assignment to download: "))
            if (assignment_index > -1 and assignment_index < len(assignments)):
                bad_input = False
            else:
                print("\nIndex out of range\n")
        except:
            print("\nNot a number\n")

    #establish assignment id for session
    assignment_id = str(assignments[assignment_index]["id"])

    #create directory to hold submissions for this assignment
    assignment_dir = assignments[assignment_index]["name"].replace(" ", "_")
    try:
        #fails if directory already exists
        os.mkdir(course_dir + "/" + assignment_dir)
        bash("cp autoTestsTemplate.txt " + course_dir + "/" + assignment_dir + "/autoTests.txt")
    except:
        pass

    #get students 
    URL = BASE_URL + "/courses/" + course_id + "/students"
    r = requests.get(URL, PARAMS)
    students = r.json()

    set_file_name = input("set filename for all downloaded files (leave blank for default name): ")


    #Iterate through all students in section
    for student in students:
        #print(student)

        #get a student's submission
        student_id = str(student["id"])
        URL = BASE_URL + "/courses/" + course_id + "/assignments/" + assignment_id + "/submissions/" + student_id
        r = requests.get(URL, PARAMS)
        submission = r.json()
        
        #create a directory for students submission
        #print(student)
        student_name = str(student["sortable_name"])
        fileName = student_name
        try:
            os.mkdir(course_dir + "/" + assignment_dir + "/" + fileName)
        except:
            pass

        #put all attachments for student submission in their directoy
        try:
            for x in range(0, len(submission["attachments"])):
                attachment = submission["attachments"][x]
                if set_file_name == "":
                    submission_file_name = attachment["filename"]
                else:
                    submission_file_name = set_file_name
                with open("./" + course_dir + "/" + assignment_dir + "/" + fileName + "/" + submission_file_name, 'wb') as file:
                    r = requests.get(attachment["url"])
                    file.write(r.content)
                    print("success")
        except:
            #There are no submission attachments
            continue

if __name__ == "__main__":
    main()