2026.03.19
- news
  - new figure 2 (for RQ1)
  - RQ4 first draft
  - Table 1  simplifies our definition of signals; we discard the repos that only match a Github topic
- [yogya] v4p, toe, tox, ndbx: do these file extensions correspond to something else than touchdesigner, nodebox, vvvv?
- [nadia] compute the distribution of repos per art tech; then create a pie chart
- [lena] first version of the map!
  - https://observablehq.com/@sparkrew/quick-map-with-index-of-locations
  - we have points all over the world :)
  - next steps: work on the map and on the size of the points
- [benoit]
  - https://github.com/bbaudry/genart-classifier 
  - cluster more sketches
  - add a color for using random or noise
  - add a color for audio functions
- [roxana] look at the cluster and check if it relates to the classification
- [roxana] The json file for the source code and classification of 74 artworks: https://github.com/Selleen/arc-web/blob/main/src/data/artworks.json

2026.03.05
- [nadia, roxana, yogya] write a section about how we cleaned
  - number we had at the very beginning: nb of repos acc to GH topics + repos acc file ext
  - number after deduplication (nadia removed 'exact' duplicates, yogya removed 'pseudo' duplicates)
  - number after removing scd that are not supercollider, removed cpp that are not openframeworks
  - plot distribution of signals
- [yogya, lena] work on RQ2 data + vizualization
      
2026.02.19
- [RQ1]
  - [nadia] check if some user names are only among the dead origins
  - [nadia] order the 'dead' origins by size; plot; decide on a threshold; check all origins larger than threshold to collect the signals; then we'll manually check some of them
  - [nadia] plot for the dead/alive origins: change position of urls to the right side of the bars, add "0" when there are no repos, add a row for hosts that have less than 10 origins (how many hosts? how many origins?)
  - [nadia] data about signals of orgins that are in hosts where all is dead: add this file in the repo
  - [nadia] what are the signals of the large repos in the dead origins
  - [yogya] remove duplicate origins
  - structure of txt for RQ1
    - one par: describe the plot
    - one par: discuss the GH monoculture and still lot of of diversity
    - one par: discuss the dead ones, in particular the totally dead
    - one par: the hosts that have only dead
    - one par: codeberg
    - one par? 'the others'
- [benoit]
  - invite stefano as author
