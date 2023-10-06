"""
menu.py
"""

import sys
import json

def select_obj_scheme(obj_types):
    """
    Shows the menu with all the available Object Schemes and
    returns a dict with the selected object scheme or None, 
    if the selected scheme is not in the list of valid schemes.
    """
    result = None

    control = {'valid': list()}

    print('Available Object Schemes:\n')
    for scheme in obj_types.keys():
        obj_id = str(obj_types[scheme]['id'])

        control['valid'].append(obj_id)
        control[obj_id] = scheme

        print(f'{obj_id}:\t{scheme}')

    print()
    while True:
        selection = input('Select an Object Schema: ')
        if selection not in control['valid']:
            print('\nPlease select a valid Object Schema from the list.\n')
        else:
            print(f'Selected Object Schema: {selection}: {control[selection]}')
            result = obj_types[control[selection]]['object_types']
            break

    return result

def select_obj_types(scheme, selected):
    """
    Shows the menu with all the available Object Types and
    returns a list with the selected ones or None, 
    if the scheme has no object types.
    """
    result = list()

    control = {'valid': ['ALL']}

    if len(scheme) == 0: 
        print('\nNo available object types. Returning to previous menu.\n')
        return None

    print('\nAvailable object types:')
    sorted_scheme = sorted(scheme, key=lambda i: i['name'])
    for i in sorted_scheme:
        obj_name = i['name']
        obj_id = str(i['id'])

        control['valid'].append(obj_id)
        control[obj_id] = obj_name

        print(f'{obj_id}:\t{obj_name}')

    while True:
        selection = input('\nSelect an Object (or type ALL for all of them).\nType c to confirm the selection: ')
        if selection == 'ALL':
            result = list(control.keys())
            result.remove('valid')
            print(f'\nSelected: {str(result)}')

            confirm = input('\nType ALL again to confirm the selection: ')
            if confirm == 'ALL':
                return result

        if selection in result:
            print(f'\n{selection}: {control[selection]} already selected.')
            print('Skipping.\n')
            print(f'\nSelected: {str(result)}')
            continue

        if selection not in control['valid']:
            if selection != 'c':
                print(f'\nItem [{selection}] not found.')
                print('Please select a valid Object Type from the list.')
        else:
            print(f'\nSelected Object Type: {selection}: {control[selection]}')
            result.append(selection)

        print(f'\nSelected: {str(result)}.')

        if selection == 'c':
            confirm = input('\nConfirm selection? [y/n] ')
            if confirm.lower() in ['y', 'yes']:
                return result

    return result

def multiple_selection(obj_types, selection):
    """
    Trigger for the interactive menu. 
    obj_types from get_obj_types(schemas) from get_jira_data.py
    selection should be an empty list in the first call.
    """
    scheme = select_obj_scheme(obj_types)
    selection = select_obj_types(scheme, selection)

    while selection is None:
        selection = multiple_selection(obj_types, selection)

    return selection
