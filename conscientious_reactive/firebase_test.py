from firebase import firebase
firebase = firebase.FirebaseApplication('https://patrolling-7f86a-default-rtdb.firebaseio.com/')
data = {
	'name' : 'vishwajeet bhagywant',
	'Email' : 'vishwajeet724728@gmail.com',
	'phone' : 8766543498
}
results = firebase.put('/cars','yo',4)
print(results)