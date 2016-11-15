#!/usr/bin/env python
from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3.client import Client

import collectd
import datetime
import traceback

class Base(object):

    def __init__(self):

        self.username            = 'admin'
        self.password            = 'admin'
        self.project             = 'project'
        self.url                 = 'http://api.example.com:5000/v3'
        self.user_domain_id      = 'default'
        self.user_domain_name    = 'default'
        self.project_domain_id   = 'default'
        self.project_domain_name = 'default'
        self.interval            = 30

    def config_callback(self, conf):
        for node in conf.children:
            if node.key == "Username":
                self.username = node.values[0]
            elif node.key == "Password":
                self.username = node.values[0]                
            elif node.key == "AuthURL":
                self.url = node.values[0]
            elif node.key == "Project":
                self.project = node.values[0]
            elif node.key == "Interval":
                self.interval = node.values[0]

    def get_keystone(self):

        kauth = v3.Password(
            auth_url=self.url,
            password=self.password,
            project_name=self.project,
            project_domain_id=self.project_domain_id,
            project_domain_name=self.project_domain_name,
            username=self.username,
            user_domain_id=self.user_domain_id,
            user_domain_name=self.user_domain_name,
        )

        # session
        ksession = session.Session(auth=kauth)
        keystone = Client(session=ksession)

        return ksession
        # , keystone
