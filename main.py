from tkinter import *

# Code to test multiplying by a matrix and its inverse
import numpy as np
from collections import deque
from random import seed
from random import randint
seed(0)

# function to print out the array to the frame passed to it
def print_array(arr, frame):
  # string variable for label
  out_string = StringVar()
  for i in arr:
     for j in i:
       out_string.set(out_string.get() + str(round(j)) + " ")
     out_string.set(out_string.get() + "\n")
  output = Label(frame, textvariable=out_string)
  output.pack()

# used at the beginning of almost every frame in order to print out the original NDID
def print_ndid(ndid, frame):
  ndid_label = Label(frame, text="NDID: ")
  ndid_output = Label(frame, textvariable = ndid)
  ndid_label.pack()
  ndid_output.pack()

# function to decrypt the addition of matrices
def subtraction(ndid, key):
  for i in range(len(ndid)):
    for j in range (len(ndid[0])):
      ndid[i][j] = ndid[i][j] - key[i][j];
  return ndid

# Code for multiplying by a matrix inverse
def mult_inv_matrix(ndid, key):
  key_inv = np.linalg.inv(key)
  ndid = np.dot(ndid, key_inv)
  return ndid

# used to decrypt the multiplication & addition encryption
def mult_inv_matrix1(ndid, key):
  ndid = mult_inv_matrix(ndid, key)
  ndid = subtraction(ndid, key)
  return ndid

# Code for mutliplying by a matrix
def mult_matrix(ndid, key):
  ndid = np.dot(ndid, key)
  return ndid

# function to encrypt based on addition of matrices
def addition(ndid, key):
    for i in range(len(ndid)):
        for j in range (len(ndid[0])):
            ndid[i][j] = ndid[i][j] + key[i][j];
    return ndid

# function to randomly generate a key
def random_key(ndid):
  key = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
  for i in range(len(ndid)):
    for j in range(len(ndid[0])):
      key[i][j] = randint(1,9)
  return key

# encryption method for matrix multiplication
def matrix_mult(notredameID, ndid, stack):
  # set up the screen
  frame_mult = Frame(root)
  frame_mult.place(height=800, width=500)
  print_ndid(notredameID, frame_mult)

  # generate a random key
  key = random_key(ndid)

  # print out the orginal matrix
  original_matrix = Label(frame_mult, text="Original Matrix: ")
  original_matrix.pack()
  print_array(ndid, frame_mult)

  # encrypt the ndid and print out result 
  encryption = Label(frame_mult, text="Encryption: ")
  encryption.pack()
  ndid = addition(ndid, key)
  ndid = mult_matrix(ndid, key)
  print_array(ndid, frame_mult)

  # set up buttons for returning & and the stack for decrypting later
  return_button = Button(frame_mult, text="Return to Options", command=lambda: build_own(notredameID, ndid, stack))
  return_button.pack()
  output_string = StringVar()
  output_string = "mult_inv_matrix1(ndid, "
  output_string += str(key)
  output_string += ")"
  stack.append(output_string)

# used as an intermediate screen for the shift columns encryption option
def shift_cols(notredameID, ndid, stack):
  # set up screen
  frame_shift_cols = Frame(root)
  frame_shift_cols.place(height = 800, width = 500)
  print_ndid(notredameID, frame_shift_cols)

  # set up & print out buttons for the user to pick from
  shift_op1 = Button(frame_shift_cols, text="Shift Right", command=lambda: shift_cols_right(notredameID, ndid, stack))
  shift_op2 = Button(frame_shift_cols, text="Shift Left", command=lambda: shift_cols_left(notredameID, ndid, stack))
  shift_op1.pack()
  shift_op2.pack()

# used for the intermedite screen for the shift columns right encryption option
def shift_cols_right(notredameID, ndid, stack):
  # set up screen
  frame_cols_right = Frame(root)
  frame_cols_right.place(height=800, width=500)
  print_ndid(notredameID, frame_cols_right)
  col_label = Label(frame_cols_right, text = "Enter the number of the column you want to shift right: (0-2)")

  # get user input
  col_var = StringVar()
  col_entry = Entry(frame_cols_right, width=10, textvariable=col_var)
  col_label.pack()
  col_entry.pack()
  enter_button = Button(frame_cols_right, text = "Enter", command=lambda: check_cols_right(notredameID, ndid, col_var, stack))
  enter_button.pack()

