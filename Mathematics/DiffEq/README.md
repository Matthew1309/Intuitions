# 10/9/2023
## ODE with constant $F_{ext}$
Solving a system with a damper and the force of gravity is not that hard, and it took way to much time to figure out. Essentially the system looks like 
$$m\frac{d^2 x}{dt^2} + \gamma \frac{dx}{dt} = mg$$
You can imagine a person jumping out of an airplane and feeling the air resistance until they reach a terminal velocity.

The solution to the homogenous solution is 
$$\begin{bmatrix}x_H(t) = C_1 + C_2e^{-\frac{\gamma}{m}t}\\ \dot{x}_H(t) = -\frac{\gamma}{m}C_2e^{-\frac{\gamma}{m}}\end{bmatrix}$$
And here, plugging in intial conditions break this so that is the first clue that we need the particular solution. The secret is that the $F_{ext} = mg$ is a zeroth order polynomial, and we know how to handle polynomials. Lets try the Ansatz of 
$$\begin{bmatrix} x_p(t) = A\cdot t \\ \dot{x}_p(t) = A \\ \ddot{x}_p(t) = 0\end{bmatrix}$$
And plugging these in give me
$$m\cdot 0 + \gamma \cdot A = mg \therefore A = \frac{mg}{\gamma}$$

And so we get a solution of the form
$$x(t) = C_2e^{-\frac{\gamma}{m}t} + C_3t + C_1$$

We can confirm this result by taking that intital second order ODE, replacing dx\dt with v, now we have a first order ODE that the integrating factor trick works beautifully with, and wam bam, this whole problem is replicated :)


# 5/29/2023
This directory houses Matthew's experiment with humidity and temperature sensing. I initially constructed a model for the data as a first order linear ODE in `Modeling_evaporation.ipynb` and `Visualize_Sensor_Reading.ipynb`. I realized I couldn't understand how I derived the formula great from my documentation in these two files or even find the data (I have moved it to google docs under projects/incubator since). So I revisited the model, re-made it, and put a detailed documentation of it into `Visualize_Sensor_Reading2.ipynb`. The fits are the same, but this new model is much more interpretable and well documented. 