To manually monitor the server, ```htop``` is an incredible
tool to show CPU usage, memory usage, broken down by user.

However sometimes I want to monitor the memory for hours, and
it was so awkwardly hard to find something that just logs it!

I came up with this little ratchet construction:
> ```free -g -s 10 | stdbuf -o0 awk '{ print $3 }' > <filename>.txt```

```free``` is a bash command to output the memory at a moment, the g flag
makes it so that it outputs in GB, the s flag tells us to update every 10
seconds. This is being piped into an awk command to grab the third column
which tells us the swap and core memory usages. This is then being piped
into a file of our chosing. Now unfortunately there is something wonky with
its STDOUT, so you need that ```stdbuf -o0``` command before the awk.

Anywho, a simple python script can then parse this.
