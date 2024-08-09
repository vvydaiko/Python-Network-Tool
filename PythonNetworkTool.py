#Created  by Vladyslav Vydaiko 24/03/2024 
#Final Python Project

import tkinter as tk #library for creating GUI applications
import socket #library that provides low-level network programming
import platform #library which gives information about OS
import os #library taht provides a way of using operating system dependent functionality
import datetime #library that supplies classes for manipulating dates and times
import threading #library for multiple tasks concurrently
import paramiko #library for SSH protocol

#Globals
window = tk.Tk()
window.title(" - Python Network Tool - ")
window_Width = 1100
window_Height = 630
ScreenWidth = window.winfo_screenwidth()
ScreenHeight = window.winfo_screenheight()
#Placing window appear in center of a screen
Appear_in_the_Middle = '%dx%d+%d+%d' % (window_Width, window_Height, (ScreenWidth - window_Width) / 2, (ScreenHeight - window_Height) / 2)
window.geometry(Appear_in_the_Middle)
window.resizable(width=False, height=False) #Absolute positioning of window won't allow to resize it
window.configure(bg='black') 
GUI = None #pointer that will be used to reference GUI class for functions (instantiated later)

#---Class--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Main_GUI:

#------Inline Functions------           
        #Refreshing window state
      def refresh(self):
          window.update()
          window.after(1000,self.refresh)

#-------#IP Scan function---------------------------------------------------------------------------------------------------------------       
      def IP_Scan(self):
          self.TXT_Main_Output.delete("0.0", "end") #In a tkinter Text widget, the string "0.0" represents the starting position where the text is inserted.
          Net_IP = self.ENT_Network.get()
          Start_Host = self.ENT_Start_Host.get()
          End_Host = self.ENT_End_Host.get()

          MESSAGE = "\n Initiating PING Sweep.\n"
          MESSAGE += " Received from GUI:\n"
          MESSAGE += "\n Network Address: " + Net_IP 
          MESSAGE +=  "\n Starting Host: " + Start_Host
          MESSAGE +=  "\n Ending Host: " + End_Host + "\n"

          self.TXT_Main_Output.insert("0.0", MESSAGE)
          print(MESSAGE)

          Ping_Command = ""

          IP_PARTS = Net_IP.split('.')
          #Gets a value for three first octets of IP address
          NETWORK_IP = IP_PARTS[0] + '.' + IP_PARTS[1] + '.' + IP_PARTS[2] + '.'

          Starting_Host = int(Start_Host)
          Ending_Host = int(End_Host)
          Ending_Host += 1 #Increment last host to include it in the scan range

          #Identify system OS for right ping command
          OS = platform.system()

          if(OS == "Windows"):
             print("Windows OS detected.")
             Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
             self.TXT_Main_Output.delete(1.0,"end")
             self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + " Windows OS detected.")
             Ping_Command = "ping -n 1 "
          else:
             print("Linux OS detected.")
             Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
             self.TXT_Main_Output.delete(1.0,"end")
             self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + "Linux OS detected.")
             Ping_Command = "ping -c 1 "   

          #Get starting time of scan
          Time_Start = datetime.datetime.now()
          MESSAGE = " Start time: " + str(Time_Start)  
          MESSAGE += "\n Scanning ...\n"  
          print(MESSAGE)
          Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
          self.TXT_Main_Output.delete(1.0,"end")
          self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE) 

          for IP in range(Starting_Host,Ending_Host):
              ADDRESS = NETWORK_IP + str(IP)
              MESSAGE = " Pinging " + ADDRESS 
              Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
              self.TXT_Main_Output.delete(1.0,"end")
              self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE)
              self.TXT_Main_Output.see("end") #Autoscrolls TEXT object to bottom
              print(MESSAGE)
              The_Command = Ping_Command + ADDRESS
              The_Response = os.popen(The_Command) #open a pipe to execute shell commands within a Python script and capture the output of those commands.
              LIST = The_Response.readlines()

              for LINE in LIST:
                  if(LINE.count("TTL")):
                     MESSAGE = "        " + ADDRESS + "---> Live!" 
                     print(MESSAGE) 
                     Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
                     self.TXT_Main_Output.delete(1.0,"end")
                     self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE)
                     break  

          Time_End = datetime.datetime.now()
          Total_Time = Time_End - Time_Start
          MESSAGE = "\nScan completed in: " + str(Total_Time)
          print(MESSAGE)
          Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
          self.TXT_Main_Output.delete(1.0,"end")
          self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE) 

