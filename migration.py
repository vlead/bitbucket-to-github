import json
import requests
import os
import time
import config
import getpass

bit_user = config.bit_user
bit_psswd = config.bit_psswd
bit_org = config.bit_org

git_user = config.git_user
git_psswd = config.git_psswd
git_org = config.git_org

r = requests.get('https://bitbucket.org/api/1.0/users/%s' %(bit_org), auth = (bit_user, bit_psswd))
labs_spec = json.loads(r.text)
lab_names = []
for labs in labs_spec['repositories']:
	lab_names.append(labs['slug'])


for labs in lab_names:
	if labs=="eee12-plc":
		url = "https://api.github.com/orgs/%s/repos" %(git_org)
		args = {"name":labs}
		r = requests.post(url, auth=(git_user, git_psswd), data=json.dumps(args))
		clone_cmd = "git clone --bare https://%s:%s@bitbucket.org/%s/%s.git" %(bit_user, bit_psswd, bit_org, labs)
		os.system(clone_cmd)
		os.chdir('./%s.git' %(labs))
		os.system('git push --mirror https://%s:%s@github.com/%s/%s.git' %(git_user, git_psswd, git_org, labs)) 
		os.chdir('./..')
		os.system('rm -rf %s.git' %(labs))
