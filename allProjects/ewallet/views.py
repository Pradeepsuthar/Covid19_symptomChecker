from django.shortcuts import render, redirect
import re
import os
from datetime import datetime
# datetime object containing current date and time
now = datetime.now()

# Create your views here.
bal = ["Current Bal : Rs.10.0\n", "Cashback : Rs.0.0\n", "Refund : Rs.0.0\n"] 
# Writing to file 
bal_file = open('ewallet/walletBalance.txt', 'w') 
bal_file.writelines(bal) 
bal_file.close()


filename = 'ewallet/walletBalance.txt'

if os.path.isfile(filename):
    print("file exist at this time")
else:
    print("file not exists at this time")
    # Create your views here.
    bal = ["Current Bal : Rs.10.0\n", "Cashback : Rs.0.0\n", "Refund : Rs.0.0\n"] 
    # Writing to file 
    bal_file = open('ewallet/walletBalance.txt', 'w') 
    bal_file.writelines(bal) 
    bal_file.close()


def index(request):
    title = "e-wallet"
    # Opening file 
    bal_file = open('ewallet/walletBalance.txt', 'r') 
    # Using for loop 
    for line in bal_file: 
        if line.startswith('Current Bal'):
            num = re.findall("\d+\.\d+", line)
            CurrentBal = float(num[0])
        elif line.startswith('Cashback'):
            num = re.findall("\d+\.\d+", line)
            CashbackAmt = float(num[0])
        elif line.startswith('Refund'):
            num = re.findall("\d+\.\d+", line)
            RefundAmt = float(num[0])
        else:
            print("Not found line")
    # Closing files 
    bal_file.close() 
    return render(request, 'ewallet/index.html', {'title':title,'currentbal':CurrentBal, 'cashback':CashbackAmt, 'refund':RefundAmt})

def addMoney(request):
    if request.method == 'POST':  
        print("Add Money successfully")
        addedAmount = request.POST['amount']  
        print("Add Amount is :",addedAmount)

        # Old bal Opening file 
        bal_file = open('ewallet/walletBalance.txt', 'r') 
        # Using for loop 
        for line in bal_file: 
            if line.startswith('Current Bal'):
                num = re.findall("\d+\.\d+", line)
                CurrentBal = float(num[0]) + float(addedAmount)
            elif line.startswith('Cashback'):
                num = re.findall("\d+\.\d+", line)
                CashbackAmt = float(num[0])
            elif line.startswith('Refund'):
                num = re.findall("\d+\.\d+", line)
                RefundAmt = float(num[0])
            else:
                print("Not found line")
        # Closing files 
        bal_file.close() 

        # Update bal Opening file 
        update_bal_file = open('ewallet/walletBalance.txt', 'w') 
        addAmt = 'Current Bal : Rs.{}\n'.format(str(CurrentBal))
        bal_list = [addAmt,"Cashback : Rs.0.0\n", "Refund : Rs.0.0\n"]
        update_bal_file.writelines(bal_list) 
        update_bal_file.close()

        updateTransactions(now.strftime("%d/%m/%Y"),now.strftime("%H:%M:%S"),"Add money to wallet","+",str(addedAmount),str(CurrentBal))
        return redirect('/ewallet/')
    return redirect('/')

def updateTransactions(currentDate,currentTime,transactionsDetails,amtSign,amount,availableBalance):


    filename = 'ewallet/Transactions.txt'
    TransactionsFile = open('ewallet/Transactions.txt', 'a')

    if os.path.isfile(filename):
        print("file exist at this time")
    else:
        print("file not exists at this time")
        TransactionsFile = open('ewallet/Transactions.txt', 'a')

        
    # createTrans = ["DATE & TIME", "TRANSACTION DETAILS", "amtSign","AMOUNT", "AVAILABLE BALANCE"] 
    createTrans = [str(currentDate)+", ",str(currentTime)+", ",str(transactionsDetails)+", ",str(amtSign)+" ",str(amount)+", ",str(availableBalance)+" "] 
    TransactionsFile.writelines(createTrans)
    TransactionsFile.writelines("\n")
    TransactionsFile.close()

def Transactions(request):
    filename = 'ewallet/Transactions.txt'
    title = "e-wallet | Transactions"

    if os.path.isfile(filename):
        print("file exist at this time")

        mylist = []
        # Opening file 
        TransactionsViewFile = open('ewallet/Transactions.txt', 'r') 
        # Using for loop 
        for line in TransactionsViewFile: 
            mylist.append(line.split(', ', 6))
        # Closing files 
        TransactionsViewFile.close() 

        print(mylist)
        for i in mylist:
            print("{}|{}  {}  Rs.{}   Rs.{}".format(i[0],i[1],i[2],i[3],i[4]))
            date = i[0]
            time = i[1]
            TRANSACTION_DETAILS = i[2]
            updateAmt = i[3]
            AVAILABLE_BALANCE = i[4]


        ViewTransactionsList = [date,time,TRANSACTION_DETAILS,updateAmt,AVAILABLE_BALANCE]
        return render(request, 'ewallet/transactions.html', {'title':title,'TransactionsList':mylist})
    else:
        return redirect('/ewallet/')

