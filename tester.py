import time

def main():
    
    counter = 0
    print("Time: " + str(time.time()))
    while(counter < 10):
        print("hello")
        time.sleep(3)
        counter += 1
    print(time.time())
main()

# sorted = sorted("Sorting something alphabetically".split(), key=str.lower)
# print(sorted)