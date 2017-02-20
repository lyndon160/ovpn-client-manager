from CursesMenu import *

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

m = CursesMenu(menu)
selected_action = m.display()

while selected_action['type'] != 'exitmenu':
    if selected_action['type'] == 'display':
	#Create new menu where options are list items.


        list_1 = {'title' : 'test-swine-lyndon.ovpn',
                    'type' : 'key-opts',
                    'command' : 'test-swine-lyndon.ovpn'}


        
        list_2 = {'title' : 'Add new key',
                    'type' : 'new-key',
                    'command' : 'key name'}


	list_menu['options'] = [list_1, list_2]
	lm = CursesMenu(list_menu)
	selected_list_action = lm.display()
	if select_list_action['type'] == 'key-opts':
            #Create new menu with opts to revoke or quit?
	
            revoke_1 = {'title' : 'Revoke test-swine-lyndon.ovpn',
                        'type' : 'revoke',
                        'command' : 'cat test-swine-lyndon.ovpn'}
	
	    revoke_menu['options'] = [revoke_1]
	    rm = CurseMenu(revoke_menu)
	    selected_revoke_action = rm.display()

	#Have end element where you can add new key

	#On entry of menu item option to revoke key or pass

	
    if selected_action['type'] == 'command':
    	os.system(selected_action['command'])
    m = CursesMenu(menu)
    selected_action = m.display()
