import subprocess
from bash import bash
import os
import gc

def run_auto_tests(auto_tests, auto_tests_input, auto_tests_display):
    for x in range(0, len(auto_tests)):
        print(auto_tests_display[x])
        run_subprocess(auto_tests[x], auto_tests_input[x], auto_tests_display[x])
        
    print("")

def run_subprocess(test, test_input, test_display):
    try:
        if test[0] == "SUB":
            args = [test[i] for i in range(1,len(test))]
            print(args)
            if test_input == "":
                print("running with no input")
                subprocess.run(args, encoding='utf8')
            else:
                subprocess.run(args, input=test_input, encoding='utf8')
        else:
            print(bash(test_display))
    except:
        print("invalid command")

def parse_line(line):
    x = 0
    test = []
    cur_test = ""
    test_input = ""
    while x < len(line) and line[x] != "{":
        if cur_test != "" and line[x] == " ":
            test.append(cur_test)
            cur_test = ""
        else:
            cur_test += line[x]
        x+=1
    x+=1
    if cur_test != "":
        test.append(cur_test)
    while x < len(line) and line[x] != "}":
        if line[x] == ",":
            test_input += "\n"
        else:
            test_input += line[x]
        x+=1
    return test, test_input

def load_auto_tests(prefix):
    #get auto grade commands
    auto_tests = []
    auto_tests_input = []
    auto_tests_display = []
    try:
        with open(prefix + "autoTests.txt", "r") as auto_grade_file:
            for line in auto_grade_file:
                if line[0] != "#" and line != "":
                    print(line)
                    try:
                        my_line = line.replace("\n", "")
                        test, test_input = parse_line(my_line)
                        auto_tests.append(test)
                        auto_tests_input.append(test_input)
                        auto_tests_display.append(my_line)
                    except:
                        print("line misformatted")
        print(auto_tests, auto_tests_input)
        return auto_tests, auto_tests_input, auto_tests_display
    except:
        try:
            #copies template to new spot
            bash("cp " + prefix + "../../autoTestsTemplate.txt " + prefix + "autoTests.txt")
            return [], [], []
        except:
            print("Problem with autoTest.txt file path")
            return [], [], []

def get_last_viewed_student():
    try:
        with open("assignmentMetaData.txt", "r") as my_file:
            x = ""
            for line in my_file:
                if line[0] == "l":
                    i = 2
                    while line[i] != "}":
                        x += line[i]
                        i+=1
        return int(x)
    except:
        set_last_viewed_student(0)
        return 0

def set_last_viewed_student(x):
    with open("assignmentMetaData.txt", "w") as my_file:
        my_file.write("l{" + str(x) + "}")

def main():
    #asks which class to grade for

    #get class directories
    directories = []
    for osobj in os.scandir("."):
        if osobj.is_dir():
            directories.append(osobj.path)

    #ask for user input:
    for x in range(0, len(directories)):
        print(x, ") ", directories[x], sep="")
    bad_input = True
    while (bad_input):
        try:
            directory_index = int(input("\nPlease select a class directory: "))
            if (directory_index > -1 and directory_index < len(directories)):
                bad_input = False
            else:
                print("\nIndex out of range\n")
        except:
            print("\nNot a number\n")

    os.chdir(directories[directory_index])

    #asks which assignment to grade

    #get class directories
    directories = []
    for osobj in os.scandir("."):
        if osobj.is_dir():
            directories.append(osobj.path)

    #ask for user input:
    for x in range(0, len(directories)):
        print(x, ") ", directories[x], sep="")
    bad_input = True
    while (bad_input):
        try:
            directory_index = int(input("\nPlease select an assignment directory: "))
            if (directory_index > -1 and directory_index < len(directories)):
                bad_input = False
            else:
                print("\nIndex out of range\n")
        except:
            print("\nNot a number\n")

    os.chdir(directories[directory_index])

    #gather all student dirs
    directories = {}
    directory_names = []
    for osobj in os.scandir("."):
        if osobj.is_dir():
            directory_names.append(osobj.name)
            directories[osobj.name] = osobj

    directory_names = sorted(directory_names)

    gc.collect()

    #asks to start grading from the front or the back
    print("0) Start grading from top")
    print("1) Start grading from bottom")
    print("2) Start from last save")
    bad_input = True
    while (bad_input):
        try:
            grade_order = int(input("What order would you like to grade in: "))
            if grade_order == 0:
                start_index = 0
                bad_input = False
            elif grade_order == 1:
                start_index = len(directories) - 1
                bad_input = False
            elif grade_order == 2:
                start_index = get_last_viewed_student()
                bad_input = False
            else:
                print("\nIndex out of range\n")
        except:
            print("\nNot a number\n")


    auto_tests, auto_tests_input, auto_tests_display = load_auto_tests("")
            
    #iterate through all student directories in specified order
        #runs an automated portion specified in a file called autoTests.txt whcih is in the assignment dir
        #gives the user time to do manual tests
        #moves on to next student

    user_input = ""
    min_index = 0
    max_index = len(directories) - 1
    x = start_index
    while (x >= min_index and x <= max_index) and user_input != "q":
        name = directory_names[x]
        os.chdir(directories[name].path)
        print("\n#####################################")
        print("Viewing submission for:", name, end="\n\n")
        print("Running auto tests:")
        run_auto_tests(auto_tests, auto_tests_input, auto_tests_display)
        user_input = ""
        while user_input != "n" and user_input != "b" and user_input != "q":
            if user_input == "t":
                user_input = ""
                #in the auto tests cli
                while user_input != "q":
                    print("a: rerun all test commands\nl: reload auto tests")
                    for y in range(0, len(auto_tests_display)):
                        print(str(y) + ": " + auto_tests_display[y])
                    user_input = input("auto_tests# ")
                    if user_input == "a":
                        run_auto_tests(auto_tests, auto_tests_input, auto_tests_display)
                    elif user_input == "l":
                        auto_tests, auto_tests_input, auto_tests_display = load_auto_tests("../")
                    else:
                        try:
                            run_subprocess(auto_tests[int(user_input)], auto_tests_input[int(user_input)], auto_tests_display[int(user_input)])
                        except:
                            print("command not recognized")
            else:
                #if user enters command other than the custom commands, run as a bash command
                try:
                    test, test_input = parse_line(user_input)
                    run_subprocess(test, test_input, user_input)
                except:
                    print("problem with command")
            print("\nInput bash command or (\n'n' to go to next student, \n'b' to go to previous student, \n'q' to stop grading, \n't' to go to auto tests)")
            user_input = input("/" + name + "# ")
        os.chdir("..")
        if user_input == "n":
            x += 1
        else:
            x -= 1
        set_last_viewed_student(x)


if __name__ == "__main__":
    main()
