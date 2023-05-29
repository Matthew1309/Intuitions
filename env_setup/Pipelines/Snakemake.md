

Documentation can be found here: https://snakemake.readthedocs.io/en/stable/.

Here might be a good blog post on how to start moving a workflow/pipeline over to Snakemake: https://pages.charlesreid1.com/how-do-i-snakemake/converting/.

This reddit thread went over Snakemake and Nextflow floozies: https://www.reddit.com/r/bioinformatics/comments/4jyjwk/your_favorite_workflow_manager/


# Tutorials:

<details>
    <summary>Click me</summary>

## Basic: 
* https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#snakefiles-external-scripts
* https://snakemake.readthedocs.io/en/stable/tutorial/advanced.html
## Configuration: 
* https://snakemake.readthedocs.io/en/latest/snakefiles/configuration.html
## NBIS course: 
* https://nbis-reproducible-research.readthedocs.io/en/course_1911/snakemake/
(Incomplete) going from workflow to snakemake tutorial:
* https://pages.charlesreid1.com/how-do-i-snakemake/converting/
Nice bioinformatics toolkit by Colorado professor Eric (In the works):
* https://eriqande.github.io/eca-bioinf-handbook/managing-workflows-with-snakemake.html#using-snakemake-on-a-computing-cluster
Lachlan deer snakemake tutorial with heavy R and econ: 
* https://lachlandeer.github.io/snakemake-econ-r-tutorial/


## Cloud:
* https://snakemake.readthedocs.io/en/stable/executor_tutorial/tutorial.html

* This seems like a handy blog tutorial: https://www.bsiranosian.com/bioinformatics/large-scale-bioinformatics-in-the-cloud-with-gcp-kubernetes-and-snakemake/

## Running jobs in containers/HPCs
* https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html
* Snakemake with slurm: https://bihealth.github.io/bih-cluster/slurm/snakemake/
* Cluster execution documentation: https://snakemake.readthedocs.io/en/stable/executing/cluster.html 
    * a blogpost that helps https://hackmd.io/@bluegenes/BJPrrj7WB 
    * another blog post with more examples https://github.com/SchlossLab/snakemake_cluster_tutorial
    * HPC tutorial, scaling a workflow to an HPC: https://carpentries-incubator.github.io/workflows-snakemake/09-cluster/index.html
    * Snakemake with slurm: https://bluegenes.github.io/hpc-snakemake-tips/
    * Incredible overall tutorial for bioinformatics: https://eriqande.github.io/eca-bioinf-handbook/managing-workflows-with-snakemake.html#using-snakemake-on-a-computing-cluster
    * Yet another blog of how to run snakemake pipeline on HPC: https://www.sichong.site/2019/10/17/how-to-run-snakemake-pipeline-on-hpc/




######################################################################
######################################################################
How does Snakemake submit jobs to a job scheduler. 
* https://www.youtube.com/watch?v=NNPBDOBHlxo
* https://www.youtube.com/watch?v=h2CJ-qr8fjs
* https://www.youtube.com/watch?v=AZSJKNvkRcg
* http://ivory.idyll.org/blog/2018-repeatability-in-practice.html



######################################################################
######################################################################

</details>
    
# Additional features tutorial
https://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html

<details>
    <summary>Click me</summary>

## Benchmarking: 
Can benchmark, just need to give it a path to a file. All wildcards need to be the same as the output file. The benchmarking process can be repeated several times to give user a feel for how variable the time may take. Repeat up to 3 times. 


## Modularization:
So we can split a workflow into smaller modules with the "include" statement. OR Snakemake can define sub-workflows which refers to a directory with a complete snakemake workflow. https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#snakefiles-sub-workflows<br><br>The include statement worked first try and was pretty nice tbh.<br><br>Automatic deployment of software dependencies:
We can specify a conda environment for each separate rule! Just include a conda directive with a path toward a conda yaml file. Then when making the call, just use `snakemake --use-conda --cores 1`<br><br>This has a benefit that the workflow can be executed on a vanilla system.
<br><br>Jesus this is taking forever.

## Tool wrappers:
Wrappers are short scripts that make use of a commandline application and makes it directly addressable from Snakemake? We got the wrapper directive. I genuinely don't get the point of this????

## Cluster execution:
Clustered file system(https://en.wikipedia.org/wiki/Clustered_file_system): Can provide features like location-independent addressing.<br><br>Distributed file systes(): Do not have lock level access, instead using network protocol. Also known as network file systems.
<br><br>The documentation says it can execute jobs in distributed environments. https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html#snakefiles-cluster-configuration


## Constraining wildcards:
To not let these wildcards get every value under the sun, we can constrain them using a regular expression. This can be made per rule or globally! https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#snakefiles-wildcards

</details>

# Advanced Tutorials
https://snakemake.readthedocs.io/en/stable/tutorial/advanced.html

<details>
    <summary>Click me</summary>
    
## Step 1: Specifying the number of used threads
A thread means a core, and if you specify a rule to use more threads than cores available, they will be automatically lessened to an appropriate number.

The resources directive can specify memory, GPUs, etc.

Leaving # of coures out of --cores will use all available cores.

## Step 2: Config files
These are needed to make an adaptable and customizable method. 
https://snakemake.readthedocs.io/en/latest/snakefiles/configuration.html

Config can be yaml or json, and they can be called from the snake file as a dictionary that belongs to the "config" object. Access to which is dictated by config['samples'] where samples is the name you gave your inputs.

## Step 3: Input functions
Snakemake workflows are executed in 3 phases
§ Initialization phase, the files are parsed and rules made
§ In the DAG phase the tree is built and inputs are mapped to outputs and all the wildcards/matching of input and output is performed.
§ In the Scheduling phase the jobs are executed in the order of available resources.
Function expansion is performed in the initialization phase, therefore we cannot specify FASTQ paths for bwa_map from bcftools_call because the propogation of wildcards hasn't happened yet.

We cheat and use an input function. These HAVE TO RETURN a string or a list of strings that can be seen as paths to input files. Input functions are performed after wildcard values have been determined.

## Step 4: Rule parameters
More adaptability, if something  outputs more than a static flag, and that needs a new course of action, we can do that through the params directive!  

I am having an incomprehensible time trying to get this exercise done, posted a question about it on stackoverflow -_- jesus christ this is frustrating. The issue I was having was explained here: https://stackoverflow.com/questions/68776818/why-are-my-wildcard-attributes-not-being-filled-in-snakemake. And additional resources by the guy to help understand the logic: [https://stackoverflow.com/questions/50198628/snakemake-confusion-on-how-to-access-config-files-properly/50216057#50216057, https://bitbucket.org/blaiseli/snakemake/src/f11247997a378c48fe0f1dc4f921f0cb64e19a37/docs/snakefiles/understanding.rst?at=doc_contrib&fileviewer=file-view-default]

## Step 5: Logging
Wow can specify at each rule, where the log file will go! Can also decide to pump the stderr into the log file.

Nothing seems to be put into the log files -_- I think log refers to the errors that may pop up in the scripts, not the log of snakemake activity.

I noticed that if you mess up a bit of shell script (bad pipe) that the dryrun won't catch it!

## Step 6: Temporary/protected files
We can save disk-space by marking certain files as temporary using a simple temp() function around the output file name.

This even deletes the directory they were in! and boots you out if your working directory on the shell was in there.
    
</details>