# check to make sure the user entered a column between 0-2
def check_cols_right(notredameID, ndid, col_var, stack):
  col_var = int(col_var.get())
  if((col_var != 0) and (col_var != 1) and (col_var != 2)):
    restart_screen()
  else:
    shift_cols_right2(notredameID, ndid, col_var, stack, 1)

# used to actually shift the columns right and then print out the response
def shift_cols_right2(notredameID, ndid, col, stack, user):
  # only make the screen if it is used in encryption because the user shouldn't
  # see the screen when decrypting
  if(user == 1):
    # set up the screen
    frame_cols_right2 = Frame(root)
    frame_cols_right2.place(height=800, width=500)
    print_ndid(notredameID, frame_cols_right2)
    original_label = Label(frame_cols_right2, text="Original Matrix: ")
    original_label.pack()
    print_array(ndid, frame_cols_right2)

  # the actual encryption steps
  tempVal = ndid[2, col]
  ndid[2, col] = ndid[1, col]
  ndid[1, col] = ndid[0, col]
  ndid[0, col] = tempVal

  # print output & etc. when encrypting only
  if(user == 1):
    encrypted_label = Label(frame_cols_right2, text="Encrypted Matrix: ")
    encrypted_label.pack()
    print_array(ndid, frame_cols_right2)
    return_button = Button(frame_cols_right2, text="Return to Options", command=lambda: build_own(notredameID, ndid, stack))
    return_button.pack()
    output_string = "shift_cols_left2(notredameID, ndid, "
    output_string += str(col)
    output_string += ", stack, 0)"
    stack.append(output_string)

# intermediate screen when shifting columns left so the user can pick a column to shift
def shift_cols_left(notredameID, ndid, stack):
  # set up screen
  frame_cols_left = Frame(root)
  frame_cols_left.place(height=800, width=500)
  print_ndid(notredameID, frame_cols_left)
  col_label = Label(frame_cols_left, text = "Enter the number of the column you want to shift left: (0-2)")

  # get user input
  col_var = StringVar()
  col_entry = Entry(frame_cols_left, width=10, textvariable=col_var)
  col_label.pack()
  col_entry.pack()
  enter_button = Button(frame_cols_left, text = "Enter", command=lambda: check_cols_left(notredameID, ndid, col_var, stack))
  enter_button.pack()

# check to make sure the user actually entered a number between 0 and 2
def check_cols_left(notredameID, ndid, col_var, stack):
  col_var = int(col_var.get())
  if((col_var != 0) and (col_var != 1) and (col_var != 2)):
    restart_screen()
  else:
    shift_cols_left2(notredameID, ndid, col_var, stack, 1)

# prints the screen for shifting the columns and actually does the encryption
def shift_cols_left2(notredameID, ndid, col, stack, user):
  # only makes a frame if the user is actually encrypting and wants to view the output
  if(user == 1):
    # set up the screen
    frame_cols_left2 = Frame(root)
    frame_cols_left2.place(height=800, width=500)
    print_ndid(notredameID, frame_cols_left2)
    original_label = Label(frame_cols_left2, text="Original Matrix: ")
    original_label.pack()
    print_array(ndid, frame_cols_left2)

  # the actual encryption
  tempVal = ndid[0, col]
  ndid[0, col] = ndid[1, col]
  ndid[1, col] = ndid[2, col]
  ndid[2, col] = tempVal

  # only prints the output if the user is looking at the encryption
  if(user == 1):
    encrypted_label = Label(frame_cols_left2, text="Encrypted Matrix: ")
    encrypted_label.pack()
    print_array(ndid, frame_cols_left2)
    return_button = Button(frame_cols_left2, text="Return to Options", command=lambda: build_own(notredameID, ndid, stack))
    return_button.pack()
    output_string = StringVar()
    output_string = "shift_cols_right2(notredameID, ndid, "
    output_string += str(col)
    output_string += ", stack, 0)"
    stack.append(output_string)

# intermediate screen for the shifting rows encryption allowing the user to pick
def shift_rows(notredameID, ndid, stack):
  # set up the screen
  frame_shift = Frame(root)
  frame_shift.place(height=800,width=500)
  print_ndid(notredameID, frame_shift)
  shift_op1 = Button(frame_shift, text="Shift Right", command=lambda: shift_right(notredameID, ndid, stack))
  shift_op2 = Button(frame_shift, text="Shift Left", command=lambda: shift_left(notredameID, ndid, stack))
  shift_op1.pack()
  shift_op2.pack()