#----------------------------------------------------------------------------------------------------------------------           
         #Threading is used to ensure that the GUI remains responsive during the scanning process.
      def Threaded_IP_Scan(self):
          self.refresh()
          threading.Thread(target=self.IP_Scan).start()

#-------#Port Scan function---------------------------------------------------------------------------------------------------------------     
      def Port_Scan(self):
          self.TXT_Main_Output.delete("0.0", "end")
          The_Host = self.ENT_Host.get()
          Start_Port = self.ENT_Start_Port.get()
          End_Port = self.ENT_End_Port.get()

          MESSAGE = "\n Initiating PORT Scan.\n"
          MESSAGE += " Received from GUI:\n"
          MESSAGE += "\n Host to scan: " + The_Host 
          MESSAGE +=  "\n Starting Port: " + Start_Port
          MESSAGE +=  "\n Ending Port: " + End_Port + "\n"

          self.TXT_Main_Output.insert("0.0", MESSAGE)
          print(MESSAGE)

          # Check time when scan started
          Time_Start = datetime.datetime.now()
          
          Remote_Server = The_Host
          Remote_Server_IP = socket.gethostbyname(Remote_Server)
          Port_Start = int(Start_Port)
          Port_End = int(End_Port)

          MESSAGE =  "\n Scanning remote host: " + Remote_Server_IP + "\n"
          Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
          self.TXT_Main_Output.delete(1.0,"end")
          self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE) 
          print(MESSAGE)

          try:
              for port in range(Port_Start,Port_End): 
                  MESSAGE = " Scanning port: " + str(port)
                  Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
                  self.TXT_Main_Output.delete(1.0,"end")
                  self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE) 
                  self.TXT_Main_Output.see("end") #autoscrolls TEXT object to bottom
                  print(MESSAGE)  
                  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET socket used for IPv4, SOCK_STREAM means TCP communication
                  socket.setdefaulttimeout(.1) #0.1 sec
                  result = sock.connect_ex((Remote_Server_IP, port)) #Listening port 
                  if result == 0:
                     MESSAGE = "\n ********** Port " + str(port) + ":-->Open!"
                     Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
                     self.TXT_Main_Output.delete(1.0,"end")
                     self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE) 
                     print(MESSAGE)
                  sock.close()

          except KeyboardInterrupt:
                 MESSAGE = "\n You pressed Ctrl + C to terminate process."
                 Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
                 self.TXT_Main_Output.delete(1.0,"end")
                 self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE) 
                 print(MESSAGE)
                 self.sys.exit()

          except socket.gaierror:
                 print("")
                 MESSAGE = "\n Hostname could not be resolved. Exiting ..."
                 Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
                 self.TXT_Main_Output.delete(1.0,"end")
                 self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE)
                 print(MESSAGE)                 
                 self.sys.exit()

          except socket.error:
                 MESSAGE = "\n Couldn't connect to server. Exiting ..."
                 Txt_Box_Contents = self.TXT_Main_Output.get("0.0",tk.END)
                 self.TXT_Main_Output.delete(1.0,"end")
                 self.TXT_Main_Output.insert("0.0", Txt_Box_Contents + MESSAGE)
                 print(MESSAGE)                 
                 self.sys.exit()

          # Checking the time again
          Time_Finish = datetime.datetime.now()

          # Calculates the difference of time, to see how long it took to run the script
          Time_Total =  Time_Finish - Time_Start

          # Printing the information to screen     
          MESSAGE = "Scanning Completed in: " + str(Time_Total)
          self.TXT_Main_Output.insert("1.0", MESSAGE)
          print(MESSAGE)                     
#---------------------------------------------------------------------------------------------------------------------- 
        #Threading is used to ensure that the GUI remains responsive during the scanning process.
      def Threaded_Port_Scan(self):
          self.refresh()
          threading.Thread(target=self.Port_Scan).start()
          
