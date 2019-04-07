## Purchase Analytics insight challenge
## @Author: Yuanzheng Zhu
## python version 2.7

import sys

def read_file(file_object):
    """Generator for large csv read """
    features = file_object.readline().rstrip('\n') # skip first line
    while True:
        data = file_object.readline().rstrip('\n')
        if not data:
            break
        yield data


if __name__ == "__main__":

    TEST= 0
    if(TEST):
        # For TESTS
        input_order_path = "../insight_testsuite/tests/test_1/input/order_products.csv"
        input_products_path = "../insight_testsuite/tests/test_1/input/products.csv"
        #Test large filrs
        #input_order_path = "../insight_testsuite/tests/test_1/input/order_products__train.csv"
        #input_products_path = "../insight_testsuite/tests/test_1/input/products_all.csv"
        output_path = "../insight_testsuite/tests/test_1/output/report.csv"
    else:
        input_order_path = sys.argv[1]
        input_products_path = sys.argv[2]
        output_path = sys.argv[3]
    # input_order_path = "./input/order_products.csv"
    # input_products_path = "./input/products.csv"
    # output_path = "./output/report.csv"

    ## first step, read products.csv, create a hashmap for {product-ID: department-ID} pair
    prod_depa_dict = {}
    try:
        with open(input_products_path) as file_handler:
            for line in read_file(file_handler):
                # process line
                line = line.split(",")
                prod_id = int(line[0])
                depa_id = int(line[-1])
                prod_depa_dict[prod_id] = depa_id

            #print prod_depa_dict
    except (IOError, OSError):
        print("Cannot open file")

    # second step, create 2 hashmaps for counting orders and first-time orders
    prod_order = {}
    prod_first_order = {}

    try:
        with open(input_order_path) as file_handler:
            for line in read_file(file_handler):
                # process line
                line = line.split(",")
                prod_id_order = int(line[1])
                ordered_before = int(line[-1])


                depa_id_order = prod_depa_dict[prod_id_order]

                if(depa_id_order not in prod_order):
                    prod_order[depa_id_order] = 1
                else:
                    prod_order[depa_id_order] += 1

                if(ordered_before == 0):
                    if(depa_id_order not in prod_first_order):
                        prod_first_order[depa_id_order] = 1
                    else:
                        prod_first_order[depa_id_order] += 1

            #print prod_order
            #print prod_first_order

    except (IOError, OSError):
        print("Cannot open file")

    # Third step, output file
    output_file = open(output_path, 'w')
    output_file.write('department_id,number_of_orders,number_of_first_orders,percentage\n') #first line
    for key in sorted(prod_order.keys()):
        total_order = prod_order[key]
        if(key not in prod_first_order):
            unique_order = 0
        else:
            unique_order = prod_first_order[key]

        output_file.write("{},{},{},{:.2f}\n".format(key, total_order, unique_order, 1.0*unique_order/total_order))

