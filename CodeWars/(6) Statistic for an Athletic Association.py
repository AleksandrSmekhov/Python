#Kata - https://www.codewars.com/kata/55b3425df71c1201a800009c

def stat(strg):
    if len(strg) == 0:
        return ''

    strs = [int(x) for y in strg.replace(' ', '').split(',') for x in y.split('|')]
    
    time = sorted([strs[3 * i] * 3600 + strs[3 * i + 1] * 60 + strs[3 * i + 2] for i in range(len(strs) // 3)])
    stats = [time[-1] - time[0], 
             sum(time) // len(time), 
             time[len(time) // 2] if len(time) % 2 == 1 else (time[len(time) // 2] + time[len(time) // 2 - 1]) // 2]
    
    hms = [[stat // 3600, stat % 3600 // 60, stat % 60] for stat in stats]
    results = ["{:02d}|{:02d}|{:02d}".format(x[0], x[1], x[2]) for x in hms]
    
    return f'Range: {results[0]} Average: {results[1]} Median: {results[2]}'