# Entry 1: Neural Networks
Motivation: I have been asked to explain neural networks to people that know nothing,
to very little about neural networks, and I feel I have come up short every time. I
would like to fix that, and perhaps create a very good intuitive explaination for
myself at the same time :)


Brainstorm:
* I have tried black box that takes an input and an output, that didn't seem to work
very well because it is abstract.
* I liked the real-life situation I had going on with sophia, I believe using a survey
to predict some category would be a very good intro to this topic.
* Zia like the example of dog weight and cat weight to predict whether the animal we are
measuring is a dog or a cat.


---

# Entry 2: Neural Network Layers
Brainstorm:
* Layers are very tough to explain, but Sophia at least understood that they are transforming
the input data somehow into a usable form. I personally am going off of that video I saw where
space was morphed in linear, and non-linear ways until we ended up with two categories. It helps
that I have developed my own inutition of how linear algebra.
* Each neuron in the layer recieves the same input, and each neuron is its own linear
equation. A layer of neurons is a stack of linear equations, whose answers will be the input for the
next layer, and so on.
* It may be useful to personify each neuron in isolation. (POOPY METAPHOR---->) Maybe use construction workers when a two
way street is made into a one way, and they wait to until enough cars have piled up one one side, and
there are no cars on the other to make a decision. They let you go if there is nobody on the other side.
If there are cars coming from the other side they stop you. If a lot of cars pile up on their side, the
other construction worker will tell the other stream of cars to stop and let your side through?
* Better personification may be a chef on a gameshow, they are all given the same ingredients, and told
to make something. That something is generally different and unique, and that product then goes on to
be taste tested by the judges, who ultimately give it a score. The above honestly sounds like a
better explaination of the full neural net than the layers :(
* An assembly line of cake makers. Raw ingredients --> Shapeless mush --> Cake shape --> Frosting. Each
layer is able to make its own decision, for example if too much shapeless mush was passed to the "Cake
Shape" layer, it could make the decision to make a slightly bigger cake, or potentially split it into
cupcakes. Then the "Frosting Layer" should be able to handle that.



# 6/1/2022
I learned of something called one-shot or few-shot encoding. Some frameworks build in Keras
are Reptile and MAML. The idea behind this neural network type is to mimic the ability of humans
to classify many objects from only a few training examples. It re-frames the training problem from
the classical "here are thousands of examples of an apple, recognize it", into "here are several objects,
learn that there is a difference between them". Apparently this rephrasing of the problem is very
generalizable, and can require far fewer training examples.

From what I understand, the classical MINST dataset traditionally used in neural network performance
problems isn't used for one-shot learning, rather it uses a transpose dataset called Omniglot. What I
mean by transpose is, while the MINST dataset has 10 digits and 1000s of traning examples, Omniglot has
160 characters but only 20 examples each. This dataset and tough learning problem were donated to the
public space by the authors of 10.1126/science.aab3050.

My current intuition of this architecture isn't the best, but I have an idea of what I would like to do
using this framework. I want to construct a network that can tell you which author an input sentence
most resembles, because I suspect such a tool will help me with my current project: improving my writing.
Recently, I have been working on improving my sentence structures by mimicing and studying
author's I admire such as Strunk and White, Jonathan Epstein, and Brenden M. Lake. It would be very nice
to have a tool that takes a sentence as input, and returns an well written sentence that preserves the
meaning of the input, but in the style of a chosen author. While this dream may be impossible considering
my current skill, I can use one-shot learning to create a simplified tool that takes a sentence as input,
and returns a softmax estimate of which author likely wrote it. I could use a tool like this to revise
my sentences until they approximate the style of an author I admire.

My plan is to download a PDF of *Elements of Style* by Strunk and White, extract all the sentences that
aren't quotes, and potentially pad them to be a fixed length. I will then take my previous writing from
school and personal life, and repeat the process. With my two authors ready, I need to build a few-shot
comparitor using Keras; there are videos and guides on how to build the models, but I will probably
have to build my own sampler and autoencoder. Hopefully this won't take to many comparisons, but I think
the number of pairwise comparisons possible between one of Strunk and White's sentences and mine are huge.
If everything goes well my neural net will learn to learn to spot the differences between our two authors.
Some validation sets can be me just coming up with random sentences, and some of Strunk and White's other
works, or later versions of the book.
