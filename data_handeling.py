'''
This file contains functions that save and load data from files
'''
import pickle
import os
import animation
#Save charPosition, username, score to a file
def save(char_position, username,password, level, score, coin_history,controls,platforms, file_name):
    '''
    Saves the player's data to a file
    '''
    data_list = load(file_name)
    data_list = [] if data_list is None else data_list
    for data in data_list:
        if data['username'] == username:
            data['password'] = password
            data['charPosition'] = char_position
            data['level'] = level
            data['score'] = score
            data['controls'] = controls
            if coin_history is not None:
                data['coin_history'] = [coin[1] for coin in coin_history if coin[0].collected]
            else:
                data['coin_history'] = None
            data['platforms'] = platforms
            break
    else:
        data = {
            'charPosition': char_position,
            'username': username,
            'password': password,
            'level': level,
            'score': score,
            'controls': controls,
            'platforms': platforms
        }
        if coin_history is not None:
            data['coin_history'] = [coin[1] for coin in coin_history if coin[0].collected]
        else:
            data['coin_history'] = None
        data_list.append(data)

    with open(file_name, 'wb') as file:
        pickle.dump(data_list, file)

def load(file_name):
    '''
    Loads data from a file
    '''
    if os.path.getsize(file_name) == 0:
        return None
    with open(file_name, 'rb') as file:
        data_list = pickle.load(file)
    return data_list

def load_coin(coins,collected_coins):
    '''
    deletes the coins that have been collected
    '''
    for coin in coins:
        for collected_coin in collected_coins:
            if coin[1] == collected_coin:
                coin[0].collected = True
                animation.AnimateCoin.delete(coin[0])


def update_high_score(username, score):
    '''
    checks if the player's score is higher than the previous high score and updates it in the 
    leadrboard file if it is
    '''
    data_list = load('leaderboard.dat')
    data_list = [] if data_list is None else data_list
    for data in data_list:
        if data['username'] == username:
            if score > data['score']:
                data['score'] = score
            break
    else:
        data = {
            'username': username,
            'score': score,
        }
        data_list.append(data)
    with open('leaderboard.dat', 'wb') as file:
        pickle.dump(data_list, file)


def update_controls(username,controls):
    '''
    updates the controls of the player in the saves file
    '''
    data_list = load('saves.dat')
    if data_list is None:
        return
    for data in data_list:
        if data['username'] == username:
            data['controls'] = controls
            data_list.append(data)
            break
    with open('saves.dat', 'wb') as file:
        pickle.dump(data_list, file)

def print_binary_file(file_name):
    '''
    prints the contents of a binary file
    '''
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    print(data)
