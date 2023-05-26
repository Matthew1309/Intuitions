# How to Change/Set up bash custom prompt (PS1) in Linux: 
<details open>
    <summary>Click me</summary>
    
* Just tells me that I can mess around with the PS1 command, and gives me a list of all the expantions: https://www.cyberciti.biz/tips/howto-linux-unix-bash-shell-setup-prompt.html

* This tells me how to change the color: https://www.cyberciti.biz/faq/bash-shell-change-the-color-of-my-shell-prompt-under-linux-or-unix/

* How to chuck the gitbranch over my prompt: https://superuser.com/questions/1469215/how-to-show-git-status-and-conda-environment-in-command-prompt

* The issue is if you have logic or other stuff you don't want to show up in the prompt not in \[\] it will cause strange wrapping issues. So use this: https://unix.stackexchange.com/questions/105958/terminal-prompt-not-wrapping-correctly. Also if you put a \n into \[\] then it will cause problems.

My current bashrc on the server: 
```
git_branch() {                                                                     
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1) /'            
}                                                                                  

PS1='\[\e[0;31m\]$(git_branch)\[\e[m\]\n${debian_chroot:+($debian_chroot)}\[\033[01
;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '                          

# Add conda environment to prompt                                                  
if [ ! -z "$CONDA_DEFAULT_ENV" ]                                                   
then                                                                               
    PS1="\n($CONDA_DEFAULT_ENV) "$PS1    
fi
```
</details>