# intermediate screen for the shift right function so the user can pick the row
def shift_right(notredameID, ndid, stack):
  # set up the screen
  frame_right = Frame(root)
  frame_right.place(height=800, width=500)
  print_ndid(notredameID, frame_right)
  row_label = Label(frame_right, text="Please enter the number of the row you want to shift right: (0-2)")

  # get user input
  row_var = StringVar()
  row_entry = Entry(frame_right, width=10, textvariable=row_var)
  row_label.pack()
  row_entry.pack()
  enter_button = Button(frame_right, text = "Enter", command=lambda: check_rows_right(notredameID, ndid, row_var, stack))
  enter_button.pack()

# check that the user actually entered a number between 0-2
def check_rows_right(notredameID, ndid, row_var, stack):
  row_var = int(row_var.get())
  if((row_var != 0) and (row_var != 1) and (row_var != 2)):
    restart_screen()
  else:
    shift_right2(notredameID, ndid, row_var, stack, 1)


# intermediate screen for the shift right function so the user can pick the row
def shift_left(notredameID, ndid, stack):
  # set up the screen
  frame_left = Frame(root)
  frame_left.place(height=800, width=500)
  print_ndid(notredameID, frame_left)
  row_label = Label(frame_left, text="Please enter the number of the row you want to shift left: (0-2)")

  # get user input
  row_var = StringVar()
  row_entry = Entry(frame_left, width=10, textvariable=row_var)
  row_label.pack()
  row_entry.pack()
  enter_button = Button(frame_left, text = "Enter", command=lambda: check_row_left(notredameID, ndid, row_var, stack))
  enter_button.pack()

# check to make sure the user actually entered a number between 0-2
def check_row_left(notredameID, ndid, row_var, stack):
  row_var = int(row_var.get())
  if((row_var != 0) and (row_var != 1) and (row_var != 2)):
    restart_screen()
  else:
    shift_left2(notredameID, ndid, row_var, stack, 1)

# the shift left screen that has the output from the function
def shift_left2(notredameID, ndid, row, stack, user):
  # the row is passed as an integer when decrypting
  if type(row) is not int:
     row = int(row.get())

  # only show the screen if the user is encrypting
  if(user == 1):
    frame_left2 = Frame(root)
    frame_left2.place(height=800, width=500)
    print_ndid(notredameID, frame_left2)
    original_label = Label(frame_left2, text="Original Matrix: ")
    original_label.pack()
    print_array(ndid, frame_left2)

  # call the function that does the row shifting
  shift_row_left3(ndid, row, stack, user)

  # only show the output if the user is encrypting
  if(user == 1):
    encrypt_label = Label(frame_left2, text="Encrypted Matrix: ")
    encrypt_label.pack()
    print_array(ndid, frame_left2)
    return_button = Button(frame_left2, text="Return to Options", command=lambda: build_own(notredameID, ndid, stack))
    return_button.pack()
 
# the function to actually shift the rows and if encrypting add info to the stack
def shift_row_left3(ndid, row, stack, user):
  tempVal = ndid[row, 0]
  ndid[row, 0] = ndid[row, 1]
  ndid[row, 1] = ndid[row, 2]
  ndid[row, 2] = tempVal

  # if the user is encrypting information add the decryption method to the stack that is passed
  if(user == 1):
    output_string = StringVar()
    output_string = "shift_right2(notredameID, ndid, "
    output_string += str(row)
    output_string += ", stack, 0)"
    stack.append(output_string)

# shift right function that puts all the encryption info/options on the frame
def shift_right2(notredameID, ndid, row, stack, user):
  # row needs to be an int but is sometimes passed as a string
  if type(row) is not int:
     row = int(row.get())

  # only want to put stuff on the screen when encrypting in build own 
  if(user == 1):
    frame_right2 = Frame(root)
    frame_right2.place(height=800, width=500)
    print_ndid(notredameID, frame_right2)
    original_label = Label(frame_right2, text="Original Matrix: ")
    original_label.pack()
    print_array(ndid, frame_right2)

  # call the function that actually shifts the rows
  shift_row_right3(ndid, row, stack, user)

  # only print info & options if encrypting during build own
  if(user == 1):
    encrypt_label = Label(frame_right2, text="Encrypted Matrix: ")
    encrypt_label.pack()
    print_array(ndid, frame_right2)
    return_button = Button(frame_right2, text="Return to Options", command=lambda: build_own(notredameID, ndid, stack))
    return_button.pack()

