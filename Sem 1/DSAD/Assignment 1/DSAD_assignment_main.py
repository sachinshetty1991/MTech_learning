import os
import sys

# Lets Create a Max Heap class
class MaxHeap:
    """
    Max Heap Class to create a max Heap using Python List (Array)
    """
    def __init__(self,max_size):
        """
        Initialize the heap with max size
        """
        self.heap = []
        self.size = 0
        self.max_size = max_size
    
    def insert(self, value):
        """
        Insert a value into the heap and heapify up to make it a max heap again
        """
        if self.size >= self.max_size:
            raise Exception('Heap is full')

        self.heap.append(value)
        self.size += 1
        self.heapify_up(self.size - 1)
    
    def heapify_up(self, index):
        """
        This function would heapify up the value at index
        """
        parent = (index - 1) // 2
        if parent < 0:
            return
        if self.heap[index] > self.heap[parent]: # Exchange the value if the parent is smaller than the child
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self.heapify_up(parent)

    def extract_max(self):
        """
        This function would get the maximum value from the heap and index 0, replace the 0 index with last elemeent 
        and heapify down to make it a max heap again
        """
        if self.size <= 0:
            raise Exception('Heap is empty')
        max_value = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heapify_down(0)
        return max_value

    def heapify_down(self, index):
        """
        This function would heapify down the value at index
        """
        left = (2 * index) + 1
        right = (2 * index) + 2
        largest = index

        # check which is the largest value among the left and right child
        if left < self.size and self.heap[left] > self.heap[largest]:
            largest = left
        if right < self.size and self.heap[right] > self.heap[largest]:
            largest = right

        # if the largest value is not the index, exchange the value and heapify down
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self.heapify_down(largest)
    
    def get_max(self):
        '''
        This function would get the maximum value from the heap
        '''
        if self.size <= 0:
            raise Exception('Heap is empty')
        return self.heap[0]
    
    def get_size(self):
        """
        This function would get the size of the heap
        """
        return self.size

class get_max_cost_heap:
    """
    This class implement the max cost finding algorithm for Sweet box assignment problem
    """
    def __init__(self,price_list,shipping_list,items_to_be_selected):
        """
        Initialize the class with all the input parameters and call the get_max_cost function
        """
        self.price_list = price_list
        self.shipping_list = shipping_list
        self.items_to_be_selected = items_to_be_selected
        
    def get_cost_for_selected_sweets(self,selected_price_list,selected_shipping_list):
        """
        This function would calculate the total cost for the selected sweets based on total price and min of shipping cost times number of sweets
        """
        return sum(selected_price_list) + min(selected_shipping_list)*len(selected_shipping_list)

    # fetches the all index values for the given element available in the list
    def getIndex(self,listOfElements, element):
        indexList = []
        for i in range(len(listOfElements)):
            if listOfElements[i] == element:
                indexList.append(i)
        return indexList

    def get_max_cost(self):
        """
        This function would select the items_count number of sweets from price_list that get maximum cost 
        """
        price_list = self.price_list
        shipping_list = self.shipping_list
        items_count = self.items_to_be_selected

        no_of_sweets = len(price_list)
        if no_of_sweets != len(shipping_list):
            raise Exception('Price and shipping list should be of same length')
        if items_count > no_of_sweets:
            raise Exception('Items count should be less than or equal to the number of sweets')

        # If only one sweet, return the sweet with maximum sum of price and shipping cost
        if items_count == 1:
            return max([price_list[i]+shipping_list[i] for i in range(no_of_sweets)])

        # If total items required is equally to total sweets available, then no need to go for selection logic and we can 
        # compute the max cost directly
        if items_count == no_of_sweets:
            return self.get_cost_for_selected_sweets(price_list,shipping_list)
        
        # Now when items to select is less the total sweets available then we have to select the items greedily
        # We can use a heap to select the items greedily based on hint provided in the problem


        # Create a MaxHeap with the size of the number of sweets to store the cost of each sweet and shippping price so that we 
        # can get the top shipping price with the least time compexity
        # price_max_heap = MaxHeap(no_of_sweets)
        shipping_max_heap = MaxHeap(no_of_sweets)

        for i in range(no_of_sweets):
            # price_max_heap.insert(price_list[i])
            shipping_max_heap.insert(shipping_list[i])

        selected_items_price_list = []
        selected_items_shipping_cost_list = []
        last_max_shipping_price = 0
        all_selected_indx = []

        # Select the items_count - 1 sweets based on max shipping price
        while len(selected_items_price_list) < (items_count - 1):
            shipping_list_max_value = shipping_max_heap.extract_max()

            # print(shipping_list_max_value)
            # If the max shipping price is same as the last max shipping price, then we can ignore that sweet and move to next largest
            # as the logic in hint provided
            if shipping_list_max_value == last_max_shipping_price:
                continue
            
            last_max_shipping_price = shipping_list_max_value

            # we have to get the sweet's price based on the shipping price we got above also add it to list of all_selected_indx
            sweet_indx = self.getIndex(shipping_list,shipping_list_max_value)
            
            if len(sweet_indx) > 1:
                # if more than one sweet has the same shipping price, then we have to get the sweet with maximum price
                max_value = -1
                for indx in sweet_indx:
                    if price_list[indx] > max_value:
                        max_value = price_list[indx]
                        max_index = indx
                all_selected_indx.append(max_index)
                selected_items_price_list.append(max_value)
                selected_items_shipping_cost_list.append(shipping_list_max_value)
            else:
                # In case there is only one sweet with the same shipping price, then add that to select items list
                all_selected_indx.append(sweet_indx[0])
                selected_items_price_list.append(price_list[sweet_indx[0]])
                selected_items_shipping_cost_list.append(shipping_list[sweet_indx[0]])
        
        # Now we have to get the last sweet by iterating through rest of the sweets and finding maximum cost
        max_cost = -1
        # lets iterate through the rest of the sweets
        for i in range(no_of_sweets):
            if i not in all_selected_indx:
                temp_price_list = selected_items_price_list.copy()
                temp_price_list.append(price_list[i])
                temp_shipping_list = selected_items_shipping_cost_list.copy()
                temp_shipping_list.append(shipping_list[i])
                cost = self.get_cost_for_selected_sweets(temp_price_list,temp_shipping_list)
                if cost > max_cost:
                    max_cost = cost
                    

        return max_cost

