# Bsf1
#cd C:\Users\miker\Documents\rss
#python basic_rss.py


#button1 = Button(root, text="Add", width=14,  command=add)
#add()

#button2 = Button(root, text="Delete", width=14,  command=delete)
#delete()

#button3 = Button(root, text="List", width=14,  command=list_ep)
#list_ep()

#button5 = Button(root, text="Print", width=14,  command=print_info)
#print_info()

#button6 = Button(root, text="Browse", width=14,  command = lambda:open_dir_dest()) 
#open_dir_dest()

#button7 = Button(root, text="Download", width=14,  command=download)
#download()

#button7b = Button(root, text="Dn. Latest", width=14,  command=dn_latest)
#dn_latest()

#button8 = Button(root, text="Options", width=14,  command=options)
#options()

#button9 = Button(root, text="Exit", width=14,  command=CloseIt)
#CloseIt()

#button11 = Button(root, text="Select all", width=14,  command=select_all)
#select_all()

#button12 = Button(root, text="Deselect all", width=14,  command=deselect_all)
#deselect_all()


from tkinter import * 
from tkinter import filedialog
import tkinter as tk
import sys
import subprocess
import os
import threading
import string 
import feedparser
import ssl
import time
import random
import urllib.request
#import urllib.request as urlRequest
import csv
import trace
import requests

#set_dir = "A"
#set_dir = "B"

width = 900
height = 410 


lower_case = list(string.ascii_lowercase)

upper_case = list(string.ascii_uppercase)

num_list = list(map(str, list(range(10))))

download_path = ""

set_dir = "B"

if set_dir == "A":
   download_path = "C:/Users/miker/Desktop/"
elif set_dir == "B":
   download_path = "C:/Users/miker/OneDrive/Desktop/"

#download_path = "C:/Users/miker/OneDrive/Desktop/"
#download_path = "C:/Users/miker/Desktop/"

main_title_list = []

main_link_list = []

db_level = 10
seconds = 3600

dir_files = os.listdir(download_path) 
edit_dir_files = []


browse_dir_dest = ''


rss_list = []
rss_title_list = []
rss_list_backup = []

ep_count = 40
max_ep_count = 80

selected_cur = -1

set_m4a = 0

prev_sel = -1


def newline():
   print("")

def select_all():
   listbox2.select_set(0, END)

def deselect_all():
   listbox2.selection_clear(0, END)

def month_name(number):
    if number == 1:
        return "Jan"
    elif number == 2:
        return "Feb"
    elif number == 3:
        return "Mar"
    elif number == 4:
        return "Apr"
    elif number == 5:
        return "May"
    elif number == 6:
        return "Jun"
    elif number == 7:
        return "Jul"
    elif number == 8:
        return "Aug"
    elif number == 9:
        return "Sept"
    elif number == 10:
        return "Oct"
    elif number == 11:
        return "Nov"
    elif number == 12:
        return "Dec"

def open_dir_dest(): 
   global browse_dir_dest

   browse_dir_dest = filedialog.askdirectory()
   browse_dir_dest += "/"

   newline()
   newline()
   print(browse_dir_dest)
   newline()
   newline()

   E2.insert('end', browse_dir_dest)

def format_str(str):
   
   data_list = []

   for i in range(0, len(str)):
      find_match = -1

      for k in range(0, len(lower_case)):
         if (str[i] == lower_case[k]):
            find_match = 1

      for k in range(0, len(upper_case)):
         if (str[i] == upper_case[k]):
            find_match = 1

      for k in range(0, len(num_list)):
         if (str[i] == num_list[k]):
            find_match = 1

      if (find_match == -1):
         data_list.append(str[i])

   for i in range(0, len(data_list)):
      str = str.replace(data_list[i], "_")

   return str

def print_info():
   global rss_list
   global rss_title_list 
   global main_title_list
   global main_link_list


   newline()
   newline()
   print("print")

   newline()
   newline()

   if (len(rss_title_list) == 0):
      print("rss list empty")
      return 0

   newline()
   newline()

   for i in range(0, len(rss_title_list)):

      print(rss_title_list[i])
      print(rss_list[i])
   
      newline()
      newline()

   if (len(main_title_list) > 0):
      for i in range(0, len(main_title_list)):

         print(main_title_list[i])
         print(main_link_list[i])
      
         newline()
         newline()
   else:
      newline()
      newline()
      print("list empty")
      newline()
      newline()
      
def on_closing():
   CloseIt()

def CloseIt():
   save_rss_list()

   root.destroy()

def save_rss_list():
   global rss_list
   global rss_title_list 

   newline()
   newline()
   
   print("save rss_list")

   newline()
   newline()

   print("rss_list size: " + str(len(rss_list)))
   newline()
   newline()


   outputFile = open('basic_rss_list.csv', 'w', encoding="utf-8", newline='')
   outputWriter = csv.writer(outputFile)

   for i in range(0, len(rss_list)):
      outputWriter.writerow([rss_title_list[i], rss_list[i]])

   outputFile.close()


          


def add():
   x = threading.Thread(target=thread_function_add, args=(1,))
   x.start()

def thread_function_add(name):
   global rss_list
   global rss_title_list 

   newline()
   newline()
   print("add")
   newline()
   newline()

   url = E1.get()
   print(url) 

   if (url == ''):
      print("empty string")
      return -1

   if hasattr(ssl, '_create_unverified_context'):
      ssl._create_default_https_context = ssl._create_unverified_context

   blog_feed = feedparser.parse(url)

   print(blog_feed)
   # returns title of the blog site
   newline()
   newline()
   print(blog_feed.feed.title)
   newline()
   newline()



   if url not in rss_list:
      rss_list.append(url.strip())
      rss_title_list.append(blog_feed.feed.title)

   listbox1.delete(0, tk.END)

   temp_rss_title_list = rss_title_list.copy()
   temp_rss_title_list.sort()

   print(temp_rss_title_list)

   index_list = []

   for i in range(0, len(temp_rss_title_list)):
      for k in range(0, len(rss_title_list)):
         if (temp_rss_title_list[i] == rss_title_list[k]):
            index_list.append(k)

   print(index_list)

   temp_rss_list = [] 

   for i in index_list:
      print(rss_list[i])
      temp_rss_list.append(rss_list[i])

   print(rss_list)
   print(temp_rss_list)

   rss_list.clear()
   rss_list = temp_rss_list.copy()

   rss_title_list.clear()
   rss_title_list = temp_rss_title_list.copy()
   
   for i in range(0, len(rss_title_list)):
      listbox1.insert(tk.END, rss_title_list[i])

def delete():
   global rss_list
   global rss_title_list 

   print("delete")

   newline()
   newline() 

   if (len(rss_title_list) == 0):
      print("rss list empty")
      return 0

   newline()
   newline() 
   
   cur = listbox1.curselection()

   print(cur[0])

   del rss_list[cur[0]]
   del rss_title_list[cur[0]]

   listbox1.delete(0, tk.END)

   for i in range(0, len(rss_title_list)):
      listbox1.insert(tk.END, rss_title_list[i])


def dn_latest():
   print("dn_latest")
   #list_ep()
   #thread_function_list_ep(0)

   x = threading.Thread(target=thread_function_dn_latest, args=(1,))
   x.start()

