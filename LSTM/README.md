# Entry 1: shape
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