# actually shift the rows right & add to stack
def shift_row_right3(ndid, row, stack, user):
  tempVal = ndid[row, 2]
  ndid[row, 2] = ndid[row, 1]
  ndid[row, 1] = ndid[row, 0]
  ndid[row, 0] = tempVal

  # only add the decryption to the stack if it is being encrypted
  if(user == 1):
    output_string = StringVar()
    output_string = "shift_left2(notredameID, ndid, "
    output_string += str(row)
    output_string += ", stack, 0)"
    stack.append(output_string)
  
# there needs to be a number added for caesar's cipher so this function
# gives the screen for that and get's the user's input
def caesar_cipher(notredameID, ndid):
  # set up the screen
  frame_caesar = Frame(root)
  frame_caesar.place(height=800, width=500)
  print_ndid(notredameID, frame_caesar)
  num_label = Label(frame_caesar, text="Please enter a number for Caesar's Cipher: ")

  # get the user input
  num_var = StringVar()
  num_entry = Entry(frame_caesar, width=10, textvariable=num_var)
  num_label.pack()
  num_entry.pack()
  enter_button = Button(frame_caesar, text="Enter", command=lambda: caesar_cipher2(notredameID, ndid, int(num_var.get())))
  enter_button.pack()

# this function actually does the ceasar's cipher encryption steps
def caesar_cipher2(notredameID, ndid, num):
  # set up the screen
  frame_caesar2 = Frame(root)
  frame_caesar2.place(height=800, width=500)
  print_ndid(notredameID, frame_caesar2)
  output_label = Label(frame_caesar2, text="Final Output of Caesar's Cipher:")
  output_label.pack()

  # convert to ascii
  for i in range(len(ndid)):
    for j in range(len(ndid[0])):
      ndid[i][j] = ndid[i][j] + 65

    # initialize cipher array
  cipher_array = np.array([['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']])

    # iterate through ndid and store shifted value in cipher
  for i in range(len(ndid)):
   for j in range(len(ndid[0])):
    val = ndid[i][j]
    cipher_array[i][j] = chr(val + num)
  
  # set up the string of the ouput to print out the result
  output_cipher = StringVar()
  for i in cipher_array:
    for j in i:
      output_cipher.set(output_cipher.get() + j + " ")
    output_cipher.set(output_cipher.get() + "\n")
  output = Label(frame_caesar2, textvariable=output_cipher)
  output.pack()
  
  # the buttons for return/quit options
  op1 = Button(frame_caesar2, text="Decrypt to Original Value", command=lambda: decrypt_caesar(notredameID, cipher_array, num))
  op2 = Button(frame_caesar2, text="Quit", command=lambda: root.destroy())
  op1.pack()
  op2.pack()

# the function the decrypt the ceasar's cipher and put the results on the screen
def decrypt_caesar(notredameID, cipher, num):
  # frame setup
  frame_decrypt_caesar = Frame(root)
  frame_decrypt_caesar.place(height=800, width=500)
  print_ndid(notredameID, frame_decrypt_caesar)
  output_label = Label(frame_decrypt_caesar, text="Decrypted Caesar's Cipher Output: ")
  output_label.pack()

  # initialize ndid array
  ndid = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

  # iterate through cipher and store shifted value back in ndid
  for i in range(len(cipher)):
    for j in range(len(cipher[0])):
      val = ord(str(cipher[i][j]))
      ndid[i][j] = val - num

  # convert to ascii
  for i in range(len(ndid)):
    for j in range(len(ndid[0])):
      ndid[i][j] = ndid[i][j] - 65
  print_array(ndid, frame_decrypt_caesar)

  # return/quit buttons
  option2 = Button(frame_decrypt_caesar, text="Return to Options", command=lambda: new_page(notredameID))
  option2.pack()
  option1 = Button(frame_decrypt_caesar, text="Quit", command=lambda: root.destroy())
  option1.pack()