def thread_function_dn_latest(name):
   global download_path
   global main_title_list
   global main_link_list
   global rss_title_list 
   global set_m4a


   counter_list = []

   #list_ep()
   thread_function_list_ep(0)

   newline()
   newline()

   print("thread_function_dn_latest")

   newline()
   newline()

   #if (len(listbox2.curselection()) == 0):
      #newline()
      #newline()
      #print("none selected")
      #return -1
   #else:
      #print(main_title_list)
   print(listbox2.size())

   value=listbox2.get(0)
   value = value.split(" ")[0]
   value = value.split("-")[1]
      
   print(value)

      #counter = 0
      #counter_list.append(value)

   for i in range(0, listbox2.size()):
      val_c = listbox2.get(i)
      val_b = val_c.split(" ")[0]
      val_b = val_b.split("-")[1]

      if (value == val_b and val_c.find("Best") == -1 and val_c.find("best") == -1):
         print(val_c.find("Best"))
         print('match')
         counter_list.append(i)
      elif (val_c.find("Best") != -1 or val_c.find("best") != -1):
         pass
      else:
         break

      #return 0
   
   dest_dir = clicked_dir.get()
   print(dest_dir)
   

   print(dest_dir.split("/"))
   length = len(dest_dir.split("/"))
   print(dest_dir.split("/")[length - 2])
   end_folder = dest_dir.split("/")[length - 2]

   if (end_folder != "download"):
      if not os.path.exists(dest_dir):
      # if the demo_folder directory is not present
      # then create it
         os.makedirs(dest_dir)


   if (browse_dir_dest != ''):
      dest_dir = browse_dir_dest

   for i in counter_list: #listbox2.curselection():
      newline()
      print("downloading")
      newline()
      newline()

      # select 2 digits at random
      digits = random.choices(string.digits, k=2)

      # select 9 uppercase letters at random
      letters = random.choices(string.ascii_uppercase, k=9)

      # shuffle both letters + digits
      sample = random.sample(digits + letters, 11)

      random_number = random.randint(1000, 9000)
      #result = "A3UZ4" + ''.join(sample) + str(random_number)
      result = str(random_number)
      #print(result)

      fileName = rss_title_list[selected_cur] + " "# + "_" + main_title_list[i]

      if (len(format_str(fileName)) > 15):
         fileName = format_str(fileName)[0:10] + "_" + main_title_list[i]
      else:
         fileName = format_str(fileName) + "_" + main_title_list[i]

      if (set_m4a == 0):
         if (len(format_str(fileName)) > 40):
            fileName = format_str(fileName)[0:40] + "_" + result + ".mp3"
         else:
            fileName = format_str(fileName) + "_" + result + ".mp3"
      else:
         if (len(format_str(fileName)) > 40):
            fileName = format_str(fileName)[0:40] + "_" + result + ".m4a"
         else:
            fileName = format_str(fileName) + "_" + result + ".m4a"

      print(fileName)
      

      #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
      #req = urllib.request.Request(main_link_list[i], headers = headers)
      # open the url
      #x = urllib.request.urlopen(req, timeout=20)
      # get the source code
      #data = x.read()

      # If you want to save the data to a file:
      #with open(dest_dir + fileName, "wb") as f:
         #f.write(data)


      with open(dest_dir + fileName, "wb") as f:
         print(f"Downloading {fileName}")
         response = requests.get(main_link_list[i], stream=True)
         total_length = response.headers.get("content-length")

         if total_length is None:
            # No content length header, just write the content
            f.write(response.content)
         else:
            dl = 0
            total_length = int(total_length)

            for data in response.iter_content(chunk_size=4096):
                  dl += len(data)
                  f.write(data)
                  done = int(50 * dl / total_length)
                  sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}]")
                  sys.stdout.flush()


      newline()
      newline()
      print("done downloading")

   newline()
   newline()
   print("all done")
   newline()
   newline()


