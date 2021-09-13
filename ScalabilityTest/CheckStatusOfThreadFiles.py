import os
import math

n_cycles = 20  # Queries
n_threads = 30  # 30 Threads for each Query or Cycle

OUTPUT_DIRECTORY = "C:\\Users\\rkundeti\\Desktop\\"

is_every_thread_size_greater_than_one_KB = True

for cycleNumber in range(0, n_cycles):
    cycleFoldarPath = OUTPUT_DIRECTORY + str(cycleNumber)
    if os.path.isdir(cycleFoldarPath):
        for threadNumber in range(1, n_threads+1):
            threadFilePath = cycleFoldarPath + "\\Thread_" + str(threadNumber) + ".csv"
            if os.path.isfile(threadFilePath):
                fileSize = math.ceil(os.stat(threadFilePath).st_size / 1000)    # Convert bytes to KBs
                print("Cycle : " + str(cycleNumber) + " | Thread : " + str(threadNumber) + " | Size : " + str(fileSize) + " KB")
                if fileSize <= 1:
                    is_every_thread_size_greater_than_one_KB = False
                    break
    if is_every_thread_size_greater_than_one_KB == False:
        break

if is_every_thread_size_greater_than_one_KB == False:
    print("One/more of the Thread Files didn't recieve any data as it's/their file size is 1 KB or even less.. \nPlease check again...")
else:
    print("Done.")

