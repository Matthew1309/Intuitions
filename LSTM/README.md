# Entry 1: shape
## V2
Going off of the previous explaination, I think I understand it better. Film is
still a great analogy, because it has scenes and frames. We want to teach the 
LSTM to recognize a particular set of scenes, where each scene is composed of 
lets say 10 frames, and predict the next scene that would logically follow.


For example, a little short skit of a basketball player with 3 scenes. One of him
dribbling the ball, one of him juking a defender, and one of him lining up his shot.
The next scene, we may expect to see the ball going through the hoop. Well in each of
these 3 scenes, we have 10 frames each. Flattening that into a roll, we have a single roll
of film with 30 frames in total.


Now we need to tell our machine how many rolls of film we have (in this case 1), how many scenes
to expect (3 time steps), and how many frames per scene (10 categories).


The final shape of this particular dataset of one skit will be (1,30), or as input for the 
LSTM (1,3,10).


## V1
The shape of the LSTM is interesting, and I haven't seen a good explaination
 of why it is a 3-D object. Well, I think I finally understand. Imagine a 
machine shop. Now within this shop there is a mysterious machine with multiple
openings the size of match boxes. Beside it are rolls of 
old timey film. When you spin it up, it almost acts like a 
vending machine taking money, and sucks the film in.


Now we can think of the LSTM shape as this machine analogy. Each row of our 
normal 2D dataset is a film roll. And as we feed this roll in, the machine
needs to know how many times to spin its wheels, so we provide the length
of our roll. And finally, we have the option to feed our machine several rolls
at a time, in case there are multiple occuring variables. 


So finally we have the dimensions we need to shape our input data to:<br>
X(n_total_rolls, length_to_feed_machine, n_rolls_at_a_time) 
