from faker import Faker
import datetime
import random
import time
import sys
import csv

start = time.time()

def progress_display(blk_size, exp_size):

	end = time.time()
	block_amount_mb = '{:.2f}'.format(blk_size/(1024*1024))
	percent_done_frmt = '{:.2%}'.format(blk_size / exp_size)
	outsize_mb = '{:.2f}'.format(exp_size/(1024*1024))

	sys.stdout.write('\r'
					+ percent_done_frmt
					+ ' '
					+ block_amount_mb
					+ '/'
					+ outsize_mb
					+ ' mb, '
					+ timer(start, end))

	sys.stdout.flush()

def percent_points(exp_size):
 
	base_chunk = exp_size / 20
	percentage_points = {}

	for i in range(1, 21):
		percentage_points[i] = base_chunk * i

	return percentage_points

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

	percent_dict = percent_points(outsize)

	#Get fake data Lists
	profile_people = people()
	amt_list, qty_list, purchase_date_list, product_list = random_data_points()

	#size = 0

	print('Creating fake data file {0}...\n'.format(outfile))

	with open(outfile, 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		i = 0
		while csvfile.tell() <= outsize:
			
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
			block_amount = csvfile.tell()
			try:
				if block_amount >= percent_dict[i + 1]:
					progress_display(block_amount, outsize)

					i = i + 1
			except:
				pass


	progress_display(outsize, outsize)

if __name__ == "__main__":

	outfile = 'fake_data.csv'
	outsize = 1024 * 1024 * 1024 #1gb file

	main()
