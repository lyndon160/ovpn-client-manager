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
            'command' : ''}


menu['options'] = [option_1]

#Get config
with open('config.conf') as json_data:
    data = json.load(json_data)
    ovpn_data = data['ovpn-data']

command = '/usr/bin/docker run -v ' + ovpn_data + ':/etc/openvpn --rm -it kylemanna/openvpn ovpn_listclients'
revoke_command = 'docker run -v '+ovpn_data+':/etc/openvpn --rm -it kylemanna/openvpn easyrsa revoke '
create_command_1 = '/usr/bin/docker run -v' + ovpn_data + ':/etc/openvpn --rm -it kylemanna/openvpn easyrsa build-client-full ' 
create_command_2 = '/usr/bin/docker run -v' + ovpn_data + ':/etc/openvpn --rm kylemanna/openvpn ovpn_getclient '
revoke_command_2= '/usr/bin/docker run --rm -it -v '+ovpn_data+':/etc/openvpn kylemanna/openvpn easyrsa gen-crl'

m = CursesMenu(menu)
selected_action = m.display()

while selected_action['type'] != 'exitmenu':
    if selected_action['type'] == 'display':
	#Create new menu where options are list items.
	#Get VPN client list

        output = subprocess.check_output(command, shell=True)
        lines = str(output).split('\n')
        list_items = []
	for line in lines:
            tmp = line.split(',')
            if 'name' not in tmp[0] and '' != tmp[0]:
                list_items.append({'title':tmp[0],'type':'key-opts','command':tmp[0]})

	#        raw_input("Press Enter to continue...") 
 
        list_items.append({'title' : 'Add new key',
                    'type' : 'new-key',
                    'command' : 'key name'})

	list_menu['options'] = list_items
	lm = CursesMenu(list_menu)

        #os.system('clear')
	selected_list_action = lm.display()
	if selected_list_action['type'] == 'key-opts':
            #Create new menu with opts to revoke or quit?
	
            revoke_1 = {'title' : 'Revoke '+selected_list_action['title'],
                        'type' : 'revoke',
                        'command' : selected_list_action['title']}

	
            revoke_2 = {'title' : 'Dump '+selected_list_action['title'],
                        'type' : 'print',
                        'command' : 'cat test-swine-lyndon.ovpn'}
	
	    revoke_menu['options'] = [revoke_1, revoke_2]
            os.system('clear')
	    rm = CursesMenu(revoke_menu)
	    selected_revoke_action = rm.display()

	    if selected_revoke_action['type'] == 'print':
                os.system(create_command_2+selected_list_action['title']+' > keys/' +selected_list_action['title']+'.ovpn' )
		raw_input('Key has been sent to keys/' +selected_list_action['title']+'.ovpn')
	    if selected_revoke_action['type'] == 'revoke':
                check = raw_input('Are you sure you want to remove ' +selected_list_action['title']+'? $: ')
		if check == 'y' or check == 'Y' or check == 'Yes' or check == 'yes':
                    os.system(revoke_command+selected_list_action['title'])
                    raw_input(selected_list_action['title']+' has been removed continue to update CRL')
                    os.system(revoke_command_2)
                    raw_input('Key removed and CRL updated. To apply changes the OVPN server may have to be restarted')
                else:
                    raw_input('Key not removed')
 
        if selected_list_action['type'] == 'new-key':
             new_key_name = raw_input("Enter key name $: ") 
             os.system(create_command_1+new_key_name+' nopass')		
             raw_input('Press to continue')

	#On entry of menu item option to revoke key or pass

	
    if selected_action['type'] == 'command':
    	os.system(selected_action['command'])
    m = CursesMenu(menu)
    selected_action = m.display()