class get_max_cost_brute_force:
    """
    This class implement the brute force method to find the maximum cost for Sweet box
    """

    def __init__(self,price_list,shipping_list,items_to_be_selected):
        """
        Initialize the class with all the input parameters
        """
        self.price_list = price_list
        self.shipping_list = shipping_list
        self.items_to_be_selected = items_to_be_selected
    
    def get_total_cost(self,list_item_price, list_shipping_price):
        return sum(list_item_price) + (min(list_shipping_price) * len(list_shipping_price))

    def get_max_value(self):

        import itertools
        
        val1 = self.price_list
        val2 = self.shipping_list
        num = self.items_to_be_selected

        if len(val1) != len(val2):
            raise Exception('Length of both array should be same')
        if num > len(val1):
            raise Exception('Number of element should be less than length of array')
        if num <= 0:
            raise Exception('Number of element should be greater than 0')
        for i in range(len(val1)):
            if val1[i] < 0 or val2[i] < 0:
                raise Exception('Value of both array should be greater than 0')
        # Lets brute force through all combination of values and find the max value
        max_value = 0
        max_combination = []
        indx_list = list(range(len(val1)))
        # combination_dataframe = pd.DataFrame(list(itertools.combinations(indx_list, num)), columns=["combination{}".format(i) for i in range(num)])
        for selected_combo_indx in itertools.combinations(indx_list, num):
            # selected_combo_indx = combination_dataframe.iloc[i,].to_list()
            total = self.get_total_cost([val1[i] for i in selected_combo_indx],[val2[i] for i in selected_combo_indx])
            # print([val1[i] for i in selected_combo_indx],total)
            if total > max_value:
                max_value = total
                max_combination = selected_combo_indx
        
        return max_value


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
    
    # Check first line that would be the number of test cases
    no_of_test_cases = input_data[0]
    if not no_of_test_cases.isdigit():
        raise "First line of input file should be the number of test cases"

    # Check if the number of test cases is valid
    if int(no_of_test_cases) < 1 or (int(no_of_test_cases)*3 + 1) != len(input_data):
        raise "Number of test cases is not valid"

    # lets iterate over the test cases
    for i in range(int(no_of_test_cases)):
        # read the next line to get the number of sweets and number of items to be taken
        line = input_data[i*3 + 1]
        test_price_values = input_data[i*3 + 2]
        test_shipping_values = input_data[i*3 + 3]

        no_of_sweets = int(line.split(" ")[0])
        no_of_items = int(line.split(" ")[1])

        price_list = [int(x) for x in test_price_values.split(" ")]
        shipping_list = [int(x) for x in  test_shipping_values.split(" ")]

        # Check if the number of sweets and number of items are valid
        if no_of_sweets < 1 or no_of_sweets != len(price_list) or no_of_items < 1 :
            raise "Number of sweets or items are not valid"

        # pass the price list, shiping list and number of items to the get_total_cost function
        total_cost = get_max_cost_heap(price_list, shipping_list, no_of_items).get_max_cost()

        # total_cost_brute_force = get_max_cost_brute_force(price_list, shipping_list, no_of_items).get_max_value()

        Outputfile.write(str(total_cost))
        if i != (int(no_of_test_cases) - 1):
            Outputfile.write("\n")
        # Outputfile.write('\n')

        # print([no_of_items,no_of_sweets,price_list,shipping_list,total_cost,total_cost_brute_force])