# substitution function 
def substitution(notredameID, ndid, stack):
  # set up frame
  frame_s = Frame(root)
  frame_s.place(height=800, width=500)
  print_ndid(notredameID, frame_s)
  original_label = Label(frame_s, text="Original Matrix: ")
  original_label.pack()
  print_array(ndid, frame_s)

  # initialize number for encryption
  num = 9

  # convert to ascii
  for i in range(len(ndid)):
    for j in range(len(ndid[0])):
      ndid[i][j] = ndid[i][j] + 65

  # initialize cipher array
  cipher_array = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

  # iterate through ndid and store shifted value in cipher
  for i in range(len(ndid)):
    for j in range(len(ndid[0])):
      val = ndid[i][j]
      cipher_array[i][j] = int(val + num)

  ndid = cipher_array
  
  # output and button options
  final_label = Label(frame_s, text="Encrypted Matrix: ")
  final_label.pack()
  print_array(ndid, frame_s)

  option1 = Button(frame_s, text="Return to Options", command=lambda: build_own(notredameID, ndid,stack))
  option1.pack()

  # only used for encryption so put the decryption method on the stack automatically
  output_string = "decrypt_substitution(notredameID, ndid, "
  output_string += str(num)
  output_string += ")"
  stack.append(output_string)


# decrypts the substitution encrypted array
def decrypt_substitution(notredameID, ndid, num):
  # iterate through cipher and store shifted value back in ndid
  for i in range(len(ndid)):
    for j in range(len(ndid[0])):
      val = ndid[i][j]
      ndid[i][j] = val - num

  for i in range(len(ndid)):
    for j in range(len(ndid[0])):
      ndid[i][j] = ndid[i][j] - 65

# vigenere cipher encryption screen function
def vigenere_cipher(notredameID, ndid, key):
  # set up the screen
  frame_vigenere = Frame(root)
  frame_vigenere.place(height=800, width=500)
  print_ndid(notredameID, frame_vigenere)
  output_label = Label(frame_vigenere, text="Final Output of Vigenere Cipher: ")
  output_label.pack()

  # call the function that does the official encryption steps
  ndid = vigenere_cipher2(ndid, key)
  
  # put output on the screen
  print_array(ndid, frame_vigenere)
  option1 = Button(frame_vigenere, text="Decrypt Vigenere Cipher", command=lambda: decrypt_vigenere(notredameID, ndid, key))
  option1.pack()
  option2 = Button(frame_vigenere, text="Quit", command=lambda: root.destroy())
  option2.pack()

# the function for the actual encryption steps for vigenere's cipher
def vigenere_cipher2(ndid, key):
  for i in range(len(ndid)):
    for j in range (len(ndid[0])):
      ndid[i][j] = (ndid[i][j]+key[i][j])%10
  return ndid
  
# the function the call the screen to decrypt the cipher (for when the user picks an already made encryption)
def decrypt_vigenere(notredameID, ndid, key):
  # set up the screen 
  frame_decrypt_vinegar = Frame(root)
  frame_decrypt_vinegar.place(height=800, width=500)
  print_ndid(notredameID, frame_decrypt_vinegar)
  output_label = Label(frame_decrypt_vinegar, text="Decrypted Result from Vigenere Cipher: ")
  output_label.pack()

  # call the function that does the actual encryption steps
  ndid = vigenere_cipher_decrypt2(ndid, key)
  
  # put the output on the screen
  print_array(ndid, frame_decrypt_vinegar)
  option1 = Button(frame_decrypt_vinegar, text="Return to Options", command=lambda: new_page(notredameID))
  option1.pack()
  option2 = Button(frame_decrypt_vinegar, text="Quit", command=lambda: root.destroy())
  option2.pack()

# the actual decryption steps for vigenere
def vigenere_cipher_decrypt2(ndid, key):
  for i in range(len(ndid)):
    for j in range (len(ndid[0])):
      ndid[i][j] = (ndid[i][j] - key[i][j])%10
  return ndid

# the rail fence encryption method
def rail_fence(notredameID, ndid):
  # initialize key
  key = 3

  # set up the screen
  frame_fence = Frame(root)
  frame_fence.place(height = 800, width=500)
  print_ndid(notredameID, frame_fence)
  output_label = Label(frame_fence, text="Final Output of Rail Fence Encryption: ")
  output_label.pack()

  # initialize array with ''
  cipher = [[ '' for i in range(9)] for j in range(key)]

  #initialize values
  cipher_row = 0
  cipher_col = 0
  ndid_row = 0
  ndid_col = 0
  count = 0

  # initialize first value in cipher
  cipher[cipher_row][cipher_col] = ndid[ndid_row][ndid_row]
  count += 1
  ndid_col += 1

  while (count < 9):
   # check direction
    if (cipher_row == 0):
      dirDown = 1
    elif (cipher_row == key - 1):
      dirDown = 0
    # update cipher rows and columns
    if (dirDown):
      cipher_row += 1
      cipher_col += 1
    else:
      cipher_row -= 1
      cipher_col += 1
    # add ndid value to cipher
    cipher[cipher_row][cipher_col] = ndid[ndid_row][ndid_col]
    # update ndid rows and columns
    if (ndid_col == 2):
      ndid_row += 1
      ndid_col = 0
    else:
      ndid_col += 1
    count += 1
  # initialize final cipher
  final_cipher = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
  # iterate through cipher by row and get values that aren't ''
  row = 0
  col = 0
  for i in range(key):
    for j in range(9):
      if(cipher[i][j] != ''):
        final_cipher[row][col] = cipher[i][j]
        col += 1
        if(col == 3):
          row += 1
          col = 0
  # print out final results & buttons for options
  print_array(final_cipher, frame_fence) 
  op1 = Button(frame_fence, text="Decrypt Rail Fence Encryption", command=lambda: decrypt_rail_fence(notredameID, final_cipher, key))
  op2 = Button(frame_fence, text="Quit", command=lambda: root.destroy())
  op1.pack()
  op2.pack()

