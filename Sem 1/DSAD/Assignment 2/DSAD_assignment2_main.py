'''
This is the main file for the assignment 2.
Group number: 329
Members:
    Sachin Shetty
    Ashok Kumar
'''

# Import the required libraries
import os,sys

class get_overtake_count:

    def __init__(self,no_of_cars,pos,speed):
        """
        Initialize the class with all the input parameters
        """
        self.no_of_cars = no_of_cars
        self.pos = pos
        self.speed = speed


    def get_overtake_count(self):
        '''
        This function returns the number of cars that can overtake the current car

        # Divide and conquer
        # Approach to be used : 
        # step 1 : (Divide) For each car, identify the cars behind it using position of the car 
        # step 2 : (conquer) find how many of this cars have speed more than that of the current car because all these cars would overtake the current car.
        # step 3 : (combine) find the total overtake by adding all these overtake .
        '''
        overtake_count = 0
        for i in range(self.no_of_cars):
            # Identify the current position of the car
            init_position = self.pos[i]

            # Identify the current speed of the car
            speed_of_car = self.speed[i]

            # Check for the cars behind the current car and having speed more than the current car
            overtaking_cars = [j for j in range(self.no_of_cars) if self.pos[j] < init_position and self.speed[j] > speed_of_car]

            # Add the overtake count for this car to total overtake count
            overtake_count += len(overtaking_cars)

        return overtake_count


if __name__ == "__main__":
    # set working directory to the directory of this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

    # check if inputPS9.txt exists
    if not os.path.exists("inputPS9.txt"):
        raise "Input file inputPS9.txt not found in same directory as code"

    
    with open("inputPS9.txt", "r") as f:
        input_data = f.read().splitlines()

    # create a text file to write the output if it does not exist 
    if not os.path.exists("outputPS9.txt"):
        with open("outputPS9.txt", "w") as f:
            pass
    
    Outputfile = open("outputPS9.txt","w+")

    # Since as per requirement we have one input in one file we can test the logic by changing value in same file

    # Check first line that would be the number of cars
    no_of_cars = input_data[0]
    if not no_of_cars.isdigit():
        raise "First line of input file should be the number of test cases"

    # Check if the number of cars is greater than 0
    if int(no_of_cars) <= 0:
        raise "Number of test cases should be greater than 0"

    # Check if the number of cars is less than or equal to 105
    if int(no_of_cars) > 105:
        raise "Number of test cases should be less than or equal to 105"

    speed_list = input_data[1].split(" ")
    position_list = input_data[2].split(" ")

    speed_list = [int(i) for i in speed_list]
    position_list = [int(i) for i in position_list]

    get_overtake_count_obj = get_overtake_count(int(no_of_cars),position_list,speed_list)
    overtake_count = get_overtake_count_obj.get_overtake_count()

    # # Check if the output is same as the expected output in promptsPS9.txt file
    # with open("promptsPS9.txt", "r") as f:
    #     expected_output = f.read().splitlines()

    # expected_output = expected_output[0]
    # if expected_output.isdigit():
    #     expected_output = int(expected_output)
    # else:
    #     raise "Expected output should be an integer"
    
    # if overtake_count == expected_output:
    #     print("Test case passed")

    Outputfile.write(str(overtake_count))