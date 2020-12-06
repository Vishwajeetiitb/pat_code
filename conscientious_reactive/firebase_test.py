from firebase import firebase
import time
firebase = firebase.FirebaseApplication('https://patrolling-7f86a-default-rtdb.firebaseio.com/')
data = {
	'name' : 'vishwajeet bhagywant',
	'Email' : 'vishwajeet724728@gmail.com',
	'phone' : 8766543498
}
a = 0
for i in range(20):
	tic = time.time()
	results = firebase.put('/cars','yo',4)
	toc = time.time()
	a +=toc-tic
	# print(a)
print(a/20)