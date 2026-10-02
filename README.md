# Docker Images <img src=".doc/dockers.ico" width="40" align="top"> 

Collection of docker projects. Each project lives in its own GitHub repository and is linked here as a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules), tracking its `main` branch.

## Download

Clone the parent repository first:
```bash
git clone https://github.com/LeonardoMarcello/Dockers.git
cd Dockers
```

### Download all projects
```bash
./download_all.sh
```
(Same as cloning with `git clone --recurse-submodules https://github.com/LeonardoMarcello/Dockers.git`.)

### Download only some projects
```bash
./download.sh                          # list available projects
./download.sh its-docker               # download one project
./download.sh its-docker ati_ft-docker # download several
```
Projects not downloaded stay as empty folders.

## Update

```bash
./update.sh                 # update Dockers and every downloaded project to the latest main
./update.sh its-docker      # update only the given project(s)
```
`update.sh` pulls `Dockers`, then switches each project to its `main` branch and pulls it. A project with uncommitted changes or a diverged branch is skipped and reported at the end.

## Working on a project

Commit and push inside the project, as in any repository:
```bash
cd its-docker
git switch main
# ...edit...
git add -A && git commit -m "..." && git push
```
Then record the new project commit in `Dockers`, so that fresh clones get it:
```bash
cd ..
git add its-docker && git commit -m "Update its-docker" && git push
```

## Adding a new project

Create an empty repository on GitHub, push the project to it, then from `Dockers`:
```bash
git submodule add https://github.com/LeonardoMarcello/<project>.git <project>
git submodule set-branch --branch main <project>
git commit -m "Add <project> submodule" && git push
```
Do not list project folders in the `Dockers` `.gitignore`, otherwise they cannot be added as submodules.

---

## Projects
## [ATI-FT](https://github.com/LeonardoMarcello/ati_ft-docker)
## [ITS](https://github.com/LeonardoMarcello/its-docker)
## ROS1_BRIDGE
## YOLOPIPE
## REALSENSE
## CONTACTILE
## FLEXIVE
## DEXRETARGETING
