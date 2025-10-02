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

