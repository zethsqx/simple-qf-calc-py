class Validation(Object){
	def PB_C(self):
	
		# valid number input
		try:
			# for integer input			
			number =  int(self.input())
			
			# for double or float number input
			#number = float(self.input())
			#number = double(self.input())
			
			# check the number is not zero or negative
			if number <= 0:			
				print("Please enter a valid number!")
				number = False # if 
			
			# if passed validation, return True
			number = True
			
		except ValueError:
			print ("Please enter a valid number!")
			number = False
	
	
	
		# valid string input
		word = str(self.input())
		
		if not word.isalpha():
			word = False
		else:
			word = True
			
	
	# check for input file but not sure whether it can work or not 
	def validFile(x):
		try:
			x = open("xxx.csv")
			read = x.readline()
			value = int(read.strip())
		except IOError as eer:
			print("Wrong File Format!")
		except ValueError:
			print("Could not convert data to an integer.")
		finally:
			x.close()
	
	# check or zeroDivisionError
	def vaildCalculation(x):
		try:
			y = 1/x
			# y = x/1
		except ZeroDivisionError as err:
			print('Handling run-time calculation error:',err)
	
}