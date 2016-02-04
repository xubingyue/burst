#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import argparse
from netkit.box import Box
from netkit.contrib.tcp_client import TcpClient
from burst import constants


class BurstCtl(object):

    args = None

    tcp_client = None

    def __init__(self, args):
        self.args = args

    def make_send_box(self, cmd, username, password):
        return Box(dict(
            cmd=cmd,
            body=json.dumps(
                dict(
                    auth=dict(
                        username=username,
                        password=password,
                    )
                )
            )
        ))

    def output(self, s):
        print '/' + '-' * 80
        print s
        print '-' * 80 + '/'

    def process_stat(self):
        send_box = self.make_send_box(constants.CMD_ADMIN_SERVER_STAT, self.args.username, self.args.password)
        self.tcp_client.write(send_box)

        rsp_box = self.tcp_client.read()

        if not rsp_box:
            self.output('disconnected.')
            return False

        if rsp_box.ret != 0:
            self.output('fail. rsp_box.ret=%s' % rsp_box.ret)
            return False

        self.output(json.dumps(json.loads(rsp_box.body), indent=4))

        return True

    def run(self):
        self.tcp_client = TcpClient(Box, self.args.host, self.args.port, self.args.timeout)

        try:
            self.tcp_client.connect()
        except Exception, e:
            self.output('connect fail: %s' % e)
            return False

        loop_times = 0

        while True:

            result = False
            if self.args.cmd == 'stat':
                result = self.process_stat()

            if not result:
                break

            loop_times += 1
            if loop_times >= self.args.loop > 0:
                break

            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break

        return True


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--host', help='burst admin host', action='store', default='127.0.0.1')
    parser.add_argument('-P', '--port', type=int, help='burst admin port', action='store', required=True)
    parser.add_argument('-u', '--username', help='username', action='store', default=None)
    parser.add_argument('-p', '--password', help='password', action='store', default=None)
    parser.add_argument('-c', '--cmd', help='cmd', action='store', default='stat', choices=('stat',))
    parser.add_argument('-o', '--timeout', type=int, help='connect/send/receive timeout', action='store', default=10)
    parser.add_argument('-l', '--loop', type=int, help='loop times, <=0 means infinite loop', action='store', default=-1)
    return parser


def send_and_recv(tcp_client, box):
    tcp_client.write(box)

    rsp_box = tcp_client.read()

    if not rsp_box:
        print 'disconnected.'
        return False

    if rsp_box.ret != 0:
        print 'fail. rsp_box.ret=%s' % rsp_box.ret
        return False
    else:
        print '/' + '-' * 80
        print json.dumps(json.loads(rsp_box.body), indent=4)
        print '-' * 80 + '/'
        return True


def main():
    args = build_parser().parse_args()
    ctl = BurstCtl(args)
    ctl.run()

if __name__ == '__main__':
    main()

