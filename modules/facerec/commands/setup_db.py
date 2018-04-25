import os
import yaml

import postgresql

description = "setup postgres database for face recognition module"
usage = "usage: setupdb <config file>"

def command(args):
    if len(args) < 1:
        print('setupdb:', description)
        print(usage)
        exit(1)

    main(*args)

def main(config_file: str):
    if not os.path.exists:
        print('config file does not exist:', config_file)
        exit(1)

    load_conf = yaml.safe_load(open(config_file))
    if 'postgres' not in load_conf:
        print('[ERROR] cannot find `postgres` key in config file')
        exit(1)

    conf = load_conf['postgres']

    db_path = '{}:{}/{}'.format(conf['host'], conf['port'], conf['db'])
    print('- using postgres connection from config:', db_path)
    db = postgresql.open('pq://{}:{}@{}'.format(conf['user'],
                                                      conf['pass'],
                                                      db_path))

    try:
        db.execute("create extension if not exists cube;")
        db.execute("create table vectors (id SERIAL, file VARCHAR, vec_low CUBE, vec_high CUBE, profile_id INT, created_at  TIMESTAMP DEFAULT NOW());")
        db.execute("create table profiles (id SERIAL, name VARCHAR, created_at  TIMESTAMP DEFAULT NOW());")
        db.execute("create index vectors_vec_idx on vectors (vec_low, vec_high);")
    
    except Exception as e:
        print('[ERROR] failed to setup face recognition db:', e)