#-------SSH Bruteforce function---------------------------------------------------------------------------------------------------------------- 
      def SSH_connect(self, password, host, username, code=0):
        ssh = paramiko.SSHClient() #Create a new SSH client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy) #Policy for adding the hostname and new host key 

        try:
            ssh.connect(host, port=22, username=username, password=password)
        except paramiko.AuthenticationException: #Authentication (login) process failed due to incorrect credentials
            code = 1
        except socket.error: #Failure to establish a network connection
            code = 2

        ssh.close()
        return code

      def BTN_Init_SSH_Handler(self):
        host = self.ENT_Target.get() #gets IP value from GUI entry box 
        username = self.ENT_SSH_User.get() #gets login value from GUI entry box 
        input_file = self.ENT_Pass_List.get() #gets password file value from GUI entry box
    
        result_message = ''
        
        if not os.path.exists(input_file):
            result_message = ('[!!] That File/Path Does Not Exist')
        else:
            result_message = '' 
            with open(input_file, 'r') as file:
                for line in file.readlines():
                    password = line.strip()
                    #I changed this part a to fix an error
                    try:
                        response = self.SSH_connect(password, host, username)
                        if response == 0:
                            result_message += f'\n[+] Found Password:  {password}, For Account:  {username}\n'
                            break
                        elif response == 1:
                            result_message += f'\n[-] Incorrect Login:  {password}, For Account:  {username}\n'
                        elif response == 2:
                            result_message += f'\n[!!] Can Not Connect To {username}\n'
                            break
                    except Exception as e:
                        print(e)
                        pass
        self.TXT_Main_Output.insert(tk.END, result_message)
        
#---------------------------------------------------------------------------------------------------------------------- 

    #---Constructor of the GUI class----------------------------------------------------------------------------     
      def __init__(self, master=None):

          self.RB_Ping_Port_SSH_Var = tk.IntVar()
          
          #Event Handlers for Radio Buttons
          #If one function was selected - the other one will be disabled.
          def RB_Ping_Selection_Handler():
              self.BTN_Init_Port['state'] = tk.DISABLED
              self.BTN_Init_Ping['state'] = tk.NORMAL
              self.ENT_Host['state'] = tk.DISABLED
              self.ENT_Start_Port['state'] = tk.DISABLED
              self.ENT_End_Port['state'] = tk.DISABLED              
              self.ENT_Network['state'] = tk.NORMAL
              self.ENT_Start_Host['state'] = tk.NORMAL
              self.ENT_End_Host['state'] = tk.NORMAL  
              self.BTN_Init_SSH['state'] = tk.DISABLED 
              self.ENT_Target['state'] = tk.DISABLED
              self.ENT_SSH_User['state'] = tk.DISABLED
              self.ENT_Pass_List['state'] = tk.DISABLED                                   

          def RB_Port_Selection_Handler():   
              self.BTN_Init_Ping['state'] = tk.DISABLED
              self.BTN_Init_Port['state'] = tk.NORMAL 
              self.ENT_Network['state'] = tk.DISABLED
              self.ENT_Start_Host['state'] = tk.DISABLED
              self.ENT_End_Host['state'] = tk.DISABLED
              self.ENT_Host['state'] = tk.NORMAL
              self.ENT_Start_Port['state'] = tk.NORMAL
              self.ENT_End_Port['state'] = tk.NORMAL
              self.ENT_Target['state'] = tk.DISABLED
              self.ENT_SSH_User['state'] = tk.DISABLED
              self.ENT_Pass_List['state'] = tk.DISABLED
              
          def RB_SSH_Selection_Handler():   
              self.BTN_Init_Ping['state'] = tk.DISABLED
              self.BTN_Init_Port['state'] = tk.DISABLED
              self.BTN_Init_SSH['state'] = tk.NORMAL
              self.ENT_Network['state'] = tk.DISABLED
              self.ENT_Start_Host['state'] = tk.DISABLED
              self.ENT_End_Host['state'] = tk.DISABLED
              self.ENT_Host['state'] = tk.DISABLED
              self.ENT_Start_Port['state'] = tk.DISABLED
              self.ENT_End_Port['state'] = tk.DISABLED
              self.ENT_Target['state'] = tk.NORMAL
              self.ENT_SSH_User['state'] = tk.NORMAL
              self.ENT_Pass_List['state'] = tk.NORMAL

            #Event handlers for buttons
          def BTN_Init_Ping_Handler():
              self.Threaded_IP_Scan() 

          def BTN_Init_Port_Handler():
              self.Threaded_Port_Scan()   
              
          def BTN_Init_SSH_Bruteforce_Handler():
              self.BTN_Init_SSH_Handler()
                 