def thread_function_dn_latest_b(name):

   global selected_cur

   temp_link_list = []
   temp_title_list = []

   print("thread_function_dn_latest")


   newline()
   newline()
   print(selected_cur)
   print(rss_title_list[selected_cur])
   #return 0


   #for j in range(0, len(rss_list)):
   url = rss_list[selected_cur]

   set_m4a = 0

   # url of blog feed
   feed_url = url
   blog_feed = feedparser.parse(feed_url)


   # returns title of the blog site
   print(blog_feed.feed.title)
      
   # returns the link of the blog
   # and number of entries(blogs) in the site.

   try:
      print(blog_feed.feed.link)
   except:
      print("no blog_feed.feed.link")

      print(len(blog_feed.entries))
      
      entry_len = len(blog_feed.entries)


   try:
      print(blog_feed.entries[0])
      print(blog_feed.entries[0].links)


      print(blog_feed.entries[0].title)
      print(blog_feed.entries[0].published)


      newline()
      newline()
      print(blog_feed.entries[0].published_parsed.tm_mon)
      print(blog_feed.entries[0].published_parsed.tm_mday)

      newline()
      newline()

      month_num = blog_feed.entries[0].published_parsed.tm_mon
      temp_month = month_name(month_num)

      temp_day = blog_feed.entries[0].published_parsed.tm_mday

      temp_title = blog_feed.entries[0].title

      temp_duration = 0


      try:
         print("itunes duration: " + str(blog_feed.entries[0].itunes_duration))

         if (str(blog_feed.entries[0].itunes_duration).find(":") == -1):         
            temp_seconds = int(blog_feed.entries[0].itunes_duration)
            temp_duration = time.strftime('%H:%M:%S', time.gmtime(temp_seconds))
         else:
            temp_duration = blog_feed.entries[0].itunes_duration
      except:
         temp_duration = 0
         print("error a")


      if (len(temp_title) > 30): 
         temp_title = temp_title[0:30] 
         
      temp_title_list.append(blog_feed.entries[0].title)

      try:
         for k in range(0, len(blog_feed.entries[0].links)):
                 
            if (blog_feed.entries[0].links[k].href.find("mp3") != -1):
               pass

               temp_link_list.append(blog_feed.entries[0].links[k].href)
               set_m4a = 0
            elif (blog_feed.entries[0].links[k].href.find("m4a") != -1):

               temp_link_list.append(blog_feed.entries[0].links[k].href)
               set_m4a = 1
      except:
            
               
         for k in range(0, len(blog_feed.entries[0]['links'])):
            try:

               if (blog_feed.entries[0]['links'][k]['href'].find("mp3") != -1):

                  temp_link_list.append(blog_feed.entries[0]['links'][k]['href'])
                  set_m4a = 0
            except:
               continue

   except: 
      print("error")

   #print(temp_link_list)

   #global download_path
   #global main_title_list
   #global main_link_list
   #global rss_title_list 
   #global set_m4a

   #if (len(listbox2.curselection()) == 0):
      #newline()
      #newline()
      #print("none selected")
      #return -1
   
   dest_dir = clicked_dir.get()
   print(dest_dir)
   

   print(dest_dir.split("/"))
   length = len(dest_dir.split("/"))

   print(dest_dir.split("/")[length - 2])
   end_folder = dest_dir.split("/")[length - 2]

   if (end_folder != "download"):
      if not os.path.exists(dest_dir):
      # if the demo_folder directory is not present
      # then create it
         os.makedirs(dest_dir)

   if (browse_dir_dest != ''):
      dest_dir = browse_dir_dest

   for i in range(0, len(temp_link_list)): #listbox2.curselection():
      #newline()
      #print("downloading")
      #newline()
      #newline()

      # select 2 digits at random
      digits = random.choices(string.digits, k=2)

      # select 9 uppercase letters at random
      letters = random.choices(string.ascii_uppercase, k=9)

      # shuffle both letters + digits
      sample = random.sample(digits + letters, 11)

      random_number = random.randint(1000, 9000)
      #result = "A3UZ4" + ''.join(sample) + str(random_number)
      result = str(random_number)
      #print(result)

      #fileName = rss_title_list[selected_cur] + " "# + "_" + main_title_list[i]
      fileName = rss_title_list[selected_cur] + " "# + "_" + main_title_list[i]

      if (len(format_str(fileName)) > 15):
         fileName = format_str(fileName)[0:10] + "_" + temp_title_list[i]
      else:
         fileName = format_str(fileName) + "_" + temp_title_list[i]

      if (set_m4a == 0):
         if (len(format_str(fileName)) > 40):
            fileName = format_str(fileName)[0:40] + "_" + result + ".mp3"
         else:
            fileName = format_str(fileName) + "_" + result + ".mp3"
      else:
         if (len(format_str(fileName)) > 40):
            fileName = format_str(fileName)[0:40] + "_" + result + ".m4a"
         else:
            fileName = format_str(fileName) + "_" + result + ".m4a"


      print(fileName)
      

      #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
      #req = urllib.request.Request(temp_link_list[i], headers = headers)
      # open the url
      #x = urllib.request.urlopen(req)
      # get the source code
      #data = x.read()

      # If you want to save the data to a file:
      #with open(dest_dir + fileName, "wb") as f:
         #f.write(data)


   with open(dest_dir + fileName, "wb") as f:
      print(f"Downloading {fileName}")
      response = requests.get(temp_link_list[i], stream=True)
      total_length = response.headers.get("content-length")

      if total_length is None:
         # No content length header, just write the content
         f.write(response.content)
      else:
         dl = 0
         total_length = int(total_length)

         for data in response.iter_content(chunk_size=4096):
               dl += len(data)
               f.write(data)
               done = int(50 * dl / total_length)
               sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}]")
               sys.stdout.flush()




      newline()
      newline()
      print("done downloading")
      