- [roxana]
  - run the same pipeline as Rafaela, with the same 10 js files, just changing the classification framework. Then, compare both outputs (what's the impact of changing the classification framework?)
  - separated the man pages from the rest
- [RQ2]
  - geoapify has a strong limit on nb of requests
  - [yogya] update the get-readme-lang.py to filter out readme files that are less than 42 words and get the language for readme files that have more than 42 words
- [RQ4]
  - [roxana] has checked the 42 top user names
  - we'll write about it
 
   
2026.02.05
- [roxana]
  - remove from BIG file the origins that have man pages and that are labeled 'other'
  - run the same pipeline as Rafaela, with the same 10 js files, just changing the classification framework. Then, compare both outputs (what's the impact of changing the classification framework?)
- [RQ1]
  - [nadia] has the plot (log scale): it's super cool
  - git.code.sf.net, gitorious: what were these origins? what kind of art code (signal) did they have?
  - codeberg already has dead repos: what are they? what are the live repos?
  - git.sr.ht: what are the 8 haitian origins?
  - 5% of Github origins are dead
  - plot the distribution of signals
- [RQ2]
  - [yogya] collect locations for 155K
  - [benoit] working on collecting the language
    - the rust package is useless (sees Latin everywhere...)
- [RQ3]
  - [yogya] has the list of external p5 libs found in the data
  - [yogya] will collect the distribution of number of artworks per origin
  - [rafaela] we have a pipeline that generates an empty json and plots an empty plot
  - [roxana] run Qwen3 on CalculQC with the 74 examples and compare with the ground truth
- [RQ4]
  - [yogya] has the list of the 42 top contributors, will push on Github
  - [benoit, roxana] will analyze it 
 
    
2026.01.22
- [RQ1] 86000 origins cannot be reached
  - have the list on Github
  - plot the distribution of code hosting platforms with live / dead
  - look into the list of origins that are not github.com and gitlab.com and check 'what' they are (univ., research, other)
  - plot the distribution of signals
- [RQ2] 155K origins
  - collect locations
  - collect language
- [RQ3] p5.js files
  - html + p5
  - refining classification
    - process is the code
    - output is the art
    - characterize the generative art practices / processes
    - characteristics that are understandable from the code only and amenable to automatic inference by an LLM
    - [roxana] update labels on manually annotated files for art, then run the calcul-QC pipeline to check its accuracy
    - [rafaela] working on output validation and on making the code paralell 

2026.01.06
- [nadia] 1.6M origins in a single file, with live / dead status
  - super good.
  - extract the list of origins that are dead in a dead_origins.json that we will share with Stefano
  - for RQ1
    - dead / alive
    - where is the code hosted: github, gitlab and others
    - distribution of signals
      - how many did we find with topics / file extensions
      - distribution of origins per file extension
- [yogya] extract 10% of live + github-hosted origins for RQ2
  - [lena] look into the location /bio / readme to think about ways of discussing the diversity of geographical/cultural origin of contributors, example data available in [this sample file](./src/sample-rq2-data.json)
- [yogya] extract 1% of live+github+p5 for RQ3
  - [roxana] refine the classification, esp. computer interaction
  - [lena] art work, art code, rendering, etc.: can we refer to the art literature to define these different concepts?
  - [roxana, rafaela] tests are ongoing
  - [rafaela] discuss with the group to distribute the different issues related to the ML pipeline
  - [rafaela, roxana]: document the different steps of ground-truth construction, testing, refining the classification, etc. in order to document the methodology and discuss the quality of the ML-based process
- [benoit] check the presence of origins that should be the all_origins (e.g., bbaudry/sw-art)
- [yogya] get  the 42 top artists, with all their origins 


2025.12.11
- we meet at Rafaela's :)
- [nadia] which links are live?
  - ongoing
- [lena] revise classification and definitions
- [roxana] dataset of 74 artworks manually labelled
- [yogya and benoit] work on scripts
  - to fetch js files that us p5
  - to fetch metadata about a sample of the origins
- [rafaela] builds the infrastructure for the LLM-based pipeline

2025.11.25
- decision for LLM-based analysis
  - focus on p5 artworks
  - focus on artworks that are inside a single file (either html or js), i.e., the file that includes the ```setup()``` function
- we revise the classification to have process_sound/visual/text and synthesize_sound/visual/text
- [rafaela] 2 hours ago calcul QC came back!
  - the plan is to upload llama70B and more recent models
- [roxana] will share her results with her 2nd PR !
- [nadia] the analysis of dead/live repo urls is pending
- [benoit] extended mining script with
  - info about main contributor: location, bio
  - info about the language of the readme and the bio
- TODO, in order to answer the 'funnel' of research questions
  - RQ1: get info about live / dead
  - RQ2
    - sample the live repos
    - [yogya] consolidates the mining script and runs it on the sample
    - collect data about these repos (prog lang, natural lang, location, duration, etc.)
  - RQ3
    - sample the top users doing repos for art
    - [roxana] re-run the to get the top 50 most prolific users in our dataset
    - analyse these repos
  - RQ4
    - get a set of js/html files
    - [roxana] implement a script that mines all the origins that include p5.js or p5.min.js and filter the files for artwork
      - how many files do we get?
      - how many folders do we discard?
    - analyze them with an LLM

2025.11.13
- [rafaela] calcul QC sabotage ;(
  - https://qwen3lm.com/ might be better than llama
  - https://www.swebench.com/
  - **Code analysis with LLMs**
    - A Survey on Large Language Models for Code Generation - https://dl.acm.org/doi/pdf/10.1145/3747588
    - Do Code LLMs Do Static Analysis? - https://arxiv.org/pdf/2505.12118v1
    - Resource-Efficient & Effective Code Summarization - https://arxiv.org/pdf/2502.03617v1
  - **Creating Tags with LLMs**
    - [cool one] LLM4Tag: Automatic Tagging System for Information Retrieval via Large Language Models - https://arxiv.org/pdf/2502.13481v2
    - ICXML: An In-Context Learning Framework for Zero-Shot Extreme Multi-Label Classification - https://aclanthology.org/2024.findings-naacl.134.pdf
    - TagGPT: Large Language Models are Zero-shot Multimodal Taggers - https://arxiv.org/pdf/2304.03022
  - **Classification without LLM**
    - Towards an Automated Classification of Software Libraries - https://link.springer.com/article/10.1007/s42979-024-02654-2
      - trains a model to classify text
    - Fine-Tuning BERT for Text Classification: A Step-by-Step Guide with Code Examples - https://medium.com/researchify/fine-tuning-bert-for-text-classification-a-step-by-step-guide-with-code-examples-0dea8513bcf2
      - Train BERT to classify text (and the text could be code)
      - https://arxiv.org/abs/1905.05583
- [roxana] llama3-70B
  - good prompts
  - false negatives are ok in our case: we will report on conservatives estimates of the different styles
  - can we take inspiration from this, in order to document our prompts: https://sites.google.com/view/testgeneralizer/prompts/test-generalization?authuser=0
  - good progress on the 'cleaning' of scd files
- [benoit] first draft of a script to fetch data about each origin. For now, nb of commits, main contributor, readme files.
- [nadia] working on getting consistent data for live/dead origins 
- [benoit]
  - push the 'array' version of the json file in the shared folder
  - provide more examples of labeled p5.js pieces
- [roxana]
  - determine the natural language of the readme file
  - test Claude to label a few files
- [all] think about research questions for our study. we can document the RQs in overleaf

2025.11.05
- [nadia] investigate how to do efficient queries to GitHub. How many repos can we query in a reasonable time to get info such as nb of contributors, date of oldest/newest commit, etc. ?
- [roxana] can we use chatgpt to build a labeled set of code files, which we then use for RAG+LLama?
- [roxana] triage scd files
  - PENDING
- [roxana] cpp and h files
  - how many are openframeworks?
 - THE consolidated metadata file is on zenodo: https://zenodo.org/records/17536966
 - [all] how about using an LLM to find out the language in which the readme files are written (EN, SP, FR, etc.)? Do some repos mix several languages (SP+KR) ?

2025.10.23
- [rafaela] runs llama7B with 80Go of GPU
- [rafaela and roxana]
  - continue testing different prompts, different examples
  - both work on different approaches -> great for experimenting
- [nadia] works on the one single consolidated metadata file
- [benoit] write a short definition for each element of the classification
- [roxana] triage scd files
  - PENDING
- [roxana] cpp and h files
  - how many are openframeworks?
- [yogya, nadia, benoit] more examples


2025.10.09
- [rafaela] managed to upload a model on calcul quebec 
  - [all] can we access the data in the shared folder named 'rafaela'?
  - documentation: https://docs.alliancecan.ca/wiki/Rorqual/en
  - Test file is in /home/<youraccountname>/links/projects/def-baudry/rpinter
  - https://duo.com/
- [rafaela, benoit, yogya, nadia]
  - pick five different p5.js sketches
  - create one json file name-of-sketch.json per piece and document the [four different categories](https://github.com/sparkrew/art-in-swh/blob/main/gen-art-classification.md) for the piece
  - add sketch + corresponding json in the shared folder on calcul QC
- [roxana]
  - push the classification of p5-topic-repos here
  - continue looking for declaration of p5 in the 1000+ repos
  - how many of the 2000000 js files are p5.js
    - 600K+ unique origins have p5
- [nadia] has used her computer, but we cannot wait for 291 days to know how many pde files are art
- [nadia] builds THE big, clean json file for all origins
- [roxana] triage scd files
  - PENDING
- [yogya] has moved the data file (2G) from madagh to calcul QC
- [roxana] cpp and h files
  - how many are openframeworks?
- [yogya]
  - write a few sentences about the gitlab subdomains
  - update the table again when we have THE big metadate file, with available / obsolete




2025.10.02
- [nadia]
  - reorganize data and scripts
  - move images and md files from overleaf into this repo
- [roxana] REPOS dataset:
  - how many repos have the topic p5.js?
    - Answer: 7374 repos 
  - how do they declare the dependency to p5 ? (html, package.json, other?)
    - Answer: WIP, crawling ongoing
  - how many of the 2000000 js files are p5.js
    - PENDING
- [nadia] triage pde file
  - example of an 'art' pde file: https://github.com/ronikaufman/poetical_computer_vision/blob/2955696b04444bc6200b6ab9c50c7f51a47f2f6f/days21-31/day27/day27.pde#L4; or this one from cern: https://gitlab.cern.ch/cms_tk_ph2/Ph2_USBInstDriver/-/blob/master/ArdNano/Arduino_Controller/RelayControl/RelayControl.pde
  -  how many of the 10000000 pde files have a setup() method, a draw(), both?
- [roxana] triage scd files
  - example of man page: https://gitlab.alpinelinux.org/Rboccardi661/apk-tools/-/blob/master/doc/apk-update.8.scd?ref_type=heads
  - example of supercollider: https://github.com/supercollider/supercollider/blob/develop/examples/other/quines.scd
- [yogya]
  - move data from your account to a shared folder on madagh
- [nadia]
  - merge the two datasets REPOS and FILES into a single art_repos.json, according to the schma defined in art_repos_schema.json  
- [roxana] cpp and h files
  - how many are openframeworks?
- v4p, toe, tox, ndbx: patches for touchedesigner and other things, most probably 'infrastructure' for the arts. To be investigated further
- [yogya]: update the 'origins' table in the paper
  - look into the gitlab repos: how many subdomains do we have? 
  - remove all origins that have disappeared after filtering out clojure
  - add origins from the 'REPOS' dataset

2025.09.18
- alliance can / calcul québec
  - https://docs.alliancecan.ca/wiki/Tutoriel_Apprentissage_machine/en
  - https://docs.alliancecan.ca/wiki/Huggingface
  - the very big computer that we will use :) https://docs.alliancecan.ca/wiki/Rorqual/en
  - tech support, has different email aliases https://docs.alliancecan.ca/wiki/Technical_support
  - [rafaela] check with calcul quebec how to efficiently get the llm in the machine (make it work)
- server questions:
  - gpus in radar? how much?
- [roxana] REPOS dataset:
  - how many repos have the topic p5.js?
    - Answer: 7374 repos 
  - how do they declare the dependency to p5 ? (html, package.json, other?)
    - Answer: WIP, crawling ongoing
  - how many of the 2000000 js files are p5.js
    - PENDING
- [nadia] triage pde file
  - example of an 'art' pde file: https://github.com/ronikaufman/poetical_computer_vision/blob/2955696b04444bc6200b6ab9c50c7f51a47f2f6f/days21-31/day27/day27.pde#L4; or this one from cern: https://gitlab.cern.ch/cms_tk_ph2/Ph2_USBInstDriver/-/blob/master/ArdNano/Arduino_Controller/RelayControl/RelayControl.pde
  -  how many of the 10000000 pde files have a setup() method, a draw(), both?
- [roxana] triage scd files
  - example of man page: https://gitlab.alpinelinux.org/Rboccardi661/apk-tools/-/blob/master/doc/apk-update.8.scd?ref_type=heads
  - example of supercollider: https://github.com/supercollider/supercollider/blob/develop/examples/other/quines.scd
- [nadia] clj files: we remove them
    - create a new file without the clj files
      - ori_swhid from 2,245,781 -> 1,624,904
      - match_count from 25,138,058 -> 14,739,082

- [roxana] cpp and h files
  - how many are openframeworks?

- [yogya] v4p, toe, tox, ndbx: what is this?
        - toe: touchdesigner
        - v4p: maybe https://www.vide-software.at/cheatsheet_v4p.php#preferences or https://github.com/miellaby/v4p
        - tox: touch designer component
        - ndbx: Nodebox - https://www.nodebox.net/gallery/
- [rafaela] try codellama
- [nadia and yogya] start writing
- [nadia] origin_occurences: what is this?
    -----> occurrences of each origin SWHID in matching_infos
- 


2025.09.04

- list of origins : merge the two lists of origins. How many do we have now
    -> 2,277,365
- REPOS dataset: how many repos have the topic p5.js? how do they declare the dependency to p5 ? (html, package.json, other?)
- [nadia] plot
  - number of unique files / nb of occurences in FILES
  - number of origins in FILES / nb of elemens in match_info
  - plot only the files that occur more than once and the origins that have more than one element in the match_info
- [nadia] what is the distribution of files across different signals?
    - 10653580 pde
    - 10398976 clj
    - 1959222 js
    - 723298 h
    - 609888 cpp
    - 463888 scd
    - 172269 v4p
    - 84096 toe
    - 61005 tox
    - 11836 ndbx   
- what are the projects related to art and hosted on gitlab.alpinelinux.org, gitlab.cern.ch     
- LLM: distinguish between digital art (e.g. running in the browser) and art physicalization (e.g. related to plotters)
- [roxana] 670111 user names:
  - how many are organizations (e.g. schools) and how many are individual users?
  - how many unique locations for the individual users? distribution of names per location
  - how long have these users been active? are they still active (a commit in the last year)?
- [all] what would like to ask the llm?
- we will use codellama
- [rafaela] try codellama
- [nadia and yogya] start writing

2025.08.20
Two datasets
- REPOS
- FILES
Question: [rafaela/] How many origins in FILES are projects in REPOS?
-> check repos-files.pdf

Questions about FILES:
- [yogya] what is the share of different kinds of origins? (github, gitlab, bitbucket, gitea)
- what is the oldest origin in the dataset?
- [rafaela/] how many cats?
- how many pranks?
- [nadia] how many unique files? plot # versions per file / number of occurrences(y) per unique id (x) / number of elements in matches (y) in origin (x)
    {
      "total": 25,138,058,
      "unique": 2,337,451
    }
- [nadia] what is the distribution of files across different signals? 
- [yogya/] how many origins mention fxhash? artblocks?
- how many algo art course repos are in the dataset?
- [roxana] how many different github usernames ? what's the distribution of origins per username? who's the most prolific contributor to the arts in SWH?
- {Total unique GitHub usernames: 670111
 Top contributor: junkiyoshi with 2339 repos
top 10:
junkiyoshi: 2339
  League-Level0-Student: 2305
  drawwithcode: 1593
  PlumpMath: 1468
  clojure-land: 1078
  isabella232: 656
  imclab: 565
  lsudigitalart: 494
  League-level2-student: 448
  n1ckfg: 394
- }
-  

Benoit: reach out to Stefano for more info about SWH
Given an origin, how can we query SWH to:
- get the date of the oldest version of the file(s)?
- get all the versions of the file?
- get all the files inside this project?

https://openprocessing.org/
https://codepen.io
https://gateway.fxhash2.xyz/ipfs/Qma5aRBLCwd18hGP6ZzokbNbNtFWh9q4HM2rxWjBWWA64U/sketch.js

2025.07.31

We can search file content by replacing the commit IDs
Maybe we should also check the repos, becuase we only have the lists of p5.js (libraries but not the actual files that use )

2025.07.30
Now we have 2 datasets:
- DS1: set of github repos retrieved from SWH, because they are tagged by one of the topics that we curated as they relate to the arts
- DS2: set of SWH records that point to files in SWH which match some patterns or file extensions that we curated as they relat to digital arts tech
Before setting up a super AI-powered pipeline, let's gather some basic data from these datasets:
- how many file descriptions do we have in DS2? - number of files?
- how many point to different versions of the same file?
- based on file names: how many different file extensions do we have? 
- to how many different projects do these file belong?
- for the projects that are hosted github repos, how much overlap do these github repos have with the repos in DS2.
- how many of the files of DS2 and the repos of DS1 are no more accessible on their original platform (e.g., how many repos of DS1 are not accessible on github but still on SWH)?


2025.07.25
Rafaela and Yogya's unnofficial meeting :)
- What we need:
    - For us to have acces to Calcul Quebec, Benoit needs his account to be active to sponsor ours
- Questions:
    - Can we download the files once to Calcul Quebec and have multiple accounts with read access?
    - Will we have access to the GPUs?
- To do:
    - Take Stephano's list of SWHID and try to retrieve the content of the files
        - https://archive.softwareheritage.org/
        - https://gitlab.com/zacchiro/swh-repo-mining
            - Some example file content links:
              https://archive.softwareheritage.org/browse/content/sha1_git:1e732367eebedeb1ffd5c631efd94161a11e6fed/
              https://archive.softwareheritage.org/browse/content/sha1_git:6dfdee8f8e6d565fe5378db015dc5a047d72a50f/
              https://archive.softwareheritage.org/browse/content/sha1_git:537b108c4f2a88c99bb1d39191794851b144c4a6/
              https://archive.softwareheritage.org/browse/content/sha1_git:590d2c84643eacea37d429fdb83979ee902b7238/
              https://archive.softwareheritage.org/browse/content/sha1_git:5c879d08881a6fd399a277d85e7cdc3706368cae/
              
    - Upload some samples to our github
            - To download a sample of the big ndjson file, run the following command and exit early.
            "curl -L -H "Authorization: Bearer cO8WErh9Nc7bA6cpQSSJhCfMEdvETwW2nkFEKHAhwFEGrB5XgZhlEmxNKdAG" https://zenodo.org/api/files/9e8708db-27d8-4061-98f8-e00814073e32/matching_repos.ndjson --output matching_repos.ndjson"
    - Get access to Calcul Quebec
    - Choose open source model for inference
    - Use model to create label (e.g., #art, #notart) for the sample files
            - Simpler the labels, easier to implement the model
    - Draft architecture of the system: arch.png

2025.07.14
- dataset of github repos
  - update the ranking function to favor repos that have more than one topic of our list and that have more than 50 commits
  - write about this (methodology to collect and filter the repos, ranking procedure)
  - can an LLM analyze the readme to determine what the repos do (visuals, sound, interaction, etc)
- dataset of code that match certain file extensions
  - collect statistics about the number of files with each extension, number of unique repos, number of contributors
  - are some code repos in common with the previous list collected with topics?
- consolidate lists of artists with exhibitions, nft platforms and specialized platfprù (e.g. rhizome)  


2025.06.12
- Consolidate list of artists (On github)
    -   Middle East (Saudi Arabia, Emirates, Turkey)
    -   Asia (Singapore, China, South Korea, Japan, India)
    -   Europe
    -   Latin America
- Github Repos:
    - Eliminate duplicates (store info in a json)
    - Gather list of unique tags in the txt (json)
    - Links that are alive/dead
    - Live span (first/last commit)
    - Complete list of topics for each repo (for clustering or ranking)

    
Info to gather:
    - Programming languages
    - Contibutors
    

2025.06.05

- research
    - artists names 
        - social media
        - github
            - repo also if possible
        - museum website
        - events (live coding/meetups)
        - art institutions
- https://www.rightclicksave.com/article/the-real-value-of-nfts


2025.05.21

- Set up accounts on Azure 
- Check proceedings in Software Engineering in society track at ICSE 
- Related work section of the Art paper. Possible topics for papers:
  - creative coding,
  - generative art code,
  - live coding (there is an International conference)
  - qualitative studies based on Interviews with generative artists
- Journey into open source creative coding libraries (p5, openframeworks, nannou, puredata, processing, hydra, sonicpi): #commits, #contributors, date of first commit, #lines of code, #versions, #downloads / install, community (values, goals, esthetics, )refik
- nadia: journey into p5 / processing , openframeworks, nannou)
- yogya: puredata, sonic pi, hydra, nyst
- madjda: reddit in turkish creative coding + arabic
- clara: collect artists names from French / EU art places