#---A. Frame: Main Window -------------------------------------------------------------
        #Creates main window and set the parameters
          self.FRM_Main_Window = tk.Frame(master)
          self.FRM_Main_Window.configure(height=520, width=1100, borderwidth=3, relief="flat", background="#33a643")
          self.FRM_Main_Window.place(anchor="nw", height=720, width=1100, x=0, y=0)
        #Creates label for the window
          self.LAB_Title = tk.Label(self.FRM_Main_Window)
          self.LAB_Title.configure(background="#33a643",foreground="#FFFFFF", font="{Barlow Condensed} 13 {}", text="Python Network Multi Tool")
          self.LAB_Title.place(anchor="nw", height=25, width=240, x=870, y=2)  

#---B. Frame: IP Scanner -------------------------------------------------------------          
          self.LFRM_IP_Scanner = tk.LabelFrame(self.FRM_Main_Window)
          self.LFRM_IP_Scanner.configure(height=200, width=377, borderwidth=3, relief="sunken", background="#33a643", text="Ping Sweeper")
          self.LFRM_IP_Scanner.place(anchor="nw", height=200, width=377, x=5, y=3) 

          self.RB_Activate_IP_Scanner = tk.Radiobutton(self.LFRM_IP_Scanner, variable=self.RB_Ping_Port_SSH_Var, value=1, command=RB_Ping_Selection_Handler)
          self.RB_Activate_IP_Scanner.configure(height=25, width=190, background="#33a643", font="{Arial} 12 {}", text="Activate Ping Sweeper")
          self.RB_Activate_IP_Scanner.place(anchor="nw", height=25, width=190, x=18, y=10)            

          self.LAB_Network = tk.Label(self.LFRM_IP_Scanner)
          self.LAB_Network.configure(background="#33a643", borderwidth=0, relief="flat", font="{Arial} 12 {}", anchor="nw", text="Network:")
          self.LAB_Network.place(anchor="w", x=22, y=57)

          self.LAB_Start_Host = tk.Label(self.LFRM_IP_Scanner)
          self.LAB_Start_Host.configure(background="#33a643", borderwidth=0, relief="flat", font="{Arial} 12 {}", anchor="nw", text="Start Host:")
          self.LAB_Start_Host.place(anchor="w", x=22, y=92)

          self.LAB_End_Host = tk.Label(self.LFRM_IP_Scanner)
          self.LAB_End_Host.configure(background="#33a643", borderwidth=0, relief="flat", font="{Arial} 12 {}", anchor="nw", text="End Host:")
          self.LAB_End_Host.place(anchor="w", x=22, y=127)

          self.ENT_Network = tk.Entry(self.LFRM_IP_Scanner)
          self.ENT_Network.configure(width=232, background="#000000", foreground="#ffffff", borderwidth=3, justify="center", relief="sunken", font="{Courier} 12 {}")
          self.ENT_Network.insert("0", "192.168.0.0")
          self.ENT_Network.place(anchor="nw", height=25, width=232, x=105, y=45)

          self.ENT_Start_Host = tk.Entry(self.LFRM_IP_Scanner)
          self.ENT_Start_Host.configure(width=232, background="#000000", foreground="#ffffff", borderwidth=3, justify="center", relief="sunken", font="{Courier} 12 {}")
          self.ENT_Start_Host.insert("0", "1")
          self.ENT_Start_Host.place(anchor="nw", height=25, width=232, x=105, y=80)

          self.ENT_End_Host = tk.Entry(self.LFRM_IP_Scanner)
          self.ENT_End_Host.configure(width=232, background="#000000", foreground="#ffffff", borderwidth=3, justify="center", relief="sunken", font="{Courier} 12 {}")
          self.ENT_End_Host.insert("0", "254")
          self.ENT_End_Host.place(anchor="nw", height=25, width=232, x=105, y=115)

          self.BTN_Init_Ping = tk.Button(self.LFRM_IP_Scanner, command=BTN_Init_Ping_Handler)
          self.BTN_Init_Ping.configure(background="#ff0000",font="{Lucida Console} 12 {}",foreground="#ffffff",text="SCAN")
          self.BTN_Init_Ping.place(anchor="nw", height=30, width=320, x=22, y=147)
          

#---C. Frame: Port Scanner -------------------------------------------------------------            
          self.LFRM_Port_Scanner = tk.LabelFrame(self.FRM_Main_Window)
          self.LFRM_Port_Scanner.configure(height=200, width=377, borderwidth=3, relief="sunken", background="#33a643", text="Port Scanner")
          self.LFRM_Port_Scanner.place(anchor="nw", height=200, width=377, x=5, y=210)       

          self.RB_Activate_Port_Scanner = tk.Radiobutton(self.LFRM_Port_Scanner, variable=self.RB_Ping_Port_SSH_Var, value=2, command=RB_Port_Selection_Handler)
          self.RB_Activate_Port_Scanner.configure(height=25, width=190, background="#33a643", font="{Arial} 12 {}", text="Activate Port Scanner")
          self.RB_Activate_Port_Scanner.place(anchor="nw", height=25, width=190, x=18, y=10)

          self.LAB_Host = tk.Label(self.LFRM_Port_Scanner)
          self.LAB_Host.configure(background="#33a643", borderwidth=0, relief="flat", font="{Arial} 12 {}", anchor="nw", text="Host:")
          self.LAB_Host.place(anchor="nw", x=20, y=45)

          self.LAB_Start_Port = tk.Label(self.LFRM_Port_Scanner)
          self.LAB_Start_Port.configure(background="#33a643", borderwidth=0, relief="flat", font="{Arial} 12 {}", anchor="nw", text="Start Port:")
          self.LAB_Start_Port.place(anchor="nw", x=20, y=80)

          self.LAB_End_Port = tk.Label(self.LFRM_Port_Scanner)
          self.LAB_End_Port.configure(background="#33a643", borderwidth=0, relief="flat", font="{Arial} 12 {}", anchor="nw", text="End Port:" )
          self.LAB_End_Port.place(anchor="nw", x=20, y=115)

          self.ENT_Host = tk.Entry(self.LFRM_Port_Scanner)
          self.ENT_Host.configure(width=232, background="#000000", foreground="#ffffff", borderwidth=3, justify="center", relief="sunken", font="{Courier} 12 {}")
          self.ENT_Host.insert("0", "192.168.0.0")
          self.ENT_Host.place(anchor="nw", height=25, width=232, x=105, y=45)

          self.ENT_Start_Port = tk.Entry(self.LFRM_Port_Scanner)
          self.ENT_Start_Port.configure(width=232, background="#000000", foreground="#ffffff", borderwidth=3, justify="center", relief="sunken", font="{Courier} 12 {}")
          self.ENT_Start_Port.insert("0", "1")
          self.ENT_Start_Port.place(anchor="nw", height=25, width=232, x=105, y=80)

          self.ENT_End_Port = tk.Entry(self.LFRM_Port_Scanner)
          self.ENT_End_Port.configure(width=232, background="#000000", foreground="#ffffff", borderwidth=3, justify="center", relief="sunken", font="{Courier} 12 {}")
          self.ENT_End_Port.insert("0", "65534")
          self.ENT_End_Port.place(anchor="nw", height=25, width=232, x=105, y=115)

          self.BTN_Init_Port = tk.Button(self.LFRM_Port_Scanner, command=BTN_Init_Port_Handler)
          self.BTN_Init_Port.configure(background="#ff0000",font="{Lucida Console} 12 {}",foreground="#ffffff",text="SCAN")
          self.BTN_Init_Port.place(anchor="nw", height=30, width=320, x=22, y=147)
          
