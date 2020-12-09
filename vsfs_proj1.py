import random
import datetime

sb_list = {}


class superBlock():
    #Creates the memory with specified functions

    #Initiates the inode bitmap, data bitmap, and memory size from the superblock. Places them in the first 3 lists of the memory superlist. Creates inode dicts for all inode metadata.
    def __init__(self, size):
        self.size = size
        self.iMap = [0] * (size - 4)
        self.dMap = [0] * (size - 4)
        print(self.iMap)
        print(self.dMap)
        self.mem = []
        for i in range(size):
            self.mem.append([])
        self.mem[0] = self
        self.mem[1] = self.iMap
        self.mem[2] = self.dMap
        self.inodes = [{} for new_inode in range(len(self.dMap))]
        self.mem[3] = self.inodes

    def open(self, args):
        #Opens chosen file, if not found, prints error.
        res = next((sub for sub in self.inodes if sub['name'] == args), None)
        print(self.mem[res['location']])


    def write(self, args):
        #Writes a new file with the name and data
        nob = self.iMap.index(0)
        self.iMap[nob] = 1
        self.dMap[nob] = 1
        file_name = args[0]
        data = args[1]
        now = datetime.datetime.now()
        data_size = len(data)
        self.inodes[nob] = {'name':file_name, 'date_created':now, 'date_modified':now, 'data_size':data_size, 'location':nob + 4}
        self.mem[nob + 4] = data

    def update(self, args):
        #Updates the chosen file and either appends or replaces the data.
        if args.len() < 2:
            print("Please state file, data and true or false (for appending/replacing appending= true replacing = false)\n in an array")
        else:
            for inode in self.inodes:
                if inode['name'] == args[0]:
                    file = inode['location']
                    if args[2] == 'false':
                        self.mem[file] = args[1]
                    if args[2] == 'true':
                        self.mem[file].append(args[1])
                    else:
                        print("Appending/replacing boolean incorrect")
                else:
                    print("File does not exist.")

    def delete(self, args):
        #Deletes the chosen file
        for inode in self.inodes:
            if inode['name'] == args:
                file = inode['location']
                self.mem[file] == None
            else:
                print("File not found.")


systemActivate = True
while systemActivate:
    print("Please type a command. (Type help for a list of commands)")
    uI = input()
    if uI == "exit":
        systemActivate = False
    if uI == "help":
        print("Type one of the following commands:\n Superblock List\n Superblock\n Open\n Write\n Update\n Delete")
    if uI == "Superblock List":
        print(sb_list)
    if uI == "Superblock":
        print("Type the name and size separated by space")
        uI = input()
        info = uI.split(" ")
        sbName = info[0]
        sbSize = int(info[1])
        sbName = superBlock(sbSize)
        sb_list[info[0]] = sbName
        print(sb_list)
        print("Superblock created.")
    if uI == "Open":
        print("Please type the memory and file name separated by space.")
        uI = input()
        info = uI.split(" ")
        if info[0] not in sb_list:
            print("Memory not found")
        sb_called = sb_list[info[0]]
        sb_called.open(info[1])
    if uI == "Write":
        print("Please type the superblock and name of the file")
        uI = input()
        info = uI.split(" ")
        mName = info[0]
        fName = info[1]
        if mName not in sb_list:
            print("Superblock does not exist")
        if fName in sb_list[mName].inodes:
            print("File already exists with that name")
        print("Please type the data for the file")
        uI = input()
        sb_list[mName].write([fName, uI])
        print(fName + " created.")
        print(sb_list[mName].inodes)
        print(sb_list[mName].mem)
    if uI == "Update":
        print("Please type the superblock and file name separated by space.")
        uI = input()
        info = uI.split(" ")
        mName = info[0]
        fName = info[1]
        if mName not in str(sb_list):
            print("Superblock does not exist")
        print("Please type the data")
        uI = input()
        fData = uI
        print("Do you want to replace the existing data? (Type Y or N)")
        if uI == "Y":
            fBool = "true"
        if uI == "N":
            fBool = "false"
        else:
            print("Replace action not specified correctly, exiting update")
        mName.update([fName, fData, fBool])
        print(fName + " updated.")
    if uI == "Delete":
        print("Please type the superblock and file name to delete separated by space.")
        uI = input()
        info = uI.split(" ")
        mName = info[0]
        fName = info[1]
        if mName not in str(sb_list):
            print("Superblock does not exist")
        mName.delete(fName)
        print(fName + " deleted.")
    if uI == "Exit":
        break


print("Goodbye!")