def list_ep():
   x = threading.Thread(target=thread_function_list_ep, args=(1,))
   x.start()

def thread_function_list_ep(name):
   global main_title_list
   global main_link_list
   global ep_count
   global selected_cur
   global set_m4a
   global prev_sel

   print("list_ep")

   if (len(listbox1.curselection()) == 0):
      newline()
      newline()
      print("none selected")
      return -1
   else:
      if (prev_sel != listbox1.curselection()):
         prev_sel = listbox1.curselection()
      else:
         print("already listed")
         return -1

   listbox2.delete(0, tk.END)
  
   main_title_list.clear()
   main_link_list.clear()

   newline()
   newline()

   print(listbox1.curselection()[0])
   cur = listbox1.curselection()[0]
   print(listbox1.get(cur))
   selected_cur = cur


   if hasattr(ssl, '_create_unverified_context'):
      ssl._create_default_https_context = ssl._create_unverified_context
      
   url = rss_list[cur]

   feed_url = url
   blog_feed = feedparser.parse(feed_url)


   # returns title of the blog site
   try:
      print(blog_feed.feed.title)
   except:
      print("no title")

   # returns the link of the blog
   # and number of entries(blogs) in the site.

   try:
      print(blog_feed.feed.link)
   except:
      print("no blog_feed.feed.link")

   print(len(blog_feed.entries))
   
   entry_len = len(blog_feed.entries)



   print(entry_len)
   print("ended")

   #return 0


   if (entry_len > max_ep_count):
      entry_len = max_ep_count

   print(entry_len)
   print("ended")

   #return 0

   for i in range(0, entry_len): #ep_count):
      try:
         #print(blog_feed.entries[i])
         #print(blog_feed.entries[i].links)


         #print(blog_feed.entries[i].title)
         #print(blog_feed.entries[i].published)


         newline()
         newline()
         #print(blog_feed.entries[i].published_parsed.tm_mon)
         #print(blog_feed.entries[i].published_parsed.tm_mday)
         newline()
         newline()

         month_num = blog_feed.entries[i].published_parsed.tm_mon
         temp_month = month_name(month_num)

         temp_day = blog_feed.entries[i].published_parsed.tm_mday

         temp_title = blog_feed.entries[i].title

         temp_duration = 0


         try:
            #print("itunes duration: " + str(blog_feed.entries[i].itunes_duration))

            if (str(blog_feed.entries[i].itunes_duration).find(":") == -1):         
               temp_seconds = int(blog_feed.entries[i].itunes_duration)
               temp_duration = time.strftime('%H:%M:%S', time.gmtime(temp_seconds))
            else:
               temp_duration = blog_feed.entries[i].itunes_duration
         except:
            temp_duration = 0
            print("error a")
         

         if (len(temp_title) > 30): 
            temp_title = temp_title[0:30] 
      

         main_title_list.append(blog_feed.entries[i].title)

         


         try:
            for k in range(0, len(blog_feed.entries[i].links)):
               
               if (blog_feed.entries[i].links[k].href.find("mp3") != -1):
                  
                  main_link_list.append(blog_feed.entries[i].links[k].href)
                  set_m4a = 0
               elif (blog_feed.entries[i].links[k].href.find("m4a") != -1):
                  main_link_list.append(blog_feed.entries[i].links[k].href)
                  set_m4a = 1
         except:
            

            
            for k in range(0, len(blog_feed.entries[i]['links'])):
               try:

                  if (blog_feed.entries[i]['links'][k]['href'].find("mp3") != -1):
                  
                     main_link_list.append(blog_feed.entries[i]['links'][k]['href'])
                     set_m4a = 0
               except:
                  continue

         if (temp_duration != 0):
            listbox2.insert(tk.END, temp_month + "-" + str(temp_day) + " " + temp_title + " " + str(temp_duration))
         else:
            listbox2.insert(tk.END, temp_month + "-" + str(temp_day) + " " + temp_title)   
      except: 
         print("error")
   