#---D. Frame: SSH Bruteforce
          self.LFRM_SSH_Bruteforce = tk.LabelFrame(self.FRM_Main_Window)
          self.LFRM_SSH_Bruteforce.configure(height=200, width=377, borderwidth=3, relief="sunken", background="#33a643", text="SSH Bruteforce")
          self.LFRM_SSH_Bruteforce.place(anchor="nw", height=200, width=377, x=5, y=415)
          
          self.RB_Activate_SSH_Bruteforce = tk.Radiobutton(self.LFRM_SSH_Bruteforce, variable=self.RB_Ping_Port_SSH_Var, value=3, command=RB_SSH_Selection_Handler)
          self.RB_Activate_SSH_Bruteforce.configure(height=25, width=190, background="#33a643", font="{Arial} 12 {}", text="Activate SSH Bruteforce")
          self.RB_Activate_SSH_Bruteforce.place(anchor="nw", height=25, width=190, x=18, y=10)  
          
          self.ENT_Target = tk.Entry(self.LFRM_SSH_Bruteforce)
          self.ENT_Target.configure(width=232, background="#000000", foreground="#ffffff", borderwidth=3, justify="center", relief="sunken", font="{Courier} 12 {}")
          self.ENT_Target.insert("0", "192.168.0.0")
          self.ENT_Target.place(anchor="nw", height=25, width=232, x=105, y=45)
          
          self.LAB_Target = tk.Label(self.LFRM_SSH_Bruteforce)
          self.LAB_Target.configure(background="#33a643", borderwidth=0, relief="flat", font="{Arial} 12 {}", anchor="nw", text="Host:")
          self.LAB_Target.place(anchor="nw", x=20, y=45)
          
          self.ENT_SSH_User = tk.Entry(self.LFRM_SSH_Bruteforce)
          self.ENT_SSH_User.configure(width=232, background="#000000", foreground="#ffffff", borderwidth=3, justify="center", relief="sunken", font="{Courier} 12 {}")
          self.ENT_SSH_User.place(anchor="nw", height=25, width=232, x=105, y=80)
          
          self.LAB_SSH_User = tk.Label(self.LFRM_SSH_Bruteforce)
          self.LAB_SSH_User.configure(background="#33a643", borderwidth=0, relief="flat", font="{Arial} 12 {}", anchor="nw", text="SSH User")
          self.LAB_SSH_User.place(anchor="nw", x=20, y=80)
          
          self.ENT_Pass_List = tk.Entry(self.LFRM_SSH_Bruteforce)
          self.ENT_Pass_List.configure(width=232, background="#000000", foreground="#ffffff", borderwidth=3, justify="center", relief="sunken", font="{Courier} 12 {}")
          self.ENT_Pass_List.place(anchor="nw", height=25, width=232, x=105, y=115)
          
          self.LAB_Pass_List = tk.Label(self.LFRM_SSH_Bruteforce)
          self.LAB_Pass_List.configure(background="#33a643", borderwidth=0, relief="flat", font="{Arial} 12 {}", anchor="nw", text="Pass List")
          self.LAB_Pass_List.place(anchor="nw", x=20, y=115)
          
          self.BTN_Init_SSH = tk.Button(self.LFRM_SSH_Bruteforce, command=BTN_Init_SSH_Bruteforce_Handler)
          self.BTN_Init_SSH.configure(background="#ff0000",font="{Lucida Console} 12 {}",foreground="#ffffff",text="SCAN")
          self.BTN_Init_SSH.place(anchor="nw", height=30, width=320, x=22, y=147)
          
#---E. Frame: Main Output -------------------------------------------------------------
          self.LFRM_Main_Output = tk.LabelFrame(self.FRM_Main_Window)
          self.LFRM_Main_Output.configure(height=700, width=680, borderwidth=3, relief="sunken", background="#33a643", text="Main Output")
          self.LFRM_Main_Output.place(anchor="nw", height=620, width=700, x=395, y=3)

          #set scrollbar behavior
          self.SB_Vert_TXT_Main_Output = tk.Scrollbar(self.LFRM_Main_Output, orient = tk.VERTICAL) 
          self.SB_Vert_TXT_Main_Output.pack(side=tk.RIGHT, fill=tk.Y)

          self.TXT_Main_Output = tk.Text(self.LFRM_Main_Output, yscrollcommand=self.SB_Vert_TXT_Main_Output.set)
          self.TXT_Main_Output.configure(height=540, width=678, background="#000000", foreground="#ffffff", borderwidth=3, relief="sunken", font="{Courier} 10 {}")
          self.TXT_Main_Output.insert("0.0", "\n Python Network Tool made by Vlad.\n This is the MAIN OUTPUT panel.\n IP\port scan and SSH Bruteforce results will display here.")
          self.TXT_Main_Output.place(anchor="nw", height=600, width=678, x=1, y=1)
        
          self.SB_Vert_TXT_Main_Output.config(command=self.TXT_Main_Output.yview) 

#---End Class----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----Invocations-----
GUI = Main_GUI(window) #instantiate GUI class

#---SCAN Main Window---
window.mainloop()
