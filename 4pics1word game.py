from abc import ABC, abstractmethod
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import random
import string
import os

class file_handling(ABC):

    @abstractmethod
    def save(self):
        pass
    
    @abstractmethod
    def load(self):
        pass

    def read_tabular_data(self,FILE_NAME, ROW_SEPARATOR = "\n", COLUMN_SEPARATOR = ";"):
        with open(FILE_NAME, "r") as file:
            file_content = file.read()
        
        row_strings = file_content.split(ROW_SEPARATOR)
        rows = [row.split(COLUMN_SEPARATOR) for row in row_strings]
        return rows


    def write_tabular_data(self,zipped_items, FILE_NAME, ROW_SEPARATOR = "\n", COLUMN_SEPARATOR = ";"): 
        items_string = [COLUMN_SEPARATOR.join(i) for i in zipped_items]
        file_content = ROW_SEPARATOR.join(items_string)
        with open(FILE_NAME, "w") as file:
            file.write(file_content)
            
class Piclist_filehandler(file_handling):

    def __init__(self):
        self.levels = []
        self.words = []

    def load(self):
        rows = self.read_tabular_data("picList.txt")
        for row in rows:
            self.levels.append(row[0])
            self.words.append(row[1])
        
    
    def save(self):
        pass
    
class Player_filehandling(file_handling):

    def __init__(self):
        self.level = 0
        self.coins = 100

    def load(self):
        if os.path.exists("PlayerData.txt"):
            row = self.read_tabular_data("PlayerData.txt")[0]
            self.level = int(row[0])
            self.coins = int(row[1])
        else:
            self.save()

    def save(self):
        zipped_items = [[str(self.level),str(self.coins)]]
        self.write_tabular_data(zipped_items, "PlayerData.txt")
        