def download():

   x = threading.Thread(target=thread_function_download, args=(1,))
   x.start()



def thread_function_download(name):
   global download_path
   global main_title_list
   global main_link_list
   global rss_title_list 
   global set_m4a

   if (len(listbox2.curselection()) == 0):
      newline()
      newline()
      print("none selected")
      return -1
   
   dest_dir = clicked_dir.get()
   print(dest_dir)
   

   print(dest_dir.split("/"))
   length = len(dest_dir.split("/"))
   print(dest_dir.split("/")[length - 2])
   end_folder = dest_dir.split("/")[length - 2]

   if (end_folder != "download"):
      if not os.path.exists(dest_dir):
      # if the demo_folder directory is not present
      # then create it
         os.makedirs(dest_dir)


   if (browse_dir_dest != ''):
      dest_dir = browse_dir_dest

   for i in listbox2.curselection():
      newline()
      print("downloading")
      newline()
      newline()

      # select 2 digits at random
      digits = random.choices(string.digits, k=2)

      # select 9 uppercase letters at random
      letters = random.choices(string.ascii_uppercase, k=9)

      # shuffle both letters + digits
      sample = random.sample(digits + letters, 11)

      random_number = random.randint(1000, 9000)
      #result = "A3UZ4" + ''.join(sample) + str(random_number)
      result = str(random_number)
      #print(result)

      fileName = rss_title_list[selected_cur] + " "# + "_" + main_title_list[i]

      if (len(format_str(fileName)) > 15):
         fileName = format_str(fileName)[0:10] + "_" + main_title_list[i]
      else:
         fileName = format_str(fileName) + "_" + main_title_list[i]

      if (set_m4a == 0):
         if (len(format_str(fileName)) > 40):
            fileName = format_str(fileName)[0:40] + "_" + result + ".mp3"
         else:
            fileName = format_str(fileName) + "_" + result + ".mp3"
      else:
         if (len(format_str(fileName)) > 40):
            fileName = format_str(fileName)[0:40] + "_" + result + ".m4a"
         else:
            fileName = format_str(fileName) + "_" + result + ".m4a"

      print(fileName)
      

      #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
      #req = urllib.request.Request(main_link_list[i], headers = headers)
      # open the url
      #x = urllib.request.urlopen(req, timeout=20)
      # get the source code
      #data = x.read()

      # If you want to save the data to a file:
      #with open(dest_dir + fileName, "wb") as f:
         #f.write(data)



      with open(dest_dir + fileName, "wb") as f:
         print(f"Downloading {fileName}")
         response = requests.get(main_link_list[i], stream=True)
         total_length = response.headers.get("content-length")

         if total_length is None:
            # No content length header, just write the content
            f.write(response.content)
         else:
            dl = 0
            total_length = int(total_length)

            for data in response.iter_content(chunk_size=4096):
                  dl += len(data)
                  f.write(data)
                  done = int(50 * dl / total_length)
                  sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}]")
                  sys.stdout.flush()


      newline()
      newline()
      print("done downloading")

   newline()
   newline()
   print("all done")

def options():
   newline()
   newline()
   print("options")


def blank_func():
    pass


root = Tk()
root.geometry('%dx%d+%d+%d' % (width, height, 50, 50))
root.resizable(False, False)



listbox1 = Listbox(root,height=24, width=40,selectmode=SINGLE)
listbox1.grid(row=0, column=0, rowspan=24, padx = 5)

listbox2 = Listbox(root,height=24, width=50,selectmode=MULTIPLE)
listbox2.grid(row=0, column=1, rowspan=24, padx = 5)

my_label = Label(root, text = "url")
my_label.grid(row=0, column=2, sticky=NW)

E1 = Entry(root, width=38) #, bd =5)
E1.grid(row=1, column=2, sticky=N, columnspan=2, padx = 5)

