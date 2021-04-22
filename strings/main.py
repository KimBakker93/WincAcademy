# Do not modify these lines
__winc_id__ = '71dd124b4a6e4d268f5973db521394ee'
__human_name__ = 'strings'

# Add your code after this line
scorer_1 = 'Ruud Gullit'
scorer_2 = 'Marco van Basten'
goal_1 = 32
goal_2 = 54
scorers = scorer_1+str(goal_1) + ", " + scorer_2+str(goal_2)
report = f'{scorer_1} scored in the {goal_1}nd minute\n{scorer_2} scored in the {goal_2}th minute.'

player = 'Jan Wouters'
first_name = player[:player.find(' ')]
last_name_len = len(player[player.find(' '):])
name_short = player[0] + '. ' + player[player.find(' ')+1:]
chant = (first_name + '! ') * (len(first_name))
chant.rstrip(' ')
print (chant)
good_chant = chant[-1] != chant
print (good_chant)