# decryption function for the rail fence encryption
def decrypt_rail_fence(notredameID, cipher, key):
  # set up the screen
  frame_decrypt_rail = Frame(root)
  frame_decrypt_rail.place(height=800, width=500)
  print_ndid(notredameID, frame_decrypt_rail)

  # initialize ndid
  ndid = [[ '' for i in range(9)] for j in range(key)]

  #initialize values
  cipher_row = 0
  cipher_col = 0
  ndid_row = 0
  ndid_col = 0
  count = 1
  # initialize first value in ndid
  ndid[ndid_row][ndid_row] = '-'
  cipher_col += 1

  while (count < 9):
   # check direction
    if (ndid_row == 0):
      dirDown = 1
    elif (ndid_row == key - 1):
      dirDown = 0
    # update ndid rows and columns
    if (dirDown):
      ndid_row += 1
      ndid_col += 1
    else: 
      ndid_row -= 1
      ndid_col += 1
    # add '-' to ndid where next value should be
    ndid[ndid_row][ndid_col] = '-'
    count += 1
  # iterate through ndid by row and insert cipher values at '-'
  row = 0
  col = 0
  for i in range(key):
    for j in range(9):
      if(ndid[i][j] == '-'): 
        ndid[i][j] = cipher[row][col]
        col += 1
        if(col == 3):
          row += 1
          col = 0  
  # initialize final ndid
  final_ndid = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
  # read through ndid in zig zag
  #initialize values
  cipher_row = 0
  cipher_col = 0
  ndid_row = 0
  ndid_col = 0
  count = 1
  # initialize first value in ndid
  final_ndid[ndid_row][ndid_row] = ndid[cipher_row][cipher_col]
  ndid_col += 1
    
  while (count < 9):
    # check direction
    if (cipher_row == 0):
      dirDown = 1
    elif (cipher_row == key - 1):
      dirDown = 0
    # update ndid rows and columns
    if (dirDown):
      cipher_row += 1
      cipher_col += 1
    else: 
      cipher_row -= 1
      cipher_col += 1
    # store value in final_ndid
    final_ndid[ndid_row][ndid_col] = ndid[cipher_row][cipher_col]
    # update ndid rows and columns
    if (ndid_col == 2):
      ndid_row += 1
      ndid_col = 0
    else:
      ndid_col += 1
    count += 1

  # put output & buttons on the screen
  print_array(final_ndid, frame_decrypt_rail)
  op1 = Button(frame_decrypt_rail, text="Return to Options", command=lambda: new_page(notredameID))
  op2 = Button(frame_decrypt_rail, text="Quit", command=lambda: root.destroy())
  op1.pack()
  op2.pack()

# intermediate function for aes: calls the shift row function and appends the decryption function to the stack 
def encrypt_aes_shift(ndid, stack):
  # encrypt the ndid
  shift_row_left3(ndid, 1, stack, 0)
  for i in range(2):
    shift_row_left3(ndid, 2, stack, 0)

  # append the decryption function to the stack
  stack.append("decrypt_aes_shift(ndid, aes_stack)")
  return ndid

# intermediate decryption function for aes: decrypts the encrypt_aes_shift function
def decrypt_aes_shift(ndid, stack):
  shift_row_right3(ndid, 1, stack, 0)
  for i in range(2):
    shift_row_right3(ndid, 2, stack, 0)
  return ndid

