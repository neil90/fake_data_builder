from faker import Faker
import random
import time
import sys
import csv

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def timer(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)

def people():

	fake = Faker()
	
	data = []

	for i in range(15):
		name = fake.name()
		age = fake.random_int(min=18, max=99)
		address = fake.address().replace('\n',' ')
		salary = fake.random_int(min=50000, max=250000)
		
		data.append((name, age, address, salary))

	return data

def random_data_points():

	amount_list = [random.randint(1,50) for i in range(30)]
	qty_list = [i for i in range(15)]
	purchase_date_list = [datetime.date(random.randint(2005,2015), 
									  random.randint(1,12), 
									  random.randint(1,28)).strftime('%Y-%m-%d')
					 for i in range(10000)]
	product_list = [
			'water', 'beer', 'chips', 'chocolate', 
			'pretzels', 'wine', 'fish', 'steak'
		]

	return amount_list, qty_list, purchase_date_list, product_list


def main():

	outfile = 'fake_data.csv'
	outsize = 1024 * 1024 * 1024 #1gb file

	#Janky way to print at percentage points
	percentage_print = ['{:.3%}'.format(i/100) for i in range(0,105,5)]

	#Get fake data Lists
	profile_people = people()
	amt_list, qty_list, purchase_date_list, product_list = random_data_points()

	start = time.time()
	size = 0

	print('Creating fake data file {0}...\n'.format(outfile))

	with open(outfile, 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)

		while csvfile.tell() < outsize:
			
			profile = random.choice(profile_people)
			

			product = random.choice(product_list)
			amount = random.choice(amt_list)
			qty = random.choice(qty_list)
			purchase_date = random.choice(purchase_date_list)
			
			row = [
				profile[0], profile[1],
				profile[2], profile[3], 
				product, amount, 
				qty, purchase_date
			]
			
			csvwriter.writerow(row)

			end = time.time()

			block_amount = csvfile.tell()
			block_amount_mb = '{:.2f}'.format(block_amount/(1024*1024))
			percent_done_frmt = '{:.3%}'.format(block_amount / outsize)
			outsize_mb = '{:.0f}'.format(outsize/(1024*1024))

			if percent_done_frmt in percentage_print:
				sys.stdout.write('\r' 
								+ percent_done_frmt 
								+ ' ' 
								+ block_amount_mb 
								+ '/' 
								+ outsize_mb 
								+ ' mb, ' 
								+ timer(start, end))

				sys.stdout.flush()

if __name__ == "__main__":

	main()



