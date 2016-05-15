# -*- coding: utf-8 -*-
from fabric.api import local, env, run, cd


# env.hosts = ['120.27.126.195:22']
# env.password = ['Algorithm#Jl']

da_dir = '/root/PythonFlask'


def flask():
    with cd(da_dir):
        local('git pull origin master')
        local('python PythonFlask.py')
