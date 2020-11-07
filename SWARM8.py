#Algorithm
lst = []
start_time = time.time()
seconds = 7   
while(True):
    #LC1 is load cell on palmar grip
    while(LC1.inWaiting()==0): #Have run for predetermined amount of time in whcih they are to produce the max grip force
        #max([812 814 814 815 815])
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            lst.append(LC1)
            if elapsed_time > seconds:
                maxval = max(lst)
                print("Trial ended with max force of: " + str(int(maxval))  + " Units")
                break
            