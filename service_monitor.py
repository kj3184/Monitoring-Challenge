import urllib.request
import ast
import json
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import argparse



def fetch_all_cpx_servers(port):
    url = "http://localhost:"+port+"/servers"
    # print(url)
    resp = urllib.request.urlopen(url)
    serverNames=resp.read()
    strServerNameList=serverNames.decode('UTF-8')
    ls = strServerNameList.strip('[]').replace('"', '').replace(' ', '').split(',')
    return ls

def fetch_cpx_server_details(ls, str1,port):
    # print(port)
    for i in range(len(ls)):
        resp = urllib.request.urlopen('http://localhost:'+port+'/'+ls[i])
        serverdata=resp.read().decode('UTF-8')
        jsonStr=serverdata.replace("{","{\"IP\":"+"\""+ls[i]+"\",")

        if(len(str1)==0):
            str1=str1+jsonStr
        else:
            str1=str1+","+jsonStr
    return str1


def print_running_services(ls, str1):
    df=pd.read_json(str1,lines=True)
    pd.set_option('display.max_rows', len(ls))
    pd.set_option('display.colheader_justify', 'center')
    df['cpu'] = pd.to_numeric(df['cpu'].str.replace('%', ''))
    df['memory'] = pd.to_numeric(df['memory'].str.replace('%', ''))

    df.rename(columns = {'IP':'IP', 'cpu':'CPU', 'memory':'Memory',
'service':'Service'},inplace = True)
    df['Status'] = 'Healthy'
    df.loc[(df['CPU'] >= 80) & (df['Memory'] >= 80), 'Status'] = 'Unhealthy'

    column_names = ['IP','Service', 'Status','CPU','Memory']
    df = df.reindex(columns=column_names)
    df['CPU'] = df['CPU'].astype(str) + '%'
    df['Memory'] = df['Memory'].astype(str) + '%'
    df2 = df.to_string(index=False)
    print (df2)

def get_avg_cpumem_usage(ls, str1):
    df=pd.read_json(str1,lines=True)
    pd.set_option('display.max_rows', len(ls))
    pd.set_option('display.colheader_justify', 'center')
    df['cpu'] = pd.to_numeric(df['cpu'].str.replace('%', ''))
    df['memory'] = pd.to_numeric(df['memory'].str.replace('%', ''))

    df.rename(columns = {'IP':'IP', 'cpu':'CPU', 'memory':'Memory',
'service':'Service'},inplace = True)
    df['Status'] = 'Healthy'
    df.loc[(df['CPU'] >= 80) & (df['Memory'] >= 80), 'Status'] = 'Unhealthy'

    column_names = ['IP','Service', 'Status','CPU','Memory']
    df = df.reindex(columns=column_names)
    df.drop('IP', axis=1, inplace=True)
    df_groupedby=df.groupby(['Service','Status'])[['CPU', 'Memory']].mean().round(0)
    df_groupedby['CPU'] = df_groupedby['CPU'].astype(str) + '%'
    df_groupedby['Memory'] = df_groupedby['Memory'].astype(str) + '%'
    print(df_groupedby)

def topmost_fewer_healthy_instaces(ls, str1):
    df=pd.read_json(str1,lines=True)
    pd.set_option('display.max_rows', len(ls))
    pd.set_option('display.colheader_justify', 'center')
    df['cpu'] = pd.to_numeric(df['cpu'].str.replace('%', ''))
    df['memory'] = pd.to_numeric(df['memory'].str.replace('%', ''))

    df.rename(columns = {'IP':'IP', 'cpu':'CPU', 'memory':'Memory',
'service':'Service'},inplace = True)
    df['Status'] = 'Healthy'
    df.loc[(df['CPU'] >= 80) & (df['Memory'] >= 80), 'Status'] = 'Unhealthy'

    column_names = ['IP','Service', 'Status','CPU','Memory']
    df = df.reindex(columns=column_names)
    df['CPU'] = df['CPU'].astype(str) + '%'
    df['Memory'] = df['Memory'].astype(str) + '%'
    df_filtered=df.query("Status == 'Healthy'")
    df_filtered.drop('CPU', axis=1, inplace=True)
    df_filtered.drop('IP', axis=1, inplace=True)
    df_filtered.drop('Memory', axis=1, inplace=True)
    df_groupedby = df_filtered[df_filtered.groupby(['Service','Status'])['Service'].transform('count') < 2]
    fewer_instances=df_groupedby.groupby(['Service']).agg(['count'])
    print(fewer_instances)


def main(port: str, menuoption: str):
    ls = fetch_all_cpx_servers(port)
    str1=''
    str1 = fetch_cpx_server_details(ls, str1,port)

    if menuoption == '1':
        print_running_services(ls, str1)
    elif menuoption == '2':
        get_avg_cpumem_usage(ls, str1)
    elif menuoption == '3':
        topmost_fewer_healthy_instaces(ls, str1)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="the port on which to run", type=str)
    parser.add_argument("menuoption", help="the menu option for extraction", type=str)
    args = parser.parse_args()
    main(args.port,args.menuoption)