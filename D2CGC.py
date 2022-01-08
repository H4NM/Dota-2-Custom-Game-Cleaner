import os, re

############################################################
#  Welcome to the Dota 2 Custom Game Disk Cleaner Script!  #
# -------------------------------------------------------- #
# Before running this script, please ensure the path to    #
# your custom games is correct, and that you've entered    #
# the games you want to keep in the list below (game_list).#
############################################################


#The path to your dota 2 custom games directory
#Mine is C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\570
dota_path = "GIVE ME A PATH"

#List of the custom games you do NOT want to delete
#My list is [Dota 12v12", "Overthrow 2.0",  "AGHANIM'S PATHFINDERS", "ATTACK ON HERO"]
game_list = [" ", " "]


#Class for functions enablig the detection of uneccessary custom game files
class Dota2DiskCleaner():

    #Initialize variables and start cleaning
    def __init__(self):
        self.files_deleted = 0
        self.total_bytes = 0

        self.removed_custom_games = []

        self.start_cleaning()
        self.print_summary()

    #Printing a summary for the removed files
    def print_summary(self):
        if self.files_deleted == 0:
            print("No files were deleted")
        else:
            print("========== Dota 2 Custom Game Cleaning Summary ==========")
            print("Files deleted: {}".format(self.files_deleted))
            print("Total space cleared: {}".format(self.byte_conversion(self.total_bytes)))
            print("Custom games removed:\n\t{}".format("\n\t".join(self.removed_custom_games)))

    #Converting the total amount of bytes to a suitable metric
    def byte_conversion(self, byte_amount):
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
        while byte_amount > power:
            byte_amount /= power
            n += 1
        return str(round(byte_amount)) + " " + power_labels[n]+'bytes'
       
    #Deletes unwanted .vpk or .lua files
    def delete_vpk_lua_files(self, folder, game_title):
        for file in os.listdir(folder):
            if file.endswith(".lua") or file.endswith(".vpk"):

                try:
                    self.total_bytes += os.path.getsize(folder+"\\"+file)
                    os.remove(folder +"\\" +file)
                    self.files_deleted += 1
                    if not game_title in self.removed_custom_games:
                        self.removed_custom_games.append(game_title)
                except:
                    print("Unable to remove {}".format(file))

    #Iterates through all of the custom game folders in the given path
    #And checks if it contains files for unwanted games
    def start_cleaning(self):
        for folder in os.listdir(dota_path):
            folder = dota_path + "\\" + folder
            for filename in os.listdir(folder):
                if filename == "publish_data.txt":
                    with open(folder+"\\"+filename, 'rb') as f:

                        contents = f.read().decode("utf-8")
                        game_title = re.findall('"(.*?)"', contents)[2]
                        
                        if game_title in game_list:
                            continue
                        else:
                            self.delete_vpk_lua_files(folder, game_title)
                            

#Initialises the class 
Dota2DiskCleaner()  
