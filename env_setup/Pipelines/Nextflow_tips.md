Here is everything Matthew understands about Nextflow.

# Summary
### How to install
Use conda! Do not go through the trouble of getting Java yourself, it sucks

### Using Nextflow
The Nextflow tutorial is pretty extensive: https://www.nextflow.io/docs/latest/getstarted.html. 
If you wanna make a good sharable pipeline for publication, consider using the nf-core guidelines
https://nf-co.re/tools/#creating-a-new-pipeline. 


Here is a little cheat sheet for getting started making your own Nextflow script: https://github.com/danrlu/Nextflow_cheatsheet.


**Channels are nearly impossible to edit!** If you end up needing to edit them, something may be 
wrong with your pipeline definition. There has to be a better way! 


If you are dealing with filenames, directories, paths, etc, you can often access them using a 
Nextflow/Groovy built in: ${file.baseName}. It is awkardly convienient, but not advertised.


Matthew's **Doing Stuff** section details his adventure to make his own fun pipeline.
There are a lot of small unintuitive barriers to entry that make Nextflow (and snakemake)
tough.   

### Cloud and HPC usage
Amazon is supposed to work well with Nextflow, but I think that is only the case if you are 
an owner of an amazon account, or given nearly super permissions, otherwise it is a nightmare.


On our server, Matthew doesn't have super privilages, and thus Docker is a slight issue. Pipelines
that use containers like to break whenever a Docker conatiner is called. Singularity was supposed
to get around these permission issues, but ended up bringing its own suite of problems involving
pulling from remote repositories.