# intermediate function for aes: encrypts the ndid and then adds the decryption function to the stack
def encrypt_aes_mix_cols(ndid, key, stack):
  # encrypt the ndid
  ndid = mult_matrix(ndid, key)

  # add the decryption to the stack
  stack_append = StringVar()
  stack_append = "decrypt_aes_mix_cols(ndid, "
  stack_append += str(key)
  stack_append += ")"
  stack.append(stack_append)
  return ndid

# intermediate decryption function for aes: decrypts the encrypt_aes_mix_cols function
def decrypt_aes_mix_cols(ndid, key):
  ndid = mult_inv_matrix(ndid, key)
  return ndid

# aes overall function
def aes(notredameID, ndid):
  # set up the screen
  frame_aes = Frame(root)
  frame_aes.place(height=800, width=500)
  print_ndid(notredameID, frame_aes)
  key = [[7, 7, 1,], [5, 9, 8], [7, 5, 8]]
  output_label = Label(frame_aes, text="Final Output of AES Encryption: ")
  output_label.pack()

  # keeps track of all the decryption functions that need to be called (and their order)
  aes_stack = deque()
  
  # calls the first encryption function
  for i in range(7):
    ndid = vigenere_cipher2(ndid, key)

  # calls the next encryption functions
  for i in range(7):
    ndid = encrypt_aes_shift(ndid, aes_stack)
    ndid = encrypt_aes_mix_cols(ndid, key, aes_stack)

  # outputs the encrypted ndid and the options
  print_array(ndid, frame_aes)
  op1 = Button(frame_aes, text="Decrypt AES", command=lambda: aes_decrypt(notredameID, ndid, key, aes_stack))
  op2 = Button(frame_aes, text="Quit", command=lambda: root.destroy())
  op1.pack()
  op2.pack()

# overall decryption function for aes
def aes_decrypt(notredameID, ndid, key, aes_stack):
  # set up screen
  frame_aes2 = Frame(root)
  frame_aes2.place(height=800, width=500)
  print_ndid(notredameID, frame_aes2)

  # calls most of the decryption functions
  while(aes_stack):
    ndid = eval(aes_stack.pop())

  # calls the rest of the decryption
  for i in range(7):
    ndid = vigenere_cipher_decrypt2(ndid, key)

  # prints out the output and the buttons
  output_label1 = Label(frame_aes2, text="Decoded AES Matrix: ")
  output_label1.pack()
  print_array(ndid, frame_aes2)

  op1 = Button(frame_aes2, text="Return to Options", command=lambda: new_page(notredameID))
  op2 = Button(frame_aes2, text="Quit", command=lambda: root.destroy())
  op1.pack()
  op2.pack()

# screen and options for the existing encryptions the user can pick from
def apply_existing(notredameID, ndid, stack):
  # set up the screen
  frame_apply = Frame(root)
  frame_apply.place(height=800, width=500)
  print_ndid(notredameID, frame_apply)
  label3 = Label(frame_apply, text="Select an Algorithm:")
  label3.pack()

  # options defined & placed on screen
  option3 = Button(frame_apply, text="Caesar's Cipher", command=lambda: caesar_cipher(notredameID, ndid))
  option4 = Button(frame_apply, text="Vigenere Cipher", command=lambda: vigenere_cipher(notredameID, ndid, random_key(ndid)))
  option5 = Button(frame_apply, text="Advanced Encryption Standard (AES)", command=lambda: aes(notredameID, ndid))
  option6 = Button(frame_apply, text="Rail Fence Encryption", command=lambda: rail_fence(notredameID, ndid))
  option3.pack()
  option4.pack()
  option5.pack()
  option6.pack()
 

# decrypt function for build own
# calls all the decryption functions on the stack passed
def decrypt_everything(notredameID, ndid, stack):
  # set up screen
  decrypt_frame = Frame(root)
  decrypt_frame.place(heigh=800, width=500)
  print_ndid(notredameID, decrypt_frame)
  label1 = Label(decrypt_frame, text="Final Encrypted Matrix: ")
  label1.pack()

  # print out the ndid passed to it
  print_array(ndid, decrypt_frame)

  # call all the decryption functions on the stack
  while(stack):
    intermediate_label = Label(decrypt_frame, text="Partially Decrypted: ")
    intermediate_label.pack()
    
    # multiplication one was having trouble with the passing by reference so is done by returning the ndid
    if("mult_inv_matrix1" in stack[-1]):
      ndid = eval(stack.pop())

    # the rest of them pass by reference
    else:
      eval(stack.pop())
    # each time the ndid is decrypted a step the output is placed on the screen
    print_array(ndid, decrypt_frame)

  # print out the final results & give options
  final_label = Label(decrypt_frame, text="Original Matrix: ")
  final_label.pack()
  print_array(ndid, decrypt_frame)
  return_button = Button(decrypt_frame, text="Return to Options", command=lambda: new_page(notredameID))
  quit_button = Button(decrypt_frame, text="Quit", command=lambda: root.destroy())
  return_button.pack()
  quit_button.pack()

