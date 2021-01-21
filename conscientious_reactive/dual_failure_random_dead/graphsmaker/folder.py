import os
import os
rootdir ='../data/'
i = 1
for subdir, dirs, files in os.walk(rootdir):
	if 'run' in subdir:
		for _, _, files in os.walk(subdir):
			for file in files:
				if file.endswith(".xlsx"):
					path = subdir+'/'+file
					