button1 = Button(root, text="Add", width=14,  command=add)
button1.grid(row=2, column=2, sticky=N, padx = 5)

button2 = Button(root, text="Delete", width=14,  command=delete)
button2.grid(row=2, column=3, sticky=N, padx = 5)

button3 = Button(root, text="List", width=14,  command=list_ep)
button3.grid(row=3, column=2, sticky=N, padx = 5)


button5 = Button(root, text="Print", width=14,  command=print_info)
button5.grid(row=3, column=3, sticky=N, padx = 5)




options_dir_b = [
   "C:/Users/miker/OneDrive/Desktop/",
   "C:/Users/miker/OneDrive/Desktop/a/",
   "C:/Users/miker/OneDrive/Desktop/b/",
   "C:/Users/miker/OneDrive/Desktop/c/",
   "C:/Users/miker/OneDrive/Desktop/d/",
   "C:/Users/miker/OneDrive/Desktop/e/",   
   "C:/Users/miker/OneDrive/Desktop/f/",
   "C:/Users/miker/OneDrive/Documents/auto_norm/"
]

options_dir = [
   "C:/Users/miker/Desktop/",
   "C:/Users/miker/Desktop/a/",
   "C:/Users/miker/Desktop/b/",
   "C:/Users/miker/Desktop/c/",
   "C:/Users/miker/Desktop/d/",
   "C:/Users/miker/Desktop/e/",   
   "C:/Users/miker/Desktop/f/"
]

filenames= os.listdir (download_path) # get all files' and folders' names in the current directory

result = []
for filename in filenames: # loop through all the files and folders
    if os.path.isdir(os.path.join(os.path.abspath(download_path), filename)): # check whether the current object is a folder or not
        result.append(filename)
        options_dir.append(download_path + filename + "/")

result.sort()
print(result)


# datatype of menu text
clicked_dir = StringVar()
  
# initial menu text

if set_dir == "A":
   #clicked_dir.set("C:/Users/miker/OneDrive/Desktop/")
   clicked_dir.set("C:/Users/miker/Desktop/")
   drop_dir = OptionMenu( root , clicked_dir , *options_dir )
elif set_dir == "B":
   clicked_dir.set("C:/Users/miker/OneDrive/Desktop/")
   drop_dir = OptionMenu( root , clicked_dir , *options_dir_b )


drop_dir.grid(row=6, column=2, sticky=NW, columnspan=2, padx = 5, pady = 5)

E2 = Entry(root, width=38) #, bd =5)
E2.grid(row=7, column=2, sticky=N, columnspan=2, padx = 5)

button6 = Button(root, text="Browse", width=14,  command = lambda:open_dir_dest()) 
button6.grid(row=8, column=2, sticky=N, padx = 5, pady = 5)

button7 = Button(root, text="Download", width=14,  command=download)
button7.grid(row=9, column=3, sticky=N, padx = 5, pady = 5)

button7b = Button(root, text="Dn. Latest", width=14,  command=dn_latest)
button7b.grid(row=9, column=2, sticky=N, padx = 5, pady = 5)


button8 = Button(root, text="Options", width=14,  command=options)
button8.grid(row=8, column=3, sticky=N, padx = 5, pady = 5)


button9 = Button(root, text="Exit", width=14,  command=CloseIt)
button9.grid(row=22, column=3, sticky=N, padx = 5)

button11 = Button(root, text="Select all", width=14,  command=select_all)
button11.grid(row=21, column=2, sticky=N, padx = 5)

button12 = Button(root, text="Deselect all", width=14,  command=deselect_all)
button12.grid(row=21, column=3, sticky=N, padx = 5)



file_exists = os.path.exists('basic_rss_list.csv')

print(file_exists)

if (file_exists):
   exampleFile = open('basic_rss_list.csv',encoding='utf-8')
   exampleReader = csv.reader(exampleFile)
   for row in exampleReader:
      print('Row #' + str(exampleReader.line_num) + ' ' + str(row))
      rss_list.append(str(row[1]))
      rss_title_list.append(str(row[0]))
      listbox1.insert(tk.END, str(row[0]))



root.title('Rss Reader')
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()









