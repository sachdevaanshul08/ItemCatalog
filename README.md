# About The Project

This application display a list of items within a variety of categories, as well as provide a user registration and authentication system.

-   This is a web application developed on `Python` using the `Flask` framework which performs the CRUD operations on through the UI developed in HTML and delivered via flask.
-   For data persistence `SQLite` has been used which is hosted on a virtual machine (Don't worry prerequisites are explained below) 
-   User can login using `Auth2.0` using Google API and can create/edit/delete the items that they have created themselves.
-   It follows the PEP8 style guide

NOTE :- 
Python Required Version - `2.7`
Please enable javascript in your browser.


## prerequisite(s)
To execute this project you need to setup few things which are explained below in details.

### The virtual machine
This project makes use of the same Linux-based virtual machine (VM).


### Installing the Virtual Machine
You'll use a virtual machine (VM) to run this project. The VM is a Linux server system that runs on top of your own computer. You can share files easily between your computer and the VM; and you'll be running a web service inside the VM which you'll be able to access from your regular browser.

We're using tools called [Vagrant][vagrant] and [VirtualBox][virtualbox] to install and manage the VM. You'll need to install these to execute this project. The instructions on this page will help you do this.

### Conceptual overview
[This video][conceptualoverview] offers a conceptual overview of virtual machines and Vagrant. You don't need to watch it to proceed, but you may find it informative.


### Install VirtualBox
VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here][vbdownload]. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

Ubuntu users: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

### Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com. Install the version for your operating system.

Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

If Vagrant is successfully installed, you will be able to run `vagrant --version`   in your terminal to see the version number.
If Vagrant is successfully installed, you will be able to run vagrant --version in your terminal to see the version number.


### Download the VM configuration
There are a couple of different ways you can download the VM configuration.

You can download and unzip this [file: FSND-Virtual-Machine.zip][fsnd] This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder.

Alternately, you can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. `Change directory to the vagrant directory:`
Navigating to the FSND-Virtual-Machine directory and listing the files in it.


### Start the virtual machine
From your terminal, inside the vagrant subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.
Starting the Ubuntu Linux installation with `vagrant up`.

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

Logging into the Linux VM with `vagrant ssh`.
Logged in!

If you are now looking at a shell prompt that starts with the word vagrant , congratulations — you've gotten logged into your Linux VM.

### Sharing files between the vagrant virtual machine and your home machine.
Be sure to change to the `/vagrant` directory by typing `cd /vagrant` before creating new files or pasting files that you want to be shared between your host machine and the VM.


### To execute the project in your virtual machine

1. Bring the virtual machine back online (with `vagrant up`), do so now. Then log into it with `vagrant ssh`.
2. Download this repository in your `vagrant` directory.
3. Enter into sharing mode (b/w virtul m/c and host m/c) by typing cd /vagrant.
4. Execute the `python models.py`
5. Execute the `python insert_data.py`
6. Execute the `python views.py`
7. Open your brower and type 'localhost:8000'

Now you will be able to see the home page.




VOILA!!! You have succssefully executed the Item Catalog project.



[HTTPSTATUS]:<https://classroom.udacity.com/courses/ud303/lessons/6ff26dd7-51d6-49b3-9f90-41377bff4564/concepts/75becdb9-da2a-4fbf-9a30-5f3ccd1aa1d6>
[vagrant]:<https://www.vagrantup.com/>
[virtualbox]:<https://www.virtualbox.org/wiki/Download_Old_Builds_5_1>
[conceptualoverview]:<https://www.youtube.com/watch?v=djnqoEO2rLc>
[gitscm]:<https://git-scm.com/downloads>
[gitcourse]:<https://www.udacity.com/course/ud123>
[vbdownload]:<https://www.virtualbox.org/wiki/Download_Old_Builds_5_1>
[fsnd]:<https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip>