#! /usr/bin/python

import sys
sys.path.append('../src')
from task import *
from project import Project
from client import Client
from runner import Runner
import os, time

startTime = -1
def startTimer():
	global startTime
	startTime = time.time()
def ellapsedTime():
	global startTime
	return time.time() - startTime

HOME = os.environ['HOME']
os.environ['LD_LIBRARY_PATH']='%s/src/tlocal/lib:/usr/local/lib' % HOME
os.environ['LANG']=''

if sys.platform=="linux2" :
	client = Client("linux_ubuntu_edgy")
	client.brief_description = '<img src="http://clam.iua.upf.es/images/linux_icon.png"/> <img src="http://clam.iua.upf.es/images/ubuntu_icon.png"/>'
if sys.platform=="darwin" :
	client = Client("osx_10.4.8-macbook")
	client.brief_description = '<img src="http://clam.iua.upf.es/images/apple_icon.png"/>'

task = Task(
	project = Project("ardour2-trunk"), 
	client = client, 
	task_name="svn up and build" 
	)

task.set_check_for_new_commits( 
		checking_cmd="cd $HOME/src && svn status -u ardour2 | grep \*",
		minutes_idle=5
)

task.add_subtask( "List of new commits", [
	"cd $HOME/src/ardour2",
	{CMD:"svn log -r BASE:HEAD", INFO: lambda x:x },
	{CMD: "svn up", INFO: lambda x:x },
	] )

task.add_deployment( [
	"rm -rf $HOME/src/tlocal/*",
	"cd $HOME/src/ardour2",
	{INFO : lambda x: startTimer() }, 
	"scons PREFIX=$HOME/src/tlocal",
	{STATS : lambda x: {'build_time' : ellapsedTime() } },
	"scons install",
] )

Runner( task, 
	continuous = True,
	remote_server_url = 'http://192.168.1.102/testfarm_server'
#	remote_server_url = 'http://10.55.0.50/testfarm_server'
#	local_base_dir='/tmp'
)

