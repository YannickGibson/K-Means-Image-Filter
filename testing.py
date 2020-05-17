import filter
import exceptions    
import random
import time

class UnitTest:

    def k_equal_to_0_returns_exception(self):

        try:
            ##ACT
            filter.k_means("originals/balls.jpg", k=0)
            
        except exceptions.ValueTooSmall:
            ## ASSERT
            return True

        raise False

    def crete_three_lists_with_10_colors(self):

        ## ARANGE
        ## ACT
        centers = filter.generate_centers(10)


        ## ASSERT
        # Check if lengths are correct
        if  len(centers[0]) == 10 and \
            len(centers[1]) == 10 and \
            len(centers[2]) == 10:

            # Check if all numbers are int
            if isinstance(sum(centers[0] + centers[1] + centers[2]), int):
                return True

        return False

    def crete_three_lists_with_3_colors(self):

        ## ARANGE
        ## ACT
        centers = filter.generate_centers(3)

        ## ASSERT
        # Check if lengths are correct
        if  len(centers[0]) == 3 and \
            len(centers[1]) == 3 and \
            len(centers[2]) == 3:

            # Check if all numbers are int
            if isinstance(sum(centers[0] + centers[1] + centers[2]), int):
                return True

        return False

    def creating_plot_returns_correct_type(self):
        ##ARRANGE
        ## ACT
        axes = filter.create_plot("Test Plot")

        #ASSERT
        return type(axes) == filter.Axes3D

    def comparing_groups_of_numbers_with_equal_values(self):

        ## ARRANGE

        # Consists of R, G, B, Order, 12 groups
        group1 = [ ([],[],[],[]) for _ in range(12)]
        group2 = [ ([],[],[],[]) for _ in range(12)]

        # Image with 1000 pixels total
        for i in range(1000):
            r_color_group = random.randint(0,11)

            r_num1 = random.randint(0,255)
            r_num2 = random.randint(0,255)
            r_num3 = random.randint(0,255)
            r_num4 = random.randint(0,255)

            group1[r_color_group][0].append(r_num1)
            group1[r_color_group][1].append(r_num2)
            group1[r_color_group][2].append(r_num3)
            group1[r_color_group][3].append(r_num4)
            
            group2[r_color_group][0].append(r_num1)
            group2[r_color_group][1].append(r_num2)
            group2[r_color_group][2].append(r_num3)
            group2[r_color_group][3].append(r_num4)
        

        ## ACT
        result = filter.compare_groups(group1, group2)

        ## ASSERT
        return result
        

    def comparing_groups_of_numbers_with_all_unequal_values(self):

        ## ARRANGE

        # Consists of R, G, B, Order, 12 groups
        group1 = [ ([],[],[],[]) for _ in range(12)]
        group2 = [ ([],[],[],[]) for _ in range(12)]

        # Image with 1000 pixels total
        for i in range(1000):
            r_color_group = random.randint(0,11)

            r_num1 = random.randint(0,255)
            r_num2 = random.randint(0,255)
            r_num3 = random.randint(0,255)
            r_num4 = random.randint(0,255)

            group1[r_color_group][0].append(r_num1)
            group1[r_color_group][1].append(r_num2)
            group1[r_color_group][2].append(r_num3)
            group1[r_color_group][3].append(r_num4)
            
            group2[r_color_group][0].append(r_num1 + 1)
            group2[r_color_group][1].append(r_num2 + 1)
            group2[r_color_group][2].append(r_num3 + 1)
            group2[r_color_group][3].append(r_num4 + 1)
        


        ## ACT
        result = filter.compare_groups(group1, group2)


        ## ASSERT
        return result == False

        

    def comparing_groups_of_numbers_with_one_unequal_values(self):

        ## ARRANGE

        # Consists of R, G, B, Order, 12 groups
        group1 = [ ([],[],[],[]) for _ in range(12)]
        group2 = [ ([],[],[],[]) for _ in range(12)]

        # Image with 1000 pixels total
        for i in range(1000):
            r_color_group = random.randint(0,11)

            r_num1 = random.randint(0,255)
            r_num2 = random.randint(0,255)
            r_num3 = random.randint(0,255)
            r_num4 = random.randint(0,255)

            group1[r_color_group][0].append(r_num1)
            group1[r_color_group][1].append(r_num2)
            group1[r_color_group][2].append(r_num3)
            group1[r_color_group][3].append(r_num4)
            
            group2[r_color_group][0].append(r_num1)
            group2[r_color_group][1].append(r_num2)
            group2[r_color_group][2].append(r_num3)
            group2[r_color_group][3].append(r_num4)
        
        # Making one number unequal
        # Zeroth group => red color => first color in list => append the value value
        group1[0][0][0] += 1


        ## ACT
        result = filter.compare_groups(group1, group2)


        ## ASSERT

        return result == False
     

def run_all_tests():
    # Create instance of the class
    unitTest = UnitTest()

    # Get all attributes of class that are functions
    functions = [ attr for attr in  UnitTest.__dict__.values() if callable(attr) ]

    # Log
    print("Running {} tests...".format(len(functions)))
    print("|")

    for fun in functions:
        # Make readable string from function name 
        fun_name = fun.__name__.replace("_", " ").capitalize()

        error = None
        result = False
        start_time = time.time()
        try: 
            # Running test function
            result = fun(unitTest)
        except Exception as e:
            # Unexpected errors
            error = e

        str_result = "Successful" if result == True else "Failed"
        if error != None:
            str_result += ": " + str(error) 

        time_elapsed = time.time() - start_time

        # Log
        print("||{} - {} ({}ms)".format(fun_name, str_result, round(time_elapsed * 1000)))

    print("|")
            

# If this script is ran directly; it's not imported with module
if __name__ == "__main__":
    run_all_tests()
    