class Window(Frame):
    
    def __init__(self, master = None):
        picList = Piclist_filehandler()
        self.playerdata = Player_filehandling()
        picList.load()
        self.playerdata.load()
        super().__init__(master)
        self.master = master
        self.pics = [] #list for pictures
        self.words = picList.words #list for words
        self.entry_cont = [] #list of entry containers
        self.ind = [0] #index counter
        self.cont = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'] #letter holders (entry containers)
        self.input = '' #input holder
        self.chars = '' #characters holder
        self.wrongAnswer = False #checker; if answer is incorrect, update
        self.noCoins = False #checker; if coins == 0, update
        self.hint_val = False #hint value (checker; if True == retain chars, if False == randomize chars)
        self.entry_val = False #entry box status (checker; if True == retain chars, if False == randomize chars)
        self.init_window()
        
    
    
    def init_window(self):
        self.btnStart = Button(self, text = 'START GAME', width = 10, command = self.game_window)
        self.master.title("Game Start!")
        self.btnStart.pack()
        self.pack()

    def game_window(self):
        #destroy previous button widget
        self.btnStart.destroy()

        #initialize frame widget
        self.frame = Frame(self, height = 600, width = 400, bg = '#454545')
        self.master.title('4 Pics 1 Word')

        #frame for entry widget (where to place letters)
        self.entryFrame = Frame(self, height = 35, width = 400)
        
        #top side canvas (level and ooins)
        coin_level_canvas = Canvas(self, height = 45, width = 400, bg = '#05f')
        coin_level_canvas.pack(side = TOP)

        #level count
        self.playerdata.levelObj = Label(coin_level_canvas, font = 'helvetica 16 bold', bg = '#05f', fg = 'white')
        self.playerdata.levelObj.place(x = 25, y = 10)

        #coin count
        self.coinObj = Label(coin_level_canvas, font = 'helvetica 16 bold', bg = '#05f', fg = 'white')
        self.coinObj.place(x = 265, y = 10)

        #on-screen keyboard
        self.b1 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b1.place(x = 50, y = 430)
        self.b2 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b2.place(x = 90, y = 430)
        self.b3 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b3.place(x = 130, y = 430)
        self.b4 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b4.place(x = 170, y = 430)
        self.b5 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b5.place(x = 210, y = 430)
        self.b6 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b6.place(x = 250, y = 430)

        self.b7 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b7.place(x = 50, y = 475)
        self.b8 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b8.place(x = 90, y = 475)
        self.b9 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b9.place(x = 130, y = 475)
        self.b10 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b10.place(x = 170, y = 475)
        self.b11 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b11.place(x = 210, y = 475)
        self.b12 = Button(self.frame, font = 'helvetica 16 bold', fg = 'black', width = 2)
        self.b12.place(x = 250, y = 475)

        #hint button
        hint = Button(self.frame, text = 'Hint', command = self.hintAnswer)
        hint.place(x = 315, y = 460)
        
        #submit button
        submit = Button(self.frame, text = 'Pass', command = self.passAnswer)
        submit.place(x = 315, y = 490)

        #reset button
        reset = Button(self.frame, text = 'Reset', command = self.resetWord)
        reset.place(x = 315, y = 430)
        
        self.frame.pack(side = BOTTOM)
        self.pack()
        
        self.game_objects()

    #button functions
    def passAnswer(self):
        if self.playerdata.coins < 10:
            self.noCoins = True
            messagebox.showerror("Invalid", "You don't have enough coins!")
            return None
        
        else:
            self.entry_val = False
            self.hint_val = False
            self.noCoins = False
            self.input = '' #reset answer
            self.playerdata.level += 1
            self.playerdata.coins -= 10
            print("Level :", self.playerdata.level + 1)
            self.playerdata.save()
            print("Coins :", self.playerdata.coins)

            for x in range(self.current_word):
                self.entry_cont[x].destroy()

            self.ind[0] = 0
            self.i = 0
            self.entry_cont.clear()
            self.game_objects()

    def hintAnswer(self):
        if self.playerdata.coins < 2:
            self.noCoins = True
            messagebox.showerror("Invalid", "You don't have enough coins!")
            return None
        
        else:
            self.hint_val = True
            self.playerdata.coins -= 2
            self.playerdata.save()
            ind = self.ind[0]
            string = self.words[self.playerdata.level][ind]
            ind += 1
            self.inputLetter(string)

    def resetWord(self):
        for x in range(self.current_word):
            self.entry_cont[x].config(state = "normal")
            self.entry_cont[x].delete(1.0, 'end')
            self.entry_cont[x].config(state = "normal")
            
        self.ind[0] = 0
        self.input = ''

    def inputLetter(self, x):
        ind = self.ind[0]
        self.entry_cont[ind].config(state = "normal")
        self.entry_cont[ind].insert(1.0, x.upper())
        self.entry_cont[ind].config(state = "disabled")
        ind += 1
        self.ind[0] = ind
        
        self.entry_val = True
        self.input = self.input + x
        
        if len(self.input) == self.current_word:
            self.entry_val = False
            self.ind[0] = 0
            self.submitAnswer(self.input)
            
        else:        
            self.game_objects()
    

    #validations for answers
    def submitAnswer(self, answer):
        if self.words[self.playerdata.level] == answer:
            print('- correct answer')
            self.playerdata.level += 1
            self.playerdata.coins += 10
            self.playerdata.save()
            self.input = '' #reset answer

            for x in range(self.current_word):
                self.entry_cont[x].destroy()

            self.entry_val = False
            self.hint_val = False
            self.ind[0] = 0
            
            self.entry_cont.clear()
            self.wrongAnswer = False
            self.game_objects()
            
        else:
            print('- wrong answer -')
            self.input = '' #reset answer
            self.entry_val = False
            self.hint_val = False
            self.ind[0] = 0

            for x in range(self.current_word):
                self.entry_cont[x].destroy()

            self.entry_cont.clear()
            self.wrongAnswer = True
            self.game_objects()

    def game_objects(self):
        print(self.hint_val)
        print(self.entry_val)



        #try except for checking if level exceeds 50
        try:
            #get length of the current word
            self.current_word = len(self.words[self.playerdata.level])
                
            if self.hint_val == True:
                self.coinObj.config(text = 'Coins: ' + str(self.playerdata.coins))
                #retain everything
                print("pass")
                
            else:            
                if self.entry_val == True:
                    print("pass")               
                else:
                    #store into text file
                    f = open('playerLog.txt', 'a')
                    f.seek(0, 0)
                    f.write(str(self.playerdata.level) + ':' + str(self.playerdata.coins) + ':' + self.words[self.playerdata.level] + '\n')
                    f.close
                    
                    #access images by level
                    img = PhotoImage(file = "file pics/" + self.words[self.playerdata.level] + '.png')
                    self.pics.append(img)
                    self.label = Label(self.frame)

                    #change picture
                    self.label.config(image = img)
                    self.label.place(x = 50, y = 35)
                    
                    #change entry container count 
                    var = 0
                    if self.current_word == 4:
                        for x in range(self.current_word):
                            self.box = Text(self.frame, height = 1.5, width = 3, font = 'helvetica 16 bold', state = 'disabled')
                            self.box.place(x = 113 + var, y = 358)
                            self.entry_cont.append(self.box)
                            var += 45

                    elif self.current_word == 5:
                        for x in range(self.current_word):
                            self.box = Text(self.frame, height = 1.5, width = 3, font = 'helvetica 16 bold', state = 'disabled')
                            self.box.place(x = 93 + var, y = 358)
                            self.entry_cont.append(self.box)
                            var += 45

                    elif self.current_word == 6:
                        for x in range(self.current_word):
                            self.box = Text(self.frame, height = 1.5, width = 3, font = 'helvetica 16 bold', state = 'disabled')
                            self.box.place(x = 68 + var, y = 358)
                            self.entry_cont.append(self.box)
                            var += 45

                    elif self.current_word == 7:
                        for x in range(self.current_word):
                            self.box = Text(self.frame, height = 1.5, width = 3, font = 'helvetica 16 bold', state = 'disabled')
                            self.box.place(x = 47 + var, y = 358)
                            self.entry_cont.append(self.box)
                            var += 45

                    elif self.current_word == 8:
                        for x in range(self.current_word):
                            self.box = Text(self.frame, height = 1.5, width = 3, font = 'helvetica 16 bold', state = 'disabled')
                            self.box.place(x = 24 + var, y = 358)
                            self.entry_cont.append(self.box)
                            var += 45
                        
                    else:
                        for x in range(self.current_word):
                            self.box = Text(self.frame, height = 1.5, width = 3, font = 'helvetica 16 bold', state = 'disabled')
                            self.box.place(x = 133 + var, y = 358)
                            self.entry_cont.append(self.box)
                            var += 45

                    #check if wrong answer was returned
                    if self.wrongAnswer == True:
                        print("- pass -")
                        
                    else:
                        #generate letters for on-screen keyboard
                        cont = []
                        for x in range(25):
                            i = random.choice(string.ascii_lowercase)
                            if i not in cont:
                                cont.append(i)

                        cont_str = ''.join(cont)
                        cont_join = ''.join(self.words[self.playerdata.level] + cont_str)
                        self.chars = list(cont_join)
                        del self.chars[12:]
                            
                        random.shuffle(self.chars)
                        
                        #randomize letters of on-screen keyboard
                        self.b1.config(text = self.chars[0].upper(), command = lambda: self.inputLetter(self.chars[0]))
                        self.b2.config(text = self.chars[1].upper(), command = lambda: self.inputLetter(self.chars[1]))
                        self.b3.config(text = self.chars[2].upper(), command = lambda: self.inputLetter(self.chars[2]))
                        self.b4.config(text = self.chars[3].upper(), command = lambda: self.inputLetter(self.chars[3]))
                        self.b5.config(text = self.chars[4].upper(), command = lambda: self.inputLetter(self.chars[4]))
                        self.b6.config(text = self.chars[5].upper(), command = lambda: self.inputLetter(self.chars[5]))
                        self.b7.config(text = self.chars[6].upper(), command = lambda: self.inputLetter(self.chars[6]))
                        self.b8.config(text = self.chars[7].upper(), command = lambda: self.inputLetter(self.chars[7]))
                        self.b9.config(text = self.chars[8].upper(), command = lambda: self.inputLetter(self.chars[8]))
                        self.b10.config(text = self.chars[9].upper(), command = lambda: self.inputLetter(self.chars[9]))
                        self.b11.config(text = self.chars[10].upper(), command = lambda: self.inputLetter(self.chars[10]))
                        self.b12.config(text = self.chars[11].upper(), command = lambda: self.inputLetter(self.chars[11]))
                
                    #increment level
                    self.playerdata.levelObj.config(text = 'Level: ' + str(self.playerdata.level + 1))
            
                    #increment coins
                    self.coinObj.config(text = 'Coins: ' + str(self.playerdata.coins))
                    
        except IndexError:
            print('yes')
            messagebox.showinfo("Congratulations!", "You have beaten all the levels!\nThanks for playing!")
            exit() 

root = Tk()
root.geometry("400x600")
app = Window(root)
root.mainloop()