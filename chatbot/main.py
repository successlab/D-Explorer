
import shutil


import os
from alexa_chatbot_gpt import ChatWithAlexa
from openaiutils import ManualEnableException
import sys

def count_files(folder_path):
    """Counts the number of files in a given folder.

    Args:
        folder_path: The path to the folder.

    Returns:
        The number of files in the folder.
    """
    count = 0
    try:
        for item in os.listdir(folder_path):
            path = os.path.join(folder_path, item)  # Create full path
            if os.path.isfile(path):  # Check if it's a file
                count += 1
        return count
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
        return 0  # Or raise an exception if you prefer
    except NotADirectoryError:
        print(f"Error: '{folder_path}' is not a directory.")
        return 0
    except Exception as e: #Catch other potential errors
        print(f"An error occurred: {e}")
        return 0


def makeFileSystem(name, newDirName):

    newPath = newDirName
    shutil.copytree(name,
                newPath,
                ignore=ignore_files)

def ignore_files(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

def writeResults(sourceName, destName, fileName, stringList):
    newPathName = os.path.join(destName, fileName)
    newPathName = (os.path.splitext(newPathName)[0])
    newPathName = newPathName + "_results.txt"
    g = open(newPathName, 'w')
    stringlist_tuple = stringList[-1]
    conversation = stringlist_tuple[0]
    urls = stringlist_tuple[1]
    for item in conversation:
        g.write(str(item))
        g.write("\n")
    
    g.write("\n\nURLs:\n")
    for item in urls:
        g.write(str(item) )
        g.write("\n")

def main():

    if len(sys.argv) > 1:
        invocations_directory = "invocations/" + sys.argv[1]
        result_directory = "alexa_chat_results/" + sys.argv[1]
    else:
        invocations_directory = "invocations/"
        result_directory = "alexa_chat_results/"
    if len(sys.argv) > 2:
        starting_letter = sys.argv[2]
    else:
        starting_letter = None
   

    username = 'username'
    password = 'password'
    urlin = 'https://developer.amazon.com/alexa/console/ask/test/your_instance/'

    # go through each file, read in line by line, run the commands


    newDirName = "alexa_chat_results"
    ### make the directory if it does not exist
    try:
        shutil.rmtree(newDirName)
    except Exception:
        print ("No file created for " + newDirName)
    makeFileSystem(invocations_directory, newDirName)

    timecount = 0
    namecount = 0
    namecount_old = 0


    xchat = ChatWithAlexa(urlin, username, password)
    xchat.start_browser()
    #time.sleep(10)

    for root, dirs, files in os.walk(invocations_directory):
        executionCount = count_files(result_directory)
        print(root)
        for name in files:
            max_file_complete_fails = 20
            timecount = 0
            xchat.stringList = []
            if starting_letter:
                if not name.lower().startswith(starting_letter):
                    continue
            if (name != ".DS_Store"):
                oldPathName = os.path.join(root, name)
                dirname = root.split(os.path.sep)[-1]
                # This is not accurate if you are running multiple instances, but it's a decent metric.
                print( f"Now crawling {name} in category {dirname}. {(executionCount/len(files))*100}% of category completed")
                newPathName = os.path.join (newDirName, dirname)
                f = open(oldPathName, 'r')
                Lines = f.readlines()
                finalPathName = os.path.join(newPathName, name)
                finalPathName = (os.path.splitext(finalPathName)[0])
                finalPathName = finalPathName + "_results.txt"
                if not os.path.exists(finalPathName):
                    try:
                        xchat.chat_with_alexa(Lines)
                        writeResults(oldPathName,newPathName,name, xchat.stringList)
                        xchat.browser.refresh()
                        executionCount+=1
                    except ManualEnableException:
                        # refresh to get new interaction instance. This removes old conversations and resource interactions.
                        xchat.browser.refresh()
                        continue
                    except Exception as e:
                        print("Exception:")
                        print(e)
                        timecount += 1
                        print(name)
                        print(Lines)
                        if (timecount >= len(Lines)):
                            namecount +=1

                                    
            # Stops execution on multiple crashes.
            if(namecount-namecount_old >= max_file_complete_fails):
                while(True):
                    continue_code = input("Continue? Yes/No   ")
                    if (continue_code == "No"):
                        quit()
                    elif(continue_code == "Yes"):
                        print("Continuing...")
                        namecount_old = namecount
                        break
                    else:
                        print("Incorrect Input")
    xchat.browser.close()


if __name__ == "__main__":
    main()