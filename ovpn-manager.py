from CursesMenu import *
import subprocess
import json

menu = {'title' : 'OVPN client management menu',
        'type' : 'menu',
        'subtitle' : 'Options'}

list_menu = {'title' : 'OVPN client management menu',
        'type' : 'menu',
        'subtitle' : 'OVPN keys in use'}

revoke_menu = {'title' : 'OVPN client management menu',
        'type' : 'menu',
        'subtitle' : 'Choose whether to revoke key'}

option_1 = {'title' : 'List keys',
            'type' : 'display',
            'command' : 'echo Hello World!'}


option_2 = {'title' : 'Revoke key',
            'type' : 'command',
            'command' : 'echo Hello World!'}

option_3 = {'title' : 'Add key',
            'type' : 'command',
            'command' : 'echo Hello World!'}

menu['options'] = [option_1,option_2,option_3]

#Get config
with open('config.conf') as json_data:
    data = json.load(json_data)
    ovpn_data = data['ovpn-data']

m = CursesMenu(menu)
selected_action = m.display()

while selected_action['type'] != 'exitmenu':
    if selected_action['type'] == 'display':
	#Create new menu where options are list items.
	#Get VPN client list
	command = '/usr/bin/docker run -v ' + ovpn_data + ':/etc/openvpn --rm -it kylemanna/openvpn ovpn_listclients'

        output = subprocess.check_output(command, shell=True)
        lines = str(output).split('\n')
        list_items = []
	for line in lines:
            tmp = line.split(',')
            print tmp[0] 
            if tmp[0] != 'name':
                list_items.append({'title':tmp[0],'type':'key-opts','command':tmp[0]})

        raw_input("Press Enter to continue...") 


        list_1 = {'title' : 'test-swine-lyndon.ovpn',
                    'type' : 'key-opts',
                    'command' : 'test-swine-lyndon.ovpn'}
        
        list_items.append({'title' : 'Add new key',
                    'type' : 'new-key',
                    'command' : 'key name'})

	list_menu['options'] = list_items
	lm = CursesMenu(list_menu)

        #os.system('clear')
	selected_list_action = lm.display()
	if selected_list_action['type'] == 'key-opts':
            #Create new menu with opts to revoke or quit?
	
            revoke_1 = {'title' : 'Revoke test-swine-lyndon.ovpn',
                        'type' : 'revoke',
                        'command' : 'cat test-swine-lyndon.ovpn'}
	
	    revoke_menu['options'] = [revoke_1]
            os.system('clear')
	    rm = CursesMenu(revoke_menu)
	    selected_revoke_action = rm.display()

	    if selected_list_action['type'] == 'revoke':
	        print "Key removed"

	    if selected_list_action['type'] == 'add':
		print "Enter x"

	#On entry of menu item option to revoke key or pass

	
    if selected_action['type'] == 'command':
    	os.system(selected_action['command'])
    m = CursesMenu(menu)
    selected_action = m.display()