# all the options for when the user decides to build their own encryption
def build_own(notredameID, ndid, stack):
  # set up the screen
  frame_options = Frame(root)
  frame_options.place(height=800, width=500)
  print_ndid(notredameID, frame_options)
  encryption_label = Label(frame_options, text="Current Encryption Stage: ")
  encryption_label.pack()
  print_array(ndid, frame_options)
  label4 = Label(frame_options, text="Select an Encryption Step:")
  label4.pack()

  # options defined & put on the screen
  option6 = Button(frame_options, text="Substitution", command=lambda: substitution(notredameID, ndid, stack))
  option7 = Button(frame_options, text="Shift rows", command=lambda: shift_rows(notredameID, ndid, stack))
  option8 = Button(frame_options, text="Shift columns", command=lambda: shift_cols(notredameID, ndid, stack))
  option9 = Button(frame_options, text="Matrix multiplication", command=lambda: matrix_mult(notredameID, ndid, stack))
  option11 = Button(frame_options, text="Decrypt", command=lambda: decrypt_everything(notredameID, ndid, stack))
  option10 = Button(frame_options, text="Quit", command=lambda:root.destroy())
  option6.pack()
  option7.pack()
  option8.pack()
  option9.pack()
  option11.pack()
  option10.pack()

# new page screen & options, first thing after entering NDID
def new_page(notredameID):
  if(len(str(notredameID.get())) != 9):
    restart_screen()
  stack = deque() # used to store the returning function titles

  # set up the frame
  frame = Frame(root)
  frame.place(height=800, width=500)
  print_ndid(notredameID, frame)
  label2 = Label(frame, text="Select an Option:")
  label2.pack()

  # change the ndid entered from a string to a 3x3 array of integers (ints are used almost all of the time in the encryption functions)
  ndid = np.array(list(str(notredameID.get()))).reshape((3,3))
  ndid = ndid.astype(int)

  # output options for the user
  option1 = Button(frame, text = "Apply an Existing Algorithm", command=lambda: apply_existing(notredameID, ndid, stack))
  option2 = Button(frame, text = "Build your Own Algorithm", command=lambda: build_own(notredameID, ndid, stack))
  option3 = Button(frame, text = "Quit", command=lambda: root.destroy())
  option1.pack()
  option2.pack()
  option3.pack()

# used to make sure the user actually inputted a nine digit number for the NDID
def middle_page(ndid):
  if(len(str(ndid.get())) != 9):
    restart_screen()
  else:
    new_page(ndid)

# restart screen for if the user enters something they shouldn't
# i.e. a NDID that is less than 9 digits, or enter 45 for the row to rotate
def restart_screen():
  # set up screen
  restart_frame = Frame(root)
  restart_frame.place(height=800, width=500)
  notredameID = StringVar()
  output_info = Label(restart_frame, text="You entered something incorrectly, please start over")
  output_info.pack()
  ndid_input_label = Label(restart_frame, text="Please enter your nine digit NDID: ")
  ndid_input_label.pack()
  ndid_input_user = Entry(restart_frame, width=20, textvariable=notredameID)
  ndid_input_user.pack()
  button = Button(restart_frame, text="Enter", command=lambda: middle_page(notredameID))
  button.pack()

# original root screen setup
root = Tk()
root.geometry("500x800")

# use frames to "clear" the screen & do a new screen
frame1 = Frame(root, height=800, width=500)
frame1.pack()
# output for instructions for the user
newid = StringVar()
title = Label(frame1, text="Encrypt your ND ID")
title.pack()

# get user input on what the NDID they are encrypting is
notredameID_1 = Entry(frame1, width=20, textvariable=newid)
notredameID_1.pack()
button = Button(frame1, text = "Enter", command=lambda: middle_page(newid))
button.pack()
# print out the NDID as the user enters it so they can see it
idlabel = Label(root, text="Your NDID:")
idlabel.pack()
notredameID = Label(root, textvariable=newid)
notredameID.pack()

# keeps the root from destroying itself until the root.destroy() function is called when the user quits
root.mainloop()
